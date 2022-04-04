FROM python:3.10 AS python_base

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pipenv

FROM python_base AS python_dependency

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

RUN pipenv install --deploy

FROM python_dependency AS runtime

COPY --from=python_dependency /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80"]
