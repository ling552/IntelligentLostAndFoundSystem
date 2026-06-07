#!/usr/bin/env bash
# 智能校园失物招领系统 - Linux/macOS Conda 启动脚本
# 对应 Windows 的 start_conda.bat：基于 conda 环境创建/更新依赖、迁移并启动开发服务器。
set -euo pipefail

cd "$(dirname "$0")"

ENV_NAME="intelligent-lostfound"
HOST="127.0.0.1:8000"

if ! command -v conda >/dev/null 2>&1; then
    echo "[ERROR] 未找到 conda，请先安装 Miniconda 或 Anaconda。" >&2
    exit 1
fi

# 载入 conda 的 shell 函数，使 `conda activate` 可用
CONDA_BASE="$(conda info --base)"
# shellcheck disable=SC1091
source "${CONDA_BASE}/etc/profile.d/conda.sh"

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "[INFO] Conda 环境 ${ENV_NAME} 已存在，正在更新依赖..."
    if [ -f "environment.yml" ]; then
        conda env update -n "$ENV_NAME" -f environment.yml --prune
    else
        conda run -n "$ENV_NAME" python -m pip install -r requirements.txt
    fi
else
    echo "[INFO] Conda 环境 ${ENV_NAME} 不存在，正在创建..."
    if [ -f "environment.yml" ]; then
        conda env create -f environment.yml
    else
        conda create -n "$ENV_NAME" python=3.10 -y
        conda run -n "$ENV_NAME" python -m pip install -r requirements.txt
    fi
fi

conda activate "$ENV_NAME"

echo "[INFO] 执行数据库迁移..."
python manage.py migrate

echo "[INFO] 在 http://${HOST}/ 启动 Django 开发服务器..."
exec python manage.py runserver "$HOST"
