---
translation_id: home
description: "BigBigBob 的技術知識庫，收錄學習筆記、實作記錄和專題文章。"
---

# Bob Tech Notes

這裡是 BigBigBob 的中文技術知識庫，收錄學習筆記、實作記錄和專題文章。

倉庫文件按照“技術領域 → 技術或框架 → 文章”三級結構組織。



## 當前內容

| 技術領域 | 技術專題 | 文章 |
| --- | --- | --- |
| 前端開發（`frontend`） | [JavaScript](./frontend/javascript/README.md) | [JavaScript 基礎知識](./frontend/javascript/basics.md) |
| 前端開發（`frontend`） | [TypeScript](./frontend/typescript/README.md) | [TypeScript 基礎知識](./frontend/typescript/basics.md) |
| DevOps（`devops`） | [Docker](./devops/docker/README.md) | [Docker 基礎知識](./devops/docker/basics.md) |



## 技術領域命名

新增文件時優先從以下領域中選擇：

| 目錄名 | 技術領域 | 範例 |
| --- | --- | --- |
| `ai` | 人工智慧 | 大模型、Agent、機器學習 |
| `backend` | 後端開發 | Java、Go、資料庫訪問框架 |
| `frontend` | 前端開發 | JavaScript、TypeScript、Vue、React |
| `devops` | DevOps | Docker、Kubernetes、CI/CD、可觀測性 |
| `database` | 資料庫 | MySQL、PostgreSQL、Redis |
| `cloud` | 雲端計算 | 雲平臺、雲原生服務、基礎設施即程式碼 |
| `architecture` | 軟體架構 | 設計模式、系統設計、分散式架構 |
| `tools` | 工具與效率 | Git、IDE、命令列工具 |

如果新內容無法合理歸入現有領域，可以新增語義清晰、使用小寫英文命名的一級目錄。



## 歸檔規則

```text
docs/
└── <技術領域>/
    └── <技術或框架>/
        ├── README.md
        ├── <文章>.md
        └── assets/
```

- 每個技術專題使用 `README.md` 維護文章索引。
- 新領域或專題在出現第一篇文章時再建立，不預建空目錄。
- 檔名應突出主題，可以用 `-入门`、`-实战`、`-原理`、`-排错` 等字尾描述內容型別。
- 圖片、示意圖和附件放在文章同級的 `assets/` 中。
- 新增或調整文件後，同步更新本索引和倉庫的 [README](https://github.com/BigBigBob/bob-tech-notes/blob/main/README.md)。
