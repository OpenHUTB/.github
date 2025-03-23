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

如果 [127.0.0.1:1080](127.0.0.1:1080) 能够访问，但是 [http://172.21.108.56:1080](http://172.21.108.56:1080) 不能访问，则需要关闭所有防火墙。

4.使用
执行命令克隆仓库（附带端口）：
```shell
git clone http://172.21.108.56:1080/root/actors
```

