# src 目录说明

本目录存放 `OpenHUTB/.github` 仓库的维护脚本与配置，不包含 OpenHUTB 模拟器核心源码。

| 文件 | 用途 |
| --- | --- |
| `check_pr.bat` | 在 Windows 下按 PR 编号拉取 Pull Request，并切换到对应的本地分支。 |
| `git_commit_stats.py` | 统计指定时间范围内的 Git 提交记录，并生成 CSV 文件。 |
| `ignore_users.json` | 提交统计脚本使用的用户屏蔽配置。 |

## 生成提交统计

在仓库根目录运行：

```bash
python src/git_commit_stats.py \
  --since "2026-02-27 18:00" \
  --until "2026-03-08 00:00" \
  --output commit_stats.csv
```

生成的 CSV 包含 `User` 和 `Commits` 两列。脚本只读取 Git 历史，不会修改仓库内容。
