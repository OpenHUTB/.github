# 合并提交

## 摘樱桃（cherry pick）

「摘取提交」（cherry pick）是把某个分支上的**指定几个提交**单独复制到当前分支，而不是把整个分支合并过来；适合"只要其中几个改动"的场景。

### 用 TortoiseGit 操作

1. 先用 `Switch/Checkout` 切到**要接收这些提交的目标分支**（注意不要点 `New Branch`）。
2. 右键工作副本 → `TortoiseGit` → `Show log`，打开日志。
3. 在日志窗口左上角点击分支名，把日志切换显示到**包含目标提交的源分支**（这一步只切换日志视图，不会改动工作区）。
4. 选中需要摘取的一个或多个提交，右键选择 `Cherry Pick selected commits...`。
5. 在弹出的对话框中确认提交信息，点击 `Continue`；若有冲突，先按提示解决冲突再继续。
6. 完成后 `Pull`、`Push` 同步到远程。

### 用命令行操作

```bash
# 把指定提交摘取到当前分支（一次可以给多个）
git cherry-pick <提交号> [<提交号> ...]
```

### 遇到冲突

若提示冲突：先手动解决冲突，再执行 `git cherry-pick --continue`；想放弃则用 `git cherry-pick --abort`。
