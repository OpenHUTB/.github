# 搭建自定义开发环境

## 搭建自己的gitlab仓库
参考[链接](https://blog.csdn.net/weixin_41878425/article/details/134995223) 进行配置：
1. 在盘符(任意盘符)中新建docker文件夹，在docker文件夹中建立gitlab文件夹，在gitlab文件夹中建立config、data、logs三个文件夹 ，如下关系所示：
    ```text
    docker
        |-gitlab
            |-config
            |-data
            |-logs
        |-docker-compose.yml
    ```

2. 在第1步中新建的docker文件夹中新建文件：docker-compose.yml，内容如下：
    ```yaml
    version: '3' # 版本号
    services: # 开启服务
      gitlab: # 服务名称
        image: 'twang2218/gitlab-ce-zh:latest' # 使用镜像
        restart: always
        hostname: 'GitLab' # 主机名称（自定义）
        environment: # 环境配置
          TZ: 'Asia/Shanghai'
          GITLAB_OMNIBUS_CONFIG: |
            external_url 'http://172.21.108.56'
            gitlab_rails['gitlab_shell_ssh_port'] = 1022
            unicorn['port'] = 8888
            nginx['listen_port'] = 8080
        ports: # 端口映射，格式为“本机IP：Docker镜像内部IP”
          - '1080:8080'    #http
          - '1043:1443'    #https
          - '1022:22'      #ssh
        volumes: # 挂载卷
        # 前面是Windows的地址所以斜杠向右；后面是Linux的地址所以向左
          - C:\docker\gitlab\config:/etc/gitlab
          - C:\docker\gitlab\data:/var/opt/gitlab
          - C:\docker\gitlab\logs:/var/log/gitlab
    ```
3. 执行docker-compose.yml文件完成服务器部署
    ```shell
    docker-compose up -d
    ```
修改配置后，执行重启命令：
    ```shell
    docker-compose restart
    ```

如果本机可以访问 [http://127.0.0.1:1080](http://127.0.0.1:1080)，但局域网内其他设备无法访问 [http://172.21.108.56:1080](http://172.21.108.56:1080)，可以依次检查：

1. 在 `docker-compose.yml` 所在目录运行 `docker-compose ps`，确认 GitLab 容器正在运行，并检查端口绑定。例如，`0.0.0.0:1080->8080/tcp` 表示该端口对所有 IPv4 网卡开放；如果仅绑定到 `127.0.0.1`，其他设备就无法通过局域网地址访问。使用新版 Compose 时，命令为 `docker compose ps`。
2. 在服务器上运行 `Test-NetConnection 127.0.0.1 -Port 1080`，确认本机端口可以连接。
3. 在局域网内另一台 Windows 设备上运行 `Test-NetConnection 172.21.108.56 -Port 1080`，检查远程端口是否可达。
4. 如果远程端口不通，在 Windows Defender 防火墙中为 TCP 1080 添加入站规则，并把规则限制在需要访问的网络范围内。

不建议关闭所有防火墙。端口映射或规则配置错误时，关闭防火墙不能解决根本问题，还会让其他服务失去保护。排查完成后，再用实际服务器地址替换示例中的 `172.21.108.56`。

4. 使用
   执行命令克隆仓库（附带端口）：
    ```shell
    git clone http://172.21.108.56:1080/root/actors
    ```



## 配置 Python 开发环境（Windows）

社区里人车模拟器的 Python 接口，以及各类算法实验，都在 Python 环境下运行。本节从零开始：装 Python → 配镜像源 → 建虚拟环境 → 在 VS Code 里选中它。全部以 Windows 为例。

### 1. 安装 Python

1. 打开 [Python 官方下载页](https://www.python.org/downloads/windows/) ，选择 Python 3.13 的 `Windows installer (64-bit)` 下载。如果项目文档明确要求某个版本，以项目要求为准，不要随意换版本。
2. 运行安装程序，**先勾选 `Add python.exe to PATH`**，再点 `Install Now`。这一步漏勾，后面所有命令都会提示「不是内部或外部命令」，这是新手最常见的第一个坑。
3. 安装结束后，**重新打开一个**终端窗口（已经打开的窗口不会刷新环境变量），执行：

```shell
python --version
python -m pip --version
```

两条命令都能输出版本号，说明装好了。

### 2. 看清电脑上有几个 Python

一台机器上经常不止一个 Python：系统装的、某些编辑器自带的、Anaconda 的……混用会导致「明明装了包却导入不了」。Windows 自带的 Python 启动器可以把它们列出来：

```shell
py --list
```

输出中带 `*` 的是默认版本。需要指定版本运行时用 `py -3.13 脚本名.py` 这样的写法。更多说明可参考 Python 官方文档：

- [Python Launcher for Windows](https://docs.python.org/3.13/using/windows.html#python-launcher-for-windows)

**装包时统一用 `python -m pip install 包名`，而不是直接 `pip install 包名`**。前者保证包被装进当前 `python` 对应的环境，后者可能装到另一个 Python 上。

### 3. 为 pip 配置国内镜像源

直接从官方源下载常常很慢甚至超时。配置清华镜像源（写进用户配置，一次生效、长期有效）：

```shell
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

确认是否生效：

```shell
python -m pip config list
```

输出中出现 `global.index-url='https://pypi.tuna.tsinghua.edu.cn/simple'` 即为成功。

### 4. 建立虚拟环境

虚拟环境是项目专属的一份独立 Python，各项目的依赖互不干扰。**每个项目建一个，这是必须的习惯，不是可选优化**——直接在系统 Python 上装包，早晚会遇到两个项目要求同一个库的不同版本。

进入项目目录，创建名为 `.venv` 的环境：

```shell
cd 你的项目目录
python -m venv .venv
```

激活它。不同终端用的命令不一样，请按自己当前打开的终端选择：

```powershell
# PowerShell
.venv\Scripts\Activate.ps1
```

```cmd
# cmd
.venv\Scripts\activate.bat
```

```shell
# Git Bash
source .venv/Scripts/activate
```

不同 Shell 激活虚拟环境的方式可参考 Python 官方文档：[How virtual environments work](https://docs.python.org/3.13/library/venv.html#how-venvs-work)


激活成功后，命令行开头会出现 `(.venv)`。此后 `python`、`pip` 都指向这个环境。退出用：

```shell
deactivate
```

如果 PowerShell 提示「无法加载文件……因为在此系统上禁止运行脚本」，先执行下面这条命令（只对当前用户生效，不需要管理员权限）：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

按提示输入 `Y` 确认，再重新激活。

### 5. 在 VS Code 里选中这个环境

1. 在 VS Code 扩展商店安装 **Python** 扩展（搜索 `Python`，发布者为 Microsoft）。
2. 按 `Ctrl+Shift+P`，输入 `Python: Select Interpreter`，选择路径中带 `.venv` 的那一项。
3. 新建终端（菜单「终端 → 新建终端」）会自动激活虚拟环境，命令行前同样出现 `(.venv)`。**这一步不做，VS Code 仍会用系统 Python 运行代码**，于是出现「终端里 import 成功、点运行却报错」这类看似玄学的问题。

### 6. 安装常用库并验证

以数据科学常用的一套为例，按需增删：

```shell
python -m pip install numpy pandas scikit-learn matplotlib jupyter
```

装完验证能否导入：

```shell
python -c "import numpy, pandas, sklearn, matplotlib; print('ok')"
```

输出 `ok` 即完成。

### 7. 常见问题速查表

| 现象 | 原因 | 处理 |
|------|------|------|
| `'python' 不是内部或外部命令` | 安装时未勾选 Add to PATH | 重新运行安装包 → `Modify` → 补勾该项，或卸载重装 |
| 装包时报 `PermissionError` / 拒绝访问 | 正在往系统 Python 里装 | 改用虚拟环境（第 4 步），或加 `--user` 参数 |
| pip 下载极慢或 `Read timed out` | 连的是境外官方源 | 配置镜像源（第 3 步） |
| PowerShell 提示禁止运行脚本 | 执行策略限制 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 终端能 import，VS Code 运行却报 `ModuleNotFoundError` | 编辑器选中的解释器不是装包的那个 | `Ctrl+Shift+P` → `Python: Select Interpreter` 改选 `.venv` |
| `python -m venv` 报 ensurepip 失败 | Python 安装不完整 | 重新运行安装包修复；Linux 上需先 `apt install python3-venv` |
| pip 提示版本过旧 | 安装包自带的 pip 较老 | `python -m pip install --upgrade pip` |