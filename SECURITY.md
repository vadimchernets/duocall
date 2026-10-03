# Security

## What Duocall touches

- It runs an AI program that is **already installed and already signed in** on this computer, and
  sends it the question the person asked. Nothing else.
- It never reads, copies, stores or forwards any credential, token or configuration of those
  programs. It calls them the way a person would from their own terminal.
- It writes no files and keeps no history of its own.
- A seat that does not answer within 180 seconds (`DUOCALL_TIMEOUT`) is reported as not having
  answered.

## Reporting a vulnerability

Write to polyhelper.ai@gmail.com with `duocall` in the subject.
