# Find matching values

A simple script used for comparing from two joined tables directly from database.
At the start of my manual QA career I was working at a Data team, and at one point of DB development I had perform checks on data population. For which I had written a script, that would get the values from DB, check them, and store their discrepancies into a csv file. It was my first ever program and it took me a lot of time, even though it was quite simple, but it saved me so much more.
Now i've decided to rewrite it to so it wouldn't take 20 mins to iterate over 300000 rows.

### Old script
Relied on a shared pre-prod database within copied schema for testing. Can't share the code for NDA reasons.
```json
Elapsed time 20-30 mins
```
### This script
Relies on a containerized postgres database. Data is persisted in volumes. Methods for creating tables from models, reseting specified tables, populating data with random data for specified ammount of rows and multiple data comparison methods are realised. Comparing the same dataset the slowest takes 10 secs and the fastest:
```json 
Elapsed time: 7.23 seconds
```

## How To Run
- Make sure docker is installed
1. Run in terminal from project root, to install dependencies
    ```json
    pip install -r requirements.txt
    ```

2. Run in terminal from project root, to start postgres
    ```json
    docker-compose up
    ```

3. Run in terminal from project root, to start the sorting
    ```json
    python compare.py
    ```
