# Bob Tech Notes

一个持续整理的中文技术知识库，用于沉淀学习笔记、实践记录和专题文章。

这里不仅记录“命令怎么写”，也尽量说明相关原理、适用场景、验证方式和风险边界，让内容能够被查阅、复现和长期维护。



## 文档导航

| 方向 | 专题 | 文档简介 |
| --- | --- | --- |
| DevOps | [Docker 基础知识](./docs/devops/docker/Docker基础知识.md) | 从核心概念、安装和常用命令，逐步讲到数据持久化、镜像构建、网络、Compose 与离线交付。 |



## 目录结构

```text
bob-tech-notes/
├── README.md
├── LICENSE
└── docs/
    └── devops/
        └── docker/
            └── Docker基础知识.md
```

新增文档按照 `docs/<技术方向>/<专题>/` 的结构归档，并在上方的文档导航中补充入口。



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
4. 新增文档时同步更新本 README 的文档导航。



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
