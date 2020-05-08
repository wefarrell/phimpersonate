Example:

This will take a file that has a first and last name in the first 24 characters and replace them with fake values:
```
phimpersonate -c 1-12:first_name,13-24:last_name file_with_phi.txt
```

Output:

```
Bob         Smith
```

