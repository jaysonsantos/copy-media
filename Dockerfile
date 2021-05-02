FROM python:3.9 as builder
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
ENV PATH="/root/.poetry/bin:$PATH"
WORKDIR /code
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root
COPY copy_media copy_media/
RUN poetry build && mv dist/*.whl /copy_media-0.0.0-py3-none-any.whl

FROM python:3.9
COPY --from=builder /copy_media-0.0.0-py3-none-any.whl /
RUN pip install /copy_media-0.0.0-py3-none-any.whl && rm /copy_media-0.0.0-py3-none-any.whl
