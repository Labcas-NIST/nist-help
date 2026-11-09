# 💽🔭 NIST Help Portal

This software implements a [Wagtail](https://wagtail.org)-based content management system with NASA-JPL style that provides through-the-web editable web pages, a CDE explorer, password reset, and other features for the [NIST-JPL collaboration featuring LabCAS](https://github.com/Labcas-NIST).


## 🤓 Development

To run this software locally, you'll need:

-   Python 3.11 (not tested on any other version)
-   PostgreSQL 15 (16 could also work)
-   A search engine; either:
    -   OpenSearch 2.9–2.11 (preferred)
    -   Elasticsearch 7.17

You'll also need a copy of the current content database from `ddsa-labcas` if you want to experiment with the current content. Alternatively, you can also start from scratch.

Common [Task](https://taskfile.dev/) commands:

- `task clean` — removes the Python virtual environment
- `task venv` — creates the Python virtual environment
- `task dev-rebuild` — rebuilds the NIST Help portal for local development, gathering the latest content from the production host
- `task run` — also the default, starts a local server


## Transfering Production Content

A cron job runs `@weekly` on `ddsa-labcas` under the `ddsaops` user that runs `pg_dump` to get a dump of the content database. Meanwhile on `cancer`, a cron job runs `@weekly` that executes `support/sync-from-ops.sh` to bring that SQL dump and the `media` folder from `ddsa-labcas` to `cancer`.

The `task dev-rebuild` command will then take that content from `cancer` and rebuild the NIST help portal for local development.


## Containerization

Run `task image` to make the Docker image, `edrndocker/nisthelp:latest`, which will be loaded into the local Docker registry. You can then tag and push it to the Docker Hub or elsewhere.

Start the Docker composition locally with

    task compose -- up --detach

Then load the database and apply migrations:

    task compose -- exec db createuser --username=postgres --createdb --login --createrole unh
    task compose -- exec db psql --username=postgres --command="ALTER ROLE unh PASSWORD 's3cr3t'"
    task compose -- exec db createdb --username=postgres --encoding=UTF8 --owner=postgres nisthelp
    bzip2 --decompress --stdout latest.sql.bz2 | task compose -- exec --no-tty db psql --username=postgres --dbname=nisthelp --echo-errors --set=ON_ERROR_STOP=on
    task compose -- exec portal bin/django-admin migrate 
    
Then you can visit the site at https://localhost:4239/ (ignoring the self-signed certificate warning).


## Deployment at JPL

Run `support/jpl-deploy.sh` to deploy the NIST Help portal to the JPL production server.
