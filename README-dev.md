# Documentation update
```
./setup/update_docs.sh
```

See also: `src/docs/README-doc-generation.txt`

# Code linting and formatting

## SyntaxWarning: invalid-escape-sequence (W605)
```
ruff check --select W605 --fix --unsafe-fixes src
```

# References
https://stackoverflow.com/questions/38048945/how-to-turn-warnings-into-errors-when-building-sphinx-documentation-with-setupto
