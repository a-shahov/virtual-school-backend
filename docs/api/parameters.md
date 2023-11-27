# Description GET parameters in [API](./api.md)

---

+ __[users](#users)__
+ __[news](#news)__
+ __[notifications](#notifications)__

---

### __users__

__Description:__<br>
_С помощью параметров запроса **GET** `/user/users` можно фильтровать какие конкретно users будут запрошены из базы данных. Без указания параметров будут возвращены все users_

__Description of parameters:__<br>

+ __id__ - запрос конкретного user из базы данных с указанным id<br>
_incompatible with:_ __class__<br> 
_available values:_
    + integers

+ __class__ - отфильтровать учеников по указанному классу<br>
_incompatible with:_ __id__<br>
_available values:_
    + integers [1, ..., 11]

__Examples:__<br>

```
GET /user/users  # All users
GET /user/users?id=12
GET /user/users?class=7
GET /user/users?class=7&id=12  # Bad request
```
---

### __news__

__Description:__<br>
_С помощью параметров запроса **GET** `/main/news` можно группировать новости по страницам. Если не указывать параметров вернёт все новости, то есть 1 страницу максимального размера. Если указать только параметр __size__ то вернёт первую страницу, с указанным размером. Новости возвращаются в порядке добавления сначала самые новые_

__Description of parameters:__<br>

+ __page__ - номер страницы<br>
_depends on:_ __size__<br>
_available values:_
    + integers

+ __size__ - размер страницы (в новостных блоках)<br>
_available values:_
    + integers

__Examples:__<br>

```
GET /main/news  # All news
GET /main/news?size=10  # First page with {size} news
GET /main/news?page=3&size=7
```
---

### __notifications__

__Description:__<br>
_С помощью параметров запроса **GET** `/user/notifications` можно группировать уведомления по страницам. Если не указывать параметров вернёт все новости, то есть 1 страницу максимального размера. Если указать только параметр __size__ то вернёт первую страницу, с указанным размером. Также уведомления можно фильтровать по тегам. Уыедомления возвращаются в порядке добавления сначала самые новые_

__Description of parameters:__<br>

+ __tag__ - определённый тег который установлен для уведомления, определяет приоритет уведомления<br>
_available values:_
    + low
    + medium
    + high

+ __page__ - номер страницы<br>
_depends on:_ __size__<br>
_available values:_
    + integers

+ __size__ - размер страницы (в новостных блоках)<br>
_available values:_
    + integers

__Examples:__<br>

```
GET /user/notifications  # All notifications available for current user
GET /user/notifications?tag=high  # All high priority notifications
GET /user/notifications?tag=medium&size=7  # The first page with medium priority notifications
GET /user/notifications?page=3&size=7
```
---