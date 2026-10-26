# reports 文件夹

这里头主要放 OpenHUTB 项目跑自动化统计时生成的数据报告，基本都是 CSV 这些格式。后面要是想追溯某个时间段的项目活跃度或者提交记录，来这个目录翻就行。

报告不用手动弄，跑 `src` 目录下的 `git_commit_stats.py` 脚本就自动生成了。

想自己出一份报告的话，大概这么搞：

1. 先确认电脑里有 Python 环境。
2. 切到项目根目录，把命令行终端开起来。
3. 跑下面的命令，比如统计特定时间段的提交：

```bash
python src/git_commit_stats.py --since "2026-02-27 18:00" --until "2026-03-08 00:00" --output reports/commit_stats.csv
```
