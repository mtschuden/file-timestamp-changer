# File Timestamp Changer

This script changes the created/modified timestamp of all files in a specified directory. The files in the directory can still be filtered (currently hardcoded). At the moment the script only replaces years. Feel free to extend the script. :)

To execute, run the following command:
```
python main.py DIR
```

In case of an error, the script creates a backup file (YYYY_MM_DDTHHMSS.bak) to restore the old timestamps.