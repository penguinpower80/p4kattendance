#P4K
This project will be a student attendance tracking for partnership 4 kids. 

## Setting up
- Clone the repo from GitHub
  - Make sure your product has a valid venv set up for python 3.8 or later.
- install requirements: `pip install -r requirements.txt`
- **copy** the file called `env.sample` to a file called `.env`
- Set the appropriate settings values.
- The format used below is `KEY` = `DEFAULT VALUE`
- Settings:

### General Settings
  - `DEBUG` = True
    - Run in default mode. Set to False for production.
  - `HOSTING` = 'LOCAL'
    - Set to "HEROKU" if hosting in HEROKU
      - Sets up settings file for heroku
  - `SECRET_KEY` = '---'
    - Generate a new one here: https://miniwebtool.com/django-secret-key-generator/
    - DO NOT COMMIT TO REPO!!
  
### Email Settings
  - `EMAIL` = 'LOCAL'
    - Can use LOCAL to store in a folder in project
    - Set to SENDGRID to use sendgrid.
  - `EMAIL_HOST_USER` = ''
    - The appropriate username for the SMTP host
  - `EMAIL_HOST_PASSWORD` = ''
    - The appropriate email for the SMTP host
  - `FROM` = ''
    - The default from address when sending emails

### Database Settings
  - `DB` = 'sqlite'
    - The Database system to use. 
    - Set to 'MYSQL' if using MySQL 
  - `DB_NAME` = 'db.sqlite3'
    - The name of the database 
  - `DB_HOST` = ''
    - The hosting address for the database
    - Not used for SQLITE
  - `DB_USER` = ''
    - The database user
    - Not used for SQLITE
  - `DB_PASSWORD` = ''
    - The database password
    - Not used for SQLITE
  - `DB_PORT` = '3306'
    - The database port
    - Not used for SQLITE
  
### AWS S3 Storage Settings
  Instructions to get these can be found here: https://blog.theodo.com/2019/07/aws-s3-upload-django/
  - `AWS_ACCESS_KEY_ID` = ''
    - The access key id for your AWS S3 bucket
  - `AWS_SECRET_ACCESS_KEY` = ''
    - The access key secret for your AWS S3 bucket
  - `AWS_STORAGE_BUCKET_NAME` = ''
    - The AWS S3 bucket name 
  
### Social Login
Full documentation is available here: https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
Helpful tutorial available here: https://www.bogotobogo.com/python/Django/Python-Django-OAuth2-Getting-Client-ID-Application-ID-Social-Sites-Facebook-Twitter-Google.php
If they key/secret are not filled in, then the option will not show up in the login screen.

  - `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` = ''
    - Google OAuth2 Key
  - `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` = ''
    - Google OAuth2 Secret

  
  - `SOCIAL_AUTH_TWITTER_KEY` = ''
    - Twitter Auth Key
  - `SOCIAL_AUTH_TWITTER_SECRET` = ''
    - Twitter Auth Secret

    **NOTE: You must request elevated privileges for this to work**

  
  - `SOCIAL_AUTH_FACEBOOK_KEY` = ''
    - Facebook Auth Key
  - `SOCIAL_AUTH_FACEBOOK_SECRET` = ''
    - Facebook Auth Secret
  

### Initial Setup
*YOU CAN ALSO RUN THIS TO START OVER!!*
- First, run `python manage.py setup` 
  - This will:
    1. Prompt to erase sqlite db 
    2. Prompt to erase any migrations, and make/apply the migrations fresh
    3. Prompt to import sample data from test folder
    4. Prompt to create a new superuser
- Then, `python manage.py runserver`

## Adding views, forms, or admin:
- Create a new file in the appropriate folder. For example, homepage.py in the view folder
- Edit the __init__.py in that folder, and add "from .[filename] import *".  (don't forget the leading dot)

## Importing data (for now)
- open `http://127.0.0.1:8000/import`
- Select 'School File'
- For the file, select 'p4kattendance\attendance\tests\samples\schools.csv'
- Click import
- (wait to finish)
- Select 'Student file'
- For the file, select 'p4kattendance\attendance\tests\samples\students.csv'
- Click import
- (wait to finish)


## Resources

- Date Picker:
  - https://bulma-calendar.onrender.com/