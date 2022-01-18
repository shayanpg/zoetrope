<a href='https://urbandisplacement.org/'><img src='home/static/home/UDP_Logo.png' align="right" height="120" /></a>  

# Zoetrope

A tool for visualizing neighborhood change

## Developer Installation
*Prereqs: Python 3.6 or later, git*
1. `git clone https://github.com/shayanpg/zoetrope.git`
2. Navigate to project directory (`zoetrope`)
3. `pip install virtualenv` OR `pip3 install virtualenv`
4. `virtualenv venv`
5. `source venv/bin/activate` (Linux/MacOS) OR `source venv/Scripts/activate` (Windows)
6. `pip3 install -r requirements.txt`
7. To create a database:
    1. `python3 manage.py makemigrations`
    2. `python3 manage.py migrate`
8. Create environment variables for each of the following:
    * DEBUG <- True
    * GMAIL_PASS
9. Now to run development server run `python3 manage.py runserver`
10. Go to link specified in terminal (localhost:8000)

**NOTE: In development the secret key is randomly generated upon startup - this means you will need to log in again each time you startup the application**
**in production, we will us environment variables for this purpose**


## TODO: Production Installation guide and product description

(Uses Adrian Letchford's `streetview` library which allows users to download old images)
