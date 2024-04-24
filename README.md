## Сравнение асинхронных HTTP-клиентов в Python: httpx vs aiohttp

В Python существует несколько библиотек для работы с HTTP-запросами. Рассмотрим две популярные асинхронные библиотеки: *
*httpx** и **aiohttp**, сравним их возможности и выберем подходящий инструмент для регулярного опроса 100_000 сайтов.

### httpx

**httpx** - это современная библиотека, которая предоставляет как синхронный, так и асинхронный интерфейс для отправки
HTTP-запросов. Она совместима с API библиотеки `requests`, что облегчает переход для тех, кто уже знаком с ней.

**Основные фичи httpx:**

* **Совместимость с `requests` API**
* **Синхронный и асинхронный интерфейс**
* **Поддержка HTTP/1.1 и HTTP/2**
* **Запросы к WSGI/ASGI приложениям**
* **Полная аннотация типов**

### aiohttp

**aiohttp** - это асинхронная библиотека, специально разработанная для создания высокопроизводительных веб-приложений с
использованием `asyncio`. Она фокусируется на асинхронной работе и предоставляет инструменты для создания как
HTTP-клиентов, так и серверов.

**Основные фичи aiohttp:**

* **Асинхронные HTTP-запросы**
* **Клиентские сеансы**
* **Поддержка WebSockets**
* **Большое сообщество**

### Сравнение на основе открытых источников

| Характеристика                    | httpx   | aiohttp  |
|-----------------------------------|---------|----------|
| Асинхронная совместимость         | Да      | Да       |
| Синхронная совместимость          | Да      | Нет      |
| Автоматическое декодирование JSON | Да      | Нет      |
| Поддержка HTTP/2                  | Да      | Нет      |
| Cookies                           | Да      | Да       |
| Перенаправления                   | Да      | Да       |
| Аутентификация                    | Да      | Да       |
| Пользовательские заголовки        | Да      | Да       |
| Потоковая обработка ответов       | Нет     | Нет      |
| Размер библиотеки                 | Большой | Меньше   |
| Производительность                | Хорошая | Отличная |

### Собественное Тестирование асинхронных HTTP-клиентов: aiohttp vs httpx

#### Методология тестирования

1. **Сбор данных**: Был собран список из ~700 открытых API, сохраненных в файле `urls.json`.
2. **Сравнение библиотек**: Производительность aiohttp и httpx сравнивалась по времени выполнения 100 запросов к каждому API с различными параметрами `timeout` и `connections`. 
3. **Логирование**: Весь процесс тестирования и результаты были залогированы для дальнейшего анализа.
4. **Сбор характеристик**: Процесс сбора данных занял около 10 часов.
5. **Анализ данных**: Собранные данные были проанализированы для выявления различий в производительности и поведении библиотек.

#### Как запустить тестирование

##### Docker
`docker compose up`

##### Без докера
`poetry install`
`poetry shell`
`python main,py`

#### Результаты и выводы тестирования

* **Обработка ошибок**: aiohttp тратит значительно больше времени на обработку ошибок (429, 404, 403, 502) по сравнению с httpx.
* **Перенаправления**: httpx не следует перенаправлениям автоматически, в отличие от aiohttp. 
* **Скорость**: aiohttp демонстрирует более высокую скорость отправки запросов по сравнению с httpx по всех вариациях. 

### Вывод
Для поставленной задачи в сборе данных со `100_000` сайтов нужно выбрать *aiohttp*, из-за большей производительности, меньшего размера, активной разработки и поддержки сообщества.

