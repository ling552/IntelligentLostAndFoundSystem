# 智能校园失物招领系统

基于 `Django + SQLite` 的校园失物招领平台，支持失物 / 招领信息发布、图片上传、关键词搜索、分类筛选，以及基于文本相似度的智能匹配推荐。

## 项目亮点

- 全站统一视觉风格，覆盖首页、详情页、表单页、用户中心和后台统计页
- 支持失物与招领双类型信息发布
- 支持关键词搜索、分类筛选、类型筛选和排序
- 支持图片上传与本地 `media/` 存储
- 支持个人发布记录管理、状态关闭、管理员统计面板

## 技术栈

- Python 3.10
- Django 4.2
- Pillow 10
- SQLite
- Django Templates + 原生 HTML / CSS

## 目录结构

```text
IntelligentLostAndFoundSystem/
├─ items/                    # 失物 / 招领业务模块
├─ lostfound_system/         # Django 项目配置
├─ media/                    # 上传图片目录
├─ static/                   # 静态资源
├─ templates/                # 页面模板
├─ users/                    # 用户登录 / 注册 / 资料设置
├─ manage.py
├─ requirements.txt
├─ environment.yml
└─ README.md
```

## 使用 Conda 启动

推荐直接双击或执行项目根目录下的脚本：

```powershell
.\start_conda.bat
```

脚本会自动：

- 检查并创建 `intelligent-lostfound` conda 环境
- 根据 `environment.yml` 同步依赖
- 自动执行 `python manage.py migrate`
- 启动 Django 开发服务器

### 1. 创建环境

```powershell
conda env create -f environment.yml
```

如果你想手动创建，也可以使用：

```powershell
conda create -n intelligent-lostfound python=3.10 -y
conda activate intelligent-lostfound
python -m pip install -r requirements.txt
```

### 2. 激活环境

```powershell
conda activate intelligent-lostfound
```

### 3. 初始化数据库

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建管理员账号

```powershell
python manage.py createsuperuser
```

### 5. 启动项目

```powershell
python manage.py runserver 127.0.0.1:8000
```

启动后访问：

- 首页：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 我的发布：[http://127.0.0.1:8000/me/items/](http://127.0.0.1:8000/me/items/)
- 后台统计：[http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- Django Admin：[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 不使用 Conda，直接用 Python 启动

如果你的电脑已经安装了可用的 Python 3.10，也可以不使用 Conda，直接启动项目。

推荐直接双击或执行项目根目录下的脚本：

```powershell
.\start_python.bat
```

脚本会自动：

- 检查并创建本地 `.venv` 虚拟环境
- 安装 `requirements.txt` 中的依赖
- 自动执行 `python manage.py migrate`
- 启动 Django 开发服务器

说明：

- `start_python.bat` 会优先尝试 `py -3.10`
- 如果系统里只有不兼容的 Python 版本，脚本会直接给出提示并停止

### 方式一：直接使用系统 Python

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### 方式二：使用 Windows 的 `py` 启动器

```powershell
py -3.10 -m pip install --upgrade pip
py -3.10 -m pip install -r requirements.txt
py -3.10 manage.py migrate
py -3.10 manage.py runserver 127.0.0.1:8000
```

如果你希望隔离依赖但又不想使用 Conda，也可以额外创建一个原生虚拟环境：

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py runserver 127.0.0.1:8000
```

## 常用管理命令

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## 常见问题

### 1. `ModuleNotFoundError: No module named 'django'`

说明依赖尚未安装，请先执行：

```powershell
python -m pip install -r requirements.txt
```

或确认你已经正确激活 Conda / 虚拟环境。

### 2. 图片上传后无法显示

开发模式下，项目会通过 `MEDIA_URL` 自动映射本地 `media/` 目录。请确认：

- 项目是通过 `python manage.py runserver` 启动的
- `DEBUG = True`
- 上传后 `media/` 目录中确实已生成文件

### 3. 端口被占用

可以更换端口运行：

```powershell
python manage.py runserver 127.0.0.1:8001
```

## 开发说明

- 主要业务逻辑位于 [items/views.py](D:/HTML/IntelligentLostAndFoundSystem/items/views.py)
- 匹配服务位于 [items/services.py](D:/HTML/IntelligentLostAndFoundSystem/items/services.py)
- 全局样式位于 [static/css/app.css](D:/HTML/IntelligentLostAndFoundSystem/static/css/app.css)
- 全站基础布局位于 [templates/base.html](D:/HTML/IntelligentLostAndFoundSystem/templates/base.html)

## License

项目仅用于学习、课程设计和演示，可按需二次修改。
