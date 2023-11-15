
# JSON objects used in [API](./api.md)

## TODO: Надо выяснить формат времени и формат error

---

+ __[error](#error)__
+ __[news](#news)__
+ __[oid](#oid)__
+ __[login](#login)__
+ __[registration](#registration)__
+ __[main](#main)__
+ __[course](#course)__
+ __[entity](#entity)__
+ __[user](#user)__
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
_Этот объект используется для пересылки сообщения об ошибке в случае 400 статус кода_

```json
{
    err: string,
}
```
__Description of attributes:__<br>

+ __err__ - сообщение об ошибке (в каком формате то??)

__Examples:__<br>

```json
{
    err: "email validation error"
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
    email: string,
    password: string,
}
```
__Description of attributes:__<br>

+ __email__ - почта
+ __password__ - пароль, минимум 8 символов (строчные, прописные, цифры)

__Examples:__<br>

```json
{
    email: "andrey.shahov@example.ru",
    password: "qwerty1234QW",
}
```

---

### __registration__

__Description:__<br>
_Этот объект используется при регистрации новых пользователей_

```json
{
    email: string,
    password: string,
    name: string,
    secondName: string,
    patronymic: string,
    phone: string,
    class: int,
}
```
__Description of attributes:__<br>

+ __email__ - почта, ограничение 64 символа
+ __password__ - пароль, минимум 8 символов (строчные, прописные, цифры)
+ __name__ - имя пользователя, ограничение 24 символа
+ __secondName__ - фамилия, ограничение 24 символа
+ __patronymic__ - Отчество, ограничение 24 символа
+ __phone__ - Телефон
+ __class__ - класс

__Examples:__<br>

```json
{
    email: "andrey.shahov@example.ru",
    password: "qwerty1234QW",
    name: "Андрей",
    secondName: "Шахов",
    patronymic: "Владимирович",
    phone: "89993332211"
    class: 1,
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

### __entity__

__Description:__<br>
_Этот объект используется для определения конкретной сущности с правами на сайте_

```json
{
    id: int,
    role: string,
    date: string,
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при создании объекта сущности. __id__ у разных ролей могу пересекаться. __id__ у этого объекта и объекта __[user](#user)__ будут совпадать в случае когда __role__ = user
+ __role__ - этот атрибут, служит цели авторизации определённого пользователя, то есть определяет какой спектр API доступен под данным аккаунтом<br>
_available values:_
    + anonym - любой не аутентифицированный пользователь с __id__ = 0
    + user - пользователь, который зарегистрирован как ученик
    + admin - административный аккаунт, на данный момент существует всего один с __id__ = 1
    + teacher - аккаунт учителя (модератора), создаётся через административный аккаунт
+ __date__ - дата создания данной сущности

__Examples:__<br>

```json
{
    id: 0,
    role: "anonym",
    date: "..."
}

{
    id: 1,
    role: "admin",
    date: "..."
}

{
    id: 15,
    role: "user",
    date: "..."
}
```

---

### __user__

__Description:__<br>
_Этот объект содержит в себе всю информацию о конкретном user, этот объект генерируется на бекенде на основе **[registration](#registration)**_

```json
{
    id: int
    email: string,
    name: string,
    secondName: string,
    patronymic: string,
    phone: string,
    class: int,
}
```
__Description of attributes:__<br>

+ __id__ - уникальный числовой идентификатор, который генерируется на стороне бекенда при регистрации пользователя
+ __email__ - почта, ограничение 64 символа
+ __name__ - имя пользователя, ограничение 24 символа
+ __secondName__ - фамилия, ограничение 24 символа
+ __patronymic__ - Отчество, ограничение 24 символа
+ __phone__ - Телефон
+ __class__ - класс

__Examples:__<br>

```json
{
    id: 15,
    email: "andrey.shahov@example.com",
    name: "Андрей",
    secondName: "Шахов",
    patronymic: "Владимирович",
    phone: "89993332211",
    class: 1,
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