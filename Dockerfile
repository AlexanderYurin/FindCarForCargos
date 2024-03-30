FROM python:3.11-alpine3.16
COPY service /service
WORKDIR /service
COPY requirements.txt /temp/requirements.txt
EXPOSE 8000

RUN pip install --no-cache-dir -r /temp/requirements.txt

CMD ["sh", "-c", "python manage.py migrate"]