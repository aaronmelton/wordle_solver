#
# Start with Base image
#
ARG PYTHON_VER=3.10

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .

RUN poetry install --no-dev

#
# Perform any tests
#

FROM base AS test

RUN poetry install

COPY . .

#
# Perform code checks
#

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

ENTRYPOINT ["pytest"]

CMD ["--color=yes", "-vvv"]

#
# Build final image
#

FROM python:${PYTHON_VER}-slim AS cli

ENV LOG_LEVEL=INFO
ENV LOG_PATH=./log/
ENV LOG_PREFIX=wordle_solver_

ARG PYTHON_VER

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/log/

COPY --from=base /usr/src/app /usr/src/app
COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

COPY ./wordle_solver .

ENTRYPOINT ["python"]

CMD ["wordle_solver.py"]