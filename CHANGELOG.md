# Changelog

## 0.2.0 — 2026-10-03

- Five languages. Every word `scripts/second.py` says to a person - the list, and the `why` of a second opinion
  that did not happen - lives in `lang/en.json`, `es.json`, `pt.json`, `ru.json`, `uk.json`, English underneath
  anything missing. `--lang` on `list`, `ask` and the new `words`; without it `DUOCALL_LANG`, then the system's
  language. `second.py words --lang <code>` prints the sentences the skills say word for word (the browser block,
  "<who> answered:", the allowance that ran out, what a second opinion costs), and `ask` uses them instead of an
  improvised translation. Each failure also carries a stable `code` (`none`, `absent`, `timeout`, `start-failed`,
  `allowance`, `failed`). The skills pass the person's language. Tests: every language has every word with the
  same placeholders, each language reaches the output, the system language is honoured, and the tests themselves
  run in English whatever the machine's language is.

## 0.1.6 — 2026-10-02

- On Windows the step-0 launcher (`hooks/python.ps1`, and `hooks/python.sh` in Git Bash) also finds a Python installed
  after Claude Code started, with no restart: Claude Code hands its hooks and shells the PATH it was started with, so
  python.org's fresh Python is not on it. After `python`, `py -3` and `python3` on that PATH the launcher now looks at the
  `py` launcher (`%LOCALAPPDATA%\Programs\Python\Launcher`, `%SystemRoot%`), `%LOCALAPPDATA%\Programs\Python\Python3*`
  (and `%ProgramFiles%\Python3*`), newest first, and the install paths in the registry
  (`HKCU`/`HKLM\Software\Python\PythonCore\*\InstallPath`). Same proof as before: a candidate counts only once `-c`
  says 3.8+, and the Microsoft Store stub is never started. The step-0 line no longer asks for a restart. Checked on
  GitHub Actions windows-latest: Python installed silently in the middle of a job, then a hook (PowerShell 7 and 5.1),
  a skill's script and Git Bash ran on it with the PATH unchanged.

## 0.1.5 — 2026-10-02

- Skills run their scripts through the step-0 launcher, on every system: the Bash tool runs
  `sh "${CLAUDE_PLUGIN_ROOT}/hooks/python.sh" duocall say scripts/<name>.py ...`, the PowerShell tool (Windows without
  Git Bash) the same line starting with the bare path `${CLAUDE_PLUGIN_ROOT}/hooks/python.ps1`. No skill calls `python3`
  any more (on Windows it is often missing or the Microsoft Store stub). The launcher takes a Python only once `-c`
  proves 3.8+, tries `python`, `py -3`, `python3` on Windows, never starts the Store or Apple stub, and with no Python
  says one step-0 line. Scripts are passed relative to the plugin root; text piped in PowerShell reaches the script as
  UTF-8 with no BOM (Windows PowerShell 5.1 wrote one). `allowed-tools` grant both forms, quoted as the command is -
  the old unquoted `Bash(python3 ${CLAUDE_PLUGIN_ROOT}/...)` never matched the quoted commands and always prompted.
  Checked on GitHub Actions on windows-latest, macos-latest and ubuntu-latest, including a real `claude -p` that opens a
  skill and runs its command with no prompt, through Bash and through PowerShell.
- New `hooks/python.sh` and `hooks/python.ps1` (the launcher only; duocall has no hooks).

## 0.1.4 — 2026-10-02

- README: install from Poly A1's catalogue by its raw link (`/plugin marketplace add https://raw.githubusercontent.com/vadimchernets/poly-a1-plugins/main/.claude-plugin/marketplace.json`,
  then `/plugin install duocall@poly-a1`) - no git needed; the Poly A1 folder is the way without internet,
  and `marketplace remove` is never the way to switch.

## 0.1.3 — 2026-10-02

- Every release now carries `duocall-0.1.3.zip` (one top folder `duocall-0.1.3/`), built by the new
  `scripts/release-zip.sh` and attached by `.github/workflows/release.yml` on each `v*` tag. The Poly A1
  catalogue installs it as an `archive` source with its `sha256`, so installing needs no git: a
  beginner's Linux has none, and on a Mac without Apple's Command Line Tools `git` is the stub that
  opens Apple's install window.

## 0.1.2 — 2026-10-02

- Language check: `scripts/check_language.py` (run by `tests/test_check_language.py`) fails if Cyrillic
  appears outside a language place (`ru/`, `uk/` folders, `README.ru.md`, `lang/ru.json`, `lang/uk.json`),
  in file names or text. Controls plant Cyrillic in a code comment, a file name, a JSON key and Markdown.

## 0.1.1 — 2026-10-02

- Project language is English: comments, skill instructions, script output (including the JSON keys of `second.py`: family, binary, name, path, why, who, answer) and tests translated; skills answer in the person's language.
- The Russian-scenario behaviour suite now lives in `tests/behavior/ru/` as the Russian localization of the suite; `run.py --language` picks a language (default: every language folder present).
