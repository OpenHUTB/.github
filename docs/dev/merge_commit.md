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

## 参考

- [TortoiseGit：摘取提交](https://tortoisegit.org/docs/tortoisegit/tgit-dug-cherrypick.html)
