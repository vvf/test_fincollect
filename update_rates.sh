#!/bin/bash
# setup crontab to call this script every day, for example in 5 - adde next line to the crontab
#  0 5 * * * PROJECT_PATH/manage.py update_rates
PROJECT_HOME=$(dirname $(readlink -f $0))
export DJANGO_SETTINGS_MODULE=test_fincollect.settings
cd PROJECT_HOME
# if you use virtualenv - there you need to activate it
#. ../fincollect-env/bin/activate
python manage.py update_rates
