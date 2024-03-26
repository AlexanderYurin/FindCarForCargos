FROM python:3.11-alpine3.16
COPY . /services
WORKDIR /services
EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata app/fixtures/fixtures.json"]