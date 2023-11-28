# In this file we'll be using the industry-standard methodology known as multi-stage builds
# 1st stage to build dependancy wheels: Wheels are a binary distribution format for Python packages, 
# it means that they can be installed very quickly, as compared to source distributions, which need to be compiled before installing.
# 2nd stage run the application

ARG PYTHON_VERSION=3.11.4-bullseye

FROM python:${PYTHON_VERSION} as python


FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

# Get set of essential tools to compile code libpq-dev is used for postgresql
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

# Build wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt


FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# This way within django we can tell if running from a docker container
ENV AM_I_IN_DOCKER_CONTAINER Yes

WORKDIR ${APP_HOME}


RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  # Clean up
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  # Helps to reduce the size of the image
  && rm -rf /var/lib/apt/lists/*


COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Installing the wheels, with --no-index we avoid pip searching for packages on PyPI
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY ./docker/local/django/entrypoint /entrypoint
# Ensure /entrypoint has unix line endings
RUN sed -i 's/\r$//g' /entrypoint
# Give execute permissions to /entrypoint
RUN chmod +x /entrypoint


COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY . ${APP_HOME}

ENTRYPOINT [ "/entrypoint" ]