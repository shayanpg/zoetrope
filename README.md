<a href='https://urbandisplacement.org/'><img src='home/static/home/UDP_Logo.png' align="right" height="120" /></a>  

# Zoetrope

A tool for visualizing neighborhood change

## Developer Installation
*Prereqs: Python 3.6 or later, git*
1. `git clone https://github.com/shayanpg/zoetrope.git`
2. Navigate to project directory (`cd zoetrope`)
3. `pip3 install virtualenv`
4. `virtualenv venv`
5. `source venv/bin/activate` (Linux/MacOS) OR `source venv/Scripts/activate` (Windows)
6. `pip3 install -r requirements.txt`
    * if this fails, manually install relevant packages using pip (Django, django-crispy-forms, Pillow, Shapely, requests)
7. Create environment variables for each of the following (guide for macOS <a href='https://phoenixnap.com/kb/set-environment-variable-mac'>here</a>):
    * DEBUG <- True
    * DOWNLOAD_LOCAL
      * False if you have AWS S3 configured, True otherwise
    * GMAIL_PASS
      * request from developer (include what OS you are running)
    * AMAZON_S3_BUCKET_NAME
      * need only if DOWNLOAD_LOCAL == False
      * <a href='https://erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140'>guide</a>
    * AMAZON_S3_ACCESS_KEY_ID
      * need only if DOWNLOAD_LOCAL == False
      * <a href='https://erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140'>guide</a>
    * AMAZON_S3_SECRET_ACCESS_KEY
      * need only if DOWNLOAD_LOCAL == False
      * <a href='https://erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140'>guide</a>
8. Create a database:
    1. `python3 manage.py makemigrations`
    2. `python3 manage.py migrate`
9. Run development server (`python3 manage.py runserver`)
10. Go to link specified in terminal

**NOTE: In development the secret key is randomly generated upon startup - this means you will need to log in again each time you startup the application**

**in production, we will us environment variables for this purpose**


## TODO: Production Installation guide and product description

(Uses Adrian Letchford's `streetview` library which allows users to download old images)
