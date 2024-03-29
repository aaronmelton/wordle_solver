##################
### BASE IMAGE ###
##################

ARG PYTHON_VER=3.10

FROM python:${PYTHON_VER}-alpine AS base
LABEL prune=true

WORKDIR /app

RUN apk --update add build-base gcc libffi-dev libstdc++
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .

RUN poetry install --no-dev

##################
### TEST IMAGE ###
##################

FROM base AS test
LABEL prune=true

RUN poetry install

COPY . .

RUN echo '-->Running Flake8' && \
    flake8 . && \
    echo '-->Running Black' && \
    black --check --diff . && \
    echo '-->Running isort' && \
    find . -name '*.py' | xargs isort && \
    echo '-->Running Pylint' && \
    find . -name '*.py' | xargs pylint --rcfile=pyproject.toml && \
    echo '-->Running pydocstyle' && \
    pydocstyle . --config=pyproject.toml && \
    echo '-->Running Bandit' && \
    bandit --recursive ./ --configfile pyproject.toml

###################
### FINAL IMAGE ###
###################

FROM python:${PYTHON_VER}-alpine

ARG PYTHON_VER

WORKDIR /app

RUN mkdir -p /app/log/

COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=base /usr/lib/libstdc* /usr/lib/
COPY --from=base /usr/lib/libgcc* /usr/lib/

COPY ./wordle_solver .

ENTRYPOINT ["python"]

CMD ["wordle_solver.py"]
