# GitHub 提交记录

> 用途：每次把 vault 内容提交到 GitHub 前，先阅读本文件；对比“上一次提交”和“本次准备提交”的差异，然后在对应提交条目中记录本次修改/新增的笔记内容。

## 提交前记录流程

每次提交前按下面顺序做：

1. 先阅读本文件，确认上一次记录的提交哈希。
2. 用 Git 对比上一次提交与本次待提交内容，例如：
   - 已提交之间对比：`git diff --name-status <上一次提交> HEAD`
   - 提交前查看工作区：`git status --short`、`git diff --name-status`
3. 重点记录：
   - 新增的笔记
   - 修改的笔记
   - 移动/重命名的笔记
   - 新增的重要课件/PDF/图片资源
   - Obsidian 配置或 CSS snippet 的变化
4. 提交前先把本文件更新并纳入同一次提交。

---

## 提交记录

### 2026-07-22 — `bae06ac` Update study notes and course materials

对比范围：`fb481b9` → 本次提交

#### 本次修改/新增笔记内容

- 新增 [[02-学习/2026暑假/2026暑假学习计划]]。
- 新增并整理 [[02-学习/C++/C++期末复习]]、[[02-学习/C++/C++期末自测]]、[[02-学习/C++/cpp_exam_review_guide]] 及 C++ 并发、程序设计、数据结构相关笔记。
- 将部分 C++、DLCO 笔记移动到对应分类目录，并新增 [[02-学习/C++/课程/并行程序设计 C++.md]] 等课程资料。
- 新增 [[02-学习/DLCO/DLCO期末复习]]、[[02-学习/DLCO/DLCO期末复习最终版]]、实验 8 报告，并更新 CPU、流水线 CPU 等笔记。
- 新增数据结构教材与线性表、栈、队列、链表等整理笔记。
- 新增离散数学期末复习、图论、树及课程讲义/习题资源。
- 新增马原复习笔记与相关课件资源。
- 新增 [[AI_memory/01_我的基本信息]] 至 [[AI_memory/06_AI助手规则]]，以及 [[作业]]。
- 修改 [[dashboard]] 与 [[海权对历史的影响_测试题整理_章节0-13_完整版]]。

#### 附件与图片变化

- 新增 C++、离散数学、数据结构、马原等课程的 PPT/PPTX/PDF/ZIP 资源。
- 新增多张 [[图片/Pasted image 20260608144426.png]] 等图片附件。
- 删除旧版 DLCO 实验 6 PDF，并新增数据结构第三版教材 PDF。

#### Obsidian 配置变化

- 更新 [[.obsidian/app.json]]、apex-dashboard、editing-toolbar、obsidian42-brat、realclaudian 插件配置，以及 Phycat 主题文件。
- 新增/更新 [[CLAUDE]]、[[小红书发布/CLAUDE]] 与 [[_verify.py]]。

---

### 2026-06-06 21:27 — `fb481b9` Update Obsidian vault notes and settings

对比范围：`7ad720b` → `fb481b9`

#### 本次修改/新增笔记内容

##### DLCO / CPU 相关

- 新增 [[02-学习/DLCO/DLCO笔记]]。
- 新增 [[02-学习/DLCO/单周期CPU设计(最重要)]]，整理单周期 CPU 设计内容。
- 新增 [[02-学习/DLCO/多周期CPU设计_习题集]]。
- 新增 [[02-学习/DLCO/多周期CPU设计复习]]。
- 新增 [[02-学习/DLCO/标志信号和大小判断]]。
- 新增 [[02-学习/DLCO/流水线CPU设计]]。
- 新增 [[02-学习/DLCO/训练]]。
- 新增/整理 DLCO 实验报告目录：
  - [[02-学习/DLCO/DLCO实验报告/实验1实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验2实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验3实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验4实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验5实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验5实验报告1]]
  - [[02-学习/DLCO/DLCO实验报告/实验6实验报告]]
  - [[02-学习/DLCO/DLCO实验报告/实验报告模板]]
- 新增 DLCO 课件资源：
  - [[02-学习/DLCO/课件/第8章 中央处理器-非流水线CPU (1).pdf]]
  - [[02-学习/DLCO/课件/第8章 中央处理器-流水线CPU.pdf]]
  - [[02-学习/DLCO/DLCO实验报告/实验6：单周期CPU设计与测试.pdf]]

##### 离散数学 / 图论相关

- 新增 [[02-学习/离散数学/图论导引]]。
- 新增 [[02-学习/离散数学/图论]]。
- 新增 [[02-学习/离散数学/图的连通性]]。
- 新增 [[02-学习/离散数学/带权图与最短路]]。
- 新增 [[02-学习/离散数学/二部图及其匹配]]。
- 新增离散数学图论课件资源：
  - [[02-学习/离散数学/课件/第13讲：图论导引 (1).pdf]]
  - [[02-学习/离散数学/课件/第14讲：图的连通性 (1).pdf]]
  - [[02-学习/离散数学/课件/第15讲：欧拉图与哈密顿图.pdf]]
  - [[02-学习/离散数学/课件/第16讲：带权图与最短路.pdf]]
  - [[02-学习/离散数学/课件/第17讲：二部图及其匹配.pdf]]

##### C++ / 程序设计相关

- 新增 [[std-thread和this_thread]]。
- 新增 [[并行程序设计 C++]]。
- 修改 [[C++中的lambda表达式与python的lambda表达式的比较]]。
- 修改 [[包装函数对象]]。
- 修改 [[程序设计中回调函数的设计]]。
- 新增 [[02-学习/PA历程]]，同时根目录 [[PA历程]] 也有修改。

##### 英语单词本相关

- 将原来的 `02-学习/CET4_CET6_high_frequency_vocab.md` 移动/整理到 [[02-学习/单词本/CET4_CET6_high_frequency_vocab]]。
- 新增 [[02-学习/单词本/CET4_CET6_high_frequency_vocab_backup]]。
- 新增词频数据文件 `02-学习/.cet_exam_freq.csv`。

##### 其他学习资料

- 新增 [[海权对历史的影响_测试题整理_章节0-13_完整版]]。

#### 附件与图片变化

- 新增多张 `图片/Pasted image ... .png` 图片附件。
- 将根目录 `Pasted image 20260330104531.png` 移动到 `图片/` 目录。
- 删除 `图片/Pasted image 20260524143103.png`。

#### Obsidian 配置变化

- 新增 CSS snippets：
  - [[.obsidian/snippets/compact-table-spacing.css]]：全局压缩表格与上下文间距。
  - [[.obsidian/snippets/bold-color-fix.css]]
  - [[.obsidian/snippets/vocab-strikethrough.css]]
  - [[.obsidian/snippets/vscode-default-dark-code.css]]
- 修改 [[.obsidian/appearance.json]]，启用 `compact-table-spacing` 等 CSS snippets。
- 修改若干 Obsidian 插件配置，包括 apex-dashboard、editing-toolbar、style-settings、realclaudian 等。

---

### 2026-05-29 11:54 — `7ad720b` Initial commit: upload Obsidian vault - MyNotes

#### 本次修改/新增笔记内容

- 首次将 Obsidian vault `MyNotes` 上传到 GitHub。
- 作为后续提交记录的基线提交。
