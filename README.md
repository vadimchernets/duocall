# Duocall

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23107731.svg)](https://doi.org/10.5281/zenodo.23107731)

**A second opinion from a different company's AI — and an honest account of where the two
disagreed. Because two AIs agreeing is not proof.**

A plugin for [Claude Code](https://claude.com/claude-code), written for the person who is not a
programmer and is about to act on something an AI told them: a contract, a sum, a deadline, a dose,
a letter they cannot unsend.

## What it does

| | |
|---|---|
| `/duocall:ask` | Puts the same question to an AI of **another company** and brings the answer back whole. If there is no second program on the machine, hands over the exact block to paste into a free browser chat. |
| `/duocall:compare` | Where they agreed — **with both quotes**. Where they differed — every number, date and next step. And the line that agreement is not proof. |
| `/duocall:deepen` | A second round on the **disputed point only**, keeping the first answers intact. |
| `/duocall:who` | Who answered, who did not, who was never there — and how many *companies* that is. |

No hooks. Nothing runs by itself: a second opinion spends the person's own allowance with another
vendor, so it happens on their word, never on a guess.

## The rule it will not bend

**A second opinion has to come from a different company.** Two answers from the same vendor are one
opinion wearing two hats. The script knows the families it can reach — OpenAI (`codex`), Google
(`agy`/`gemini`), xAI (`grok`), Moonshot (`kimi`), Alibaba (`qwen`) — and Claude is deliberately not
among them, because Claude is the one asking. If no second family is installed, the plugin says so
and points at the browser instead of inventing a pair.

This is V1's rule: *"Pair = a DIFFERENT vendor, else the pair is OFF (no same-vendor fake
diversity)."*

## What it never does

Never installs anything. Never signs anyone in. Never asks for an API key. Never buys anything and
never suggests buying anything — when a second AI runs out of its monthly allowance, the plugin says
so, says it will come back by itself, and points at the free browser chat. It drives only a program
that is **already installed and already signed in**.

It never merges two answers into one confident voice, never claims agreement it cannot quote, and
never presents one opinion as two.

## Install

```
/plugin marketplace add https://raw.githubusercontent.com/vadimchernets/poly-a1-plugins/main/.claude-plugin/marketplace.json
/plugin install duocall@poly-a1
```

The first line adds Poly A1's catalogue by its link - one file, no git and no GitHub account - and
later corrections reach you from the same place (Claude Code 2.1.224 or later; `claude update`). If
`poly-a1` is already there, from the Poly A1 folder or from before, skip it: the second line is enough.

Without internet, from the Poly A1 folder:

```
/plugin marketplace add <path to the Poly A1 folder>
/plugin install duocall@poly-a1
```

Once there is internet, the folder is switched to the link in place, keeping everything installed
([how](https://github.com/vadimchernets/poly-a1-plugins/blob/main/OFFER-THESE.md#later-from-the-folder-to-github-without-losing-anything)). Never `/plugin marketplace remove poly-a1`: it uninstalls every plugin that came from
it and deletes their saved data.

Then, in `/plugin` → Marketplaces, **turn on auto-update** — for marketplaces that are not
Anthropic's own it is off by default.

## Languages

Everything the script says to the person, and the sentences the skills say word for word (the block
for the browser chat, the answer's heading, the allowance that ran out), live in `lang/<code>.json`:
English, Spanish, Portuguese, Russian and Ukrainian, with English underneath any word a language is
missing. The skills pass the person's language with `--lang`; on its own the script takes
`DUOCALL_LANG`, then the system's language. `second.py words --lang <code>` prints the skills'
sentences. Failures keep a stable `code` (`none`, `absent`, `timeout`, `start-failed`, `allowance`,
`failed`) next to the translated `why`, so a program never has to read a sentence.

## Requirements

Claude Code with plugin support and `python3`. A second AI program is optional: without one the
plugin works through a free chat in the browser, which is a real second company and costs nothing.

## Licence

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
