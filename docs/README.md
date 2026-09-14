# 文档索引

仓库文档按照“技术领域 → 技术或框架 → 文章”三级结构组织。



## 当前内容

| 技术领域 | 技术专题 | 文章 |
| --- | --- | --- |
| 前端开发（`frontend`） | [JavaScript](./frontend/javascript/README.md) | [JavaScript 基础知识](./frontend/javascript/JavaScript基础知识.md) |
| DevOps（`devops`） | [Docker](./devops/docker/README.md) | [Docker 基础知识](./devops/docker/Docker基础知识.md) |



## 技术领域命名

新增文档时优先从以下领域中选择：

| 目录名 | 技术领域 | 示例 |
| --- | --- | --- |
| `ai` | 人工智能 | 大模型、Agent、机器学习 |
| `backend` | 后端开发 | Java、Go、数据库访问框架 |
| `frontend` | 前端开发 | JavaScript、TypeScript、Vue、React |
| `devops` | DevOps | Docker、Kubernetes、CI/CD、可观测性 |
| `database` | 数据库 | MySQL、PostgreSQL、Redis |
| `cloud` | 云计算 | 云平台、云原生服务、基础设施即代码 |
| `architecture` | 软件架构 | 设计模式、系统设计、分布式架构 |
| `tools` | 工具与效率 | Git、IDE、命令行工具 |

如果新内容无法合理归入现有领域，可以新增语义清晰、使用小写英文命名的一级目录。



## 归档规则

```text
docs/
└── <技术领域>/
    └── <技术或框架>/
        ├── README.md
        ├── <文章>.md
        └── assets/
```

- 每个技术专题使用 `README.md` 维护文章索引。
- 新领域或专题在出现第一篇文章时再创建，不预建空目录。
- 文件名应突出主题，可以用 `-入门`、`-实战`、`-原理`、`-排错` 等后缀描述内容类型。
- 图片、示意图和附件放在文章同级的 `assets/` 中。
- 新增或调整文档后，同步更新本索引和根目录 [README](../README.md)。
