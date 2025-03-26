#!/bin/sh -e
#
# Devrebuild
# ==========
#
# Download the latest production database, apply migrations, and get ready to rock and roll.


jpl_sys_ipv4=172.16.16.10


# Argument check

if [ $# -ne 0 ]; then
    echo "😩 This program takes no arguments; try again?" 1>&2
    exit 1
fi


# Sentinel files check

if [ \! -f "manage.sh" ]; then
    echo "🤔 Not finding the manage.sh file; are you in the right directory?" 1>&2
    exit 1
fi


# Warning

cat <<EOF
❗️ This program will wipe out your local "nisthelp" PostgreSQL database, copy
the latest operations database, and then upgrade it to the current development
software you have in this working directory. If you have any local changes to
your content database or media blobs you want to preserve, abort now!

⏱️ You have 5 seconds.
EOF

sleep 5
trap 'echo "😲 Interrupted" 1>&2; exit 1' SIGINT


# Let's go

echo "🏃‍♀️Here we go"
dropdb --force --if-exists "nisthelp"
createdb "nisthelp" 'Wagtail DB for NIST Help Portal'
# Must use --checksum here because the nightly refresh to tumor munges all the timestamps
rsync --checksum --no-motd --recursive --delete --progress $jpl_sys_ipv4:/Users/kelly/nist-help/media .
scp $jpl_sys_ipv4:/Users/kelly/nist-help/latest.sql.bz2 .
bzip2 --decompress --stdout latest.sql.bz2 | psql --dbname=nisthelp --echo-errors --quiet

./manage.sh makemigrations
./manage.sh migrate
./manage.sh collectstatic --no-input --clear --link

# Add additional upgrade steps here:
# TBD

# Final steps
./manage.sh clear_cache --all

echo '🏁 Done! You can start it with:'
echo './manage.sh runserver 6468'

exit 0
