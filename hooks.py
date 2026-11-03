from datetime import datetime
import logging
import shutil
import os
from pathlib import Path


# 动态获取页脚版权页面的年份
def on_config(config, **kwargs):
    year = str(datetime.now().year)
    copyright_text = getattr(config, "copyright", None)
    if copyright_text:
        config.copyright = copyright_text.replace("{year}", year)


# CONTRIBUTING.md 是从仓库根目录复制的，编辑按钮也应指回根目录源文件。
def on_page_context(context, page, config, **kwargs):
    if page.file.src_uri != "CONTRIBUTING.md" or not page.edit_url:
        return context

    docs_name = Path(config["docs_dir"]).name
    generated_suffix = f"/{docs_name}/CONTRIBUTING.md"
    if page.edit_url.endswith(generated_suffix):
        page.edit_url = page.edit_url[: -len(generated_suffix)] + "/CONTRIBUTING.md"
    return context


# 在 MkDocs 构建开始前，将根目录下的 CONTRIBUTING.md
# 拷贝到 docs 目录下，确保文档站点能够引用到它。
# （名称必须为 on_pre_build）
def on_pre_build(config, **kwargs):
    # 源文件：项目根目录下的文件
    src_file = os.path.join(os.path.dirname(__file__), 'CONTRIBUTING.md')
    # 目标文件：MkDocs 配置中的 docs_dir
    docs_dir = config["docs_dir"]
    os.makedirs(docs_dir, exist_ok=True)
    dest_file = os.path.join(docs_dir, 'CONTRIBUTING.md')
    
    # 执行拷贝
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print("Successfully copied CONTRIBUTING.md to docs/CONTRIBUTING.md")
    else:
        logging.getLogger(__name__).warning(
            "Source file not found: %s; contribution guide was not copied", src_file
        )
 # 构建完成后，输出文档构建统计信息
def on_post_build(config, **kwargs):
    import os
    docs_path = config["docs_dir"]
    md_count = 0
    # 遍历统计所有md文档数量
    for root, dirs, files in os.walk(docs_path):
        for f in files:
            if f.endswith(".md"):
                md_count += 1
    print(f"✅ 文档网站构建完成！")
    print(f"📄 检测到Markdown文档总数：{md_count}")
