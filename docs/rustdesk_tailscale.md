# 远程办公解决方案：tailscale（免费）+rustdesk（开源）

## 1. 把多台机器放进同一个虚拟局域网

* [注册tailscale](https://login.tailscale.com/start)并在需要远程登录的机器上下载对应操作系统版本的[tailscale](https://tailscale.com/download/windows)进行安装。

 ![注册页面](./img/rustdesk/sign_up.png)

* 将本机加入到虚拟局域网中

 ![加入虚拟局域网](./img/rustdesk/sign_in_network.png)

 ![](./img/rustdesk/connect_device.png)

* 将设备添加到同一网络中（添加后就可以在[tailscale后台](https://console.tailscale.com/admin/machines)进行管理)。
可以将key设置成永久，防止过段时间需要重新登录）
 ![](./img/rustdesk/disable_key_expiry.png)

> 启动软件后会点击`sign in to your network`
![](./img/rustdesk/sign_in_network.png)

> 以 GitHub 授权使用为例
 ![](./img/rustdesk/sign_in_github.png)
 ![](./img/rustdesk/authorize_tailscale.png)

> 提示登录成功后，点击`visit the console`访问控制台，就可以看到已加入虚拟局域网的设备列表
![](./img/rustdesk/login_successful.png)


## 2. RustDesk配置与连接

* [下载](https://github.com/rustdesk/rustdesk/releases)并安装RustDesk客户端。

* 控制端/被控端：打开RustDesk，设置->解锁安全设置->勾选“允许IP直接访问”

![](./img/rustdesk/enable_IP.png)

输入被控端的 IP 地址即可远程登录（注意这里是 Tailscale IP，不是台式机的IP ）。

![](./img/rustdesk/rustdesk_control.png)

!!! 问题
    如果连接时报错：`连接错误 Failed to connect to 100.*.*.*:21118:请稍后再试`，确认被控端下面是否有“服务未运行”的提示，如果有请点击“启动服务”，然后再次连接即可。额外排查：确认被控端防火墙没有拦截 TCP 21118 端口。


## 附：Windows远程登录

先确认被控机的 Windows 版本：打开“设置 → 系统 → 系统信息”，查看 Windows 版本。Windows 专业版、企业版和教育版可以接受内置远程桌面连接；家庭版可以连接其他电脑，但不能作为这种连接的被控端。家庭版被控机可使用前面的 RustDesk 方式。

在支持的被控机上，打开“设置 → 系统 → 远程桌面”并启用连接。确认两台设备都已接入 Tailscale，且被控机保持开机、联网，没有进入睡眠状态。

 ![](./img/rustdesk/enable_remote.png)


在本地电脑打开`远程桌面连接`，输入被控机的 Tailscale IP 地址，再使用被控机上有远程登录权限的 Windows 账户和密码登录。这里使用账户密码，不是平时解锁电脑时输入的 Windows Hello PIN。图中的 `*` 需要替换为实际 IP 地址。
 ![](./img/rustdesk/win_remote.png)


!!! 注意
    如果使用 windows 这一步登录成功，前面第二步的“RustDesk配置与连接”就不再需要。如果是 Ubuntu、Mac、Android、iOS等其他平台，请查第二步的“RustDesk配置与连接”。


## 高级操作

### 邀请其他成员进入虚拟局域网

![](./img/rustdesk/invite_external_user.png)


服务器所在的是**个人 tailnet**，不能直接"加成员"，正规做法是**节点共享**。

**使用tailscale共享具体步骤**

**共享方操作**

1. 打开 [链接](https://login.tailscale.com/admin/machines)并在需要远程登录的机器上下载对应操作系统版本的[tailscale](https://tailscale.com/download/windows)进行安装。
2. 找到所需要的机器 **机器名（服务器ip地址）**，点右侧 **⋯（三个点）→ Share machine（共享设备）**
3. 在tailscale的设置页面选择Reusable link并点击Copy share link
  
   ![](./img/rustdesk/copylink.png)

**接收方操作**

1. 使用github账号登录并打开[链接](https://login.tailscale.com/admin/invitations)（或注册邮箱里的邀请邮件），**接受**这台共享设备
2. 接受后在 admin/machines 里即可看到该设备，用  服务器ip地址  访问
   
![](./img/rustdesk/Share%20successful.png)
## 参考
* [tailscale 源代码仓库](https://github.com/tailscale/tailscale) - [tailscale 开源介绍](https://tailscale.com/opensource)
* [rustdesk 源代码仓库](https://github.com/rustdesk/rustdesk)
* [微软：启用远程桌面的条件与设置](https://learn.microsoft.com/zh-cn/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access)
* [使用 Tailscale 实现内网穿透+RDP远程控制](https://www.cnblogs.com/lefour/p/18866579)



