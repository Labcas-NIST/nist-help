# NIST Help — production image
# ============================
#
# Python dependencies from requirements.txt plus the application source under
# src/, served by Gunicorn. Build from the repository root:
#
#     docker buildx build --file docker/Dockerfile --tag edrndocker/nisthelp:latest .

FROM python:3.11-slim-bookworm
ARG userid=500

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src \
    DJANGO_SETTINGS_MODULE=nisthelp.settings.production \
    STATIC_ROOT=/app/static \
    MEDIA_ROOT=/app/media

# Runtime libraries (Pillow, LDAP, PostgreSQL client, healthcheck)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update --quiet --yes \
    && apt-get install --quiet --yes --no-install-recommends \
        ca-certificates \
        curl \
        gosu \
        libjpeg62-turbo \
        zlib1g \
        libtiff6 \
        libfreetype6 \
        libwebp7 \
        libopenjp2-7 \
        libldap-2.5-0 \
        libsasl2-2 \
        libssl3 \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN addgroup --system --gid ${userid} nisthelp \
    && adduser --system --uid ${userid} --ingroup nisthelp nisthelp \
    && install --owner=nisthelp --group=nisthelp --directory /app/media /app/static

# Virtualenv + Gunicorn
RUN python -m venv /app \
    && /app/bin/pip install --quiet --upgrade pip setuptools wheel \
    && /app/bin/pip install --quiet --progress-bar off "gunicorn==21.2.0"

# Python dependencies (psycopg2 / python-ldap need a short-lived toolchain)
COPY --chown=nisthelp:nisthelp requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update --quiet --yes \
    && apt-get install --quiet --yes --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        libldap2-dev \
        libsasl2-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
    && /app/bin/pip install --progress-bar off --requirement /app/requirements.txt \
    && apt-get purge --quiet --yes --auto-remove \
        gcc g++ libpq-dev libldap2-dev libsasl2-dev libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Application source
COPY --chown=nisthelp:nisthelp src /app/src
COPY --chown=nisthelp:nisthelp docker/entrypoint.py docker/gunicorn.conf.py /app/

# Collect static assets into /app/static (dummy secrets only for build-time Django boot)
RUN gosu nisthelp env \
        SECRET_KEY=build-only-not-for-runtime \
        LDAP_URI=ldaps://localhost \
        /app/bin/django-admin collectstatic --no-input --clear \
    && chown -R nisthelp:nisthelp /app \
    && ln -sf /app/bin/django-admin /usr/bin/django-admin

EXPOSE 8000
VOLUME ["/app/media"]
USER nisthelp
ENTRYPOINT ["/app/bin/gunicorn"]

HEALTHCHECK --interval=5m --timeout=2m --start-period=10m \
    CMD curl --fail --retry 6 --max-time 5 --retry-delay 10 --retry-max-time 60 http://127.0.0.1:8000/
