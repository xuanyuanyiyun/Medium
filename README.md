# Media AI Agent

一站式智能媒体内容生产平台

## 功能特性

- 🤖 **AI 智能创作**：支持文章、视频、图文等多种内容形态的 AI 自动生成
- 📊 **智能选题**：自动聚合多平台热点数据，提供选题建议
- ✅ **内容审核**：多维度内容合规检查，确保发布安全
- 🚀 **一键分发**：支持 8+ 主流内容平台的一键发布
- 📈 **效果分析**：实时追踪内容传播效果，生成数据报告
- 🔧 **自定义工作流**：模块化组装，灵活配置创作流程

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 安装部署

1. 克隆项目
```bash
git clone <repository-url>
cd media-ai-agent
```

2. 配置环境变量
```bash
cp backend/.env.example backend/.env
# 编辑 .env 填写必要的 API 密钥
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问应用
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 技术架构

- **后端**：Python / FastAPI / LangChain
- **前端**：React 18 / TypeScript / TailwindCSS
- **数据库**：PostgreSQL / Redis
- **AI 服务**：OpenAI GPT-4 / Claude

## 项目结构

```
media-ai-agent/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── agents/       # AI Agent 实现
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据模型
│   │   ├── platforms/    # 平台适配器
│   │   └── services/     # 服务层
│   └── tests/            # 测试代码
├── frontend/             # 前端代码
│   └── src/
│       ├── components/   # UI 组件
│       ├── pages/        # 页面组件
│       └── api/          # API 调用
├── docker-compose.yml    # Docker 编排
└── README.md
```

## 许可证

MIT License
