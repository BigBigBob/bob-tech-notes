---
translation_id: docker-basics
description: "Docker 核心概念、命令、儲存、映像、網路、Compose 和離線交付。"
---

# Docker 基礎知識

## 一、核心概念與架構

 Docker 中最常見的幾個物件：

- **映像（Image）**：只讀、分層的應用交付模板，包含執行應用所需的檔案系統、執行階段和預設配置。一個映像可以建立多個容器。
- **容器（Container）**：映像的一個執行實例，擁有獨立的程序、網路和可寫層。容器本身應儘量無狀態、可隨時重建。
- **映像倉庫（Registry）**：儲存與分發映像的服務，例如 Docker Hub、企業 Harbor 或自建 Registry。
- **資料卷（Volume）**：由 Docker 管理的持久化資料；容器刪除後資料仍可保留。

- **映像分層與容器可寫層** ：映像通常使用 OverlayFS 等聯合掛載機制實現分層複用：映像層只讀，容器啟動時在頂部新增一個可寫層（copy-on-write）。容器可寫層隨容器刪除而消失，因此資料庫、上傳檔案、日誌等需要持久化的資料應寫入 Volume、繫結掛載或外部儲存，而非容器檔案系統。



## 二、安裝 Docker

### 1. 選擇平臺

- **Windows / macOS 本地開發**：優先使用 Docker Desktop，並啟用 WSL 2（Windows）或預設虛擬化後端。
- **Linux 伺服器**：安裝 Docker Engine。


### 2. Ubuntu24 安裝 Docker 範例

```bash
# 1. 更新軟體包索引並安裝必要工具
sudo apt update
sudo apt install -y ca-certificates curl

# 2. 新增 Docker 官方 GPG 金鑰
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. 新增 Docker 官方 apt 軟體源
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# 4. 安裝 Docker Engine、CLI、containerd、Buildx 和 Compose 外掛
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# 5. 檢視 Docker 服務狀態並執行測試容器
sudo systemctl status docker --no-pager
sudo docker run --rm hello-world
```



## 三、常用命令

### 1. 檢視狀態與資源

```bash
# Docker 環境與服務端狀態
docker version                     # 檢視 Client / Server 版本；Server 不可達時會顯示連線錯誤
docker info                        # 檢視 Engine、容器數量、儲存驅動、網路、執行階段等總體資訊

# Docker 物件列表
docker ps                          # 僅列出正在執行的容器
docker ps -a                       # 列出全部容器，包括已退出和已建立但未啟動的容器
docker image ls                    # 列出本地映像（docker images 的現代同義寫法）
docker volume ls                   # 列出 Docker 管理的資料卷
docker network ls                  # 列出 Docker 網路

# 單個容器的執行狀態與排障資訊；將 web 替換為容器名或容器 ID
docker stats                       # 實時顯示所有執行中容器的 CPU、記憶體、網路和塊 I/O；Ctrl+C 退出
docker stats --no-stream web       # 只採集一次指定容器的資源使用情況，便於指令碼或快速檢查
docker top web                     # 檢視指定容器內正在執行的程序
docker inspect web                 # 檢視容器配置、狀態、掛載、網路等完整 JSON 資訊
docker logs --tail 100 web         # 檢視容器最近 100 行標準輸出和標準錯誤日誌
docker port web                    # 檢視容器埠到主機埠的對映

# Docker 磁碟佔用
docker system df                   # 彙總映像、容器、資料卷和構建快取的磁碟佔用
docker system df -v                # 显示每个对象的详细磁盘占用，输出可能较长
```

### 2. 映像

```bash
# 獲取與列出映像
docker pull nginx:1.28                         # 從映像倉庫拉取明確版本，避免生產環境依賴會變化的 latest
docker image ls                                # 列出本地映像、標籤、映像 ID、建立時間和佔用空間

# 檢視映像詳情；將 nginx:1.28 替換為映像名:標籤、摘要或映像 ID
docker image inspect nginx:1.28                # 以 JSON 檢視入口命令、環境變數、架構、層等完整後設資料

# 標記與刪除映像
docker image rm nginx:1.28                     # 刪除未被容器引用的映像；正在使用時會拒絕刪除
docker image prune                             # 删除悬空镜像，执行前会要求确认
```

### 3. 建立、執行與停止容器

```bash
# 建立並立即啟動一個後臺容器
# -d 後臺執行；--name 指定容器名；--restart 設定 Docker 重啟後的恢復策略
# -p 的順序是“主機地址:主機埠:容器埠”,127.0.0.1 表示限制只允許本機訪問
docker run -d --name web --restart unless-stopped \
  -p 127.0.0.1:8080:80 \
  nginx:1.28

# 啟動一個臨時互動式容器；退出後自動刪除，適合測試和排障
docker run --rm -it alpine:3.22 sh

# 檢視日誌和進入執行中的容器
docker logs --tail 100 -f web       # 先顯示最近 100 行並持續跟蹤；Ctrl+C 退出
docker exec -it web sh              # 在執行中的容器內啟動 shell

# 停止、重啟
docker stop web                      # 停止容器
docker start web                     # 啟動容器
docker restart web                   # 重啟容器

# 刪除
docker rm web                       # 刪除已停止的容器；執行中的容器會拒絕刪除
docker rm -f web                    # 强制终止并删除运行中的容器，可能造成未完成写入
```

- `docker run` 相當於先 `docker create` 再 `docker start`，每執行一次都會**新建**容器；已有容器應使用 `docker start` 或 `docker restart`。

- -p 和 -P 都用於把容器埠釋出到主機，但控制方式不同

  - -p：手動指定埠對映。完整的格式是：-p [主機IP:]主機埠:容器埠
  - -P：隨機發布所有宣告埠
  - 常開發和生產部署通常優先使用 `-p`；`-P` 更適合臨時測試。



### 4. 複製、匯出與匯入

```bash
# 在主機與容器之間複製檔案
docker cp web:/usr/share/nginx/html/index.html ./index.html  # 從容器複製單個檔案到主機的當前目錄
docker cp ./nginx.conf web:/tmp/nginx.conf      # 從主機複製檔案到容器的 /tmp 目錄

docker cp web:/etc/nginx ./backup/     # 複製 nginx 整個目錄，保留 nginx 這一層
docker cp web:/etc/nginx/. ./backup/    # 只複製 nginx 目錄裡面的內容，不保留 nginx 這一層

# export 匯出容器根檔案系統的扁平快照，不包含資料卷內容、映像分層歷史和容器執行配置
docker container export --output web-rootfs.tar web

# import 從根檔案系統歸檔建立一個新映像；它不會恢復原映像的 CMD、ENTRYPOINT、ENV 等配置
docker image import web-rootfs.tar example/web-rootfs:backup

# 若目的是完整遷移映像，應使用 save/load：它們會保留映像層、標籤和映像配置
docker image save --output nginx_1.28.tar nginx:1.28
docker image load --input nginx_1.28.tar
```

| 命令組合 | 操作物件 | 保留內容 | 適用場景 |
| --- | --- | --- | --- |
| `docker cp` | 單個檔案或目錄 | 檔案內容，許可權盡量保留 | 臨時取日誌、複製配置或排障檔案 |
| `docker export/import` | 容器根檔案系統 | 扁平化後的檔案系統 | 製作臨時根檔案系統快照；不適合作為標準映像交付方式 |
| `docker save/load` | Docker 映像 | 映像層、標籤和映像配置 | 離線遷移或歸檔映像 |



## 四、資料持久化與掛載

容器的可寫層與容器生命週期繫結：停止、重啟容器時資料仍在，但刪除容器後可寫層也會被刪除。因此，資料庫檔案、使用者上傳內容等重要資料必須放在 Volume、繫結掛載或外部儲存中，而不能只寫入容器檔案系統。

### 1. 三種掛載方式如何選擇

| 型別 | 資料位置與管理者 | 適用場景 | 主要特點 |
| --- | --- | --- | --- |
| 命名 Volume | Docker 管理 | 資料庫、應用持久化資料 | 預設首選；不依賴固定主機路徑，便於複用、檢查和遷移。 |
| Bind mount | 指定的主機檔案或目錄 | 本地原始碼、配置檔案、已有資料目錄 | 內容對主機直接可見，但依賴主機路徑、許可權和安全策略。 |
| tmpfs | 主機記憶體 | 臨時快取、短期敏感檔案 | 不寫入磁碟，容器停止後內容消失；僅適用於 Linux 容器。 |

`--mount` 引數含義更明確，複雜掛載優先使用；`-v`/`--volume` 寫法更短，仍然受支援。容器內的目標路徑必須使用絕對路徑。

### 2. 使用命名 Volume 儲存資料庫資料

```bash
# 建立並檢視命名卷
docker volume create mysql-data
docker volume inspect mysql-data

# 將 MySQL 資料目錄掛載到命名卷
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4

# 或者我們也可以使用 -v 的簡寫方式，但其實官方更推薦 --mount，因為語義更加明確
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  -v mysql-data:/var/lib/mysql \
  mysql:8.4

# 確認容器實際使用的掛載
docker inspect mysql --format '{{json .Mounts}}'
```

刪除容器不會自動刪除這裡顯式建立的 `mysql-data`。只要重新掛載同一個卷，新容器就能繼續讀取原資料：

```bash
docker stop mysql
docker rm mysql

docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<replace-with-secret>' \
  --mount type=volume,src=mysql-data,dst=/var/lib/mysql \
  mysql:8.4
```

重新掛載已有 MySQL 資料卷時，`MYSQL_ROOT_PASSWORD` 不會重置資料庫中已經存在的 root 密碼；這類初始化變數通常只在資料目錄為空時生效。

Volume 的生命週期獨立於容器，但並非不會丟失。`docker volume rm mysql-data`、`docker compose down -v` 和帶 `--volumes` 的清理命令都可能刪除資料卷；執行前必須確認備份和目標範圍。不要直接修改 Docker 內部儲存目錄（通常位於 `/var/lib/docker`）。

### 3. 使用 Bind mount 掛載配置或原始碼

```bash
# 當前目錄必須已經存在 nginx.conf
docker run --rm \
  --mount type=bind,src="/opt/nginx/nginx.conf",dst=/etc/nginx/nginx.conf \
  nginx:1.28
```

使用 `--mount type=bind` 時，源路徑不存在會直接報錯，能避免把拼錯的檔案路徑意外建立成目錄。生產環境應儘量使用絕對路徑和只讀掛載。Bind mount 強依賴主機目錄結構，遷移到另一臺機器時需要同步複製對應檔案。



## 五、Dockerfile 與映像構建

### 1. 基本規則

Dockerfile 是映像的可復現構建清單。`docker build` 按順序解析指令，每條會形成可快取的構建結果；最終得到映像，而不是直接得到正在執行的容器。

```text
原始碼與依賴描述
      │
      ▼
構建上下文 + Dockerfile
      │ docker build
      ▼
只讀映象 ── docker run ──> 帶可寫層的容器
```

`docker build -f docker/Dockerfile .` 中最後的 `.` 才是構建上下文。`COPY` 和 `ADD` 只能讀取上下文內、且未被 `.dockerignore` 排除的檔案。



### 2. 常用指令

| 指令 | 用途與要點 |
| --- | --- |
| `FROM` | 開始一個構建階段並指定基礎映像；多階段構建可以出現多次。生產環境應固定明確版本，必要時固定 digest。 |
| `ARG` | 宣告構建期變數，只在其作用域內參與構建；不是安全的金鑰傳遞方式。 |
| `WORKDIR` | 設定後續 `RUN`、`COPY`、`CMD` 等指令的工作目錄；優先於反覆使用 `cd`。 |
| `COPY` | 從構建上下文或其他構建階段複製檔案；可使用 `--from`、`--chown` 和 `--chmod`。普通複製優先使用它。 |
| `ADD` | 額外支援本地 tar 自動解壓和遠端源等語義；只有明確需要這些能力時再使用，避免隱式行為。 |
| `RUN` | 在構建期執行命令併產生映像層；可配合 `RUN --mount=type=cache` 或 `type=secret` 使用臨時掛載。 |
| `ENV` | 設定映像和容器中的持久環境變數；適合非敏感預設值，不存放密碼或 Token。 |
| `USER` | 設定後續構建步驟及容器啟動時使用的使用者和組。 |
| `EXPOSE` | 記錄應用預期監聽的容器埠，僅是後設資料；不會像 `docker run -p` 一樣釋出埠。 |
| `CMD` | 提供預設命令或預設引數；Dockerfile 中只有最後一條生效，可被 `docker run IMAGE ...` 覆蓋。 |
| `ENTRYPOINT` | 定義容器入口程式；exec 形式與 `CMD` 組合時，`CMD` 通常提供可覆蓋的預設引數。 |
| `HEALTHCHECK` | 宣告應用健康檢查，便於編排工具判斷服務狀態。 |
| `LABEL` | 寫入版本、原始碼地址、許可證等 OCI 映像後設資料；`MAINTAINER` 已廢棄。 |



### 3. 簡單 Java 應用範例

假設已經有一個 Maven + Spring Boot 專案，並且在主機或 CI 中執行 `mvn clean package` 生成了 `target/my-service.jar`：

```text
my-service/
├── Dockerfile
├── pom.xml
├── src/
└── target/
    └── my-service.jar
```

專案根目錄中的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jre

WORKDIR /app
COPY target/my-service.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

這個 Dockerfile 只有一個構建階段：

- `FROM` 提供執行 Java 21 應用所需的 JRE。
- `WORKDIR` 把容器內的工作目錄設定為 `/app`。
- `COPY` 把主機已經構建好的 JAR 複製進映像；JAR 檔名需要與實際構建結果一致。
- `EXPOSE 8080` 記錄應用預期監聽的埠，但不會自動把埠釋出到主機。
- `ENTRYPOINT` 讓容器啟動時執行 `java -jar /app/app.jar`。



### 4. 構建、檢查與執行驗證

```bash
# 先在主機生成 target/my-service.jar
mvn clean package -DskipTests

# 再構建映像；最後的點表示當前目錄是構建上下文
docker build --pull -t example/my-service:1.0.0 .

# 檢視映像大小、入口程式、預設引數和執行使用者
docker image ls example/my-service:1.0.0
docker image inspect example/my-service:1.0.0 \
  --format 'user={{.Config.User}} entrypoint={{json .Config.Entrypoint}} cmd={{json .Config.Cmd}}'

# 前臺試執行；Ctrl+C 後容器會停止並自動刪除
docker run --rm -p 8080:8080 example/my-service:1.0.0
```



## 六、網路

### 1. 容器網路的基本模型

在 Linux 上，每個普通容器擁有獨立的網路名稱空間，包括自己的網絡卡、IP 地址、路由表、埠和 DNS 配置。使用 bridge 網路時，Docker 通常透過虛擬網絡卡把容器接入主機上的軟體網橋，並透過轉發/NAT 訪問外部網路。

```text
同一 Docker 主機

外部客戶端
    │ 訪問主機IP:8080
    ▼
主機埠 8080 ──埠釋出──> app:8080
                                │
                         自定義 bridge 網路
                                │ 使用服務名 db:3306
                                ▼
                             db:3306

app ──NAT/路由──> 主機網絡卡 ──> 外部網路
```

需要牢記三個邊界：

- 容器內的 `127.0.0.1` 或 `localhost` 指向**當前容器自身**，不是主機，也不是其他容器。

- 同一自定義網路中的容器直接使用“容器名或網路別名 + 容器埠”通訊，不需要把埠釋出到主機。



### 2. 常見網路模式

| 模式 | 說明 |
| --- | --- |
| `bridge` | 單機 Docker 最常用的驅動。自定義 bridge 提供容器名 DNS、網路隔離和埠釋出。 |
| `host` | 容器直接共享主機網路名稱空間，沒有獨立容器 IP；`-p` 會失去意義，並可能產生埠衝突。主要用於特定 Linux 場景。 |
| `none` | 除迴環介面外不配置網路，適合不應進行網路通訊的離線任務。 |
| `container:<name-or-id>` | 與指定容器共享同一個網路名稱空間和埠空間，適合少數緊耦合 sidecar 場景。 |
| `overlay` | 連線多個 Docker daemon 的多主機網路，通常配合 Swarm；普通單機 bridge 不能直接跨主機。 |
| `macvlan` / `ipvlan` | 讓容器更直接地接入物理網路或 VLAN；對交換機、網段和路由有額外要求，不作為普通應用預設選擇。 |

如果 `docker run` 沒有指定 `--network`，Linux 容器通常接入預設 `bridge`。實際應用應優先建立**自定義 bridge 網路**：它支援自動 DNS 解析，隔離範圍也比所有容器共用預設 bridge 更清晰。舊的 `--link` 方式已經不推薦。

### 3. 自定義 bridge 與容器 DNS

```bash
# 建立自定義 bridge 網路
docker network create app-net

# redis 自動獲得該網路中的 IP 和 DNS 名稱 redis
docker run -d --name redis --network app-net redis:7.4

# 臨時客戶端加入同一網路，透過名稱 redis 和容器埠 6379 訪問
docker run --rm --network app-net redis:7.4 redis-cli -h redis ping
# 返回 PONG；這裡的 redis 是容器名，同時也是 DNS 名稱

# 檢視網路的驅動、網段、閘道器和已連線容器
docker network inspect app-net

# 執行中的容器也可以動態加入或離開自定義網路
docker run -d --name toolbox alpine:3.22 sleep 1d
docker network connect app-net toolbox
docker network disconnect app-net toolbox

# 網路仍被容器佔用時無法刪除
docker rm -f redis toolbox
docker network rm app-net
```

Docker 內建 DNS 會把同一自定義網路中的容器名或網路別名解析成當前容器 IP。容器重建後 IP 可能改變，但名稱可以保持不變，因此應用配置應寫 `redis:6379`、`db:3306`，不要固定某個 `172.x.x.x` 地址。

### 4. 埠釋出：`EXPOSE`、`-p` 與 `-P`

`EXPOSE` 只是映像後設資料，用於說明應用預期監聽的容器埠；真正允許主機或外部客戶端進入容器，需要在執行階段使用 `-p`/`--publish`。

```bash
# 僅允許主機本地訪問：主機 8080 -> 容器 8080
docker run -d --name app-local \
  -p 127.0.0.1:8080:8080 \
  example/my-service:1.0.0

# 未指定主機 IP，通常會繫結所有主機地址，暴露範圍更大
docker run -d --name app-public \
  -p 8081:8080 \
  example/my-service:1.0.0

# 隨機發布映像中宣告的所有 EXPOSE 埠，再查詢實際對映
# Docker會讀取映像的Expose 8080，隨機選擇一個主機埠
docker run -d --name app-random -P example/my-service:1.0.0
docker port app-random
```

`-p` 的順序是：

```text
-p [主機IP:]主機埠:容器埠[/協議]
```

埠釋出也不等於已經配置好防火牆、雲安全組、TLS 或身份認證。

### 5. 常見通訊路徑

| 訪問方向 | 推薦地址 | 是否需要 `-p` |
| --- | --- | --- |
| 同一自定義網路：app 訪問 db | `db:3306` | 不需要 |
| 主機訪問 app | `127.0.0.1:8080` 或主機 IP + 已釋出埠 | 需要 |
| 外部客戶端訪問 app | 域名/主機 IP + 已釋出埠，通常再經過反向代理 | 需要 |
| 容器訪問網際網路 | 目標域名或 IP | 預設 bridge 通常可直接出站 |
| 不同 Docker 主機上的容器互訪 | 負載均衡入口、路由、Swarm overlay 或其他編排網路 | 單機 bridge 不適用 |

### 6. 網路隔離與生產邊界

一個容器可以同時連線多個網路。例如前端連線 `frontend-net` 和 `backend-net`，資料庫只連線 `backend-net`，從而減少不必要的網路可達範圍。還可以使用 `--internal` 建立預設不對外路由的內部網路：

```bash
docker network create frontend-net
docker network create --internal backend-net

docker run -d --name cache --network backend-net redis:7.4
docker run -d --name app --network frontend-net example/my-service:1.0.0
docker network connect backend-net app

# 清理本範例
docker rm -f app cache
docker network rm frontend-net backend-net
```

### 7. 常用排障命令

```bash
# 檢視網路和容器連線關係
docker network ls
docker network inspect app-net
docker inspect app --format '{{json .NetworkSettings.Networks}}'

# 檢視釋出到主機的埠
docker port app
```



## 七、Docker Compose（容器編排）

Docker Compose V1 的獨立命令 `docker-compose` 已是 Legacy。當前優先使用 Compose 外掛，命令為 **`docker compose`**（中間空格）。以下命令應在 `compose.yaml` 所在目錄執行；其中 `app`、`db` 是 Compose 檔案中的服務名：

```bash
# 檢視 Compose 外掛版本，確認使用的是 docker compose（V2）
docker compose version

# 拉取 db 服務引用的遠端映像；不會啟動容器
docker compose pull db

# 建立並啟動Compose檔案中的所有服務
docker compose up -d

# 檢視本專案全部容器，包括已經退出的容器
docker compose ps --all

# 先顯示 app 最近 100 行日誌，再持續跟蹤；Ctrl+C 只退出日誌檢視
docker compose logs --tail=100 --follow app

# 在正在執行的 app 容器內啟動 shell；精簡映像可能沒有 bash
docker compose exec app sh


# 重新使用Dockerfile構建app映像，並啟動 app
# --build：啟動前構建映像
docker compose up -d --build --no-deps app

# 僅重啟現有 app 容器，不會應用 Compose 配置或映像變更
docker compose restart app

# 停止服務但保留容器、專案網路和資料卷，之後可用 start 恢復
docker compose stop
docker compose start

# 停止並刪除本專案容器和非 external 網路；預設保留映像和命名卷
docker compose down

# 同時刪除 Compose 宣告的命名卷和容器匿名卷，資料庫資料可能永久丟失
# external 卷不會被刪除；執行前必須確認目標專案並完成可恢復備份
docker compose down --volumes
```

範例：一個 Java 服務連線 MySQL。Compose 會為同一專案建立預設網路，服務名可直接作為主機名使用；`depends_on` 只控制啟動順序。

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
      # 真實密碼放在 .env（不要提交）或 Compose secrets / 外部金鑰系統中
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

建議把 `.env` 寫入 `.gitignore`，並提交 `.env.example`（僅保留變數名、無真實密碼）。生產環境的秘密應交由部署平臺或專用金鑰系統管理。



## 八、離線環境交付

離線安裝 Docker Engine 時，應從目標發行版與 CPU 架構對應的官方 RPM/DEB 或官方靜態二進位制包準備**完整且版本匹配**的依賴。離線前應在同版本測試機上完成安裝演練、校驗雜湊並保留安裝包清單。

離線傳輸映像使用 `docker image save/load`，它會保留映像的標籤和歷史：

```bash
# 聯網機器：可同時儲存多個映像，並壓縮傳輸
docker pull nginx:1.28
docker image save nginx:1.28 -o nginx_1.28.tar
gzip -9 nginx_1.28.tar
sha256sum nginx_1.28.tar.gz > nginx_1.28.tar.gz.sha256

# 離線機器：先校驗檔案，再載入
sha256sum -c nginx_1.28.tar.gz.sha256
gunzip -c nginx_1.28.tar.gz | docker image load
docker image ls nginx
```
