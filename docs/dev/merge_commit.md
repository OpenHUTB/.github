# 合并提交

## 摘取指定提交（Cherry-pick）

如果只想把另一个分支中的几次修改带到当前分支，可以使用 Cherry-pick。例如，将 `docs-fix` 分支中的一处文档修正带到 `master`，接收修改的分支是 `master`，提供提交的分支是 `docs-fix`。

### 操作步骤

1. 先检查工作区，将尚未提交的修改提交或暂存到 Stash，避免与本次操作混在一起。
2. 在仓库目录右键选择 `TortoiseGit → Switch/Checkout`，切换到**接收修改的目标分支**。以上面的例子来说，应切换到 `master`。
3. 打开 `TortoiseGit → Show log`，在日志窗口中选择源分支 `docs-fix`，查看需要摘取的提交。这里只切换日志显示的分支，不再切换工作区分支。
4. 选中需要的提交，右键选择 `Cherry Pick this commit...`；选中多个提交时，选择对应的批量摘取选项。
5. 在弹出的窗口中检查提交列表和顺序。如果后面的修改依赖前面的修改，应先应用较早的提交，再点击 `Continue`。

### 完成后检查

操作完成后，查看当前分支的日志和文件差异，确认需要的修改已经进入目标分支。检查文档页面或运行相关程序，确认没有问题后再推送该分支。源分支中的原提交仍然保留。

如果出现冲突，先按[解决冲突](../resolve_conflict.md)中的步骤处理文件，再回到 Cherry-pick 窗口继续操作；不要直接另开普通提交窗口结束本次操作。

## 摘取中断后如何处理

终端提示冲突后，先执行 `git status`，确认当前正在进行 Cherry-pick，并查看哪些文件尚未解决。下面的 `docs/example.md` 仅表示发生冲突的文件，应替换为状态列表中的实际路径。

### 保留本次摘取并继续

1. 打开冲突文件，逐处决定保留的内容，清除 `<<<<<<<`、`=======`、`>>>>>>>` 标记，检查修改后的完整段落或代码。
2. 只暂存已经解决的文件，再检查暂存差异：

   ```shell
   git add -- docs/example.md
   git diff --cached
   git diff --check
   git cherry-pick --continue
   ```

3. 如果弹出提交信息编辑器，确认信息后保存并关闭；批量摘取时，后续提交也可能再次遇到冲突，按相同步骤处理。
4. 最后运行 `git status` 和 `git log -5 --oneline`，确认摘取流程已结束、提交顺序正确，再检查实际文件效果并推送。

### 放弃或跳过

| 需要做什么 | 命令 | 执行前确认 |
| --- | --- | --- |
| 放弃本轮摘取，回到开始前的状态 | `git cherry-pick --abort` | 本轮已处理的冲突内容如需保留，应先另存；批量摘取时会撤销本轮已经应用的提交 |
| 跳过当前提交，继续后续提交 | `git cherry-pick --skip` | 已核对该提交的修改已存在，或确实不需要；不能仅因为出现冲突就跳过 |

如果提示当前提交为空，先比较目标分支已有内容与本次修改，再决定是否跳过。不要在原因不明时反复执行普通 `git commit`；用 `git status` 确认正在进行的操作，并通过对应的继续或撤销命令结束流程。

## 参考

- [TortoiseGit：摘取提交](https://tortoisegit.org/docs/tortoisegit/tgit-dug-cherrypick.html)

- [Git：cherry-pick 的继续、跳过与撤销](https://git-scm.com/docs/git-cherry-pick#_sequencer_subcommands)
