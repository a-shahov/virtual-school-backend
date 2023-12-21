# API

## TODO Нужно понять тут че надо сделать с teacher, admin + ещё вопрос с документами + решить вопрос с шестерёнкой -> обновить API для коррелляции с новыми схемами

В рамках сайта школы на данный момент используются четыре сущности:

| Entity             | Description                          |
|--------------------|--------------------------------------|
|  __anonym__        | любой неавторизованный пользователь  |
|  __user__          | конкретный зарегистрированный пользователь (ученик)|
|  __teacher__       | своего рода это аккаунт модератора, который может создавать тесты|
|  __admin__         | администратор имеет доступ к панели администратора, через которую можно управлять сайтом|

> __For detailed information about objects see [objects](./objects.md)__

> __For detailed information about parameters in GET requests see [parameters](./parameters.md)__

---

+ __[API for auth](#auth)__
+ __[API for main page](#main-page)__
+ __[API for user account](#user-account)__
+ __[API for teacher account](#teacher-account)__
+ __[API for admin account](#admin-account)__

---

### __auth__

> Authorization flow: первоначально неаутентифицированный клиент шлёт запрос на __/auth/login__ с парой email/password, в случае успешной аутентификации он в ответе получает access token и время его жизни, а также у него в cookie выставляется HttpOnly refresh_token. Далее выставляя полученный access token в заголовок запроса __Authorization: Bearer \<token\>__, клиент получает возможность делать аутентифицированные запросы на endpoints. К концу срока жизни access token, клиент может получить новый access token с помощью своего refresh token послав __GET /auth/refresh_token__. В случае если его refresh token валиден (его ещё не использовали и не истёк срок жизни), то в ответ он получит новую пару access token и refresh token. Access token никак нельзя отозвать. При отправлении запроса на __/auth/logout__ все refresh token с данным jti станут невалидными и будут удалены из бд. В случае истечения срока жизни refresh token, клиенту нужно будет пройти повторную аутентификацию.

+ __POST__ `/auth/login`<br>
_description:_ endpoint for login action<br>
_permission:_ __anonym__<br>
_request body:_ __[login](./objects.md#login)__<br>
_responses:_<br>
    + 200 - OK. With __[entity](./objects.md#entity)__
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 404 - not found in the case of authorized user
    + 500 - internal error

+ __POST__ `/auth/registration`<br>
_description:_ endpoint for registration action<br>
_permission:_ __anonym__<br>
_request body:_ __[registration](./objects.md#registration)__<br>
_responses:_<br>
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__
    + 404 - not found in the case of authorized user
    + 500 - internal error

+ __GET__ `/auth/logout`<br>
_description:_ endpoint for logout action<br>
_permission:_ __user__, __teacher__, __admin__<br>
_responses:_<br>
    + 200 - OK
    + 404 - not found in the case of non authorized user
    + 500 - internal error

+ __GET__ `/auth/whoami`<br>
_description:_ endpoint for getting information about an entity<br>
_permission:_ __all__<br>
_responses:_<br>
    + 200 - OK. With __[entity](./objects.md#entity)__
    + 404 - not found in the case of non authorized user
    + 500 - internal error

---

### __main page__

+ __GET__ `/main/info`<br>
_description:_ endpoint for getting short main page info<br>
_permission:_ __all__<br>
_responses:_<br>
    + 200 - OK. With __[main](./objects.md#main)__
    + 500 - internal error

+ __PUT__ `/main/info`<br>
_description:_ endpoint for upload short main page info<br>
_permission:_ __admin__<br>
_request body:_ __[main](./objects.md#main)__<br>
_responses:_<br>
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for non admin entities
    + 500 - internal error

+ __GET__ `/main/news[?parameters]`<br>
_description:_ endpoint for getting news from db<br>
_permission:_ __all__<br>
_parameters:_ __[news parameters](./parameters.md#news)__<br>
_responses:_<br>
    + 200 - OK. With array \[__[news](./objects.md#news)__\]
    + 500 - internal error

+ __POST__ `/main/news`<br>
_description:_ endpoint for adding new posts with news<br>
_permission:_ __admin__<br>
_request body:_ __[news](./objects.md#news)__ without __id__ and __date__<br>
_responses:_
    + 200 - OK. With __[oid](./objects.md#oid)__
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for non admin entities
    + 500 - internal error

+ __PATCH__ `/main/news/<id:int>`<br>
_description:_ endpoint for editing posts with news. __id__ - unique identifier of the __[news](./objects.md#news)__<br>
_permission:_ __admin__<br>
_request body:_ fields of __[news](./objects.md#news)__<br>
_responses:_
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for non admin entities
    + 404 - not found
    + 500 - internal error

+ __DELETE__ `/main/news/<id:int>`<br>
_description:_ endpoint for deleting posts with news. __id__ - unique identifier of the __[news](./objects.md#news)__<br>
_permission:_ __admin__<br>
_responses:_
    + 200 - OK
    + 403 - forbidden for non admin entities
    + 404 - not found
    + 500 - internal error

+ __GET__ `/main/courses`<br>
_description:_ endpoint for getting all available courses in school<br>
_permission:_ __all__<br>
_responses:_
    + 200 - OK. With array \[__[course](./objects.md#course)__\]
    + 500 - internal error

+ __POST__ `/main/courses`<br>
_description:_ endpoint for adding new courses in school<br>
_permission:_ __admin__<br>
_request body:_ __[course](./objects.md#course)__ without __id__<br>
_responses:_
    + 200 - OK. With __[oid](./objects.md#oid)__
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for non admin entities
    + 500 - internal error

+ __PATCH__ `/main/courses/<id:int>`<br>
_description:_ endpoint for editing course in school. __id__ - unique identifier of the __[course](./objects.md#course)__<br>
_permission:_ __admin__<br>
_request body:_ fields of __[course](./objects.md#course)__<br>
_responses:_
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for non admin entities
    + 404 - not found
    + 500 - internal error

+ __DELETE__ `/main/courses/<id:int>`<br>
_description:_ endpoint for deleting course in store. __id__ - unique identifier of the __[course](./objects.md#course)__<br>
_permission:_ __admin__<br>
_responses:_
    + 200 - OK
    + 403 - forbidden for non admin entities
    + 404 - not found
    + 500 - internal error

---

### __user account__

+ __GET__ `/user/users[?parameters]`<br>
_description:_ endpoint for getting user objects. Without params return all users<br>
_permission:_ __user__, __teacher__, __admin__<br>
_parameters:_ __[users parameters](./parameters.md#users)__<br>
_responses:_
    + 200 - OK. With array \[__[user](./objects.md#user)__\]
    + 400 - bad request. With __[error](./objects.md#error)__
    + 403 - forbidden for non authenticated user
    + 500 - internal error<br>

+ __PATCH__ `/user/users/<id:int>`<br>
_description:_ endpoint for editing user info. __id__ - unique identifier of the __[user](./objects.md#user)__<br>
_permission:_ __admin__<br>
_request body:_ fields of __[user](./objects.md#notification)__<br>
_responses:_
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__
    + 403 - forbidden for non admin
    + 404 - not found
    + 500 - internal error<br>

+ __DELETE__ `/user/users/<id:int>`<br>
_description:_ endpoint for deleting user from db. __id__ - unique identifier of the __[user](./objects.md#user)__<br>
_permission:_ __admin__<br>
_responses:_
    + 200 - OK
    + 403 - forbidden for non admin
    + 404 - not found
    + 500 - internal error

+ __GET__ `/user/monitor`<br>
_description:_ endpoint for getting miscellaneous information about authorized user<br>
_permission:_ __user__<br>
_responses:_
    + 200 - OK. With __[misc](./objects.md#misc)__
    + 403 - forbidden for other users or non authenticated user
    + 500 - internal error

+ __GET__ `/user/notifications[?parameters]`<br>
_description:_ endpoint for receives notifications from db<br>
_permission:_ __user__, __teacher__, __admin__<br>
_parameters:_ __[notifications parameters](./parameters.md#notifications)__<br>
_responses:_
    + 200 - OK. With array \[__[notification](./objects.md#notification)__\]
    + 403 - forbidden for other users or non authenticated user
    + 500 - internal error

+ __POST__ `/user/notifications`<br>
_description:_ endpoint for adding new notification in db<br>
_permission:_ __teacher__, __admin__<br>
_request body:_ __[notification](./objects.md#notification)__ without __id__<br>
_responses:_
    + 200 - OK. With __[oid](./objects.md#oid)__
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for user and anonym
    + 500 - internal error

+ __PATCH__ `/user/notifications/<id:int>`<br>
_description:_ endpoint for editing notifications in db. __id__ - unique identifier of the __[notification](./objects.md#notification)__<br>
_permission:_ __teacher__, __admin__<br>
_request body:_ fields of __[notification](./objects.md#notification)__<br>
_responses:_
    + 200 - OK
    + 400 - bad request. With __[error](./objects.md#error)__ 
    + 403 - forbidden for user and anonym, in the case when a teacher edits another teacher's or admin's notifications
    + 404 - not found
    + 500 - internal error

+ __DELETE__ `/user/notifications/<id:int>`<br>
_description:_ endpoint for deleting notifications in db. __id__ - unique identifier of the __[notification](./objects.md#notification)__<br>
_permission:_ __teacher__, __admin__<br>
_responses:_
    + 200 - OK
    + 403 - forbidden for user and anonym, in the case when a teacher deletes another teacher's or admin's notifications
    + 404 - not found
    + 500 - internal error

+ __GET__ `/user/courses/<id:int>`<br>
_description:_ endpoint for getting available courses for specifying user. __id__ - unique identifier of the __[user](./objects.md#user)__<br>

+ __GET__ `/user/estimations/<id:int>`<br>
_description:_ endpoint for getting estimations for specifying user. __id__ - unique identifier of the __[user](./objects.md#user)__<br>

+ __GET__ `/user/certification/<id:int>`<br>
_description:_ endpoint for getting available certifications for specifying user. __id__ - unique identifier of the __[user](./objects.md#user)__<br>

+ __POST__ `/user/certification/<id:int>`<br>
_description:_ endpoint for adding access to new courses for specifying user. __id__ - unique identifier of the __[user](./objects.md#user)__<br>

+ __DELETE__ `/user/certification/<id:int>`<br>
_description:_ endpoint for deleting access to courses for specifying user. __id__ - unique identifier of the __[user](./objects.md#user)__<br>

---

### __teacher account__

### __admin account__