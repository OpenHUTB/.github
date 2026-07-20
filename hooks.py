from datetime import datetime
import shutil
import os


# 动态获取页脚版权页面的年份
def on_config(config, **kwargs):
    year = str(datetime.now().year)
    config.copyright = config.copyright.format(year=year)


# 在 MkDocs 构建开始前，将根目录下的 CONTRIBUTING.md 
# 拷贝到 docs 目录下，确保文档站点能够引用到它。
# （名称必须为 on_pre_build）
def on_pre_build(**kwargs):
    # 源文件：项目根目录下的文件
    src_file = os.path.join(os.path.dirname(__file__), 'CONTRIBUTING.md')
    # 目标文件：文档目录（相对于 docs_dir）
    dest_file = os.path.join(os.path.dirname(__file__), 'docs', 'CONTRIBUTING.md')
    
    # 执行拷贝
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print("Successfully copied CONTRIBUTING.md to docs/CONTRIBUTING.md")