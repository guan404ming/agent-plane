---
name: tvm-build
description: Build TVM for C++ changes.
---

# TVM Build

Build when C/C++ files are modified.

## When to run

Run if any `*.cc`, `*.h`, `*.cpp` files changed.

## Command

```bash
make -C build -j8
```
