Description
------------
This repo contains python script which updates cvs in some job sites, e.g. hh.ru and superjob.ru

Requirements
------------
* [ChromeDriver](https://chromedriver.chromium.org/)
* [Selenium](https://www.selenium.dev/)
* [Python 3](https://www.python.org/)


How to use
----------------
Before using the script, add username(s) and password(s) 
into .env file.
The file must be in the same directory with autoupdate.py.

Clone repo:

    $ git clone git@github.com:sapegin-o1eg/cv_autoupdater.git
    $ cd cv_autoupdater
    
Create separate environment:

    $ python -m venv env_name

Activate environment:

    $ . env_name/bin/activate
    
Install requirements:

    $ pip install -r requirements.txt
    
Put appropriate ChromeDriver from [HERE](https://chromedriver.chromium.org/downloads) into PATH, e.g. into env_name/bin/

Run the script:

    $ python autoupdate.py

License
-------

BSD
