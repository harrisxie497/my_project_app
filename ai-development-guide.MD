
---

## `docs/ai-development-guide.md`

```md
# AI Development Guide（必读）

本项目使用 AI 编程 IDE（如 Trae）进行开发。
为了避免生成不符合项目结构的代码，请严格遵循以下约定。

---

## 1. 项目基本约定（不可违反）

### 目录结构约定
- 前端代码 **只能** 放在 `frontend/`
- 后端代码 **只能** 放在 `backend/`
- Docker / Nginx / Compose 配置 **只能** 放在 `deploy/`
- 规则模板 **只能** 放在 `rule_templates/`
- 运行数据 **只能** 放在 `data/`（不进 Git）

禁止创建新的顶层目录。

---

## 2. 后端代码规范（FastAPI）

### 目录分层
```