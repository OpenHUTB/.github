# 搭建自定义开发环境

## 搭建自己的gitlab仓库
参考[链接](https://blog.csdn.net/weixin_41878425/article/details/134995223) 进行配置：
1.在盘符(任意盘符)中新建docker文件夹，在docker文件夹中建立gitlab文件夹，在gitlab文件夹中建立config、data、logs三个文件夹 ，如下关系所示：
```text
docker
    |-gitlab
        |-config
        |-data
        |-logs
    |-docker-compose.yml
```

2.在第1步中新建的docker文件中新建文件：docker-compose.yml，内容如下：
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
3.执行docker-compose.yml文件完成服务器部署
```shell
docker-compose up -d 
```
修改配置后，执行重启命令：
```shell
docker-compose restart
```

如果本机可以访问 [http://127.0.0.1:1080](http://127.0.0.1:1080)，但局域网内其他设备无法访问 [http://172.21.108.56:1080](http://172.21.108.56:1080)，可以依次检查：

1. 使用 `docker compose ps` 确认 GitLab 容器正在运行，并且端口显示为 `0.0.0.0:1080->8080/tcp`，而不是只绑定到 `127.0.0.1`。
2. 在服务器上运行 `Test-NetConnection 127.0.0.1 -Port 1080`，确认本机端口可以连接。
3. 在局域网内另一台 Windows 设备上运行 `Test-NetConnection 172.21.108.56 -Port 1080`，检查远程端口是否可达。
4. 如果远程端口不通，在 Windows Defender 防火墙中为 TCP 1080 添加入站规则，并把规则限制在需要访问的网络范围内。

不建议关闭所有防火墙。端口映射或规则配置错误时，关闭防火墙不能解决根本问题，还会让其他服务失去保护。排查完成后，再用实际服务器地址替换示例中的 `172.21.108.56`。

4.使用
执行命令克隆仓库（附带端口）：
```shell
git clone http://172.21.108.56:1080/root/actors
```

