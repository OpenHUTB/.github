# 查看仓库提交统计

仓库提供 `src/git_commit_stats.py`，可将指定时间段内的 Git 提交次数写入 CSV。脚本按提交邮箱统计，CSV 中显示该邮箱在提交记录中的用户名。

在仓库根目录运行：

```bash
python src/git_commit_stats.py --since "2026-10-01 00:00" --until "2026-11-01 00:00" --output commit_stats.csv
```

`--since` 和 `--until` 可以省略，此时统计当前仓库的全部提交。`--output` 默认是 `commit_stats.csv`；指定其他名称时，输出路径相对于运行命令的目录。

默认屏蔽名单位于 `src/ignore_users.json`。如需使用另一份名单，可传 `--ignore 路径/名单.json`；名单内容为用户名或邮箱组成的 JSON 数组。生成后先核对 CSV 的时间范围和屏蔽名单，再分享统计结果。
