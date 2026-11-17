---
translation_id: home
description: "BigBigBob’s technical knowledge base for study notes, hands-on write-ups, and technical articles."
---

# Bob Tech Notes

This is BigBigBob’s technical knowledge base, originally written in Chinese. It brings together study notes, hands-on write-ups, and articles on specific technologies.

The repository organizes its documentation into three levels: technical area, technology or framework, and article.

## Current notes

| Area | Topic | Article |
| --- | --- | --- |
| Frontend development (`frontend`) | [JavaScript](./frontend/javascript/README.md) | [JavaScript Fundamentals](./frontend/javascript/basics.md) |
| Frontend development (`frontend`) | [TypeScript](./frontend/typescript/README.md) | [TypeScript Fundamentals](./frontend/typescript/basics.md) |
| DevOps (`devops`) | [Docker](./devops/docker/README.md) | [Docker Fundamentals](./devops/docker/basics.md) |

## Naming technical areas

When adding documentation, start with the following technical areas.

| Directory | Area | Examples |
| --- | --- | --- |
| `ai` | Artificial intelligence | Large models, agents, and machine learning |
| `backend` | Backend development | Java, Go, and database access frameworks |
| `frontend` | Frontend development | JavaScript, TypeScript, Vue, and React |
| `devops` | DevOps | Docker, Kubernetes, CI/CD, and observability |
| `database` | Databases | MySQL, PostgreSQL, and Redis |
| `cloud` | Cloud computing | Cloud platforms, cloud-native services, and infrastructure as code |
| `architecture` | Software architecture | Design patterns, system design, and distributed architecture |
| `tools` | Tools and productivity | Git, IDEs, and command-line tools |

If none of the existing areas fits, create a top-level directory with a clear, lowercase English name.

## Organizing notes

```text
docs/
└── <area>/
    └── <technology-or-framework>/
        ├── README.md
        ├── <article>.md
        └── assets/
```

- Use `README.md` to index the articles in each topic.
- Create new areas and topics when their first article is ready to avoid empty directories.
- Give each file a descriptive name. You can add a suffix such as “getting started,” “hands-on,” “concepts,” or “troubleshooting” to distinguish types of articles.
- Keep images, diagrams, and attachments in an `assets/` directory alongside the article.
- When adding or updating documentation, update this index and the repository [README](https://github.com/BigBigBob/bob-tech-notes/blob/main/README.md).
