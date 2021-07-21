<a href='https://urbandisplacement.org/'><img src='home/static/home/UDP_Logo.png' align="right" height="120" /></a>  

# Zoetrope

A tool for visualizing neighborhood change

## Developer Installation
*Prereqs: Python 3.6 or later, git*
1. `git clone https://github.com/shayanpg/zoetrope.git`
1. Navigate to project directory (`zoetrope`)
2. `pip install virtualenv`
3. `virtualenv venv`
4. `source venv/bin/activate` (Linux/MacOS) OR `source venv/Scripts/activate` (Windows)
5. `pip install -r requirements.txt`
6. To create a database:
  1. `python manage.py makemigrations`
  2. `python manage.py migrate`
7. Now to run development server run `python manage.py runserver`
8. Go to link specified in terminal (localhost:8000)


## TODO: Production Installation guide and product description

(Uses Adrian Letchford's `streetview` library which allows users to download old images)
