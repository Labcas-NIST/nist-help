#!/bin/sh -e
#
# Sync NIST Help Portal DB
# ========================
#
# Synchronize the NIST Help portal DB from ops

PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
export PATH
BACKUP_DIR=${BACKUP_DIR:-/home/ddsaops/backups/nisthelp}
MEDIA_DIR=${MEDIA_DIR:-/home/ddsaops/nist-help/media}
WORKSPACE=${WORKSPACE:-${PWD:-`pwd`}}
source="ddsa-labcas.jpl.nasa.gov"
user=ddsaops

# Do it
# -----

[ -d ${WORKSPACE}/media ] || mkdir ${WORKSPACE}/media
rm --force latest.sql.bz2
scp ${user}@${source}:$BACKUP_DIR/database/latest.sql.bz2 .
rsync --checksum --no-motd --recursive --delete --progress ${user}@${source}:$MEDIA_DIR ${WORKSPACE}

# Done!
# -----

exit 0
