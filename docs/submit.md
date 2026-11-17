# 文档修改指南   
（创建拉取请求之后一定要在下方的评论区@有权限的人审核）

## 1. 下载 Git
下载后会得到一个 `.exe` 文件，双击运行安装：
[https://git-scm.com/install/windows](https://git-scm.com/install/windows)

## 2. 下载 Visual Studio Code
下载后会得到一个 `.exe` 文件，双击运行安装：    
(打开下载页面，区分Visual Studio 2026和Visual Studio Code，选择Visual Studio Code下载)
[https://visualstudio.microsoft.com/zh-hans/downloads/](https://visualstudio.microsoft.com/zh-hans/downloads/)

## 3. 克隆仓库
> **注意**：该命令中的 `{用户名}` 请替换为自己的用户名。

```bash
git clone https://github.com/{用户名}/.github.git
```

克隆完成后进入仓库目录：

```bash
cd .github
```

## 4. 介绍 .github 文件结构

- **`docs`**：主要修改的地方。
- **`docs/img`**：存放图片的地方。图片需使用语义化英文名称，禁止使用系统自动生成的截图默认文件名。
- **`docs/src`**：存放代码的地方。
- **`docs/paper`**：放论文的地方。
- **`docs` 下的 `.md` 文件**：修改的具体地址（`.md` 文件也是 Markdown 源文件）。

## 5. 快速修改方向（红色部分是原句，绿色部分是改句）

1. 核对操作步骤中的命令、路径和链接，发现不一致时直接修正。
![wmx002](./img/wmx002.png)
![wmx003](./img/wmx003.png)
2. 按文档步骤实际操作后，补上缺少的前提、结果和常见问题。
![wmx004](./img/wmx004.png)
![wmx005](./img/wmx005.png)
3. 检查示例中的错误或遗漏并直接修正，让读者能按步骤完成。
![wmx006](./img/wmx006.png)
4. 把表达不清的句子改写得更具体，说明操作对象和结果。

5. 添加相关跳转链接，并确认目标页面能打开。
![wmx007](./img/wmx007.png)

## 6. 如何修改

1. 在文档网站找到你要修改的地方。(你现在在看的就是文档网站)
2. 在克隆仓库的根目录中打开 `mkdocs.yml`，根据文档网站上的页面名称查找对应的 `.md` 文件。
3. 打开对应的 `.md` 文件，在 Visual Studio Code 中修改。
4. 保存修改（`Ctrl+S`）。
5. 如果是添加文档，要在 `mkdocs.yml` 里对应的地方加入链接，或在其他 `.md` 文件加入跳转链接。

**在 `mkdocs.yml` 里对应的地方加入链接的格式：**

```yaml
- 标题: '.md文件路径(在docs之后的路径，docs不用写)'
```

例如：

```yaml
- 模拟器演示：涉水效果: 'introduction.md'
- 使用 VScode 推送代码: 'dev/vscode_push.md'
```

**在其他 `.md` 文件加入跳转链接格式：**

```markdown
[标题](.md文件路径)
```

（如果两个 `.md` 文件在同一个目录下，括号里直接写该文件名即可）
例如：

```markdown
[HoloOcean Windows 搭建教程](HoloOcean-Windows-Setup.md)
```

## 7. 预览成果

1. 下载 MkDocs（在命令行中运行以下命令下载）：
   ```bash
   pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin
   ```
   *（如果出现报错，可以将错误信息发给 AI 解决）*

2. 在终端 `cd` 到你的 `.github` 文件夹路径下（例如：`cd 你的路径/.github`），然后运行预览指令：
   ```bash
   mkdocs serve
   ```

3. 找到终端里输出的类似于 `http://127.0.0.1:8000/` 的网址，复制到浏览器中打开，预览你的修改成果。（检查界面是否出错、图片是否正常显示、跳转链接是否失效）。

### 填写网页链接

整理报告中的页面地址时，先在 PR 的 Files changed（文件变更）中确认源文件路径，再对照仓库根目录的 mkdocs.yml 导航查找对应页面。本地预览用于检查页面效果；填写报告时，打开已部署页面并确认内容，再复制他人能访问的网页地址，不要填写本地预览地址，也不要只按文件名拼网址。尚未部署的修改，或 README、脚本和配置文件等没有对应文档页的内容，填写具体的 GitHub 文件链接。

## 8. 提交

[提交流程](CONTRIBUTING.md)
