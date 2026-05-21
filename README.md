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

构建 1.0.0 镜像：

```bash
docker build -t intelligent-lostfound-system:1.0.0 .
```

运行容器：

```bash
docker run --rm -p 8000:8000 \
  -e DJANGO_SECRET_KEY="change-me" \
  -e DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1" \
  intelligent-lostfound-system:1.0.0
```

容器启动时会自动执行数据库迁移，并通过 Gunicorn 监听 `0.0.0.0:8000`。

## GitHub Release 打包

仓库已包含 `.github/workflows/docker-release.yml`。推送版本标签后会自动构建 Docker 镜像，并把镜像归档文件上传到 GitHub Release。

```bash
git tag v1.0.0
git push origin v1.0.0
```

工作流产物：

- `intelligent-lostfound-system-1.0.0.tar.gz`
- `intelligent-lostfound-system-1.0.0.tar.gz.sha256`

下载后可导入镜像：

```bash
docker load -i intelligent-lostfound-system-1.0.0.tar.gz
docker run --rm -p 8000:8000 intelligent-lostfound-system:1.0.0
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
- `DJANGO_ALLOWED_HOSTS`：允许访问的主机名，多个值用英文逗号分隔

## License

本项目用于学习、课程设计和演示，可按需二次修改。
