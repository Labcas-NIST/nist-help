#!/bin/sh -e
#
# Sync NIST Help Portal DB to local directory
# ===========================================
#
# Synchronize the NIST Help portal DB from Jenins to local for development

PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/bin
export PATH
WORKSPACE=${WORKSPACE:-${PWD:-`pwd`}}
media=${WORKSPACE}/media
source=tumor.jpl.nasa.gov:/usr/local/edrn/nist/help/ops-nist


# PostgreSQL Database
# -------------------
#
# We always assume this thing is changing and frequently, so we delete our local copy
# and get a fresh one every time.

echo "📈 Retrieving database" 1>&2
rm -f "latest.sql.bz2"
scp -p $source/latest.sql.bz2 ${WORKSPACE}

if [ \! -f "latest.sql.bz2" ]; then
    echo "Failed to get $source/latest.sql.bz2" 1>&2
    exit 1
fi


# Media Blobs
# -----------
#
# The blobs hardly change and some day there could be many of them. In that eventuality,
# we definitely take advantage of the thumbprinting (checksum) features of `rsync` in
# order to speed things up on subsequent runs.

echo "📀 Retrieving blobs" 1>&2
[ -d "$media" ] || mkdir -p "$media"
rsync --checksum --no-motd --recursive --delete --progress $source/media ${WORKSPACE}


# That's all folks
# ----------------

echo "😌 All done" 1>&2
exit 0
