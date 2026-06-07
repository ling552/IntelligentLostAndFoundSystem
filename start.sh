#!/usr/bin/env bash
# 智能校园失物招领系统 - Linux/macOS 启动脚本（venv + pip）
# 对应 Windows 的 start_python.bat：首次运行会创建虚拟环境、安装依赖、执行迁移并启动开发服务器。
set -euo pipefail

cd "$(dirname "$0")"

VENV_DIR=".venv"
HOST="127.0.0.1:8000"

# 选择可用的 Python 解释器（优先 python3）
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "[ERROR] 未找到可用的 Python 解释器，请先安装 Python 3.10 / 3.11 / 3.12。" >&2
    exit 1
fi

# 校验 Python 版本（推荐 3.10 - 3.12）
PYTHON_VERSION="$("$PYTHON_CMD" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
case "$PYTHON_VERSION" in
    3.10|3.11|3.12) ;;
    *)
        echo "[WARN] 检测到 Python ${PYTHON_VERSION}，本项目推荐使用 3.10 / 3.11 / 3.12。" >&2
        echo "[WARN] 将继续尝试启动，如遇依赖问题请切换到推荐版本。" >&2
        ;;
esac

# 创建虚拟环境（如不存在）
if [ ! -x "${VENV_DIR}/bin/python" ]; then
    echo "[INFO] 未找到虚拟环境 ${VENV_DIR}，正在创建..."
    "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# 激活虚拟环境
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "[INFO] 升级 pip 并安装依赖..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[INFO] 执行数据库迁移..."
python manage.py migrate

echo "[INFO] 在 http://${HOST}/ 启动 Django 开发服务器..."
exec python manage.py runserver "$HOST"
