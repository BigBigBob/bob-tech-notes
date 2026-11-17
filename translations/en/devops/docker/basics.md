---
translation_id: docker-basics
description: "Docker concepts, commands, storage, images, networking, Compose, and offline delivery."
---

# Docker Fundamentals

## 1. Core concepts and architecture

These are the objects you will encounter most often in Docker:

- **Image**: A read-only, layered template that packages the filesystem, runtime, and default configuration needed to run an application. A single image can be used to create multiple containers.
- **Container**: A running instance of an image with its own processes, network, and writable layer. Keep containers as stateless as possible so they can be recreated at any time.
- **Registry**: A service for storing and distributing images, such as Docker Hub, an enterprise Harbor instance, or a self-hosted registry.
- **Volume**: Persistent storage managed by Docker. Data can remain after a container is removed.

- **Image layers and the container writable layer**: Images typically reuse filesystem layers through a union filesystem such as OverlayFS. Image layers are read-only. Docker adds a writable layer on top using copy-on-write when it starts a container. Removing the container also removes its writable layer. Keep databases, uploads, and logs that need to persist in a volume, bind mount, or external storage.



## 2. Installing Docker

### 1. Select the platform

- **Local development on Windows or macOS**: Use Docker Desktop with WSL 2 on Windows or the default virtualization backend.
- **Linux server**: Install Docker Engine.


### 2. Installing Docker on Ubuntu 24.04

```bash
# 1. Update the package index and install the necessary tools.
sudo apt update
sudo apt install -y ca-certificates curl

# 2. Add the official Docker GPG key.
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. Add the official Docker apt software source.
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# 4. Install Docker Engine, CLI, containerd, Buildx, and Compose plugins.
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# 5. Check the status of the Docker service and run the test container.
sudo systemctl status docker --no-pager
sudo docker run --rm hello-world
```



## 3. Common commands

### 1. Checking status and resource use

```bash
# Docker environment and server status
docker version                     # Check the Client/Server version; a connection error will be displayed when the Server is unreachable.
docker info                        # View overall information such as the number of engines, containers, storage drivers, networks, and runtime environments.

# Docker object list
docker ps                          # Only list the containers that are running.
docker ps -a                       # List all containers, including those that have been exited and those that have been created but not yet started.
docker image ls                    # List the local images (modern equivalent of docker images).
docker volume ls                   # List of Docker-managed data volumes.
docker network ls                  # List the Docker networks.

# The running status and troubleshooting information of a single container; replace "web" with the container name or container ID.
docker stats                       # Display the CPU, memory, network, and block I/O of all running containers in real time. Press Ctrl+C to exit.
docker stats --no-stream web       # Only collect the resource usage of the specified container once, which is convenient for scripts or quick checks.
docker top web                     # Check the processes that are running within the specified container.
docker inspect web                 # View complete JSON information on container configuration, state, mount, network, etc.
docker logs --tail 100 web         # View the last 100 lines of standard output and standard error logs of the container.
docker port web                    # Check the mapping from container ports to host ports.

# Docker disk usage
docker system df                   # Summarize the disk usage of images, containers, data volumes, and the cache built.
docker system df -v                # 显示每个对象的详细磁盘占用，输出可能较长
```

### 2. Working with images

```bash
# Obtain and list the images.
docker pull nginx:1.28                         # Pull the specific version from the image repository to avoid relying on the latest version, which may change in the production environment.
docker image ls                                # List the local images, tags, image IDs, creation times, and occupied space.

# View the image details; replace "nginx:1.28" with the image name, tag, summary, or image ID.
docker image inspect nginx:1.28                # View the complete metadata such as entry commands, environment variables, architecture, layers, etc. in JSON format.

# Mark and delete images.
docker image rm nginx:1.28                     # Delete images that are not referenced by the container; attempting to delete them will result in failure.
docker image prune                             # 删除悬空镜像，执行前会要求确认
```

### 3. Create, run, and stop containers

```bash
# Create and immediately start a backend container.
# -d backstage running; --name specifies container name; --restart setup Docker recovery strategy after restart
# The order of `-p` is "Host address: Host port: Container port". 127.0.0.1 indicates that only local access is allowed.
docker run -d --name web --restart unless-stopped \
  -p 127.0.0.1:8080:80 \
  nginx:1.28

# Launch a temporary interactive container. It will be automatically deleted after termination, making it suitable for testing and troubleshooting purposes.
docker run --rm -it alpine:3.22 sh

# Check the logs and access the running container.
docker logs --tail 100 -f web       # Display the last 100 lines and continue tracking. Press Ctrl+C to exit.
docker exec -it web sh              # Launch the shell within the running container.

# Stop, restart
docker stop web                      # Stop the container.
docker start web                     # Launch the container
docker restart web                   # Restart the container.

# Delete
docker rm web                       # Delete the stopped containers; running containers will refuse to be deleted.
docker rm -f web                    # 强制终止并删除运行中的容器，可能造成未完成写入
```

- `docker run` combines `docker create` and `docker start`, so each invocation creates a new container. Use `docker start` or `docker restart` for an existing container.

- Both `-p` and `-P` publish container ports on the host. They differ in how the host ports are selected.

    - `-p` specifies the mapping explicitly. The full syntax is `-p [HOST_IP:]HOST_PORT:CONTAINER_PORT`.
    - `-P` publishes all exposed ports to randomly assigned host ports.
    - Prefer `-p` for regular development and production deployments. `-P` is convenient for temporary tests.



### 4. Copying, exporting, and importing

```bash
# Copying files between the host machine and the container
docker cp web:/usr/share/nginx/html/index.html ./index.html  # Copy a single file from the container to the current directory on the host machine.
docker cp ./nginx.conf web:/tmp/nginx.conf      # Copy the file from the host to the /tmp directory of the container.

docker cp web:/etc/nginx ./backup/     # Copy the entire directory of nginx, keeping the nginx layer intact.
docker cp web:/etc/nginx/. ./backup/    # Only copy the contents of the nginx directory. Do not keep the nginx layer.

# Export a flat snapshot of the container's root file system, excluding the data volume content, image layer history, and container running configurations.
docker container export --output web-rootfs.tar web

# Import creates a new image from the root file system archive. It does not restore the original image’s CMD, ENTRYPOINT, ENV, and other configurations.
docker image import web-rootfs.tar example/web-rootfs:backup

# If the goal is to fully migrate the image, use save/load. This method preserves the image layer, tags, and image configuration.
docker image save --output nginx_1.28.tar nginx:1.28
docker image load --input nginx_1.28.tar
```

| Command | What it operates on | What it preserves | Typical use |
| --- | --- | --- | --- |
| `docker cp` | A file or directory | File contents and permissions where possible | Retrieve logs or copy configuration and diagnostic files |
| `docker export/import` | A container’s root filesystem | A flattened filesystem | Capture a temporary root filesystem snapshot. For distributing images, use save/load. |
| `docker save/load` | A Docker image | Layers, tags, and configuration | Transfer or archive images offline |



## 4. Data persistence and mounts

The writable layer is tied to the container’s lifecycle. Its data survives stops and restarts but is removed with the container. Store important data such as database files and user uploads in volumes, bind mounts, or external storage.

### 1. Choosing a mount type

| Type | Where the data lives and who manages it | Typical use | Characteristics |
| --- | --- | --- | --- |
| Named volume | Managed by Docker | Database and application data | The default choice. It is easy to reuse, inspect, and migrate without depending on a fixed host path. |
| Bind mount | A specified host file or directory | Local source code, configuration files, and existing data directories | The host can access the contents directly. Host paths, permissions, and security policies still apply. |
| tmpfs | Host memory | Temporary caches and short-lived sensitive files | Contents stay off disk and disappear when the container stops. Available for Linux containers. |

Use `--mount` to make the options explicit, especially for complex mounts. The shorter `-v` / `--volume` syntax is also supported. Use an absolute target path inside the container.

### 2. Persisting database data in a named volume

```bash
# Create and view the named volume.
docker volume create mysql-data
docker volume inspect mysql-data

# Mount the MySQL data directory to the named volume.
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4

# Or, we can use the shorthand form of -v. However, the official recommendation is to use --mount, as it provides clearer semantics.
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  -v mysql-data:/var/lib/mysql \
  mysql:8.4

# Confirm the actual mounting used by the container.
docker inspect mysql --format '{{json .Mounts}}'
```

Removing the container leaves the explicitly created `mysql-data` volume intact. Mount the same volume in a new container to reuse the existing data:

```bash
docker stop mysql
docker rm mysql

docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4
```

When you remount an existing MySQL data volume, `MYSQL_ROOT_PASSWORD` does not reset an existing root password. Initialization variables like this usually take effect only when the data directory is empty.

Volumes have a lifecycle of their own. `docker volume rm mysql-data`, `docker compose down -v`, and cleanup commands with `--volumes` can delete them. Verify your backup and confirm which resources the command will affect before running it. Leave Docker’s internal storage directory, usually `/var/lib/docker`, alone.

### 3. Bind-mounting configuration or source code

```bash
# The current directory must already contain the nginx.conf file.
docker run --rm \
  --mount type=bind,src="/opt/nginx/nginx.conf",dst=/etc/nginx/nginx.conf \
  nginx:1.28
```

With `--mount type=bind`, Docker reports an error if the source path is missing. This helps catch typos before an unintended directory is created. In production, use absolute paths and read-only mounts where practical. Bind mounts depend on the host’s directory structure, so copy the relevant files when migrating to another machine.



## 5. Dockerfiles and image builds

### 1. Basic rules

A Dockerfile specifies how to reproduce an image build. `docker build` processes its instructions in order and can cache build results. The result is an image that can be used to start containers.

```text
Source code and dependency declarations
      │
      ▼
Build context + Dockerfile
      │ docker build
      ▼
Read-only image ── docker run ──> container with a writable layer
```

In `docker build -f docker/Dockerfile .`, the final `.` specifies the build context. `COPY` and `ADD` can only read local files that are within that context and are not excluded by `.dockerignore`.



### 2. Common instructions

| Instruction | Purpose |
| --- | --- |
| `FROM` | Starts a build stage and specifies the base image. Repeat it for a multi-stage build. Pin an explicit image version for production, or pin the digest when needed. |
| `ARG` | Declares a build-time variable scoped to the relevant part of the build. Use secret mounts to pass secrets. |
| `WORKDIR` | Sets the working directory for subsequent instructions such as `RUN`, `COPY`, and `CMD`. Use it to avoid repeating `cd`. |
| `COPY` | Copies files from the build context or from another build stage. Options include `--from`, `--chown`, and `--chmod`. Prefer it for ordinary file copies. |
| `ADD` | Also supports features such as extracting a local tar archive and fetching remote sources. Use it when you need those capabilities. |
| `RUN` | Runs a command at build time and produces an image layer. Use a temporary mount such as `RUN --mount=type=cache` or `type=secret` as needed. |
| `ENV` | Sets persistent environment variables in the image and container. Use it for non-sensitive defaults and keep passwords and tokens out of the image. |
| `USER` | Sets the user and group for later build steps and at container startup. |
| `EXPOSE` | Documents the container port that the application expects to listen on. Publish ports with a runtime option such as `docker run -p`. |
| `CMD` | Supplies the default command or arguments. The last `CMD` takes effect, and `docker run IMAGE ...` can override it. |
| `ENTRYPOINT` | Defines the program that starts in the container. In exec form, `CMD` usually supplies default arguments that callers can override. |
| `HEALTHCHECK` | Defines how to check application health so an orchestrator can evaluate the service. |
| `LABEL` | Adds OCI image metadata such as the version, source URL, or license. `MAINTAINER` is deprecated. |



### 3. Simple Java application example

Suppose you already have a Maven and Spring Boot project and have run `mvn clean package` locally or in CI to produce `target/my-service.jar`:

```text
my-service/
├── Dockerfile
├── pom.xml
├── src/
└── target/
    └── my-service.jar
```

The `Dockerfile` in the project root directory:

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jre

WORKDIR /app
COPY target/my-service.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

This Dockerfile has only one build stage:

- `FROM` provides the JRE required to run applications using Java 21.
- `WORKDIR` sets the working directory in the container to `/app`.
- `COPY` puts the already-built JAR into the image. The filename must match your build output.
- `EXPOSE 8080` documents the expected application port. Publishing that port to the host is a separate runtime step.
- `ENTRYPOINT` starts the container by running `java -jar /app/app.jar`.



### 4. Building, inspecting, and testing the image

```bash
# First, generate target/my-service.jar on the host machine.
mvn clean package -DskipTests

# Build the image again. The last dot indicates that the current directory is the build context.
docker build --pull -t example/my-service:1.0.0 .

# Check the image size, entry program, default parameters, and running users.
docker image ls example/my-service:1.0.0
docker image inspect example/my-service:1.0.0 \
  --format 'user={{.Config.User}} entrypoint={{json .Config.Entrypoint}} cmd={{json .Config.Cmd}}'

# Front-end trial operation; after Ctrl+C, the container will stop and be automatically deleted.
docker run --rm -p 8080:8080 example/my-service:1.0.0
```



## 6. Networking

### 1. The basic model of container networking

On Linux, each ordinary container has its own independent network namespace, including its own network interface, IP address, routing table, ports, and DNS configuration. When using a bridge network, Docker typically connects the container to the software bridge on the host machine through virtual network interfaces, and uses forwarding/NAT to access the external network.

```text
Same Docker host

External client
    │ Connect to HOST_IP:8080
    ▼
Host port 8080 ── port publishing ──> app:8080
                                │
                         Custom bridge network
                                │ Connect to the service by name at db:3306
                                ▼
                             db:3306

app ── NAT/routing ──> host network interface ──> external network
```

It is important to keep in mind three boundaries:

- `127.0.0.1` or `localhost` in container points to **the current container itself**, not host or other container.

- Containers within the same custom network communicate directly using the "container name or network alias + container port". There is no need to publish the ports to the host machine.



### 2. Common network patterns

| Network mode | Description |
| --- | --- |
| `bridge` | The usual driver for standalone Docker. A custom bridge provides name resolution, isolation, and port publishing. |
| `host` | Shares the host network namespace and has no separate container IP. `-p` has no effect, and port conflicts are possible. Used mainly in specific Linux scenarios. |
| `none` | Provides only the loopback interface. Useful for offline work that should have no network access. |
| `container:<name-or-id>` | Shares another container’s network namespace and ports. Useful for some tightly coupled sidecars. |
| `overlay` | Connects multiple Docker daemons, typically in Swarm. A regular bridge is limited to one host. |
| `macvlan` / `ipvlan` | Attaches containers more directly to a physical network or VLAN. These drivers have additional requirements for switches, subnets, and routing, so they are not the default for general workloads. |

Without `--network`, Linux containers usually join the default `bridge` network. For applications, prefer a **custom bridge network**. It supports automatic DNS and makes isolation boundaries clearer. The older `--link` option is no longer recommended.

### 3. Custom bridge and container DNS

```bash
# Create a custom bridge network.
docker network create app-net

# Redis automatically obtains the IP address and DNS name of the network.
docker run -d --name redis --network app-net redis:7.4

# The temporary client joins the same network and accesses through the name "redis" and container port 6379.
docker run --rm --network app-net redis:7.4 redis-cli -h redis ping
# Return to PONG. Here, redis is the container name, which is also the DNS name.

# Check the network drivers, IP ranges, gateways, and connected containers.
docker network inspect app-net

# Running containers can also dynamically join or leave custom networks.
docker run -d --name toolbox alpine:3.22 sleep 1d
docker network connect app-net toolbox
docker network disconnect app-net toolbox

# It cannot be deleted when the network is still occupied by the container.
docker rm -f redis toolbox
docker network rm app-net
```

Docker’s embedded DNS resolves container names and network aliases to their current IP addresses on the same custom network. A container can get a different IP when recreated while keeping its name. Use names like `redis:6379` and `db:3306` in application settings instead of hard-coding a `172.x.x.x` address.

### 4. Port publishing: `EXPOSE`, `-p`, and `-P`

`EXPOSE` records the port the application expects to listen on as image metadata. Use `-p` or `--publish` at runtime to let the host or external clients reach that port.

```bash
# Only the host machine can access locally: Host machine 8080 -> Container 8080
docker run -d --name app-local \
  -p 127.0.0.1:8080:8080 \
  example/my-service:1.0.0

# If the host IP address is not specified, all host addresses will be bound, resulting in a wider exposure range.
docker run -d --name app-public \
  -p 8081:8080 \
  example/my-service:1.0.0

# Randomly publish all EXPOSE ports stated in the image, then check the actual mapping.
# Docker will read the Expose 8080 of the image and randomly select a host port.
docker run -d --name app-random -P example/my-service:1.0.0
docker port app-random
```

The `-p` arguments are ordered as follows:

```text
-p [HOST_IP:]HOST_PORT:CONTAINER_PORT[/PROTOCOL]
```

Port publishing does not mean that the firewall, cloud security groups, TLS, or authentication have been configured.

### 5. Common communication paths

| Traffic source and destination | Address to use | Is `-p` needed? |
| --- | --- | --- |
| App to database on the same custom network | `db:3306` | No |
| Host to app | `127.0.0.1:8080` or the host IP and published port | Yes |
| External client to app | Domain name or host IP and published port, usually through a reverse proxy | Yes |
| Container to the internet | Destination domain name or IP | The default bridge usually allows outbound access |
| Containers on different Docker hosts | Load balancer, routes, Swarm overlay, or another orchestration network | A single-host bridge does not apply |

### 6. Network isolation in production

A container can be connected to multiple networks at the same time. For example, the frontend can be connected to `frontend-net` and `backend-net`, while the database can only be connected to `backend-net`. This helps to reduce the unnecessary range of network access. It is also possible to use `--internal` to create an internal network that does not route out to the outside world by default:

```bash
docker network create frontend-net
docker network create --internal backend-net

docker run -d --name cache --network backend-net redis:7.4
docker run -d --name app --network frontend-net example/my-service:1.0.0
docker network connect backend-net app

# Clear this example
docker rm -f app cache
docker network rm frontend-net backend-net
```

### 7. Common troubleshooting commands

```bash
# Check the network and container connection relationships.
docker network ls
docker network inspect app-net
docker inspect app --format '{{json .NetworkSettings.Networks}}'

# Check the ports that are published to the host machine.
docker port app
```



## 7. Docker Compose (container orchestration)

The standalone Docker Compose V1 command, `docker-compose`, is legacy. Use the Compose plugin’s **`docker compose`** command. Run the examples below in the directory containing `compose.yaml`. Here, `app` and `db` are service names in that file.

```bash
# Check the Compose plugin version to ensure that you are using Docker Compose (V2).
docker compose version

# Fetch the remote image referenced by the DB service; no containers will be started.
docker compose pull db

# Create and launch all services in the Compose file.
docker compose up -d

# View all containers in this project, including those that have been exited.
docker compose ps --all

# First, display the last 100 lines of logs for the app. Then, continue to track the logs. Press Ctrl+C to exit the log viewing mode.
docker compose logs --tail=100 --follow app

# Launch a shell within the running app container; the slimmed-down image may not have a bash shell.
docker compose exec app sh


# Rebuild the app image using the Dockerfile again, and start the app.
# --build: Build the image before starting the process.
docker compose up -d --build --no-deps app

# Only the existing app container needs to be restarted. The Compose configuration or image changes will not be applied.
docker compose restart app

# Stop the service, but keep the containers, project networks, and data volumes intact. They can be restored using the "start" command later.
docker compose stop
docker compose start

# Stop and delete this project's containers and non-external networks. By default, the images and named volumes will be retained.
docker compose down

# Also, delete the named volumes and container anonymous volumes declared in Compose. Database data may be permanently lost.
# External Volumes will not be deleted; target items must be identified and back-up can be restored before implementation
docker compose down --volumes
```

This example connects a Java service to MySQL. Compose creates a default network for the project, and services can use other service names as hostnames. `depends_on` controls startup order.

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
      # The actual password should be stored in.env (do not submit it) or in the Compose secrets/ external key system.
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

Add `.env` to `.gitignore` and commit an `.env.example` with variable names and no real passwords. Store production secrets in the deployment platform or a dedicated secret manager.



## 8. Delivering to offline environments

For offline Docker Engine installation, gather a **complete set of version-matched dependencies** using the official RPM or DEB packages or the official static binaries for the target distribution and CPU architecture. Before moving offline, rehearse the installation on an equivalent test machine, verify hashes, and save a list of installation packages.

Use `docker image save/load` to transfer images offline while preserving their tags and history:

```bash
# Networked machines: Can save multiple images at the same time and compress the transmission process.
docker pull nginx:1.28
docker image save nginx:1.28 -o nginx_1.28.tar
gzip -9 nginx_1.28.tar
sha256sum nginx_1.28.tar.gz > nginx_1.28.tar.gz.sha256

# Offline machine: First, verify the file, then load it.
sha256sum -c nginx_1.28.tar.gz.sha256
gunzip -c nginx_1.28.tar.gz | docker image load
docker image ls nginx
```
