#P4K
This project will be a student attendance tracking for partnership 4 kids. 

## Setting up
- Clone the repo from GitHub
  - Make sure your product has a valid venv set up for python 3.8 or later.
- install requirements: `pip install -r requirements.txt`
- copy env.sample to .env
  - Add the appropriate settings values.
  
### Initial Setup
*DO THIS ONLY ONCE AT THE VERY BEGINNING OR TO START OVER!!*
- First, run `python manage setup` 
  - This will:
    1. Erase any migrations
    2. Make the migrations fresh
    3. Delete the mysql db if found
    6. Prompt to create a new superuser
- Then, `python manage.py runserver`

## Adding views, forms, or admin:
- Create a new file in the appropriate folder. For example, homepage.py in the view folder
- Edit the __init__.py in that folder, and add "from .[filename] import *".  (don't forget the leading dot)

## Importing date (for now)
- open `http://127.0.0.1:8000/import`
- Select 'School File'
- For the file, select 'p4kattendance\attendance\tests\samples\schools.csv'
- Click import
- (wait to finish)
- Select 'Student file'
- For the file, select 'p4kattendance\attendance\tests\samples\students.csv'
- Click import
- (wait to finish)