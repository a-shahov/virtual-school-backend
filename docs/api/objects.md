
# JSON objects used in [API](./api.md)

## TODO: Надо выяснить формат времени и формат error

---

+ __[news](#news)__
+ __[error](#error)__ ok
+ __[oid](#oid)__
+ __[login](#login)__ ok
+ __[login_response](#login_response)__ ok
+ __[registration](#registration)__ ok
+ __[main](#main)__
+ __[course](#course)__
+ __[token](#token)__ ok
+ __[user](#user)__ ok
+ __[misc](#misc)__
+ __[notification](#notification)__

---

### __news__

__Description:__<br>
_Этот объект используется на главной странице для отображения новостей_

```json
{
    id: int,
    title: string,
    description: string,
    body: string,
    date: string,
    image: string,
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор новости, который генерируется на стороне бекенда при создании объекта
+ __title__ - заголовок новости, максимальная длина 128 символов
+ __description__ - краткое описание новости, максимальная длина 256 символов
+ __body__ - тело новости, максимальная длина 1024 символа
+ __date__ - дата создания новости в формате "%d %m %Y" ([справка тут](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)) метка создаётся на сервере
+ __image__ - URL адрес картинки которая может отображаться в заголовке новости

__Examples:__<br>

```json
{
    id: 1,
    title: "Тестовый заголовок",
    description: "Описание для тестовой новости.",
    body: "Тестовое тело.",
    date: "...",
    image: "https://example.com/image.png"
}
```

---

### __error__

__Description:__<br>
_Этот объект используется для пересылки сообщений об ошибках в различных случаях_

```json
{
    "errors": ["string"],
}
```
__Description of attributes:__<br>

+ __errors__ - массив сообщений об ошибках

__Examples:__<br>

```json
{
    "errors": ["email validation error", "name validation error"]
}

{
    "errors": ["email already exists"]
}
```

---

### __oid__

__Description:__<br>
_Этот объект используется для передачи на фронт id созданного объекта в ответах **POST** запросов_

```json
{
    id: int
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при создании объекта

__Examples:__<br>

```json
{
    id: 1
}
```

---

### __login__

__Description:__<br>
_Этот объект используется для лоигна пользователей_

```json
{
    "email": "string",
    "password": "string",
}
```
__Description of attributes:__<br>

+ __email__ - почта
+ __password__ - пароль, минимум 8 символов (ascii заглавные, прописные и цифры)

__Examples:__<br>

```json
{
    "email": "andrey.shahov@example.ru",
    "password": "qwerty1234QW",
}
```

---

### __login_response__

__Description:__<br>
_Этот объект состоит из двух объектов **[token](#token)** and **[user](#user)**_

```json
{
    "role": "string",
    "token": <token object>,
    "user_info": <user object>,
}
```

__Description of attributes:__<br>

+ __role__ - Роль авторизованного пользователя (user, admin, teacher)
+ __token__ - **[token](#token)** object
+ __user__ - **[user](#user)** object

__Examples:__<br>

```json
{
    "role": "user",
    "token": {
        "token_type": "Bearer",
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ2aXJ0dWFsLXNjaG9vbC1iYWNrZW5kIiwic3ViIjoidXNlciIsInVlaWQiOjIsImlhdCI6MTcwNzEzNDMyNi41NDU4MDcsImV4cCI6MTcwNzEzNDY4Ni41NDU4MDd9.SUUlvcQvL4EOlKiE7lSSNQjwU7eRn_cAu7VdV1QWMhk",
        "expires_in": 360,
        "expires": 1709726327
    },
    "user_info": {
        "login_id": 2,
        "state": "new",
        "email": "andrey@yandex.ru",
        "name": "Андрей",
        "secondname": "Шахов",
        "patronymic": "Владимирович",
        "birthdate": "2000-12-22",
        "phone": "8996992229",
        "class": 1
    }
}
```

---

### __registration__

__Description:__<br>
_Этот объект используется при регистрации новых пользователей_

```json
{
    "email": "string",
    "password": "string",
    "name": "string",
    "secondname": "string",
    "patronymic": "string",
    "birthdate": "string",
    "phone": "string",
    "class": "int",
}
```
__Description of attributes:__<br>

+ __email__ - Почта, ограничение 64 символа
+ __password__ - Пароль, минимум 8 символов. Должен содержать строчные, заглавные, ascii символы и цифры, также допустимыми являются специальные символы
+ __name__ - Имя пользователя, ограничение 24 символа
+ __secondname__ - фамилия, ограничение 24 символа
+ __patronymic__ - Отчество, ограничение 24 символа
+ __birthdate__ - Дата рождения (YYYY-MM-DD)
+ __phone__ - Телефон
+ __class__ - Класс [1-11]

__Examples:__<br>

```json
{
    "email": "andrey.shahov@example.ru",
    "password": "qwerty1234QW",
    "name": "Андрей",
    "secondName": "Шахов",
    "patronymic": "Владимирович",
    "birthdate": "2000-11-22",
    "phone": "89993332211",
    "class": 1,
}
```

---

### __main__

__Description:__<br>
_Этот объект используется для редактирования основной информации на главной странице школы_

```json
{
    description: string,
    image: string,
}
```
__Description of attributes:__<br>

+ __description__ - краткое описание школы, ограничение 256 символов
+ __image__ - URL картинки, которая используется на главной странице

__Examples:__<br>

```json
{
    description: "Виртуальная школа - это полностью цифровая площадка для получения полного и неполного среднего образования, где все вопросы с документами мы берём на себя!"
}
```

### __course__

__Description:__<br>
__

```json
{
    id: int
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при создании объекта

__Examples:__<br>

```json
{
    id: 1
}
```

---

### __token__

__Description:__<br>
_Этот объект используется для отправки access token, в случае успешной аутентификации_

```json
{
    "token_type": "string",
    "access_token": "string",
    "expires_in": "int",
    "expires": "int",
}
```
__Description of attributes:__<br>

+ __token_type__ - тип токена всегда должен быть _"Bearer"_
+ __access_token__ - jwt access token, используется для получения доступа к ресурсам, нужно выставлять в заголовок запроса _"Authorization: Bearer \<access token\>"_
_available values:_
    + _anonym_ - любой не аутентифицированный пользователь (псевдосущность в ответе она не приходит)
    + _user_ - пользователь, который зарегистрирован как ученик
    + _admin_ - административный аккаунт
    + _teacher_ - аккаунт учителя (модератора), создаётся через административный аккаунт
+ __expires_in__ - время жизни access token в секундах
+ __expires__ - временная метка истечения _refresh token_ в формате _unix epoch time_

__Examples:__<br>

```json
{
    "token_type": "Bearer",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ2aXJ0dWFsLXNjaG9vbC1iYWNrZW5kIiwic3ViIjoidXNlciIsImlhdCI6MTcwNDA3ODE1NS4xMzUxNDEsImV4cCI6MTcwNDA3ODUxNS4xMzUxNDF9.5ydbPEfJZoLGd30k18rC4jY1rfHFnCUTfS4EOyTa7Mw",
    "expires_in": 360,
    "expires": 1706670155
}
```

---

### __user__

__Description:__<br>
_Этот объект содержит в себе всю информацию о конкретном user, этот объект генерируется на бекенде на основе **[registration](#registration)**_

```json
{
    "login_id": "int",
    "state": "string",
    "email": "string",
    "name": "string",
    "secondName": "string",
    "patronymic": "string",
    "birthdate": "string",
    "phone": "string",
    "class": "int",
}
```
__Description of attributes:__<br>

+ __login_id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при регистрации пользователя
+ __state__ - текущее состояние данного пользователя (new, activated, deleted, blocked)
+ __email__ - почта, ограничение 64 символа
+ __name__ - имя пользователя, ограничение 24 символа
+ __secondname__ - фамилия, ограничение 24 символа
+ __patronymic__ - Отчество, ограничение 24 символа
+ __phone__ - Телефон
+ __class__ - класс

__Examples:__<br>

```json
{
    "login_id": 15,
    "state": "new",
    "email": "andrey.shahov@example.com",
    "name": "Андрей",
    "secondname": "Шахов",
    "patronymic": "Владимирович",
    "phone": "89993332211",
    "class": 1,
}
```

---

### __misc__

__Description:__<br>
__

```json
{
    id: int
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при создании объекта

__Examples:__<br>

```json
{
    id: 1
}
```

---

### __notification__

__Description:__<br>
__

```json
{
    id: int
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при создании объекта

__Examples:__<br>

```json
{
    id: 1
}
```

---