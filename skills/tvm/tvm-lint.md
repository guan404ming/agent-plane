---
name: tvm-lint
description: Run linting based on changed files.
---

# TVM Lint

Run lint commands based on file types changed.

## Commands

| File Type            | Command                                       |
| -------------------- | --------------------------------------------- |
| `*.py`               | `bash docker/lint.sh -i python_format pylint` |
| `*.cc`, `*.h`        | `bash docker/lint.sh -i clang_format cpplint` |
| `*.java`, `*_jni.cc` | `bash docker/lint.sh jnilint`                 |
| Any file             | `bash docker/lint.sh asf`                     |
