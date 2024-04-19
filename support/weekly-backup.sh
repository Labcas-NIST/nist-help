#!/bin/sh -e
#
# Weekly Backup of NIST Help Portal
# =================================
#
# Backup the database as well as the media blobs.

PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
export PATH
BACKUP_DIR=${BACKUP_DIR:-/home/ddsaops/backups/nisthelp}
MEDIA_DIR=${MEDIA_DIR:-/home/ddsaops/nist-help/media}

# Make the backup dirs
# --------------------

[ -d ${BACKUP_DIR}/database ] || mkdir ${BACKUP_DIR}/database
[ -d ${BACKUP_DIR}/media ] || mkdir ${BACKUP_DIR}/media


# Get the secrets
# ---------------
#
# SECRETS can be set to specify a custom secrets file, otherwise we
# default to ~/.secrets/passwords.sh

SECRETS=${SECRETS:-${HOME}/.secrets/passwords.sh}
if [ -f "${SECRETS}" ]; then
    . ${HOME}/.secrets/passwords.sh
else
    echo "No secrets file found at ${SECRETS}; aborting" 1>&2
    exit 1
fi
export PGPASSWORD

# Database backup
# ---------------
#
# First, do the database. PGPASSWORD must've been set by the secrets

date=`date --utc --iso-8601=date`
pg_dump --username="${PGUSERNAME}" --dbname=nisthelp \
    | bzip2 --compress --stdout --best > ${BACKUP_DIR}/database/$date.sql.bz2

# Link the latest
rm --force ${BACKUP_DIR}/database/latest.sql.bz2
ln --symbolic ${BACKUP_DIR}/database/$date.sql.bz2 ${BACKUP_DIR}/database/latest.sql.bz2


# Media
# -----
#
# Now the blobs

rsync --quiet --recursive --backup --links --hard-links --perms ${MEDIA_DIR} ${BACKUP_DIR}


# Done!
# -----

exit 0
