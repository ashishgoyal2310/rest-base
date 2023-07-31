# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
WORKDIR /app
COPY requirements.txt /app

RUN python -m pip install -r requirements.txt
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV DEBUG True

COPY . /app
RUN python manage.py migrate

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
