#!/bin/sh
set -e

mkdir -p "${DJANGO_DATA_DIR:-/app/data}" "${DJANGO_MEDIA_ROOT:-/app/media}"

# 兼容旧镜像：把镜像里附带的 db.sqlite3 复制到挂载目录（仅当目标不存在时）
if [ ! -f "${DJANGO_DATA_DIR:-/app/data}/db.sqlite3" ] && [ -f /app/db.sqlite3 ]; then
    cp /app/db.sqlite3 "${DJANGO_DATA_DIR:-/app/data}/db.sqlite3"
fi

python manage.py migrate --noinput

exec "$@"
