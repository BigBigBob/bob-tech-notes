### 一、核心概念与架构

 Docker 中最常见的几个对象：

- **镜像（Image）**：只读、分层的应用交付模板，包含运行应用所需的文件系统、运行时和默认配置。一个镜像可以创建多个容器。
- **容器（Container）**：镜像的一个运行实例，拥有独立的进程、网络和可写层。容器本身应尽量无状态、可随时重建。
- **镜像仓库（Registry）**：存储与分发镜像的服务，例如 Docker Hub、企业 Harbor 或自建 Registry。
- **数据卷（Volume）**：由 Docker 管理的持久化数据；容器删除后数据仍可保留。

- **镜像分层与容器可写层** ：镜像通常使用 OverlayFS 等联合挂载机制实现分层复用：镜像层只读，容器启动时在顶部添加一个可写层（copy-on-write）。容器可写层随容器删除而消失，因此数据库、上传文件、日志等需要持久化的数据应写入 Volume、绑定挂载或外部存储，而非容器文件系统。



### 二、安装 Docker

#### 1. 选择平台

- **Windows / macOS 本地开发**：优先使用 Docker Desktop，并启用 WSL 2（Windows）或默认虚拟化后端。
- **Linux 服务器**：安装 Docker Engine。


#### 2. Ubuntu24 安装 Docker 示例

```bash
# 1. 更新软件包索引并安装必要工具
sudo apt update
sudo apt install -y ca-certificates curl

# 2. 添加 Docker 官方 GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. 添加 Docker 官方 apt 软件源
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# 4. 安装 Docker Engine、CLI、containerd、Buildx 和 Compose 插件
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# 5. 查看 Docker 服务状态并运行测试容器
sudo systemctl status docker --no-pager
sudo docker run --rm hello-world
```



### 三、常用命令

#### 1. 查看状态与资源

```bash
# Docker 环境与服务端状态
docker version                     # 查看 Client / Server 版本；Server 不可达时会显示连接错误
docker info                        # 查看 Engine、容器数量、存储驱动、网络、运行时等总体信息

# Docker 对象列表
docker ps                          # 仅列出正在运行的容器
docker ps -a                       # 列出全部容器，包括已退出和已创建但未启动的容器
docker image ls                    # 列出本地镜像（docker images 的现代同义写法）
docker volume ls                   # 列出 Docker 管理的数据卷
docker network ls                  # 列出 Docker 网络

# 单个容器的运行状态与排障信息；将 web 替换为容器名或容器 ID
docker stats                       # 实时显示所有运行中容器的 CPU、内存、网络和块 I/O；Ctrl+C 退出
docker stats --no-stream web       # 只采集一次指定容器的资源使用情况，便于脚本或快速检查
docker top web                     # 查看指定容器内正在运行的进程
docker inspect web                 # 查看容器配置、状态、挂载、网络等完整 JSON 信息
docker logs --tail 100 web         # 查看容器最近 100 行标准输出和标准错误日志
docker port web                    # 查看容器端口到宿主机端口的映射

# Docker 磁盘占用
docker system df                   # 汇总镜像、容器、数据卷和构建缓存的磁盘占用
docker system df -v                # 显示每个对象的详细磁盘占用，输出可能较长
```

#### 2. 镜像

```bash
# 获取与列出镜像
docker pull nginx:1.28                         # 从镜像仓库拉取明确版本，避免生产环境依赖会变化的 latest
docker image ls                                # 列出本地镜像、标签、镜像 ID、创建时间和占用空间

# 查看镜像详情；将 nginx:1.28 替换为镜像名:标签、摘要或镜像 ID
docker image inspect nginx:1.28                # 以 JSON 查看入口命令、环境变量、架构、层等完整元数据

# 标记与删除镜像
docker image rm nginx:1.28                     # 删除未被容器引用的镜像；正在使用时会拒绝删除
docker image prune                             # 删除悬空镜像，执行前会要求确认
```

#### 3. 创建、运行与停止容器

```bash
# 创建并立即启动一个后台容器
# -d 后台运行；--name 指定容器名；--restart 设置 Docker 重启后的恢复策略
# -p 的顺序是“宿主机地址:宿主机端口:容器端口”,127.0.0.1 表示限制只允许本机访问
docker run -d --name web --restart unless-stopped \
  -p 127.0.0.1:8080:80 \
  nginx:1.28

# 启动一个临时交互式容器；退出后自动删除，适合测试和排障
docker run --rm -it alpine:3.22 sh

# 查看日志和进入运行中的容器
docker logs --tail 100 -f web       # 先显示最近 100 行并持续跟踪；Ctrl+C 退出
docker exec -it web sh              # 在运行中的容器内启动 shell

# 停止、重启
docker stop web                      # 停止容器
docker start web                     # 启动容器
docker restart web                   # 重启容器

# 删除
docker rm web                       # 删除已停止的容器；运行中的容器会拒绝删除
docker rm -f web                    # 强制终止并删除运行中的容器，可能造成未完成写入
```

- `docker run` 相当于先 `docker create` 再 `docker start`，每执行一次都会**新建**容器；已有容器应使用 `docker start` 或 `docker restart`。

- -p 和 -P 都用于把容器端口发布到宿主机，但控制方式不同

  - -p：手动指定端口映射。完整的格式是：-p [宿主机IP:]宿主机端口:容器端口
  - -P：随机发布所有声明端口
  - 常开发和生产部署通常优先使用 `-p`；`-P` 更适合临时测试。

  

#### 4. 复制、导出与导入

```bash
# 在宿主机与容器之间复制文件
docker cp web:/usr/share/nginx/html/index.html ./index.html  # 从容器复制单个文件到宿主机的当前目录
docker cp ./nginx.conf web:/tmp/nginx.conf      # 从宿主机复制文件到容器的 /tmp 目录

docker cp web:/etc/nginx ./backup/     # 复制 nginx 整个目录，保留 nginx 这一层
docker cp web:/etc/nginx/. ./backup/    # 只复制 nginx 目录里面的内容，不保留 nginx 这一层

# export 导出容器根文件系统的扁平快照，不包含数据卷内容、镜像分层历史和容器运行配置
docker container export --output web-rootfs.tar web

# import 从根文件系统归档创建一个新镜像；它不会恢复原镜像的 CMD、ENTRYPOINT、ENV 等配置
docker image import web-rootfs.tar example/web-rootfs:backup

# 若目的是完整迁移镜像，应使用 save/load：它们会保留镜像层、标签和镜像配置
docker image save --output nginx_1.28.tar nginx:1.28
docker image load --input nginx_1.28.tar
```

| 命令组合 | 操作对象 | 保留内容 | 适用场景 |
| --- | --- | --- | --- |
| `docker cp` | 单个文件或目录 | 文件内容，权限尽量保留 | 临时取日志、复制配置或排障文件 |
| `docker export/import` | 容器根文件系统 | 扁平化后的文件系统 | 制作临时根文件系统快照；不适合作为标准镜像交付方式 |
| `docker save/load` | Docker 镜像 | 镜像层、标签和镜像配置 | 离线迁移或归档镜像 |



### 四、数据持久化与挂载

容器的可写层与容器生命周期绑定：停止、重启容器时数据仍在，但删除容器后可写层也会被删除。因此，数据库文件、用户上传内容等重要数据必须放在 Volume、绑定挂载或外部存储中，而不能只写入容器文件系统。

#### 1. 三种挂载方式如何选择

| 类型 | 数据位置与管理者 | 适用场景 | 主要特点 |
| --- | --- | --- | --- |
| 命名 Volume | Docker 管理 | 数据库、应用持久化数据 | 默认首选；不依赖固定宿主机路径，便于复用、检查和迁移。 |
| Bind mount | 指定的宿主机文件或目录 | 本地源码、配置文件、已有数据目录 | 内容对宿主机直接可见，但依赖主机路径、权限和安全策略。 |
| tmpfs | 宿主机内存 | 临时缓存、短期敏感文件 | 不写入磁盘，容器停止后内容消失；仅适用于 Linux 容器。 |

`--mount` 参数含义更明确，复杂挂载优先使用；`-v`/`--volume` 写法更短，仍然受支持。容器内的目标路径必须使用绝对路径。

#### 2. 使用命名 Volume 保存数据库数据

```bash
# 创建并查看命名卷
docker volume create mysql-data
docker volume inspect mysql-data

# 将 MySQL 数据目录挂载到命名卷
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4
  
# 或者我们也可以使用 -v 的简写方式，但其实官方更推荐 --mount，因为语义更加明确
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  -v mysql-data:/var/lib/mysql \
  mysql:8.4

# 确认容器实际使用的挂载
docker inspect mysql --format '{{json .Mounts}}'
```

删除容器不会自动删除这里显式创建的 `mysql-data`。只要重新挂载同一个卷，新容器就能继续读取原数据：

```bash
docker stop mysql
docker rm mysql

docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4
```

重新挂载已有 MySQL 数据卷时，`MYSQL_ROOT_PASSWORD` 不会重置数据库中已经存在的 root 密码；这类初始化变量通常只在数据目录为空时生效。

Volume 的生命周期独立于容器，但并非不会丢失。`docker volume rm mysql-data`、`docker compose down -v` 和带 `--volumes` 的清理命令都可能删除数据卷；执行前必须确认备份和目标范围。不要直接修改 Docker 内部存储目录（通常位于 `/var/lib/docker`）。

#### 3. 使用 Bind mount 挂载配置或源码

```bash
# 当前目录必须已经存在 nginx.conf
docker run --rm \
  --mount type=bind,src="/opt/nginx/nginx.conf",dst=/etc/nginx/nginx.conf \
  nginx:1.28
```

使用 `--mount type=bind` 时，源路径不存在会直接报错，能避免把拼错的文件路径意外创建成目录。生产环境应尽量使用绝对路径和只读挂载。Bind mount 强依赖宿主机目录结构，迁移到另一台机器时需要同步复制对应文件。



### 五、Dockerfile 与镜像构建

#### 1. 基本规则

Dockerfile 是镜像的可复现构建清单。`docker build` 按顺序解析指令，每条会形成可缓存的构建结果；最终得到镜像，而不是直接得到正在运行的容器。

```text
源码与依赖描述
      │
      ▼
构建上下文 + Dockerfile
      │ docker build
      ▼
只读镜像 ── docker run ──> 带可写层的容器
```

`docker build -f docker/Dockerfile .` 中最后的 `.` 才是构建上下文。`COPY` 和 `ADD` 只能读取上下文内、且未被 `.dockerignore` 排除的文件。



#### 2. 常用指令

| 指令 | 用途与要点 |
| --- | --- |
| `FROM` | 开始一个构建阶段并指定基础镜像；多阶段构建可以出现多次。生产环境应固定明确版本，必要时固定 digest。 |
| `ARG` | 声明构建期变量，只在其作用域内参与构建；不是安全的密钥传递方式。 |
| `WORKDIR` | 设置后续 `RUN`、`COPY`、`CMD` 等指令的工作目录；优先于反复使用 `cd`。 |
| `COPY` | 从构建上下文或其他构建阶段复制文件；可使用 `--from`、`--chown` 和 `--chmod`。普通复制优先使用它。 |
| `ADD` | 额外支持本地 tar 自动解压和远程源等语义；只有明确需要这些能力时再使用，避免隐式行为。 |
| `RUN` | 在构建期执行命令并产生镜像层；可配合 `RUN --mount=type=cache` 或 `type=secret` 使用临时挂载。 |
| `ENV` | 设置镜像和容器中的持久环境变量；适合非敏感默认值，不存放密码或 Token。 |
| `USER` | 设置后续构建步骤及容器启动时使用的用户和组。 |
| `EXPOSE` | 记录应用预期监听的容器端口，仅是元数据；不会像 `docker run -p` 一样发布端口。 |
| `CMD` | 提供默认命令或默认参数；Dockerfile 中只有最后一条生效，可被 `docker run IMAGE ...` 覆盖。 |
| `ENTRYPOINT` | 定义容器入口程序；exec 形式与 `CMD` 组合时，`CMD` 通常提供可覆盖的默认参数。 |
| `HEALTHCHECK` | 声明应用健康检查，便于编排工具判断服务状态。 |
| `LABEL` | 写入版本、源码地址、许可证等 OCI 镜像元数据；`MAINTAINER` 已废弃。 |



#### 3. 简单 Java 应用示例

假设已经有一个 Maven + Spring Boot 项目，并且在宿主机或 CI 中执行 `mvn clean package` 生成了 `target/my-service.jar`：

```text
my-service/
├── Dockerfile
├── pom.xml
├── src/
└── target/
    └── my-service.jar
```

项目根目录中的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jre

WORKDIR /app
COPY target/my-service.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

这个 Dockerfile 只有一个构建阶段：

- `FROM` 提供运行 Java 21 应用所需的 JRE。
- `WORKDIR` 把容器内的工作目录设置为 `/app`。
- `COPY` 把宿主机已经构建好的 JAR 复制进镜像；JAR 文件名需要与实际构建结果一致。
- `EXPOSE 8080` 记录应用预期监听的端口，但不会自动把端口发布到宿主机。
- `ENTRYPOINT` 让容器启动时执行 `java -jar /app/app.jar`。



#### 4. 构建、检查与运行验证

```bash
# 先在宿主机生成 target/my-service.jar
mvn clean package -DskipTests

# 再构建镜像；最后的点表示当前目录是构建上下文
docker build --pull -t example/my-service:1.0.0 .

# 查看镜像大小、入口程序、默认参数和运行用户
docker image ls example/my-service:1.0.0
docker image inspect example/my-service:1.0.0 \
  --format 'user={{.Config.User}} entrypoint={{json .Config.Entrypoint}} cmd={{json .Config.Cmd}}'

# 前台试运行；Ctrl+C 后容器会停止并自动删除
docker run --rm -p 8080:8080 example/my-service:1.0.0
```



### 六、网络

#### 1. 容器网络的基本模型

在 Linux 上，每个普通容器拥有独立的网络命名空间，包括自己的网卡、IP 地址、路由表、端口和 DNS 配置。使用 bridge 网络时，Docker 通常通过虚拟网卡把容器接入宿主机上的软件网桥，并通过转发/NAT 访问外部网络。

```text
同一 Docker 主机

外部客户端
    │ 访问宿主机IP:8080
    ▼
宿主机端口 8080 ──端口发布──> app:8080
                                │
                         自定义 bridge 网络
                                │ 使用服务名 db:3306
                                ▼
                             db:3306

app ──NAT/路由──> 宿主机网卡 ──> 外部网络
```

需要牢记三个边界：

- 容器内的 `127.0.0.1` 或 `localhost` 指向**当前容器自身**，不是宿主机，也不是其他容器。

- 同一自定义网络中的容器直接使用“容器名或网络别名 + 容器端口”通信，不需要把端口发布到宿主机。

  

#### 2. 常见网络模式

| 模式 | 说明 |
| --- | --- |
| `bridge` | 单机 Docker 最常用的驱动。自定义 bridge 提供容器名 DNS、网络隔离和端口发布。 |
| `host` | 容器直接共享宿主机网络命名空间，没有独立容器 IP；`-p` 会失去意义，并可能产生端口冲突。主要用于特定 Linux 场景。 |
| `none` | 除回环接口外不配置网络，适合不应进行网络通信的离线任务。 |
| `container:<name-or-id>` | 与指定容器共享同一个网络命名空间和端口空间，适合少数紧耦合 sidecar 场景。 |
| `overlay` | 连接多个 Docker daemon 的多主机网络，通常配合 Swarm；普通单机 bridge 不能直接跨主机。 |
| `macvlan` / `ipvlan` | 让容器更直接地接入物理网络或 VLAN；对交换机、网段和路由有额外要求，不作为普通应用默认选择。 |

如果 `docker run` 没有指定 `--network`，Linux 容器通常接入默认 `bridge`。实际应用应优先创建**自定义 bridge 网络**：它支持自动 DNS 解析，隔离范围也比所有容器共用默认 bridge 更清晰。旧的 `--link` 方式已经不推荐。

#### 3. 自定义 bridge 与容器 DNS

```bash
# 创建自定义 bridge 网络
docker network create app-net

# redis 自动获得该网络中的 IP 和 DNS 名称 redis
docker run -d --name redis --network app-net redis:7.4

# 临时客户端加入同一网络，通过名称 redis 和容器端口 6379 访问
docker run --rm --network app-net redis:7.4 redis-cli -h redis ping
# 返回 PONG；这里的 redis 是容器名，同时也是 DNS 名称

# 查看网络的驱动、网段、网关和已连接容器
docker network inspect app-net

# 运行中的容器也可以动态加入或离开自定义网络
docker run -d --name toolbox alpine:3.22 sleep 1d
docker network connect app-net toolbox
docker network disconnect app-net toolbox

# 网络仍被容器占用时无法删除
docker rm -f redis toolbox
docker network rm app-net
```

Docker 内置 DNS 会把同一自定义网络中的容器名或网络别名解析成当前容器 IP。容器重建后 IP 可能改变，但名称可以保持不变，因此应用配置应写 `redis:6379`、`db:3306`，不要固定某个 `172.x.x.x` 地址。

#### 4. 端口发布：`EXPOSE`、`-p` 与 `-P`

`EXPOSE` 只是镜像元数据，用于说明应用预期监听的容器端口；真正允许宿主机或外部客户端进入容器，需要在运行时使用 `-p`/`--publish`。

```bash
# 仅允许宿主机本地访问：宿主机 8080 -> 容器 8080
docker run -d --name app-local \
  -p 127.0.0.1:8080:8080 \
  example/my-service:1.0.0

# 未指定宿主机 IP，通常会绑定所有宿主机地址，暴露范围更大
docker run -d --name app-public \
  -p 8081:8080 \
  example/my-service:1.0.0

# 随机发布镜像中声明的所有 EXPOSE 端口，再查询实际映射
# Docker会读取镜像的Expose 8080，随机选择一个宿主机端口
docker run -d --name app-random -P example/my-service:1.0.0
docker port app-random
```

`-p` 的顺序是：

```text
-p [宿主机IP:]宿主机端口:容器端口[/协议]
```

端口发布也不等于已经配置好防火墙、云安全组、TLS 或身份认证。

#### 5. 常见通信路径

| 访问方向 | 推荐地址 | 是否需要 `-p` |
| --- | --- | --- |
| 同一自定义网络：app 访问 db | `db:3306` | 不需要 |
| 宿主机访问 app | `127.0.0.1:8080` 或宿主机 IP + 已发布端口 | 需要 |
| 外部客户端访问 app | 域名/宿主机 IP + 已发布端口，通常再经过反向代理 | 需要 |
| 容器访问互联网 | 目标域名或 IP | 默认 bridge 通常可直接出站 |
| 不同 Docker 主机上的容器互访 | 负载均衡入口、路由、Swarm overlay 或其他编排网络 | 单机 bridge 不适用 |

#### 6. 网络隔离与生产边界

一个容器可以同时连接多个网络。例如前端连接 `frontend-net` 和 `backend-net`，数据库只连接 `backend-net`，从而减少不必要的网络可达范围。还可以使用 `--internal` 创建默认不对外路由的内部网络：

```bash
docker network create frontend-net
docker network create --internal backend-net

docker run -d --name cache --network backend-net redis:7.4
docker run -d --name app --network frontend-net example/my-service:1.0.0
docker network connect backend-net app

# 清理本示例
docker rm -f app cache
docker network rm frontend-net backend-net
```

#### 7. 常用排障命令

```bash
# 查看网络和容器连接关系
docker network ls
docker network inspect app-net
docker inspect app --format '{{json .NetworkSettings.Networks}}'

# 查看发布到宿主机的端口
docker port app
```



### 七、Docker Compose（容器编排）

Docker Compose V1 的独立命令 `docker-compose` 已是 Legacy。当前优先使用 Compose 插件，命令为 **`docker compose`**（中间空格）。以下命令应在 `compose.yaml` 所在目录执行；其中 `app`、`db` 是 Compose 文件中的服务名：

```bash
# 查看 Compose 插件版本，确认使用的是 docker compose（V2）
docker compose version

# 拉取 db 服务引用的远程镜像；不会启动容器
docker compose pull db

# 创建并启动Compose文件中的所有服务
docker compose up -d

# 查看本项目全部容器，包括已经退出的容器
docker compose ps --all

# 先显示 app 最近 100 行日志，再持续跟踪；Ctrl+C 只退出日志查看
docker compose logs --tail=100 --follow app

# 在正在运行的 app 容器内启动 shell；精简镜像可能没有 bash
docker compose exec app sh


# 重新使用Dockerfile构建app镜像，并启动 app
# --build：启动前构建镜像
docker compose up -d --build --no-deps app

# 仅重启现有 app 容器，不会应用 Compose 配置或镜像变更
docker compose restart app

# 停止服务但保留容器、项目网络和数据卷，之后可用 start 恢复
docker compose stop
docker compose start

# 停止并删除本项目容器和非 external 网络；默认保留镜像和命名卷
docker compose down

# 同时删除 Compose 声明的命名卷和容器匿名卷，数据库数据可能永久丢失
# external 卷不会被删除；执行前必须确认目标项目并完成可恢复备份
docker compose down --volumes
```

示例：一个 Java 服务连接 MySQL。Compose 会为同一项目创建默认网络，服务名可直接作为主机名使用；`depends_on` 只控制启动顺序。

```yaml
name: my-service

services:
  app:
    build: .
    image: example/my-service:1.0.0
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/app?useSSL=false&serverTimezone=UTC
      SPRING_DATASOURCE_USERNAME: app
      # 真实密码放在 .env（不要提交）或 Compose secrets / 外部密钥系统中
      SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD:?set DB_PASSWORD in .env}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: mysql:8.4
    environment:
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: ${DB_PASSWORD:?set DB_PASSWORD in .env}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:?set MYSQL_ROOT_PASSWORD in .env}
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-p$${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 10
    restart: unless-stopped

volumes:
  mysql-data:
```

建议把 `.env` 写入 `.gitignore`，并提交 `.env.example`（仅保留变量名、无真实密码）。生产环境的秘密应交由部署平台或专用密钥系统管理。



### 八、离线环境交付

离线安装 Docker Engine 时，应从目标发行版与 CPU 架构对应的官方 RPM/DEB 或官方静态二进制包准备**完整且版本匹配**的依赖。离线前应在同版本测试机上完成安装演练、校验哈希并保留安装包清单。

离线传输镜像使用 `docker image save/load`，它会保留镜像的标签和历史：

```bash
# 联网机器：可同时保存多个镜像，并压缩传输
docker pull nginx:1.28
docker image save nginx:1.28 -o nginx_1.28.tar
gzip -9 nginx_1.28.tar
sha256sum nginx_1.28.tar.gz > nginx_1.28.tar.gz.sha256

# 离线机器：先校验文件，再加载
sha256sum -c nginx_1.28.tar.gz.sha256
gunzip -c nginx_1.28.tar.gz | docker image load
docker image ls nginx
```

