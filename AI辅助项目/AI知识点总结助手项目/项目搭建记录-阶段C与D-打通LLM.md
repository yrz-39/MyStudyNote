---
tags:
  - AI项目
  - Python
  - FastAPI
  - LLM
  - DeepSeek
  - 学习笔记
status: 进行中
start: 2026-08-07
project: AI 问答卡与复习提纲助手
---

# 项目搭建记录（阶段 C 与 D）：打通 LLM 真实调用

> [!summary] 阶段性总结
> 阶段 C 用「假 LLM」打通了业务闭环：笔记 → 生成结构化结果 → 保存 → 展示。阶段 D 把假 LLM 换成真实 DeepSeek API，重点解决了三件事：密钥怎么安全存放、**如何与 DeepSeek 服务器建立连接**、如何让模型按固定 JSON 格式返回。最终用 `LLM_PROVIDER` 开关实现假/真模式一键切换，上层路由与页面一行未改。

前置阅读：[[项目搭建记录-阶段A与阶段B]]

---

## 一、两个阶段各做了什么

| 阶段 | 做了什么 | 产物 |
|---|---|---|
| C | 假 LLM 打通生成闭环 | `llm_client.py`（假）、`services.py`、`generations` 表、生成路由、结果渲染 |
| D | 接入真实 DeepSeek API | `.env` 配置层、`config.py`、`generate_real()`、`LLM_PROVIDER` 开关 |

阶段 C 刻意先做假 LLM，是为了让「业务结构」先立住；阶段 D 只换「结果从哪来」，业务层零改动——这就是**可替换的 client 抽象**的价值。

---

## 二、打通 LLM 的完整数据流

```text
浏览器点击「生成」
        ↓
POST /api/notes/{note_id}/generations     （main.py 路由）
        ↓
services.generate_for_note(note_id, mode)  （services.py）
        ↓ 查笔记
    LLM_PROVIDER 开关
   ┌────────────┴────────────┐
   │ fake                    │ real
   ↓                         ↓
generate() 假 LLM      generate_real() 真实调用
（写死返回）            ↓
                与 DeepSeek 服务器建立连接
                → 发送 messages（系统规则 + 笔记）
                → 收到 JSON 文本
                → json.loads 解析成 dict
        ↓
repo.add_generation() 存入 generations 表
        ↓
render_generation_result() 渲染成卡片 / 提纲（main.py）
```

---

## 三、重点：如何与 DeepSeek 服务器建立连接

### 3.1 先转变视角：DeepSeek 也是一个服务器

阶段 B 我们写过一个 FastAPI 服务器——浏览器发 POST（带 `course`、`title`、`content` 字段），我们的 Python 处理并返回 HTML。

DeepSeek 的 API **本质上也是这样一个服务器**，只不过它的接口不是「保存笔记」，而是「给我一段文字，我还你一段文字」。这一次，**我们的程序要扮演客户端的角色**：

| 熟悉的（阶段 B） | 这次的（阶段 D） |
|---|---|
| 浏览器发 POST 到 `/api/notes` | 我们的程序发请求到 DeepSeek 的接口 |
| 表单字段 `course` / `title` / `content` | `messages` 列表里的 `role` 和 `content` |
| FastAPI 用 `Form()` 接字段 | DeepSeek 服务器用 `messages` 接内容 |
| 返回 `HTMLResponse` | 返回响应对象，文本在 `choices[0].message.content` |

### 3.2 连接的三要素

```python
from openai import OpenAI

client = OpenAI(
    api_key=cfg["api_key"],      # ① 身份凭证：证明「我是谁」
    base_url=cfg["base_url"],    # ② 服务器地址：我要敲谁的门
    timeout=30,                  # ③ 耐心上限：等多久算超时
)
```

| 要素 | 作用 | 类比 |
|---|---|---|
| `api_key` | 请求的身份证。DeepSeek 服务器靠它知道你是谁、有没有额度 | 门禁卡 |
| `base_url` | 服务器地址。DeepSeek 官方是 `https://api.deepseek.com`，OpenAI 兼容接口通常以 `/v1` 结尾 | 大楼地址 |
| `timeout` | 网络请求最多等 30 秒，超时就放弃，不让程序永远挂着 | 等人的耐心 |

### 3.3 关键认知：`OpenAI(...)` 不是「连接」，是「连接配置」

这是最容易误解的一点：

```text
OpenAI(api_key, base_url, timeout)   ← 只是拿着门禁卡站在楼下，登记了地址
        ↓
client.chat.completions.create(...)  ← 这才是真正刷卡、进门、开口说话
```

`client` 对象只是「把身份和地址提前存好」，**真正的网络请求发生在每次 `.create()` 调用时**。所以：

- `client` 创建一次、全程复用（不用每次生成都重新登记身份）；
- 每次「生成」都是一次独立的 `.create()` 请求。

### 3.4 请求体：messages（两张纸条）

```python
messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},   # 规则条：你是谁、必须输出什么
    {"role": "user",   "content": "笔记内容……"},    # 材料条：要处理的东西
]
```

| role | 含义 | 类比 |
|---|---|---|
| `system` | 给模型的规则：身份、行为约束、输出格式 | 面试官宣读的规则 |
| `user` | 用户真正要模型处理的内容 | 递给面试官的答卷 |

### 3.5 响应体：`choices[0].message.content` 的层级

```python
resp = client.chat.completions.create(model=..., messages=...)
text = resp.choices[0].message.content
```

这个嵌套取法看起来吓人，拆开看其实每一层都有意义：

```text
resp                      整个响应包裹（快递盒）
 └─ choices[0]            候选回复列表，取第 0 个（模型可能给多个候选，通常取第一个）
     └─ message           一条完整的消息对象
         └─ content       消息正文（模型说的话）
```

> 小知识：`choices` 是**列表**，因为 API 允许一次请求生成多个候选回复（`n` 参数）。我们只需要第一个，所以写 `[0]`。

### 3.6 一次完整对话的时序

```text
我们的程序                           DeepSeek 服务器
    │  POST /chat/completions          │
    │  Authorization: Bearer sk-***    │
    │  {model, messages}               │
    │ ────────────────────────────────→│
    │                                  │  模型根据笔记生成 JSON 文本
    │  {choices: [{message:            │
    │     {content: '{"cards": [...]}'}}]} 
    │ ←────────────────────────────────│
    ↓
json.loads() 解析 → 校验 → 存入数据库 → 渲染展示
```

---

## 四、让模型按固定 JSON 格式返回（Prompt 约束）

模型天生是「自由的」，想说什么说什么。要让它输出程序能解析的形状，必须用 system Prompt 把格式写死：

```text
你是学习助手，根据用户提供的笔记生成复习材料。
只输出 JSON，不要输出任何其他文字，不要用 markdown 代码块。
必须严格使用以下格式：
{"cards": [{"question": "问题", "answer": "答案", "tag": "知识点标签"}]}
```

三个要点：

1. **「只输出 JSON」写死**——否则模型会夹带「好的，以下是……」这类杂讯；
2. **给出精确格式样例**——模型会模仿你给的形状，比抽象描述有效得多；
3. outline 模式同理，格式换成 `{"outline": ["要点1", ...]}`。

---

## 五、解析与校验：接住模型的话

```python
text = resp.choices[0].message.content
if text is None:
    raise ValueError("模型没有返回任何文本内容")      # ① 空回复保护

data = json.loads(text)                              # ② 文本 → 字典

expected = "cards" if mode == "flashcards" else "outline"
if expected not in data:
    raise ValueError(f"模型返回的 JSON 里没有 {expected} 字段")   # ③ 结构校验
```

三层防线，每层回答一个问题：

| 防线 | 防什么 | 模型返回 None | 模型返回「抱歉我不能」 | 模型返回 `{"foo": 1}` |
|---|---|---|---|---|
| ① | 空内容 | ✅ 清晰报错 | — | — |
| ② | 坏 JSON | — | ✅ 抛 `JSONDecodeError` | — |
| ③ | 缺字段 | — | — | ✅ 指名缺哪个键 |

---

## 六、假/真开关：可替换的 client 抽象

```text
.env 里：LLM_PROVIDER=fake 或 real
        ↓
config.py 读出 provider
        ↓
services.py 二选一：
    real → llm_client.generate_real(note, mode)
    fake → llm_client.generate(note, mode)
```

- 默认 `fake`：不设变量就不花钱——**危险动作要显式授权**；
- 换实现时上层（路由、渲染）零改动，这就是「可替换抽象」的回报。

---

## 七、实测结果

用 `LLM_PROVIDER=real` 对「二叉树」笔记生成问答卡，真实返回：

```python
{'cards': [{'question': '二叉树节点的通常定义是什么？',
             'answer': '二叉树节点通常包含数据域和指向左右子节点的指针（或引用）。',
             'tag': '二叉树'}]}
```

与假 LLM 写死的「问题1 / 回答1 / 标签1」形成鲜明对比——模型真的读了笔记内容才答得出来。

---

## 八、踩过的坑

### 坑 1：Pylance 报 `reportArgumentType`（messages 类型不匹配）

```text
无法将 "list[dict[str, str]]" 类型分配给参数 "messages"
```

**原因**：OpenAI SDK 2.x 对消息有官方类型 `ChatCompletionMessageParam`（TypedDict 联合），Pylance 认为普通 `dict` 不够格。**运行时没任何问题**，纯静态检查。

**解法**：显式标注类型，Pylance 就闭嘴了：

```python
from openai.types.chat import ChatCompletionMessageParam
messages: list[ChatCompletionMessageParam] = [...]
```

### 坑 2：`content` 可能是 `None`（reportOptionalSubscript）

SDK 里 `message.content` 的类型是 `str | None`——API 允许模型返回空内容。Pylance 要求处理这个分支，于是顺手加了一层真实的运行时保护（见第五节防线①）。

### 坑 3：验证时被工具坑了一把

验证期间 `read_file` 把 `llm_client.py` 误判成二进制文件——实际是标准 UTF-8。用 `python -c "open(...).read()"` 或终端 `file` 命令确认编码即可，不是项目问题，是工具误判。

---

## 九、下一步：容错课

真实调用目前还有一块短板：**断网 / 超时 / 服务端报错时，网页会直接 500**。下一阶段要做的：

- 捕获网络异常（`APIConnectionError`、超时），给用户友好的错误提示；
- `LLM_PROVIDER` 非法值校验；
- 输出结构校验加强（字段类型、数量）；
- 阶段 E：测试补全、README 收束。
