## Summary

Adds a GitHub Actions workflow that runs the README mirror validator on PRs and pushes touching skill README pairs.

## What it checks

The validator checks:

- matching `README.md` / `README_EN.md` presence
- mirrored language-switch links
- matching heading counts
- title-first structure
- `nature-shared` support-package wording consistency

`nature-downloader` is treated as a documented layout exception because it intentionally uses a denser structure.

## Validation

Ran locally:

```text
README mirror validation passed: 18 mirrored skill docs checked.
```
