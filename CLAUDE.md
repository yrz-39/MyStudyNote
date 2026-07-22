# CLAUDE.md
注意：我没说修改文档 你就不要修改 只在交互界面输出

## GitHub 提交记录维护规则

当用户要求提交、上传、push 到 GitHub，或需要执行 `git commit` 前，必须先维护根目录笔记 [[GitHub提交记录.md]]。

提交前流程：

1. 先阅读 [[GitHub提交记录.md]]，确认上一次记录的提交哈希与记录格式。
2. 对比上一次提交与本次准备提交的差异：
   - 查看工作区：`git status --short`
   - 查看文件变化：`git diff --name-status`
   - 必要时对比上一次记录哈希：`git diff --name-status <上一次提交哈希> HEAD` 或与暂存区对比。
3. 在 [[GitHub提交记录.md]] 的“提交记录”部分新增本次条目，重点记录：
   - 新增笔记
   - 修改笔记
   - 移动/重命名笔记
   - 新增的重要课件、PDF、图片资源
   - Obsidian 配置、CSS snippet、插件配置变化
4. 把 [[GitHub提交记录.md]] 纳入同一次提交。
5. 提交完成后，如果提交哈希变化，回填或修正本次提交记录中的提交哈希。

记录内容要用 Obsidian wikilink，方便用户点击打开，例如：`[[02-学习/DLCO/单周期CPU设计(最重要)]]`。

## 内容发布相关规则

本仓库可能包含用于小红书发布的 Obsidian 笔记整理流程。

当任务涉及“小红书发布”“Export Image”“长图导出”“发布稿模板”“笔记分享”时，请优先阅读并遵守：

[[小红书发布/CLAUDE.md]]

GitHub 提交规则始终优先于小红书发布规则。  
凡是涉及 commit、push、上传 GitHub 的任务，都必须先维护 [[GitHub提交记录.md]]。
