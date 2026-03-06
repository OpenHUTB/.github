# python git_commit_stats.py --since "2026-02-27 18:00" --until "2026-03-08 00:00"运行指定时间段的提交统计，结果输出到 commit_stats.csv 文件中。可以通过 --ignore 参数指定一个 JSON 文件，里面包含需要屏蔽的用户（按邮箱或用户名）。如果不指定 --ignore 参数，则默认使用 ignore_users.json 文件作为屏蔽列表。
import subprocess
import argparse
import csv
import json
import os
from collections import Counter

def load_ignore_users(file_path):
    """从 JSON 文件加载屏蔽列表"""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取屏蔽列表失败: {e}")
        return []

def get_commits(since=None, until=None, ignore_list=[]):
    # 使用 %ae(邮箱)作为唯一键，%an(用户名)作为显示名
    cmd = ["git", "log", "--pretty=%ae|%an"]
    
    if since: cmd.append(f"--since={since}")
    if until: cmd.append(f"--until={until}")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        print("git log 执行失败")
        return [], {}

    raw_data = result.stdout.strip().split("\n")
    email_to_name = {}
    email_counts = Counter()

    for line in raw_data:
        if "|" not in line: continue
        email, name = line.split("|", 1)
        email = email.strip()
        name = name.strip()

        # 过滤屏蔽用户（支持按邮箱或用户名屏蔽）
        if email in ignore_list or name in ignore_list:
            continue
        
        # 自动映射：同一个邮箱只保留遇到的第一个用户名作为显示名
        if email not in email_to_name:
            email_to_name[email] = name
        
        email_counts[email] += 1

    return email_counts, email_to_name

def main():
    parser = argparse.ArgumentParser(description="Git 提交统计工具")
    parser.add_argument("--since", help="开始时间")
    parser.add_argument("--until", help="结束时间")
    parser.add_argument("--ignore", default="ignore_users.json", help="屏蔽列表文件(JSON)")
    parser.add_argument("--output", default="commit_stats.csv", help="输出CSV文件")
    args = parser.parse_args()

    ignore_list = load_ignore_users(args.ignore)
    counts, name_map = get_commits(args.since, args.until, ignore_list)

    # 转换结果：[(用户名, 次数), ...]
    results = sorted(
        [(name_map[email], count) for email, count in counts.items()],
        key=lambda x: x[1], 
        reverse=True
    )

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Commits"])
        writer.writerows(results)

    print(f"统计完成！共 {len(results)} 人提交。结果已写入 {args.output}")

if __name__ == "__main__":
    main()