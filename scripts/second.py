#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Duocall: find a second AI of ANOTHER company on this computer, and ask it.

The rule that makes this worth anything is V1's (`V1/docs/leaders.manifest.json`, principles):

    "Pair (second opinion) = a DIFFERENT vendor, else the pair is OFF
     (no same-vendor fake diversity)."

Two answers from the same company are one opinion wearing two hats. If the only program on this
machine is the one already answering, this script says so and offers nothing - the skill then hands
the person a block to paste into a free browser chat, which really is another company.

What it never does: install anything, sign anyone in, ask for a key, or spend money. It only drives
a program that is ALREADY installed and ALREADY signed in, which is the whole idea the product is
built on.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIR = os.path.join(ROOT, "lang")


def lang_words(code="en"):
    """lang/<code>.json, English underneath anything missing."""
    words = {}
    for name in ("en", code):
        try:
            with open(os.path.join(LANG_DIR, "%s.json" % name), encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            words.update(data)
    return words


def pick_lang(explicit=None):
    """--lang, then DUOCALL_LANG, then the system's language, then English."""
    for value in (explicit, os.environ.get("DUOCALL_LANG"), os.environ.get("LC_ALL"),
                  os.environ.get("LC_MESSAGES"), os.environ.get("LANG")):
        if isinstance(value, str) and len(value) >= 2:
            code = value[:2].lower()
            if os.path.exists(os.path.join(LANG_DIR, "%s.json" % code)):
                return code
    return "en"


WORDS = lang_words("en")


def t(key, **values):
    text = WORDS.get(key, key)
    return text.format(**values) if values else text

# family -> (binary, args builder, human name). Claude is deliberately absent: it is the one asking.
FAMILIES = [
    ("openai", "codex",  lambda p: ["exec", "--skip-git-repo-check", "-s", "read-only", p],
     "ChatGPT (Codex)"),
    ("google", "agy",    lambda p: ["-p", p], "Gemini"),
    ("google", "gemini", lambda p: ["-p", p], "Gemini"),
    ("xai",    "grok",   lambda p: ["-p", p, "--permission-mode", "dontAsk",
                                    "--deny", "Write(**)", "--deny", "Edit(**)",
                                    "--deny", "Bash(*)", "--max-turns", "6"], "Grok"),
    ("moonshot", "kimi", lambda p: ["-p", p], "Kimi"),
    ("alibaba", "qwen",  lambda p: ["-p", p], "Qwen"),
]

TIMEOUT = int(os.environ.get("DUOCALL_TIMEOUT", "180"))


def available():
    seen, out = set(), []
    for family, binary, build, label in FAMILIES:
        if family in seen:
            continue
        path = shutil.which(binary)
        if path:
            seen.add(family)
            out.append({"family": family, "binary": binary, "name": label, "path": path})
    return out


def cmd_list(args):
    found = available()
    if not found:
        print(t("list_none"))
        print(t("list_none_browser"))
        return 1
    print(t("list_found", count=len(found)))
    for f in found:
        print(f"  {f['name']} - {f['binary']}")
    return 0


def cmd_ask(args):
    found = available()
    if not found:
        print(json.dumps({"ok": False, "code": "none", "why": t("why_none")},
                         ensure_ascii=False))
        return 1

    pick = None
    if args.who:
        pick = next((f for f in found if args.who.lower() in (f["binary"], f["family"])), None)
        if pick is None:
            print(json.dumps({"ok": False, "code": "absent", "why": t("why_absent", who=args.who)},
                             ensure_ascii=False))
            return 1
    else:
        pick = found[0]

    build = next(b for fam, bin_, b, _ in FAMILIES if bin_ == pick["binary"])
    prompt = args.prompt
    if prompt == "-":
        prompt = sys.stdin.read()

    try:
        done = subprocess.run([pick["binary"], *build(prompt)],
                              capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        print(json.dumps({"ok": False, "code": "timeout", "who": pick["name"], "binary": pick["binary"],
                          "why": t("why_timeout", seconds=TIMEOUT)}, ensure_ascii=False))
        return 1
    except OSError as e:
        print(json.dumps({"ok": False, "code": "start-failed", "who": pick["name"],
                          "why": t("why_start", error=e)}, ensure_ascii=False))
        return 1

    text = (done.stdout or "").strip()
    if done.returncode != 0 or not text:
        why = (done.stderr or "").strip().splitlines()
        why = why[-1] if why else t("why_exit", code=done.returncode)
        code = "failed"
        # The single most common failure, and it is not the person's fault.
        if any(w in why.lower() for w in ("quota", "limit", "rate", "usage", "429")):
            why, code = t("why_allowance"), "allowance"
        print(json.dumps({"ok": False, "code": code, "who": pick["name"], "binary": pick["binary"],
                          "why": why}, ensure_ascii=False))
        return 1

    print(json.dumps({"ok": True, "who": pick["name"], "binary": pick["binary"],
                      "family": pick["family"], "answer": text}, ensure_ascii=False))
    return 0


def cmd_words(args):
    """The sentences the skills say to the person, in the person's language, for the skill to use
    as they are: the browser block, the answer's heading, a pair that did not happen."""
    print(json.dumps({"lang": pick_lang(args.lang),
                      "say": {k: v for k, v in WORDS.items() if k.startswith("say_")}},
                     ensure_ascii=False, indent=1))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Duocall: a second AI from another company.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="which programs from another company are here")
    s.add_argument("--lang", help="en, es, pt, ru or uk (default: the system's language)")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("ask", help="ask the second AI a question")
    s.add_argument("prompt", help="the question text, or - to read it from standard input")
    s.add_argument("--who", help="who exactly to ask (codex, agy, grok, kimi, qwen)")
    s.add_argument("--lang", help="en, es, pt, ru or uk (default: the system's language)")
    s.set_defaults(func=cmd_ask)

    s = sub.add_parser("words", help="the sentences the skills say, in the person's language")
    s.add_argument("--lang", help="en, es, pt, ru or uk (default: the system's language)")
    s.set_defaults(func=cmd_words)

    args = ap.parse_args(argv)
    global WORDS
    WORDS = lang_words(pick_lang(args.lang))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
