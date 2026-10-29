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
```bash
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的 GitHub 注册邮箱"
```

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

> ⚠️ 重要规范：**不要直接在 master 主分支修改，所有改动新建独立分支操作**
创建分支的方法
```bash
git checkout -b 你的分支名
```
检查自己所在分支的方法
```bash
git branch
```
输出的所有分支里前面带 `*` 的就是目前所在分支

更换分支的方法
```bash
git checkout 你要选择的分支
```
建立分支修改文档的好处是不会污染本地仓库
## 四、准备仓库

1. 把仓库克隆到本地
```bash
git clone 仓库地址
```
2. VS Code 打开仓库文件夹
3. 新建工作分支（终端执行）
```bash
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

```bash
# 添加改动文件
git add 文件名
```

```bash
# 提交，引号内写本次改动描述
git commit -m "新增 VSCode 推送教程"
```
## 七、推送到远程 GitHub 仓库

### 方式 A VSCode 图形界面

提交完成后，源代码管理顶部会出现 **推送** 按钮，点击推送。

### 方式 B 终端命令
```bash
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

## 十、主仓库更新后同步当前工作分支

在已经克隆的个人 Fork 中，先确认当前工作分支；以下以 `你的分支名` 为例。提交或暂存正在编辑的文件后，再进行同步。

1. 关联主仓库(如果已经关联则不用重复关联)
```bash
git remote add upstream https://github.com/OpenHUTB/.github.git
```
查看是否成功关联的方法
```bash
git switch 你的分支名
git status
```

首次同步时，添加主仓库地址。已经有 `upstream` 的话，直接查看地址即可，无需重复添加。

```bash
git remote add upstream https://github.com/OpenHUTB/.github.git
git remote -v
git fetch upstream master
git merge upstream/master
```

`fetch` 只下载更新，`merge` 才会把主仓库的 `master` 合入当前工作分支。若出现冲突，在 VS Code 中检查冲突标记，保留需要的内容并保存文件；然后只暂存已解决的文件，并完成合并提交：

```bash
git add 路径/已解决的文件.md
git commit -m "合并主仓库更新并解决冲突 / merge upstream updates and resolve conflicts"
```

没有冲突时，Git 会直接完成合并，无需再运行上述 `git add` 和 `git commit`。最后确认工作区状态，并推送当前工作分支，随后在原有 PR 中查看更新：

```bash
git status
git push origin 你的分支名
```


## 推送失败时先确认分支关系

当 `git push` 被拒绝时，不要直接重复推送，可以先按下面顺序检查：

1. 运行 `git branch --show-current` 确认当前分支。
2. 运行 `git status` 查看是否有未提交文件，并确认工作区状态。
3. 运行 `git remote -v` 核对推送目标是否为自己的 fork。
4. 如果远程已有新提交，先获取更新并处理差异，再重新推送。
5. 推送成功后，在 GitHub 的分支页面核对最新提交和改动文件。

这些检查可以区分分支选错、远程地址错误和远程分支已更新等不同情况。
