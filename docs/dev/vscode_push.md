# VS Code 安装 + 使用 VSCode 推送代码（Git 提交 + Push 完整教程）

[TOC]

## 一、环境准备：安装 Git（Windows）

> VS Code 本身不带 Git，必须先装 Git，才能提交推送代码。

### 1. 下载 Git

官网地址：[https://git-scm.com/download/win](https://git-scm.com/download/win)
下载 Windows 版本安装包。

### 2. 安装要点

1. 双击打开安装包，一路下一步，**到调整 PATH 这一步，选择 Git from the command line and also from 3rd-party software**（最重要！把 Git 加入系统环境变量）
2. 其余选项保持默认，直接下一步完成安装。

### 3. 配置 Git 用户名与邮箱（必须设置，否则提交报错）

打开 PowerShell，执行下面两行，替换成你自己 GitHub 的用户名和注册邮箱
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的 GitHub 注册邮箱"

### 4. 验证 Git 是否装好

打开 PowerShell，输入：
```
git --version
```
输出版本号即代表安装成功。
## 二、VS Code 安装（Windows）

### 1. 下载安装包

访问官网：[https://code.visualstudio.com/](https://code.visualstudio.com/)
点击页面蓝色的 **Download for Windows**，下载 Windows 安装程序。

> 
> 提示：优先官网下载，不要从第三方软件站下载，避免捆绑软件。

### 2. 安装步骤

1. 双击下载好的 `.exe` 安装包，同意许可协议，点击下一步
2. 选择安装位置（建议不要放在 C 盘很深的中文路径）
3. **勾选这几个选项（非常重要）**

- ✅ 添加到 PATH（环境变量）
- ✅ 在资源管理器右键菜单中，通过 Code 打开
- ✅ 将 Code 注册为受支持文件的编辑器

4. 一路下一步，点击安装。

### 3. 安装必要插件

打开 VS Code，左侧扩展栏（方块图标），搜索并安装：

1. Chinese (Simplified) Language Pack —— 中文语言包（可选，适合不习惯英文界面）

## 三、前置说明

本教程演示：在 VS Code 内完成 Git 提交、推送到 GitHub 的完整流程，适用于 OpenHUTB 文档仓库贡献。

> 
> ⚠️ 重要规范：**不要直接在 master 主分支修改，所有改动新建独立分支操作**

## 四、准备仓库

1. 把仓库克隆到本地
```
git clone 仓库地址
```
2. VS Code 打开仓库文件夹
3. 新建工作分支（终端执行）
```
git checkout -b 你的分支名
```
## 五、在 VS Code 内修改文件

编辑你的 Markdown / 代码文件，修改完成记得 `Ctrl+S` 保存。

## 六、提交改动（两种方式任选其一）

### 方式 A：VSCode 图形界面（推荐新手）

1. 左侧点击【源代码管理】图标（分支圆圈图标）
2. 在「更改」列表，找到修改的文件，点文件旁边 `+`，暂存更改
3. 在上方输入提交信息，简单写清楚本次修改内容
4. 点击【提交】

### 方式 B：终端命令

# 添加改动文件
```
git add 文件名
```
# 提交，引号内写本次改动描述
```
git commit -m "新增 VSCode 推送教程"
```
## 七、推送到远程 GitHub 仓库

### 方式 A VSCode 图形界面

提交完成后，源代码管理顶部会出现 **推送** 按钮，点击推送。

### 方式 B 终端命令
```
git push origin 你的分支名
```
## 八、提交 PR（Pull Request）

推送成功后，打开仓库 GitHub 网页

1. 页面弹出 `Compare & pull request`，点击
2. 填写 PR 标题和描述，说明本次改动内容
3. 点击 `Create pull request` 创建 PR
4. 等待维护人员审核，审核通过合并，内容就正式上线网站

## 九、常见踩坑

1. VS Code 找不到 Git：Git 未安装，或者安装时没有勾选添加到 PATH 环境变量
2. 提交报错缺少身份：没有配置 user.name 和 user.email
3. 推送失败：网络问题，或者仓库权限不足；确认分支名称正确
4. mkdocs 网页找不到页面：检查 mkdocs.yml 的路径和 md 文件位置完全匹配
5. 代码冲突：多人同时修改同一文件会出现冲突，解决冲突后再提交

## 十、当主仓库有更新导致有冲突时的解决办法

1. 关联主仓库(如果已经关联则不用重复关联)
```bash
git remote add upstream
你需要关联的仓库地址eg：htpps://github.com/OpenHUTB/.github.git
```
查看是否成功关联的方法
```bash
git remote -v
```
此时能看到origin和upstream即为成功

2. 拉取主仓库最新代码再手动解决冲突
```bash
git fetch upstream master
```
如果出现冲突，手动解决冲突
```bash
git add .
git commit -m "merge upstream and resolve conflicts"
```
当这个 commit 成功后，本地的合并过程就彻底完成了。此时你本地的 master 分支已经包含了主仓库的最新代码以及你解决冲突后的最终结果

3. 把同步好的master推送到自己的fork仓库(origin)
```bash
git push origin master
```
