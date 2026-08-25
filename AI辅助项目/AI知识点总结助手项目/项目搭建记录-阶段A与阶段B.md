---
tags:
  - AI项目
  - Python
  - FastAPI
  - SQLite
  - Web开发
  - 学习笔记
status: 进行中
start: 2026-07-23
project: AI 问答卡与复习提纲助手
---

# AI 问答卡助手：项目搭建记录（阶段 A 与阶段 B）

> [!summary] 阶段性总结
> 从零搭建了一个放在 D 盘的 Python Web 项目：浏览器可以录入课程、标题和笔记正文；FastAPI 接收表单并清理正文；SQLite 持久化保存笔记；用户可以查看全部笔记或按 ID 查看单篇笔记；不存在的笔记返回 HTTP 404。下一阶段将先用假 LLM 打通问答卡生成流程。

---

## 一、项目背景与目标

### 1. 项目选择

这个暑假的 AI 项目主线确定为：

```text
第一项目：AI 问答卡 / 复习提纲助手
第二项目：网易云学习音乐自动选择器
```

第一个项目的学习重点不是训练神经网络，而是理解一个典型 LLM 应用是怎样被做成产品的：

```text
用户输入
→ Python 后端接收
→ 数据校验
→ 数据库存储
→ 后续调用大模型
→ 结构化结果返回与保存
```

### 2. 第一版边界

当前项目只处理用户主动粘贴的一篇笔记，不做：

- 自动读取整个 Obsidian 仓库；
- PDF / Word 解析；
- RAG、Embedding、向量数据库；
- 多 Agent 与长期记忆；
- 用户登录和云端部署；
- 复杂前端和桌宠 GUI。

---

## 二、项目环境：为什么放在 D 盘

### 1. 目录分工

```text
D:\
├── CppProject\       # C++、数据结构、课程实验
└── AiProjects\
    └── AiStudyAssistant\
```

项目代码、`.venv`、SQLite 数据库和构建产物都放在 D 盘。C 盘只保留 Python 本体、uv、Git 等开发工具，不属于本项目内容。

### 2. 创建虚拟环境

在项目根目录执行：

```bash
uv venv --python 3.11
```

验证：

```bash
.venv/Scripts/python.exe --version
```

输出：

```text
Python 3.11.15
```

项目使用独立虚拟环境的原因：

- 不让本项目的依赖污染 Hermes 内部环境；
- 不让数学建模项目的依赖混入 AI 项目；
- 不同项目可以使用不同包版本；
- 删除项目时可以连同 `.venv` 一起删除。

### 3. 初始化项目元数据

```bash
uv init --bare --name ai-study-assistant --python 3.11 --vcs git --no-workspace
uv python pin 3.11
```

生成的主要文件：

| 文件 | 作用 |
|---|---|
| `pyproject.toml` | 项目名称、Python 要求、依赖声明 |
| `.python-version` | 固定当前项目使用 Python 3.11 |
| `uv.lock` | 锁定实际依赖版本 |
| `.git/` | Git 版本控制目录 |
| `.venv/` | 项目专属 Python 运行环境 |

### 4. 安装依赖

```bash
uv add fastapi "uvicorn[standard]"
uv add --dev pytest
```

- FastAPI：定义 Web 应用和路由。
- Uvicorn：启动 FastAPI 服务，监听本地端口。
- pytest：开发阶段的自动测试工具。

---

## 三、当前项目结构

```text
AiStudyAssistant/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
├── .venv/
├── .vscode/
│   └── setting.json
├── .hermes/
│   └── plans/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── note_validation.py
│   ├── database.py
│   └── repositories.py
├── data/
│   └── app.db
└── tests/
    └── test_note_validation.py
```

### 文件职责

```text
main.py
    FastAPI 应用、HTML 页面、HTTP 路由

note_validation.py
    笔记正文清理与空内容判断

database.py
    SQLite 连接、建表、数据库结构迁移

repositories.py
    notes 表的 INSERT / SELECT 操作

tests/
    自动化测试
```

这种拆分体现了一个重要工程原则：

> 路由负责处理请求，repository 负责访问数据库，初始化逻辑负责准备数据库结构；不要把所有逻辑堆进 `main.py`。

---

## 四、第一段 Python：`validate_note`

### 1. 功能目标

用户提交笔记后，正文不能直接原样进入数据库。首先要去掉两端的空白字符：

```text
"  链表是一种线性结构。  "
        ↓
"链表是一种线性结构。"
```

如果正文为空或全部由空白组成，应返回空字符串，供路由判断。

### 2. 自己实现的双指针版本

```python
def validate_note(content: str) -> str:
    i = 0
    j = len(content) - 1

    while i < len(content):
        if (
            content[i] != " "
            and content[i] != "\t"
            and content[i] != "\n"
        ):
            break
        i += 1

    while j >= 0:
        if (
            content[j] != " "
            and content[j] != "\t"
            and content[j] != "\n"
        ):
            break
        j -= 1

    if i > j:
        return ""

    return content[i : j + 1]
```

### 3. 遇到的问题与修复

| 问题 | 原因 | 修复 |
|---|---|---|
| 右指针从 `0` 开始 | 右侧扫描应从末尾开始 | `j = len(content) - 1` |
| 写成 `"/t"`、`"/n"` | 这是普通斜杠文本，不是转义字符 | 使用 `"\t"`、`"\n"` |
| 使用 `i <= len(content)` | `i == len(content)` 时访问越界 | 使用 `i < len(content)` |
| 写成 `content[i:j]` | Python 切片右端不包含 `j` | 使用 `content[i:j + 1]` |
| 空字符串和全空白 | 找不到有效字符 | 判断 `i > j` 后返回 `""` |

### 4. 学到的知识

- Python 函数与返回值类型注解：`content: str`、`-> str`。
- Python 字符串索引和切片。
- Python 切片采用左闭右开区间。
- `\t` 是 Tab，`\n` 是换行。
- 空字符串与全空白字符串的边界处理。
- 交互式 Python 可以快速手动调用函数。

### 5. 测试策略调整

最初计划严格使用“先写测试，再实现”的 TDD 顺序；实践后根据学习目标调整为：

```text
先理解功能、作用和边界
→ 用户自己实现代码
→ 交互式手动验证
→ 再补 pytest 和边界测试
```

这样做不是放弃测试，而是避免在 Python、FastAPI、数据库都尚未熟悉时，先被测试框架的形式打断理解过程。

当前 pytest 已能运行：

```text
1 passed
```

---

## 五、第一条 FastAPI 页面

### 1. 导入和创建应用

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
```

- `FastAPI` 是框架提供的类。
- `app = FastAPI()` 创建一个具体 Web 应用对象。
- 后续所有路由都注册到 `app` 上。
- `HTMLResponse` 用于告诉浏览器返回内容是 HTML。

### 2. GET 首页路由

```python
@app.get("/")
def home():
    return HTMLResponse(html_content)
```

```text
浏览器访问 /
→ FastAPI 找到 home()
→ home() 返回 HTMLResponse
→ 浏览器渲染页面
```

### 3. 启动服务

```bash
uv run uvicorn app.main:app --reload
```

命令拆解：

| 部分 | 含义 |
|---|---|
| `uv run` | 使用当前项目环境 |
| `uvicorn` | 启动 ASGI 服务器 |
| `app.main:app` | 从 `app/main.py` 找到变量 `app` |
| `--reload` | 修改代码后自动重载 |

---

## 六、HTML 表单与 POST 路由

### 1. HTML 表单

```html
<form action="/api/notes" method="post">
    <input name="course" placeholder="课程（可选，例如：数据结构）">
    <input name="title" placeholder="标题（可选）">
    <textarea name="content" placeholder="在此输入笔记内容"></textarea>
    <button type="submit">提交笔记</button>
</form>
```

HTML 的 `name` 是前后端连接字段：

```text
name="course"  → FastAPI 的 course 参数
name="title"   → FastAPI 的 title 参数
name="content" → FastAPI 的 content 参数
```

### 2. POST 路由

```python
from fastapi import FastAPI, Form, HTTPException


@app.post("/api/notes")
def create_note(
    course: str = Form(default=""),
    title: str = Form(default=""),
    content: str = Form(),
):
    cleaned_content = validate_note(content)
    if not cleaned_content:
        return HTMLResponse("<p>错误：笔记不能为空。</p>")

    cleaned_course = course.strip()
    cleaned_title = title.strip()

    note_id = repo.add_note(
        cleaned_course,
        cleaned_title,
        cleaned_content,
    )

    return HTMLResponse(...)
```

### 3. GET 与 POST 的区别

| | GET | POST |
|---|---|---|
| 当前用法 | 读取页面和笔记 | 提交新笔记 |
| 数据位置 | URL / 路径 | 请求体中的表单 |
| 是否改变数据 | 通常不改变 | 通常创建或修改资源 |
| 例子 | `GET /api/notes/2` | `POST /api/notes` |

---

## 七、SQLite 数据库

### 1. 为什么选择 SQLite

SQLite 适合这个本地小项目，因为：

- Python 标准库自带 `sqlite3`；
- 不需要启动 MySQL 或 PostgreSQL 服务；
- 一个 `.db` 文件就能保存完整数据库；
- 重启应用后数据仍然存在。

### 2. `notes` 表的数据模型

最终字段：

| 字段 | 作用 |
|---|---|
| `id` | 自增主键 |
| `course` | 课程分类，可为空 |
| `title` | 笔记标题，可为空 |
| `content` | 笔记正文，不能为空 |
| `created_at` | 创建时间 |

### 3. 数据库初始化

新数据库使用：

```sql
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course TEXT DEFAULT '',
    title TEXT DEFAULT '',
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

已有数据库不能只靠再次执行 `CREATE TABLE IF NOT EXISTS` 更新结构，因为这个语句遇到已存在的表会直接跳过。因此使用：

```sql
PRAGMA table_info(notes)
```

读取真实列名后，如果没有 `course`，执行：

```sql
ALTER TABLE notes ADD COLUMN course TEXT DEFAULT ''
```

完整思路：

```text
连接数据库
→ 确保 notes 表存在
→ 查询真实表结构
→ 判断 course 是否存在
→ 缺少时执行 ALTER TABLE
→ commit
→ close
```

### 4. 为什么不用 `list_notes()` 检查列

`list_notes()` 查询的是业务数据，而且它的 `SELECT` 字段由代码手写决定；它返回的字典键只能说明“这条查询取了哪些列”，不能代表数据库表的完整结构。

数据库初始化应使用数据库层的元数据接口：

```text
业务数据：SELECT ... FROM notes
表结构：PRAGMA table_info(notes)
```

### 5. `repositories.py`

新增笔记：

```python
cursor = conn.execute(
    "INSERT INTO notes (course, title, content) VALUES (?, ?, ?)",
    (course, title, content),
)
```

参数化查询中的 `?` 不能替换成 f-string 拼接。用户输入必须作为数据传入，不能被解释成 SQL 代码。

查询全部笔记：

```python
rows = conn.execute(
    "SELECT id, course, title, content, created_at "
    "FROM notes ORDER BY id DESC"
).fetchall()
```

按 ID 查询：

```python
row = conn.execute(
    "SELECT id, course, title, content, created_at "
    "FROM notes WHERE id = ?",
    (note_id,),
).fetchone()
```

这里曾经遇到过两个问题：

```python
.fetchone
```

只是取得方法对象，没有真正调用；正确写法是：

```python
.fetchone()
```

另外：

```sql
WHERE id - ?
```

是减法表达式，不是相等判断；正确写法是：

```sql
WHERE id = ?
```

---

## 八、按 ID 查看单篇笔记与 404

### 1. 路径参数

```python
@app.get("/api/notes/{note_id}")
def view_note(note_id: int):
    ...
```

访问：

```text
/api/notes/2
```

FastAPI 会把路径中的 `2` 转换为整数，传入：

```python
view_note(note_id=2)
```

### 2. 不存在时返回 404

```python
note = repo.get_note(note_id)

if not note:
    raise HTTPException(
        status_code=404,
        detail="笔记不存在",
    )
```

浏览器或 API 客户端会看到：

```json
{
  "detail": "笔记不存在"
}
```

这不是程序崩溃，而是 HTTP 对“资源不存在”的规范表达。

### 3. 成功页面

如果找到笔记，页面显示：

```text
课程
标题
正文
创建时间
```

课程或标题为空时，使用：

```python
note["course"] or "(未分类)"
note["title"] or "(无标题)"
```

---

## 九、阶段性时间线

### 2026-07-23 至 2026-07-24：项目环境与最小 Web

- 确定项目一为 AI 问答卡 / 复习提纲助手。
- 将项目放到 `D:\AiProjects\AiStudyAssistant`。
- 创建 Python 3.11 虚拟环境。
- 使用 uv 初始化项目并安装 FastAPI、Uvicorn、pytest。
- 创建 `app/`、`tests/` 包结构。
- 实现 `validate_note()`。
- 完成最小 FastAPI HTML 页面。
- 学习 GET、POST、HTML form、`Form()`、`HTMLResponse`。
- 解决 VS Code 解释器选择、错误虚拟环境和端口占用问题。

### 2026-08-03：SQLite 笔记持久化与课程分类

- 创建 `database.py`，理解 SQLite 连接、表、行、列、主键、提交和关闭连接。
- 创建 `repositories.py`，实现 `add_note()`、`list_notes()`、`get_note()`。
- 使用参数化 SQL。
- 完成按 ID 查询和 404 响应。
- 使用 `PRAGMA table_info(notes)` 检查数据库结构。
- 使用 `ALTER TABLE` 为旧数据库迁移 `course` 列。
- 修改 HTML 表单，接收课程字段。
- 修改 POST、列表和详情页面，展示课程字段。
- 实际验证创建、列表、详情和不存在 ID 的请求。
- 当前 pytest 运行结果：

```text
1 passed
```

---

## 十、当前问题与后续整理

这些问题暂不阻塞进入下一阶段，但应在项目收束前处理：

1. 已使用 `html.escape` 转义用户输入，避免 HTML 注入 / XSS。
2. 列表页可以进一步增加指向 `/api/notes/{id}` 的详情链接。
3. 当前 API 主要返回 HTML，后续使用原生 JavaScript `fetch` 后再逐步转为 JSON API。
4. 还没有 `schemas.py`、`services.py`，等生成流程变复杂后再引入，避免过早增加抽象。
5. 还没有完整的数据库、API 和错误分支测试。
6. 当前项目已完成首次提交与一次安全/健壮性修复提交；后续若提交 Obsidian 仓库，再维护根目录 `[[GitHub提交记录]]`。

---

## 十一、下一阶段预告：假 LLM

下一阶段暂不连接真实模型，而是先实现：

```text
选择一篇笔记
→ 调用本地假 LLM client
→ 返回固定 JSON 问答卡
→ 保存 generation 记录
→ 页面展示生成结果
```

将学习：

- 为什么要先用假服务打通业务流程；
- `generations` 表与 `notes` 表的关系；
- `note_id` 如何关联生成记录；
- Python 字典与 JSON 字符串之间的转换；
- `json.dumps()` 与 `json.loads()`；
- 依赖替换和可测试的外部服务抽象。

