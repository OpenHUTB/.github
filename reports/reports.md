# reports 文件夹说明

## 1. 目录用途
本目录主要用于存放 OpenHUTB 项目在自动化统计过程中生成的各类数据报告（如 CSV 文件等）。这些报告用于追溯不同时间段的项目活跃度和提交记录。

## 2. 报告是如何生成的
这些报告并非手动创建，而是通过运行 `src` 目录下的 `git_commit_stats.py` 脚本自动生成的。

以下是生成报告的具体操作步骤：

1. 确保已经安装了 Python 环境。
2. 在项目根目录下，打开命令行终端。
3. 运行统计脚本，例如统计特定时间段的提交记录：
   ```bash
   python src/git_commit_stats.py --since "2026-02-27 18:00" --until "2026-03-08 00:00" --output reports/commit_stats.csv
