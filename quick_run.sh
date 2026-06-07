#!/usr/bin/env bash
# 智能校园失物招领系统 - Linux/macOS 快速启动脚本
# 对应 Windows 的 quick_run.bat：在已创建好虚拟环境后，直接激活并启动开发服务器。
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR=".venv"
HOST="127.0.0.1:8000"

if [ ! -x "${VENV_DIR}/bin/python" ]; then
    echo "[ERROR] 未找到虚拟环境，请先运行 ./start.sh 完成初始化。" >&2
    exit 1
fi

echo "[INFO] 激活虚拟环境..."
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "[INFO] 在 http://${HOST}/ 启动 Django 开发服务器（Ctrl-C 停止）..."
exec python manage.py runserver "$HOST"
