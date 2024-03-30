# Сервис поиска ближайших машин для перевозки грузов.

### Технологический стек

- Python (Django Rest Framework)
- PostgreSQL
- Docker, docker-compose

### Структура БД

#### Характеристики груза

- Локация pick-up
- Локация delivery
- Вес (1-1000)
- Описание

#### Характеристики машины

- Уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце)
- Текущая локация
- Грузоподъемность (1-1000)
- 
#### Характеристики локации
- Город
- Штат
- Почтовый индекс (zip)
- Широта
- Долгота

### Установка

- Склонируйте репозиторий:
  ```bash
  git clone https://github.com/AlexanderYurin/FindCarForCargos
  ```
- Убедитесь, что у вас установлен Docker и Docker Compose.
- Запустите контейнеры:
    ```bash
    docker-compose up --build --force-recreate
    ```
- Сделайте миграции
  ```bash
    docker-compose run --rm  service sh -c " python manage.py migrate" 
  ```
- Загрузите локации
  ```bash
    docker-compose run --rm  service sh -c " python manage.py load_locations"
  ```
- Загрузите случайные 40 машин
  ```bash
    docker-compose run --rm  service sh -c " python manage.py load_locations"
  ```
Теперь ваше приложение должно быть доступно по адресу
http://localhost:8000/api/v1/


### Функциональность:

- Создание нового груза http://localhost:8000/api/v1/cargo/
- Получение списка грузов http://localhost:8000/api/v1/cargo/
- Получение информации о конкретном грузе по ID http://localhost:8000/api/v1/cargo/{cargo_id}
- Редактирование машины по ID http://localhost:8000/api/v1/car/{car_id}
- Редактирование груза по ID http://localhost:8000/api/v1/cargo/{cargo_id}
- Удаление груза по ID http://localhost:8000/api/v1/cargo/{cargo_id}




