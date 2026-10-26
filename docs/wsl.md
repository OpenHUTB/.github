# 安装 WSL（Ubuntu 20.04）

## 1. 一键安装（推荐）

前提：Windows 10 版本 2004+ 或 Windows 11。

 打开「控制面板 → 程序 → 启用或关闭 Windows 功能」，勾选「适用于 Linux 的 Windows 子系统」和「虚拟机平台」两项，点击「确定」，完成后按提示重启电脑。 
    ![图片](img/wmx001.png)

打开cmd

按'win+R'输入'cmd'

执行安装命令

```powershell
wsl --install -d Ubuntu-20.04
```
其中 `Ubuntu-20.04` 里的 `20.04` 是发行版版本号，可按需替换；该命令需要下载并安装完整系统，耗时较长。

设置 Linux 用户名和密码。

注意：密码输入时不显示任何字符，盲打回车即可

安装后更新软件源

```bash
sudo apt update && sudo apt upgrade
```

## 2. 删除 WSL

### 1. 彻底清除 WSL
第一步：注销所有发行版。先用 `wsl --list --verbose`（可简写为 `wsl -l -v`）查看已安装的发行版名称，再逐个注销：

```powershell
wsl --unregister <发行版名>
```

第二步：卸载 WSL 组件

```powershell
wsl --uninstall
```
注意：wsl --uninstall 需要 Microsoft Store 版 WSL 2.0 及以上。如果提示没有该命令，可在「设置 → 应用 → 安装的应用」中先卸载对应的 Linux 发行版，再卸载「适用于 Linux 的 Windows 子系统」组件，然后重启电脑。