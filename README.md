# 智能校园失物招领系统

基于 `Django + SQLite` 的校园失物招领平台，支持失物/招领信息发布、图片上传、关键词搜索、分类筛选、个人发布管理、管理员统计面板，以及基于文本相似度的匹配推荐。

## 功能特性

- 失物与招领双类型信息发布
- 物品分类、关键词搜索、类型筛选和时间排序
- 图片上传，开发环境默认保存到本地 `media/`
- 登录、注册、个人资料与个人发布记录管理
- 管理员统计面板，展示发布量、完成率、分类分布等数据
- 详情页自动推荐相似的反向类型条目

## 技术栈

- Python 3.10+，推荐 Python 3.10/3.11/3.12
- Django 4.2
- Pillow 10
- SQLite
- Django Templates + 原生 HTML/CSS/JavaScript
- Docker + Gunicorn
- WhiteNoise 静态文件服务

## 目录结构

```text
IntelligentLostAndFoundSystem/
├── items/                 # 失物/招领业务模块
├── lostfound_system/      # Django 项目配置
├── scripts/               # 环境检查脚本
├── static/                # 静态资源
├── templates/             # 页面模板
├── users/                 # 登录、注册、资料模块
├── .github/workflows/     # GitHub Actions 工作流
├── Dockerfile
├── docker-entrypoint.sh
├── environment.yml
├── manage.py
├── requirements.txt
└── README.md
```

## 本地启动

### 使用普通 Python

Windows 下可以直接运行：

```powershell
.\start_python.bat
```

也可以手动执行：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### 使用 Conda

```powershell
conda env create -f environment.yml
conda activate intelligent-lostfound
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

启动后访问：

- 首页：http://127.0.0.1:8000/
- 我的发布：http://127.0.0.1:8000/me/items/
- 后台统计：http://127.0.0.1:8000/dashboard/
- Django Admin：http://127.0.0.1:8000/admin/

## Docker 打包与运行

### 构建镜像

```bash
docker build -t intelligent-lostfound-system:1.0.2 .
```

### 本机快速试运行

容器内已声明数据目录卷 `/app/data`（SQLite 数据库）和 `/app/media`（用户上传图片）。最简单的本机访问方式：

```bash
docker run -d --name lostfound -p 8000:8000 \
  -e DJANGO_SECRET_KEY="please-change-me" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/media:/app/media" \
  intelligent-lostfound-system:1.0.2
```

Windows PowerShell 用 `${PWD}` 替换 `$(pwd)`，cmd 用 `%cd%`。

浏览器打开 http://127.0.0.1:8000/ 即可访问。容器删除后，`./data/db.sqlite3` 与 `./media/` 中的数据仍保留在本机目录。

### 通过域名或公网 IP 访问

必须把外部访问地址同时加入 `DJANGO_ALLOWED_HOSTS` 和 `DJANGO_CSRF_TRUSTED_ORIGINS`（后者要带协议前缀），否则会出现 `Bad Request (400)` 或 `CSRF验证失败. 请求被中断.` (403)。

HTTPS 域名（推荐，建议在前面挂 Nginx/Caddy 反向代理终止 TLS）：

```bash
docker run -d --name lostfound -p 8000:8000 \
  -e DJANGO_SECRET_KEY="please-change-me" \
  -e DJANGO_ALLOWED_HOSTS="lostfound.example.com" \
  -e DJANGO_CSRF_TRUSTED_ORIGINS="https://lostfound.example.com" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/media:/app/media" \
  intelligent-lostfound-system:1.0.2
```

HTTP 公网 IP（直接对外暴露 8000 端口）：

```bash
docker run -d --name lostfound -p 8000:8000 \
  -e DJANGO_SECRET_KEY="please-change-me" \
  -e DJANGO_ALLOWED_HOSTS="203.0.113.10,localhost,127.0.0.1" \
  -e DJANGO_CSRF_TRUSTED_ORIGINS="http://203.0.113.10:8000,http://localhost:8000,http://127.0.0.1:8000" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/media:/app/media" \
  intelligent-lostfound-system:1.0.2
```

多个域名或 IP 用英文逗号分隔。把 `203.0.113.10` 换成实际公网 IP，`lostfound.example.com` 换成实际域名。

容器启动时会自动 `migrate`，并通过 Gunicorn 监听 `0.0.0.0:8000`。

### 创建管理员账号

容器运行后单独执行：

```bash
docker exec -it lostfound python manage.py createsuperuser
```

## GitHub Release 打包

仓库已包含 `.github/workflows/docker-release.yml`。推送版本标签后会自动构建 Docker 镜像，并把镜像归档文件上传到 GitHub Release。

```bash
git tag v1.0.2
git push origin v1.0.2
```

工作流产物：

- `intelligent-lostfound-system-1.0.2.tar.gz`
- `intelligent-lostfound-system-1.0.2.tar.gz.sha256`

下载后可导入镜像：

```bash
docker load -i intelligent-lostfound-system-1.0.2.tar.gz
docker run -d --name lostfound -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/media:/app/media" \
  intelligent-lostfound-system:1.0.2
```

也可以在 GitHub Actions 页面手动运行 `Docker Release` workflow，并输入版本号。

## 常用管理命令

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## 环境变量

- `DJANGO_SECRET_KEY`：Django 密钥，生产环境必须设置
- `DJANGO_DEBUG`：是否开启调试模式，默认本地为 `True`，Docker 中默认 `False`
- `DJANGO_ALLOWED_HOSTS`：允许访问的主机名/IP，多个值用英文逗号分隔；Docker 镜像默认为 `*`（接受任意 Host 头）
- `DJANGO_CSRF_TRUSTED_ORIGINS`：受信任的 CSRF 来源，多个值用英文逗号分隔（必须带 `http://` / `https://` 协议前缀）；未设置时会从 `DJANGO_ALLOWED_HOSTS` 自动派生，使用域名/公网 IP 访问时**必须显式配置**
- `DJANGO_DATA_DIR`：SQLite 数据库所在目录，Docker 镜像默认 `/app/data`，建议挂载本机目录持久化
- `DJANGO_MEDIA_ROOT`：用户上传图片目录，Docker 镜像默认 `/app/media`，建议挂载本机目录持久化

## License

本项目用于学习、课程设计和演示，可按需二次修改。
