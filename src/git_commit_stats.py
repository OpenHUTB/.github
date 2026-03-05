# 终端运行：python git_commit_stats.py --since "2026-02-27 18:00" --until "2026-03-08 00:00"
import subprocess
import argparse
import csv
from collections import Counter

# ===== 用户别名映射 =====
ALIAS_MAP = {
    "HAJIMI": "ou-yang220",
    "Haidong Wang": "donghaiwang",
    # 可以继续添加别名
}

# ===== 屏蔽用户列表 =====
IGNORE_USERS = [
    "Haidong Wang"
    "donghaiwang",
    # 可以添加更多不统计的用户
]


def normalize_user(name):
    """将用户名转换为标准用户名，并去除空白"""
    name = name.strip()
    return ALIAS_MAP.get(name, name)


def get_commits(since=None, until=None):
    cmd = ["git", "log", "--pretty=%an"]

    if since:
        cmd.append(f"--since={since}")
    if until:
        cmd.append(f"--until={until}")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("git log 执行失败")
        print(result.stderr)
        return []

    authors = result.stdout.strip().split("\n")
    # 统一用户名并过滤空字符串
    authors = [normalize_user(a) for a in authors if a.strip() != ""]
    # 过滤黑名单用户
    authors = [a for a in authors if a not in IGNORE_USERS]

    return authors


def main():
    parser = argparse.ArgumentParser(description="统计指定时间段每个用户的提交次数（支持别名 + 黑名单）")
    parser.add_argument("--since", help="开始时间，例如: 2026-02-27 18:00")
    parser.add_argument("--until", help="结束时间，例如: 2026-03-08 00:00")
    parser.add_argument("--output", default="commit_stats.csv", help="输出CSV文件")

    args = parser.parse_args()

    authors = get_commits(args.since, args.until)

    counter = Counter(authors)
    results = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Commits"])
        for user, count in results:
            writer.writerow([user, count])

    print("统计完成")
    print("提交人数:", len(results))
    print("输出文件:", args.output)


if __name__ == "__main__":
    main()