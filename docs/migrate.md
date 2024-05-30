# Миграции tortoise (aerich)
Подключение к субд осуществляется на основе перезаписанных
переменных конфига (из `local.yaml`)

Все команды прописываются из корня проекта

## Связка aerich с субд и накат нулевой миграции
``` shell
poetry run aerich init-db
```

## Создание новой миграции
```shell
poetry run aerich migrate
```

## Накат новых миграций
```
poetry run aerich upgrade
```
