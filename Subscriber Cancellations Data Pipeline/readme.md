# Subscriber Cancellations Data Pipeline project

## Project Description

A semi-automated bash+python pipeline to systematically transform and load the data from messy SQLite database into a clean database.

The pipeline:
- performs unit tests to confirm data validity
- writes readable errors to an error log
- automatically checks and updates changelogs
- updates a production database with new cleased data

## Instructions

This repository is set up as if the scripts have never been run. To run,

1. Run `script.sh` and follow the prompts
2. If prompted, `script.sh` will run `dev/cleanse_data.py`, which runs unit tests and data cleaning functions on `dev/cademycode.db`
3. If `cleanse_data.py` runs into any errors during unit testing, it will raise an exception, log the issue, and terminate
4. Otherwise, `cleanse_data.py` will update the clean database and CSV with any new records
5. After a successful update, the number of new records and other update data will be written to `dev/changelog.md`
6. `script.sh` will check the changelog to see if there are updates
7. If so, `script.sh` will request permission to overwrite the production database
7. If the user grants permission, `script.sh` will copy the updated database to `prod`

If you follow these instructions, the script will run on the initial dataset in `dev/cademycode.db`. To test running the script on the updated database, change the name of `dev/cademycode_updated.db` to `dev/cademycode.db` in the `cleanse_data.py`.
