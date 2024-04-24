FROM python:3.11.1

RUN mkdir -p /aiohttp_vs_httpx/
WORKDIR /aiohttp_vs_httpx/

RUN pip install --upgrade pip

RUN pip install --upgrade poetry

COPY poetry.lock pyproject.toml /aiohttp_vs_httpx/
RUN poetry config virtualenvs.create false
RUN poetry install --only main
COPY . /aiohttp_vs_httpx/