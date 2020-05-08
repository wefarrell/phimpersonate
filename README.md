Example:

This will take a file that has a first and last name in the first 24 characters and replace them with fake values:
```
phimpersonate -c 1-12:first_name,13-24:last_name file_with_phi.txt
```

The fake names are generated deterministically based on the original value, so fake values will be consistent across multiple files if the real values are consistent.
