[![CI/CD foodgram](http://github.com/cheremyak/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/cheremyak/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
# http://leoneed.hopto.org

Учетеная запись администратора:<br/>
login: admin@admin.ru<br/>
password: admin<br/>

Документация доступна по адресу:<br/>
http://leoneed.hopto.org/api/docs/<br/>




Запуск сайта локально

# Foodgram - «Продуктовый помощник»

Пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд<br/>

Для запуска необходим Docker, установленный на Вашем ПК.
Если не установлен - выполните перейдите по ссылке и выберите необходимый Вам способ установки Docker: https://docs.docker.com/desktop/<br/>

Клонируйте репозиторий<br/>
Перейдите в каталог  /infra/  командой cd infra/. Создайте .env файл в формате.<br/>

DB_ENGINE=django.db.backends.postgresql<br/>
DB_NAME=postgres<br/>
POSTGRES_USER=postgres<br/>
POSTGRES_PASSWORD=postgres<br/>
DB_HOST=localhost<br/>
DB_PORT=5432<br/>
ALLOWED_HOSTS=localhost 127.0.0.1<br/>
CSRF_TRUSTED_ORIGINS=localhost 127.0.0.1<br/>
SECRET_KEY=top_secret<br/>

Не выходя из директории infra запустите установку и сборку контейнеров.<br/>
docker compose up -d --build # сборка и запуск контейнеров<br/>
docker compose stop # остановка работы контейнеров<br/>
docker compose down # удаление контейнеров<br/>



После запуска контейнера сайт доступен по адресу http://localhost/<br/>
Админ-панель: http://localhost/admin/<br/>

