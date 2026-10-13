# Docker Movies App

Учебный проект по контейнеризации: два Docker-контейнера,
объединённые в общую сеть через Docker Compose.

## Архитектура

- **db** — PostgreSQL 16. Хранит таблицу `movies`.
- **app** — Python 3.12 + Flask. Предоставляет HTTP API для работы
  с фильмами (чтение и добавление).
- **volume `pgdata`** — хранит данные PostgreSQL вне контейнера,
  поэтому данные не теряются при перезапуске.

Контейнер `app` обращается к `db` по имени сервиса `db` внутри
общей сети Docker Compose.

## Структура проекта

```
docker-project/
├── docker-compose.yml       # описание двух сервисов и volume
├── README.md                # этот файл
├── db/
│   ├── Dockerfile           # образ для PostgreSQL
│   └── init.sql             # создание таблицы movies
└── app/
    ├── Dockerfile           # образ для Flask-приложения
    ├── requirements.txt     # зависимости Python
    └── app.py               # код entry point
```

## Требования

- Docker Desktop
- Docker Compose (входит в Docker Desktop)

## Запуск

В папке проекта (там, где лежит `docker-compose.yml`):

```bash
docker compose up -d --build
```

Флаг `-d` запускает контейнеры в фоне, `--build` пересобирает
образы (нужно при первом запуске и после изменений в коде).

## Остановка

```bash
docker compose down
```

## API

| Метод | URL      | Описание             |
|-------|----------|----------------------|
| GET   | /movies  | Список всех фильмов  |
| POST  | /movies  | Добавить новый фильм |

## Примеры запросов

### Получить список фильмов

```bash
curl.exe http://localhost:8000/movies
```

Ожидаемый ответ (JSON-массив):

```json
[
  {"id":1, "title":"Avatar", "year":2009, "genre":"Sci-Fi"},
  {"id":2, "title":"Matrix", "year":1999, "genre":"Sci-Fi"}
]
```

### Добавить фильм

Создайте в папке проекта файл `movie.json` со следующим содержимым:

```json
{"title":"Avatar","year":2009,"genre":"Sci-Fi"}
```

Затем выполните:

```bash
curl.exe -X POST http://localhost:8000/movies -H "Content-Type: application/json" --data-binary "@movie.json"
```

Ожидаемый ответ:

```json
{"id":1,"status":"ok"}
```

Чтобы добавить другой фильм — измените содержимое `movie.json`
и повторите команду.

## Проверка сохранности данных

Убедимся, что данные не исчезают при перезапуске контейнеров.

### 1. Добавьте несколько фильмов

Используйте POST-запросы из предыдущего раздела. Затем проверьте
список:

```bash
curl.exe http://localhost:8000/movies
```

Запомните количество фильмов и их `id`.

### 2. Остановите и удалите контейнеры

```bash
docker compose down
```

**Без флага `-v`!** Флаг `-v` удаляет volume `pgdata`, вместе
с ним - все данные. На этом шаге мы этого не делаем.

### 3. Запустите контейнеры заново

```bash
docker compose up -d
```

Подождите 5–10 секунд, пока PostgreSQL инициализируется.

### 4. Проверьте список фильмов

```bash
curl.exe http://localhost:8000/movies
```

**Ожидание:** все ранее добавленные фильмы на месте, с теми же
`id`. Это доказывает, что данные хранятся в volume `pgdata` и
переживают перезапуск контейнеров.

## Ссылки

- Образ `movies-app` на Docker Hub: https://hub.docker.com/r/milashkarr/movies-app
- Образ `movies-db` на Docker Hub: https://hub.docker.com/r/milashkarr/movies-db