# Yandex Products Backend

Реализация бэкенд для веб-сервиса сравнения цен, аналогичный сервису [Яндекс Товары](https://yandex.ru/products)

- документация API: `http://localhost:80/docs`
- реализованные `routes`:
  - `base tasts`:
    - `/delete/{id}` - Удаление элемента по идентификатору
    - `/nodes/{id}` - Получение информации об элементе по идентификатору
    - `/imports` - Импорт новых товаров и/или категорий
  - `advanced tasks`
    - `/node/{id}/statistic` - Получение статистики (истории обновлений) по товару/категории за заданный полуинтервал [from, to).
    - `/sales` - Получение списка товаров, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от времени переданном в запросе.


## Service-start

### Prerequisite

- `.env.example`:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@db:5432/
POSTGRES_DB=postgres
META_DB_NAME=postgres
META_SCHEMA=public
```
  
### Запуск сервиса

- Создание виртуального окружения: `make venv`

- Запуск форматтеров кода: `make format`

- Проверка работоспособности тестов: `make test` | `90 % coverage`

- Запуск линтеров: `make lint`

- Запуск сервиса в docker: `make app`

- Запуск полного цикла тестирования API - `make ci`

## Author

- [Aleksandr Shirokov](t.me/aptmess)