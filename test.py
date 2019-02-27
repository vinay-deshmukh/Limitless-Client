from sheet_disk import main
import os

with open(os.environ.get('SH_DISK_CREDS')) as f:
    creds = f.read()


main(creds, ['upload', '.gitignore'])