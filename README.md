# simple_vpn

## Installation

### Sensitive data

1. Create in the project root (or obtain from team member) an `.env` file with 
environment variables required by application (values used as an example)

SECRET_KEY = '11'
ALLOWED_HOST= localhost 127.0.0.1
DEBUG=1
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=vpn
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=a@a.com
DJANGO_SUPERUSER_PASSWORD=admin
SITE_NAME_1=simple_site
DOMAIN_1=simple_site
SITE_NAME_2=vpn_site
DOMAIN_2=vpn_site

### Performing commits

1. Pre-commit hook installed, settings are in .pre-commit-config.yaml
2. To instantiate new hook settings change .pre-commit-config.yaml file
     and run     pre-commit install
3. To bypass hook checking run      git commit -m "..." --no-verify


### Different sites

1. For this moment created different sites with their own settings and wsgi.py.
2. Site framework was used to orginise functionality.
3. Config project has SITE_ID = 1, and we can use it as 'site' project.
4. 'vpn_site' project has SITE_ID = 2, and has its own url with path starts 'localhost'.
5. 'turnVPN.js' in 'static/js/' operates with host '127.0.0.1:8000' and vpn '127.0.0.1:8001' now to
    operate on local machine. After deployment these settings must be changed to
    support 'enable vpn' and 'disable vpn' functionality.


### Run development server from different project settings.

1. We can explicitly run
    export DJANGO_SETTINGS_MODULE=getloan.settings
    and then run django-admin runserver
2. Or run server using command
    django-admin runserver --settings=vpn_site.settings

### Performing tests

For testing application there is need to use pytest and it's plugings.
There is need to always check amount of test cases and their covering.

1. To perform created test cases, use command:

       pytest --cov

2. Also db container must be run, and in .env set 
    
   POSTGRES_HOST=localhost
   POSTGRES_PORT=8778

## Running container

### Build container

1. To build the container run command     docker-compose up 
2. To rebuild the container after some changes  

    docker-compose build --no-cache
    docker-compose up

### Using application

1. After container successfully run application will be awailable at
   http://127.0.0.1:8000 and http://127.0.0.1:8001/localhost/ (as vpn version
   with all features described in task)
2. To turn on/off vpn mode use links in upper left corner as a login user.
3. For local running DEBUG in .env should be set to 1 (True) for serving staticfiles
    by gunicorn.

### Deployment

1. For deployment will be used code version with nginx included.

## General project installation order.

1. Requirements:
   - Docker and docker-compose must be installed;
   - Python 3.10

2. Clone project with command     git clone https://github.com/victor-nuzhniy/simple_vpn.git

3. Create .env file in root directory (content can be copied from chapter 'Sensitive data')

4. In case of running project on Windows OS open docker-entrypoint.sh and add empty line 
   somewhere, save the file.

5. Create virtual environment (   virtualenv venv    or use similar) and activate it.

6. Install poetry version 1.3.0             pip install poetry==1.3.0

7. Run command     poetry install

8. Run command     docker-compose up

9. Projects will be awailable on http://127.0.0.1:8000

10. To run tests you should:
    - activate virtual environment;
    - run command          poetry install --with test;
    - run command          pytest --cov;
    