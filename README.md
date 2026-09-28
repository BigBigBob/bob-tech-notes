# Bob Tech Notes

一个持续整理的中文技术知识库，用于沉淀学习笔记、实践记录和专题文章。

这里不仅记录“命令怎么写”，也尽量说明相关原理、适用场景、验证方式和风险边界，让内容能够被查阅、复现和长期维护。



## 文档导航

完整分类和归档规则请查看 [docs 文档索引](./docs/README.md)。

| 技术方向 | 技术专题 | 文档 | 内容简介 |
| --- | --- | --- | --- |
| 前端开发 | [JavaScript](./docs/frontend/javascript/README.md) | [JavaScript 基础知识](./docs/frontend/javascript/JavaScript基础知识.md) | 介绍动态类型、作用域与闭包、函数、`this`、原型与 `class`、模块系统、`package.json` 以及异步 JavaScript。 |
| 前端开发 | [TypeScript](./docs/frontend/typescript/README.md) | [TypeScript 基础知识](./docs/frontend/typescript/TypeScript基础知识.md) | 整理语言入门、类型推断与结构类型系统、JavaScript 模块、编译工具及 Handbook 常用类型。 |
| DevOps | [Docker](./docs/devops/docker/README.md) | [Docker 基础知识](./docs/devops/docker/Docker基础知识.md) | 从核心概念、安装和常用命令，逐步讲到数据持久化、镜像构建、网络、Compose 与离线交付。 |



## 目录结构

```text
bob-tech-notes/
├── README.md
├── LICENSE
└── docs/
    ├── README.md
    ├── frontend/
    │   ├── javascript/
    │   │   ├── README.md
    │   │   └── JavaScript基础知识.md
    │   └── typescript/
    │       ├── README.md
    │       └── TypeScript基础知识.md
    └── devops/
        └── docker/
            ├── README.md
            └── Docker基础知识.md
```

文档统一按照 `docs/<技术领域>/<技术或框架>/<文章>.md` 归档。新领域或技术专题在出现第一篇文章时再创建，避免保留大量空目录。



## 文档约定

1. 文件名应直接表达主题；需要区分内容类型时，可使用 `-入门`、`-实战`、`-原理`、`-排错` 等后缀。
2. 不使用容易过时的 `最终版`、`最新版` 等名称；历史稿可以使用日期或 `-原始版本` 标识。
3. 图片和附件存放在文章同级的 `assets/` 目录中，并通过相对路径引用。
4. 一篇文章涉及多个方向时，只在核心主题目录保留一份正文，其他专题通过索引链接引用。
5. 新增、移动或重命名文档后，需要同步更新根目录、`docs/` 和对应专题的 README 索引。



## 阅读和使用

仓库中的文档使用 Markdown 编写，可以直接在 GitHub 中阅读，也可以克隆到本地后通过任意 Markdown 编辑器查看：

```bash
git clone https://github.com/BigBigBob/bob-tech-notes.git
cd bob-tech-notes
```



## 参与完善

如果你发现内容错误、链接失效、示例过时，或者有值得补充的实践经验，欢迎提交 Issue 或 Pull Request。

提交修改时建议：

1. 说明修改的背景、适用版本和验证环境。
2. 将命令、配置和输出放入对应语言的代码块。
3. 不提交密码、API Key、私钥或其他敏感信息。
4. 新增文档时同步更新相关 README 的文档导航。



## 许可证

除非文件中另有说明，本仓库中由维护者原创的文档和文档内示例采用 [Creative Commons Attribution 4.0 International（CC BY 4.0）](./LICENSE) 许可。

你可以复制、转载、修改和再发布这些内容，包括用于商业目的，但需要保留适当署名、提供许可证链接，并说明是否对原内容进行了修改。建议使用以下署名格式：

```text
来源：Bob Tech Notes
作者：BigBigBob
原文：https://github.com/BigBigBob/bob-tech-notes
许可证：CC BY 4.0
```

仓库中明确标注来源或许可证的第三方内容，继续遵循其原有版权和许可条款。未来如加入独立的软件项目或源代码模块，将在对应目录中另行声明适用的软件许可证。

完整许可条款请参阅 [LICENSE](./LICENSE)。
