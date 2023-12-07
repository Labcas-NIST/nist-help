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

Regardless, begin by creating a database:

    createdb nisthelp

Next, run the following commands:

    ./manage.sh makemigrations





```console
$ createdb nisthelp
$ ./manage.sh migrate
$ ./manage.sh createsuperuser --username root --email your@email.com
```
