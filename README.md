# api_yamdb
api_yamdb
# api_yamdb
api_yamdb



### api_final_yatube
**api_final_yatube** - это проект, на котором можно регистрироваться, и создавать посты с текстом<br>
и изображениями. На проекте реализован API интерфейс REST API, который позволяет делать запросы к<br>
различным эндпоинтам сайта и получать ответ в зависимости от статуса клиента.<br>

#### Чтобы развернуть проект на локальной машине выполните следующие действия:
  -Форкните репозиторий к себе на гитхаб<br>
  -Клонируйте репозиторий:<br>
    ```git clone <url репозитория>```<br>
  -Создайте и активируйте виртуальное окружение:<br>
    Windows:<br>
      ```python -m venv venv```<br>
      ```source venv/Script/activate```<br>
    Mac, Linux:<br>
      ```python3 -m venv env```<br>
      ```source env/bin/activate```<br>
  -Установите зависимости:<br>
    Windows:<br>
      ```python -m pip install --upgrade pip```<br>
    Mac, Linux:<br>
      ```python3 -m pip install --upgrade pip```<br>
    ```pip install -r requirements.txt```<br>
  -Примените миграции:<br>
    Windows:<br>
      ```python manage.py migrate```<br>
    Mac, Linux:<br>
      ```python3 manage.py migrate```<br>
  -Запустите проект:<br>
    ```python manage.py runserver```<br>

**Примеры запросов:**
   -Получение и создание публикаций **GET, POST**<br>
    http://127.0.0.1:8000/api/v1/posts/<br>
   -Получение, изменение, частичное изменнеие и удаление публикаци **GET, PUT, PATCH, DELETE**<br>
    http://127.0.0.1:8000/api/v1/posts/{id}/<br>
   -Получение и создание коментариев **GET, POST**<br>
    http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/<br>
   -Получение, изменение, частичное изменнеие и удаление коментария  **GET, PUT, PATCH, DELETE**<br>
    http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/<br>
   -Получение списка сообществ **GET**<br>
    http://127.0.0.1:8000/api/v1/groups/<br>
   -Информация о сообществе  **GET**<br>
    http://127.0.0.1:8000/api/v1/groups/{id}/<br>
   -Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены<br>
    http://127.0.0.1:8000/api/v1/follow/ **GET**<br>
   -Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса. Анонимные запросы запрещены<br>
    http://127.0.0.1:8000/api/v1/follow/ **POST**<br>
   -Получить JWT-токен **POST**<br>
    http://127.0.0.1:8000/api/v1/jwt/create/<br>
   -Обновить JWT-токен **POST**<br>
    http://127.0.0.1:8000/api/v1/jwt/refresh/<br>
   -Проверить JWT-токен **POST**<br>
    http://127.0.0.1:8000/api/v1/jwt/verify/<br>
    
    
    

**Примеры запросов и ответов:**
  -Получение и создание публикаций **GET, POST**<br>
  http://127.0.0.1:8000/api/v1/posts/ <br>
  **GET**<br>
  {<br>
    "count": 123,<br>
    "next": "http://api.example.org/accounts/?offset=400&limit=100",<br>
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",<br>
    "results": [<br>
      {<br>
        "id": 0,<br>
        "author": "string",<br>
        "text": "string",<br>
        "pub_date": "2021-10-14T20:41:29.648Z",<br>
        "image": "string",<br>
        "group": 0<br>
      }<br>
    ]<br>
  }<br>
  **POST**<br>
  {<br>
    "text": "string",<br>
    "image": "string",<br>
    "group": 0<br>
  }<br>
  <br>
  -Получение, изменение, частичное изменнеие и удаление публикаци **GET, PUT, PATCH, DELETE**<br>
  http://127.0.0.1:8000/api/v1/posts/{id}/ <br>
  **GET**<br>
  {<br>
    "id": 0,<br>
    "author": "string",<br>
    "text": "string",<br>
    "pub_date": "2019-08-24T14:15:22Z",<br>
    "image": "string",<br>
    "group": 0<br>
  }<br>
  **PUT, PATCH**<br>
  {<br>
    "text": "string",<br>
    "image": "string",<br>
    "group": 0<br>
  }<br>
  **DELETE**<br>
  {<br>
    "detail": "Учетные данные не были предоставлены."<br>
  }<br>
<br>
  -Получение и создание коментариев **GET, POST**<br>
  http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/ <br>
  **GET**<br>
  [<br>
    {<br>
      "id": 0,<br>
      "author": "string",<br>
      "text": "string",<br>
      "created": "2019-08-24T14:15:22Z",<br>
      "post": 0<br>
    }<br>
  ]<br>
  **POST**<br>
  {<br>
    "text": "string"<br>
  }<br>
<br>
  -Получение, изменение, частичное изменнеие и удаление коментария  **GET, PUT, PATCH, DELETE**<br>
  http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/ <br>
  **GET**<br>
  {<br>
    "id": 0,<br>
    "author": "string",<br>
    "text": "string",<br>
    "created": "2019-08-24T14:15:22Z",<br>
    "post": 0<br>
  }<br>
  **PUT, PATCH**<br>
  {<br>
    "text": "string"<br>
  }<br>
  **DELETE**<br>
  {<br>
    "detail": "Учетные данные не были предоставлены."<br>
  }<br>
<br>
  -Получение списка сообществ **GET** <br>
  http://127.0.0.1:8000/api/v1/groups/ <br>
  [<br>
    {<br>
      "id": 0,<br>
      "title": "string",<br>
      "slug": "string",<br>
      "description": "string"<br>
    }<br>
  ]<br>
<br>
  -Информация о сообществе  **GET** <br>
  http://127.0.0.1:8000/api/v1/groups/{id}/ <br>
  {<br>
    "id": 0,<br>
    "title": "string",<br>
    "slug": "string",<br>
    "description": "string"<br>
  }<br>
<br>
  -Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены <br>
  http://127.0.0.1:8000/api/v1/follow/ **GET**<br>
  [<br>
    {<br>
      "user": "string",<br>
      "following": "string"<br>
    }<br>
  ]<br>
<br>
  -Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса. Анонимные запросы запрещены <br>
  http://127.0.0.1:8000/api/v1/follow/ **POST** <br>
  {<br>
    "following": "string"<br>
  }<br>
<br>
  -Получить JWT-токен **POST** <br>
  http://127.0.0.1:8000/api/v1/jwt/create/ <br>
  {<br>
    "username": "string",<br>
    "password": "string"<br>
  }<br>
<br>
  -Обновить JWT-токен **POST**<br>
  http://127.0.0.1:8000/api/v1/jwt/refresh/ <br>
  {<br>
    "refresh": "string"<br>
  }<br>
<br>
  -Проверить JWT-токен **POST**<br>
  http://127.0.0.1:8000/api/v1/jwt/verify/<br>
  {<br>
    "token": "string"<br>
  }<br>