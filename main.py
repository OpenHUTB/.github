"""
main.py - OpenHUTB 社区信息入口模块

本脚本作为 OpenHUTB 社区信息的快速查看入口，
运行后将在终端打印核心项目列表、在线文档及社区讨论区链接。
"""

def main():
    """
    主函数：负责打印社区相关信息。
    """
    print("欢迎来到 OpenHUTB 开源社区！")
    print("核心项目：hutb, doc, traffic_twin, neuro, PFC, move")
    print("在线文档：https://openhutb.github.io/")
    print("讨论区：https://github.com/orgs/OpenHUTB/discussions")
    print("贡献指南：CONTRIBUTING.md")

if __name__ == "__main__":
    main()