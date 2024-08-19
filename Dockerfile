FROM python:3.12.4-slim-bookworm AS base
# FROM python:3.12.4-alpine3.20 as base

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

RUN apt -y update 
RUN apt -y install gcc
# RUN apt -y install build-essential
RUN apt -y install wget
RUN apt -y install curl
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN echo "6083ef1974d11f49d42ae668fb9d513f7dc2c6276ffa47caed488c4b47268593  mariadb_repo_setup" \
    | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup
# RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"

RUN apt -y install libmariadb3 libmariadb-dev

FROM base AS python-deps
# RUN apk add libmariadb3 libmariadb-dev
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv --upgrade

COPY Pipfile .
COPY Pipfile.lock .

# RUN pipenv sync
RUN pipenv install 


FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home appuser #For Bookworm
# RUN adduser -S appuser #For Alpine
WORKDIR /home/appuser
USER appuser

COPY --chmod=777 ./score_counter ./score_counter
# COPY --chmod=777 docker-entrypoint.sh .
# CMD docker-entrypoint.sh
CMD python score_counter/main.py

EXPOSE 5000