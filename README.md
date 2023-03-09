# semantify

Example workflow file:

```
on:
  push:
jobs:
  job0:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: semantify
        uses: vliz-be-opsci/semantify@main
      - name: commit
        uses: stefanzweifel/git-auto-commit-action@v4
```
