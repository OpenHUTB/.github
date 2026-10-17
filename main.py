"""
main.py
社区入口脚本。
把 OpenHUTB 的几个关键链接和项目名字按编号打印出来，方便查找。
"""

def main():
    # 把资源按序号放在字典里
    resources = {
        1: "核心项目：hutb, doc, traffic_twin, neuro, PFC, move",
        2: "在线文档：https://openhutb.github.io/",
        3: "讨论区：https://github.com/orgs/OpenHUTB/discussions",
        4: "贡献指南：CONTRIBUTING.md"
    }

    print("========== OpenHUTB 资源清单 ==========")
    
    # 循环把字典里的内容打印出来
    for num, info in resources.items():
        print(f"{num}. {info}")
        
    print("=======================================")

if __name__ == "__main__":
    main()