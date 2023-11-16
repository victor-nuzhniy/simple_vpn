# simple_vpn

## Installation

### Sensitive data

1. Create in the project root (or obtain from team member) an `.env` file with 
environment variables required by application.
    SECRET_KEY =
    ALLOWED_HOST=
    DEBUG=

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