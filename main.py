"""
main.py
这是 OpenHUTB 社区的信息入口脚本。
把常用的链接和项目名字集中打印出来，方便大家快速查阅。
"""

def main():
    # 把核心项目写进一个列表里，方便以后加新的项目
    projects = ["hutb", "doc", "traffic_twin", "neuro", "PFC", "move"]
    
    print("欢迎来到 OpenHUTB 开源社区！")
    print("核心项目包含：" + "、".join(projects))
    print("在线文档：" + "https://openhutb.github.io/")
    print("讨论区：" + "https://github.com/orgs/OpenHUTB/discussions")
    print("贡献指南：" + "CONTRIBUTING.md")

if __name__ == "__main__":
    main()