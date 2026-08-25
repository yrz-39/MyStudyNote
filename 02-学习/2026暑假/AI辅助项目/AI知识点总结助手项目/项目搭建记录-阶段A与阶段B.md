---
tags:
  - AI项目
  - Python
  - FastAPI
  - SQLite
  - Web开发
  - 学习笔记
status: 进行中
start: 2026-07-24
project: AI 问答卡与复习提纲助手
---

# AI 问答卡助手 — 项目搭建记录（阶段 A & B）

> [!summary] 今日成果
> 从零搭建了一个 Python Web 应用：浏览器端录入课程笔记，后端校验后写入本地 SQLite 数据库，重启服务后数据不丢失。覆盖了虚拟环境、FastAPI 路由、HTML 表单、SQLite 持久化全链路。

---

## 项目定位

用 Python 做一个本地运行的网页应用：用户录入一段课程笔记，保存到本地，后续可请求大模型生成复习提纲或问答卡。

**技术栈：** Python 3.11 · FastAPI · SQLite · 原生 HTML/CSS/JS · uv · pytest

---

## 1. 项目环境搭建

### 1.1 目录规划

项目全部放在 D 盘，与 C++ 工程并列：

```text
D:\
├── CppProject\              # C++ 数据结构实验
└── AiProjects\
    └── AiStudyAssistant\    # 本项目
```

### 1.2 创建独立虚拟环境

在项目根目录执行：

```bash
uv venv --python 3.11
```

- **为什么每个项目需要单独的 `.venv`？** 不同项目可能需要不同版本的第三方库；项目 A 升级依赖不应影响项目 B；也不污染 Hermes 自己的内部 Python 环境。
- `uv` 是比 `pip` + `venv` 更现代的 Python 项目管理工具，能自动管理虚拟环境和依赖锁文件。

### 1.3 初始化项目元数据

```bash
uv init --bare --name ai-study-assistant --python 3.11 --vcs git --no-workspace
```

生成 `pyproject.toml`——Python 项目的"身份证"：

```toml
[project]
name = "ai-study-assistant"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []
```

- `--bare`：只建骨架，不生成示例代码
- `--vcs git`：同时初始化 Git 仓库
- `.python-version` 通过 `uv python pin 3.11` 单独创建

### 1.4 安装依赖

```bash
uv add fastapi "uvicorn[standard]"
uv add --dev pytest
```

- `fastapi`：Web 框架，负责路由和请求处理
- `uvicorn`：ASGI 服务器，让 FastAPI 应用真正运行起来，监听网络请求
- `pytest`：测试框架（`--dev` 表示仅开发时使用）

---

## 2. 项目文件结构

当前实际目录结构：

```text
AiStudyAssistant/
├── .venv/                    # 项目独立 Python 3.11 环境
├── .git/                     # Git 版本控制
├── .gitignore
├── .python-version           # 固定 Python 版本为 3.11
├── pyproject.toml            # 项目元数据与依赖清单
├── uv.lock                   # 依赖版本锁定文件
├── data/
│   └── app.db                # SQLite 数据库（运行时自动生成）
├── app/
│   ├── __init__.py
│   ├── note_validation.py    # 输入校验
│   ├── database.py           # 数据库连接与建表
│   ├── repositories.py       # 笔记的增删查改
│   └── main.py               # Web 入口：路由定义
└── tests/
    └── test_note_validation.py
```

**分层设计原则：**

| 文件 | 职责 |
|---|---|
| `main.py` | HTTP 路由，接收请求、返回响应 |
| `note_validation.py` | 业务校验逻辑 |
| `repositories.py` | 数据库读写（增删查改） |
| `database.py` | 数据库连接管理、建表初始化 |

路由不直接写 SQL，数据库操作集中在 repository 层，便于未来替换或测试。

---

## 3. 输入校验：`note_validation.py`

### 3.1 需求

用户提交的笔记在进入数据库或传给 AI 之前，需要去掉首尾空白字符。

```text
输入："  链表是一种线性结构。  "
输出："链表是一种线性结构。"
```

### 3.2 实现

```python
def validate_note(content: str) -> str:
    i = 0
    j = len(content) - 1

    # 从左侧找到第一个非空白字符
    while i < len(content):
        if content[i] != " " and content[i] != "\t" and content[i] != "\n":
            break
        i += 1

    # 从右侧找到第一个非空白字符
    while j >= 0:
        if content[j] != " " and content[j] != "\t" and content[j] != "\n":
            break
        j -= 1

    # 全空白或空字符串
    if i > j:
        return ""

    # 切片：左闭右开，所以右侧 +1
    return content[i:j + 1]
```

### 3.3 关键知识点

| 知识点 | 说明 |
|---|---|
| **双指针法** | `i` 从左向右扫描，`j` 从右向左扫描 |
| **切片 `[start:end)`** | 左闭右开，所以要写 `j+1` |
| **转义字符** | `"\t"` 是 Tab，`"\n"` 是换行（不是 `"/t"`） |
| **边界条件** | 空字符串 / 全空白 → 返回 `""` |
| **索引越界** | 循环条件是 `i < len(content)`，不是 `<=` |

### 3.4 可改进的方向

- 用 `str.isspace()` 替代逐个字符比较，能同时覆盖 `"\r"`、全角空格等
- 后续可增强：清理后为空时抛出明确异常

---

## 4. 数据库层：`database.py` + `repositories.py`

### 4.1 为什么用 SQLite

- Python 标准库自带 `sqlite3`，无需安装
- 一个文件就是一个完整数据库，适合单机小项目
- 不需要像 MySQL/PostgreSQL 那样启动独立服务

### 4.2 `database.py`：连接与建表

```python
import sqlite3

DB_PATH = "data/app.db"


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让查询结果可以用字典方式访问
    return conn


def init_db():
    """初始化数据库，确保表存在"""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT DEFAULT '',
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
```

**关键概念：**

| 代码 | 作用 |
|---|---|
| `sqlite3.connect(DB_PATH)` | 如果文件不存在则**自动创建** |
| `row_factory = sqlite3.Row` | 查询结果可以用 `row["title"]` 而非 `row[0]` |
| `CREATE TABLE IF NOT EXISTS` | 重复执行不会报错 |
| `PRIMARY KEY AUTOINCREMENT` | 自动生成不重复的 ID |
| `conn.commit()` | **必须调用**，否则数据不写入磁盘 |
| `conn.close()` | 释放连接资源 |

### 4.3 `repositories.py`：增和查

```python
from app.database import get_connection


def add_note(title: str, content: str) -> int:
    """保存一篇笔记，返回它的 ID"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content)
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id


def list_notes() -> list[dict]:
    """返回所有笔记，按时间倒序"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, content, created_at FROM notes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

**关键知识点：**

| 知识点 | 说明 |
|---|---|
| **参数化查询 `(?, ?)`** | **不用字符串拼接**，防止 SQL 注入攻击 |
| `cursor.lastrowid` | 刚插入行的自增 ID |
| `fetchall()` | 获取所有查询结果 |
| `dict(row)` | 把 `sqlite3.Row` 转为 Python 字典 |

---

## 5. Web 层：`main.py`

### 5.1 最小 FastAPI 应用

```python
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.note_validation import validate_note
import app.repositories as repo
from app.database import init_db

app = FastAPI()

# 启动时确保数据库就绪
init_db()
```

- `FastAPI()`：创建 Web 应用实例
- `init_db()`：在服务启动时确保表存在（放在路由定义之前）

### 5.2 首页路由（GET `/`）

```python
@app.get("/")
def home():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI 问答卡助手</title>
</head>
<body>
    <h1>AI 问答卡助手</h1>
    <p>欢迎使用。这个页面由 Python 的 FastAPI 提供。</p>
    <form action="/api/notes" method="post">
        <input name="title" placeholder="标题（可选）">
        <textarea name="content" placeholder="在此输入笔记内容"></textarea>
        <button type="submit">提交笔记</button>
    </form>
</body>
</html>"""
    return HTMLResponse(html_content)
```

**关键概念：**

| 概念 | 说明 |
|---|---|
| `@app.get("/")` | 装饰器：访问 `/` 时调用此函数 |
| `<form action="/api/notes" method="post">` | 表单提交目标 URL + HTTP 方法 |
| `<input name="title">` | `name` 属性与后端参数名对应 |
| `HTMLResponse(...)` | 告诉浏览器"这是 HTML 页面" |

### 5.3 创建笔记路由（POST `/api/notes`）

```python
@app.post("/api/notes")
def create_note(title: str = Form(default=""), content: str = Form()):
    cleaned = validate_note(content)
    if not cleaned:
        return HTMLResponse("<p>错误：笔记不能为空。</p>")

    note_id = repo.add_note(title, cleaned)

    return HTMLResponse(
        f"<h1>笔记已提交</h1>"
        f"<p>编号：{note_id}</p>"
        f"<h2>{title}</h2>"
        f"<p>{cleaned}</p>"
        f'<a href="/">返回首页</a>'
    )
```

**`Form()` 的工作机制：**

```text
浏览器提交表单（name="content" → "链表笔记"）
        ↓
FastAPI 从请求体中提取字段
        ↓
注入到函数参数 content
        ↓
函数体内可直接使用
```

- `Form(default="")`：字段可选，默认空字符串
- `Form()`（无默认值）：字段必填，缺则返回 422

### 5.4 查看笔记路由（GET `/api/notes`）

```python
@app.get("/api/notes")
def view_notes():
    notes = repo.list_notes()
    if not notes:
        return HTMLResponse("<p>尚无笔记。</p>")

    html_parts = ["<h1>笔记列表</h1>"]
    for note in notes:
        html_parts.append(
            f"<div>"
            f"<h2>{note['title'] or '(无标题)'}</h2>"
            f"<p>{note['content']}</p>"
            f"<small>{note['created_at']}</small>"
            f"</div><hr>"
        )
    html_parts.append('<a href="/">返回首页</a>')
    return HTMLResponse("".join(html_parts))
```

- `note['title'] or '(无标题)'`：Python 短路求值——若 title 为空字符串则显示默认值

### 5.5 启动服务

```bash
uv run uvicorn app.main:app --reload
```

| 参数 | 含义 |
|---|---|
| `uv run` | 使用当前项目的 `.venv` |
| `uvicorn` | ASGI 服务器程序 |
| `app.main:app` | 冒号左边是模块路径，右边是 FastAPI 实例变量名 |
| `--reload` | 代码改动后自动重启 |

访问 `http://127.0.0.1:8000` 即可看到页面。

---

## 6. HTTP GET 与 POST 的区别

| | GET | POST |
|---|---|---|
| 触发方式 | 输入网址、点链接、刷新页面 | 提交表单 |
| 用途 | 取数据、看页面 | 提交数据、创建资源 |
| 数据位置 | URL 后面（可见） | 请求体内部（不可见） |
| 类比 | 向图书馆要一本书来看 | 把一本新书交给图书馆入库 |

---

## 7. 踩坑记录

| 问题 | 原因 | 解决 |
|---|---|---|
| VS Code 中 `fastapi` 下方红色波浪线 | Pylance 使用了错误的 Python 解释器 | `Ctrl+Shift+P` → `Python: Select Interpreter` → 选择项目的 `.venv` |
| 提示符显示 `(.venv)` 但实际是数学建模的环境 | 之前手动激活了别的项目的虚拟环境 | `deactivate` → `source .venv/Scripts/activate` |
| uvicorn 启动报 `[Errno 10048]` | 端口 8000 被之前的进程占用 | 找到旧终端 `Ctrl+C` 停止，或换端口 |
| `ModuleNotFoundError: No module named 'app'` | 文件刚创建但 `uv run pytest` 找不到 | 使用 `uv run python -m pytest` 替代 `uv run pytest` |

---

## 8. 项目阶段总览

```text
✅ 阶段 A：项目与最小网页         → 环境、FastAPI、HTML 页面
✅ 阶段 B：SQLite 笔记保存         → 数据库、增查功能、数据持久化
⬜ 阶段 C：假 LLM 打通生成流程
⬜ 阶段 D：接入真实模型 API
⬜ 阶段 E：测试、README 与收束
```

---

## 9. 当前完整数据流

```text
浏览器打开 http://127.0.0.1:8000
→ 首页（HTML 表单）
→ 输入标题和笔记正文
→ 点击"提交笔记"
→ POST /api/notes
→ validate_note(content) 校验
→ repo.add_note(title, cleaned) 写入 SQLite
→ 返回"笔记已提交"页面
→ 访问 /api/notes 可查看所有笔记
→ Ctrl+C 重启服务后，笔记仍在
```
