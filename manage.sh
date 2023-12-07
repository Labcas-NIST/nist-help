#!/bin/sh -e
#
#
# Run django-admin locally with this convenience script

. ${HOME}/.secrets/passwords.sh

export DATABASE_URL=${DATABASE_URL:-postgres://:@/nisthelp}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-local}
export LDAP_URI=${LDAP_URI:-ldaps://localhost:1636}
export JPL_DS_RECAPTCHA_SITE_KEY JPL_DS_RECAPTCHA_SECRET_KEY DATABASE_URL


if [ ! -d "src" -o ! -d "docker" ]; then
    echo "🚨 Run this from the checked-out nist-help source directory" 1>&2
    echo "You should have these subdirs in the current directory: src docker" 1>&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "⚠️ Local Python virtual environment missing; attempting to re-create it" 1>&2
    python3.11 -m venv .venv
    .venv/bin/pip install --quiet --upgrade setuptools pip wheel build
    .venv/bin/pip install --requirement requirements.txt
fi

. .venv/bin/activate

command=$1
shift
exec /usr/bin/env \
    "src/manage.py" $command --settings local --pythonpath . "$@"
