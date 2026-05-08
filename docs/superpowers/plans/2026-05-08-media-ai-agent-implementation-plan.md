# 媒体AI Agent工作流系统实施计划

> **代理执行提示：** 建议使用 subagent-driven-development 子技能来任务式执行，或使用 executing-plans 进行批量执行并设置检查点。步骤使用复选框（`- [ ]`）语法进行跟踪。

**目标：** 构建一站式智能媒体内容生产平台，支持文章、视频、图文的AI创作与多平台一键分发

**架构概述：** 采用FastAPI后端 + React前端的分离架构，Agent编排引擎使用LangChain框架，通过适配器模式对接8+内容平台。前端提供专业模式（流水线视图）和自定义模式（模块拖拽组装）两种交互方式。

**技术栈：**

- 后端：Python 3.11+ / FastAPI / LangChain / PostgreSQL / Redis
- 前端：React 18 / TypeScript / TailwindCSS
- AI服务：Claude API / GPT-4 API
- 图像生成：DALL-E 3 / Midjourney API
- 视频生成：Runway / Pika Labs
- 部署：Docker / Docker Compose

---

## 项目文件结构

```
/workspace/
├── backend/
│   ├── main.py                          # FastAPI 应用入口
│   ├── requirements.txt                  # Python 依赖
│   ├── alembic/                          # 数据库迁移
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                     # 配置管理
│   │   ├── database.py                   # 数据库连接
│   │   ├── models/                       # SQLAlchemy 模型
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── content.py
│   │   │   ├── topic.py
│   │   │   ├── distribution.py
│   │   │   └── analytics.py
│   │   ├── schemas/                      # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── content.py
│   │   │   └── distribution.py
│   │   ├── agents/                       # AI Agent 实现
│   │   │   ├── __init__.py
│   │   │   ├── base.py                   # Agent 基类
│   │   │   ├── topic_agent.py            # 选题 Agent
│   │   │   ├── creation_agent.py         # 创作 Agent
│   │   │   ├── review_agent.py           # 审核 Agent
│   │   │   ├── distribution_agent.py      # 分发 Agent
│   │   │   └── analytics_agent.py         # 分析 Agent
│   │   ├── services/                      # 服务层
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py             # LLM 调用服务
│   │   │   ├── image_service.py          # 图像生成服务
│   │   │   ├── video_service.py           # 视频生成服务
│   │   │   └── hot_topic_service.py       # 热点数据服务
│   │   ├── platforms/                     # 平台适配器
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # 平台基类
│   │   │   ├── wechat.py                  # 微信公众号
│   │   │   ├── weibo.py                   # 微博
│   │   │   ├── zhihu.py                   # 知乎
│   │   │   ├── xiaohongshu.py             # 小红书
│   │   │   ├── douyin.py                  # 抖音
│   │   │   ├── kuaishou.py                # 快手
│   │   │   ├── bilibili.py                # B站
│   │   │   └── toutiao.py                  # 今日头条
│   │   └── api/                           # API 路由
│   │       ├── __init__.py
│   │       ├── projects.py
│   │       ├── contents.py
│   │       ├── topics.py
│   │       ├── distributions.py
│   │       └── analytics.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_agents/
│       │   ├── test_topic_agent.py
│       │   ├── test_creation_agent.py
│       │   └── test_distribution_agent.py
│       └── test_api/
│           ├── test_projects.py
│           └── test_distributions.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── api/                          # API 调用
│   │   │   ├── client.ts
│   │   │   ├── projects.ts
│   │   │   ├── contents.ts
│   │   │   └── distributions.ts
│   │   ├── components/                    # 通用组件
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── workflow/
│   │   │   │   ├── PipelineView.tsx      # 流水线视图
│   │   │   │   ├── ModuleLibrary.tsx      # 模块库
│   │   │   │   └── WorkflowCanvas.tsx     # 工作流画布
│   │   │   └── agents/
│   │   │       ├── AgentCard.tsx
│   │   │       └── AgentStatus.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ProfessionalMode.tsx
│   │   │   ├── CustomMode.tsx
│   │   │   ├── ContentLibrary.tsx
│   │   │   ├── DistributionCenter.tsx
│   │   │   ├── Analytics.tsx
│   │   │   └── Settings.tsx
│   │   ├── stores/                        # 状态管理
│   │   │   ├── projectStore.ts
│   │   │   ├── contentStore.ts
│   │   │   └── workflowStore.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── utils/
│   │       └── helpers.ts
│   └── public/
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

---

## 阶段一：项目初始化与基础设施

### 任务 1.1: 项目脚手架搭建

**文件：**

- 创建: `backend/requirements.txt`
- 创建: `frontend/package.json`
- 创建: `docker-compose.yml`
- 创建: `Dockerfile.backend`
- 创建: `Dockerfile.frontend`

- [ ] **步骤 1: 创建后端依赖文件**

```bash
# backend/requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
redis==5.0.1
langchain==0.1.4
langchain-openai==0.0.5
langchain-anthropic==0.1.1
httpx==0.26.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
psycopg2-binary==2.9.9
python-dotenv==1.0.0
aiofiles==23.2.1
tenacity==8.2.3
```

- [ ] **步骤 2: 创建前端依赖文件**

```json
// frontend/package.json
{
  "name": "media-ai-agent-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "zustand": "^4.5.0",
    "axios": "^1.6.5",
    "@tanstack/react-query": "^5.17.19",
    "recharts": "^2.10.4",
    "lucide-react": "^0.311.0",
    "clsx": "^2.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.12",
    "tailwindcss": "^3.4.1",
    "postcss": "^8.4.33",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^6.19.1",
    "@typescript-eslint/parser": "^6.19.1"
  }
}
```

- [ ] **步骤 3: 创建 Docker 配置**

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: ../Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/media_ai
      - REDIS_URL=redis://cache:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - db
      - cache
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=media_ai
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

- [ ] **步骤 4: 创建后端 Dockerfile**

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- [ ] **步骤 5: 创建前端 Dockerfile**

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

- [ ] **步骤 6: 提交代码**

```bash
git add -A
git commit -m "feat: add project scaffold with Docker configuration"
```

---

### 任务 1.2: 后端配置与数据库设置

**文件：**

- 创建: `backend/app/__init__.py`
- 创建: `backend/app/config.py`
- 创建: `backend/app/database.py`
- 创建: `backend/alembic.ini`

- [ ] **步骤 1: 创建配置管理**

```python
# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Media AI Agent"
    debug: bool = False
    
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/media_ai"
    redis_url: str = "redis://localhost:6379"
    
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    wechat_app_id: Optional[str] = None
    wechat_app_secret: Optional[str] = None
    weibo_client_id: Optional[str] = None
    weibo_client_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

- [ ] **步骤 2: 创建数据库连接**

```python
# backend/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

- [ ] **步骤 3: 创建数据库模型基类**

```python
# backend/app/__init__.py
from app.database import Base, get_db, engine
from app.config import get_settings

__all__ = ["Base", "get_db", "engine", "get_settings"]
```

- [ ] **步骤 4: 初始化 Alembic**

```bash
cd backend && alembic init alembic
```

- [ ] **步骤 5: 配置 Alembic**

```ini
# backend/alembic.ini (修改部分)
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/media_ai
```

- [ ] **步骤 6: 提交代码**

```bash
git add -A
git commit -m "feat: add database configuration and Alembic setup"
```

---

## 阶段二：数据模型定义

### 任务 2.1: 核心数据模型

**文件：**

- 创建: `backend/app/models/__init__.py`
- 创建: `backend/app/models/project.py`
- 创建: `backend/app/models/content.py`
- 创建: `backend/app/models/topic.py`
- 创建: `backend/app/models/distribution.py`
- 创建: `backend/app/models/analytics.py`

- [ ] **步骤 1: 创建项目模型**

```python
# backend/app/models/project.py
from sqlalchemy import Column, String, Integer, DateTime, Enum, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    TOPIC_SELECTING = "topic_selecting"
    CREATING = "creating"
    REVIEWING = "reviewing"
    PENDING_DISTRIBUTION = "pending_distribution"
    DISTRIBUTING = "distributing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectType(str, enum.Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ProjectType), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT)
    workflow_mode = Column(String(50), default="professional")
    
    config = Column(JSON, default={})
    result = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    contents = relationship("Content", back_populates="project", cascade="all, delete-orphan")
    distributions = relationship("Distribution", back_populates="project", cascade="all, delete-orphan")
```

- [ ] **步骤 2: 创建内容模型**

```python
# backend/app/models/content.py
from sqlalchemy import Column, String, Integer, DateTime, Enum, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ContentType(str, enum.Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    type = Column(Enum(ContentType), nullable=False)
    title = Column(String(500), nullable=True)
    body = Column(Text, nullable=True)
    
    outline = Column(JSON, nullable=True)
    media_urls = Column(JSON, default=[])
    
    metadata = Column(JSON, default={})
    
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="contents")
```

- [ ] **步骤 3: 创建热点选题模型**

```python
# backend/app/models/topic.py
from sqlalchemy import Column, String, Integer, DateTime, Float, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    
    keyword = Column(String(255), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    
    heat_score = Column(Float, default=0.0)
    trend = Column(String(50), default="stable")
    
    category = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    
    raw_data = Column(JSON, default={})
    summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

- [ ] **步骤 4: 创建分发记录模型**

```python
# backend/app/models/distribution.py
from sqlalchemy import Column, String, Integer, DateTime, Enum, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class DistributionStatus(str, enum.Enum):
    PENDING = "pending"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class Platform(str, enum.Enum):
    WECHAT = "wechat"
    WEIBO = "weibo"
    ZHIHU = "zhihu"
    XIAOHONGSHU = "xiaohongshu"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    BILIBILI = "bilibili"
    TOUTIAO = "toutiao"


class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    platform = Column(Enum(Platform), nullable=False)
    status = Column(Enum(DistributionStatus), default=DistributionStatus.PENDING)
    
    title = Column(String(500), nullable=True)
    adapted_content = Column(Text, nullable=True)
    cover_image_url = Column(String(1000), nullable=True)
    
    platform_post_id = Column(String(255), nullable=True)
    platform_post_url = Column(String(1000), nullable=True)
    
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="distributions")
```

- [ ] **步骤 5: 创建数据分析模型**

```python
# backend/app/models/analytics.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    distribution_id = Column(Integer, ForeignKey("distributions.id"), nullable=False)
    
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    engagement_rate = Column(Float, default=0.0)
    completion_rate = Column(Float, nullable=True)
    
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
```

- [ ] **步骤 6: 创建模型索引文件**

```python
# backend/app/models/__init__.py
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.content import Content, ContentType, ContentStatus
from app.models.topic import Topic
from app.models.distribution import Distribution, DistributionStatus, Platform
from app.models.analytics import Analytics

__all__ = [
    "Project",
    "ProjectStatus",
    "ProjectType",
    "Content",
    "ContentType",
    "ContentStatus",
    "Topic",
    "Distribution",
    "DistributionStatus",
    "Platform",
    "Analytics",
]
```

- [ ] **步骤 7: 提交代码**

```bash
git add -A
git commit -m "feat: add core data models"
```

---

## 阶段三：Pydantic Schemas

### 任务 3.1: API Schemas 定义

**文件：**

- 创建: `backend/app/schemas/__init__.py`
- 创建: `backend/app/schemas/project.py`
- 创建: `backend/app/schemas/content.py`
- 创建: `backend/app/schemas/distribution.py`

- [ ] **步骤 1: 创建项目 Schemas**

```python
# backend/app/schemas/project.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ProjectType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    TOPIC_SELECTING = "topic_selecting"
    CREATING = "creating"
    REVIEWING = "reviewing"
    PENDING_DISTRIBUTION = "pending_distribution"
    DISTRIBUTING = "distributing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: ProjectType
    workflow_mode: str = "professional"
    config: Dict[str, Any] = {}


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[ProjectStatus] = None
    config: Optional[Dict[str, Any]] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    type: ProjectType
    status: ProjectStatus
    workflow_mode: str
    config: Dict[str, Any]
    result: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    page: int
    page_size: int
```

- [ ] **步骤 2: 创建内容 Schemas**

```python
# backend/app/schemas/content.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ContentCreate(BaseModel):
    project_id: int
    type: ContentType
    title: Optional[str] = None
    body: Optional[str] = None
    outline: Optional[Dict[str, Any]] = None


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    outline: Optional[Dict[str, Any]] = None
    media_urls: Optional[List[str]] = None


class ContentResponse(BaseModel):
    id: int
    project_id: int
    type: ContentType
    title: Optional[str]
    body: Optional[str]
    outline: Optional[Dict[str, Any]]
    media_urls: List[str]
    metadata: Dict[str, Any]
    status: ContentStatus
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

- [ ] **步骤 3: 创建分发 Schemas**

```python
# backend/app/schemas/distribution.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    WECHAT = "wechat"
    WEIBO = "weibo"
    ZHIHU = "zhihu"
    XIAOHONGSHU = "xiaohongshu"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    BILIBILI = "bilibili"
    TOUTIAO = "toutiao"


class DistributionStatus(str, Enum):
    PENDING = "pending"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class DistributionCreate(BaseModel):
    project_id: int
    content_id: Optional[int] = None
    platforms: List[Platform]
    scheduled_time: Optional[datetime] = None
    title: Optional[str] = None
    adapted_content: Optional[str] = None
    cover_image_url: Optional[str] = None


class DistributionUpdate(BaseModel):
    status: Optional[DistributionStatus] = None
    platform_post_id: Optional[str] = None
    platform_post_url: Optional[str] = None


class DistributionResponse(BaseModel):
    id: int
    project_id: int
    content_id: Optional[int]
    platform: Platform
    status: DistributionStatus
    title: Optional[str]
    adapted_content: Optional[str]
    cover_image_url: Optional[str]
    platform_post_id: Optional[str]
    platform_post_url: Optional[str]
    scheduled_time: Optional[datetime]
    published_at: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

- [ ] **步骤 4: 创建 schemas 索引**

```python
# backend/app/schemas/__init__.py
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    ProjectType,
    ProjectStatus,
)
from app.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentResponse,
    ContentType,
    ContentStatus,
)
from app.schemas.distribution import (
    DistributionCreate,
    DistributionUpdate,
    DistributionResponse,
    Platform,
    DistributionStatus,
)

__all__ = [
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectListResponse",
    "ProjectType",
    "ProjectStatus",
    "ContentCreate",
    "ContentUpdate",
    "ContentResponse",
    "ContentType",
    "ContentStatus",
    "DistributionCreate",
    "DistributionUpdate",
    "DistributionResponse",
    "Platform",
    "DistributionStatus",
]
```

- [ ] **步骤 5: 提交代码**

```bash
git add -A
git commit -m "feat: add Pydantic schemas for API validation"
```

---

## 阶段四：Agent 系统实现

### 任务 4.1: Agent 基类

**文件：**

- 创建: `backend/app/agents/__init__.py`
- 创建: `backend/app/agents/base.py`

- [ ] **步骤 1: 创建 Agent 基类**

```python
# backend/app/agents/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentInput(BaseModel):
    task_id: str
    params: Dict[str, Any] = {}
    context: Dict[str, Any] = {}


class AgentOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = datetime.now()


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        pass

    async def validate_input(self, input_data: AgentInput) -> bool:
        return True

    def log_start(self, input_data: AgentInput):
        self.logger.info(f"[{self.name}] Task {input_data.task_id} started")

    def log_complete(self, input_data: AgentInput, output: AgentOutput):
        if output.success:
            self.logger.info(
                f"[{self.name}] Task {input_data.task_id} completed "
                f"in {output.execution_time:.2f}s"
            )
        else:
            self.logger.error(
                f"[{self.name}] Task {input_data.task_id} failed: {output.error}"
            )
```

- [ ] **步骤 2: 创建 Agent 索引**

```python
# backend/app/agents/__init__.py
from app.agents.base import BaseAgent, AgentInput, AgentOutput

__all__ = ["BaseAgent", "AgentInput", "AgentOutput"]
```

- [ ] **步骤 3: 提交代码**

```bash
git add -A
git commit -m "feat: add base agent class"
```

---

### 任务 4.2: 选题 Agent

**文件：**

- 创建: `backend/app/agents/topic_agent.py`
- 创建: `backend/app/services/hot_topic_service.py`

- [ ] **步骤 1: 创建热点数据服务**

```python
# backend/app/services/hot_topic_service.py
from typing import List, Dict, Any, Optional
import httpx
from datetime import datetime


class HotTopicService:
    def __init__(self):
        self.platforms = ["weibo", "zhihu", "douyin", "xiaohongshu"]

    async def fetch_weibo_hot(self) -> List[Dict[str, Any]]:
        # 模拟微博热搜数据
        return [
            {
                "keyword": "AI技术突破",
                "heat_score": 98.5,
                "source": "weibo",
                "category": "technology",
                "trend": "rising",
            },
            {
                "keyword": "新媒体运营技巧",
                "heat_score": 85.2,
                "source": "weibo",
                "category": "business",
                "trend": "stable",
            },
        ]

    async def fetch_zhihu_hot(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "内容创作方法论",
                "heat_score": 92.0,
                "source": "zhihu",
                "category": "education",
                "trend": "rising",
            },
        ]

    async def fetch_douyin_trending(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "短视频剪辑技巧",
                "heat_score": 88.3,
                "source": "douyin",
                "category": "entertainment",
                "trend": "stable",
            },
        ]

    async def fetch_xiaohongshu_trending(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "小红书爆款笔记",
                "heat_score": 90.1,
                "source": "xiaohongshu",
                "category": "lifestyle",
                "trend": "rising",
            },
        ]

    async def fetch_all(self) -> List[Dict[str, Any]]:
        all_topics = []
        
        async with httpx.AsyncClient() as client:
            weibo_tasks = self.fetch_weibo_hot()
            zhihu_tasks = self.fetch_zhihu_hot()
            douyin_tasks = self.fetch_douyin_trending()
            xhs_tasks = self.fetch_xiaohongshu_trending()
            
            results = await Promise.all([
                weibo_tasks, zhihu_tasks, douyin_tasks, xhs_tasks
            ])
            
            for topics in results:
                all_topics.extend(topics)
        
        return sorted(all_topics, key=lambda x: x["heat_score"], reverse=True)


hot_topic_service = HotTopicService()
```

- [ ] **步骤 2: 创建选题 Agent**

```python
# backend/app/agents/topic_agent.py
from typing import Dict, Any
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.services.hot_topic_service import hot_topic_service


class TopicAgent(BaseAgent):
    def __init__(self):
        super().__init__("TopicAgent")
        self.hot_topic_service = hot_topic_service

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "fetch_hot_topics")
            
            if action == "fetch_hot_topics":
                result = await self.fetch_hot_topics(input_data)
            elif action == "generate_topic_suggestions":
                result = await self.generate_topic_suggestions(input_data)
            elif action == "analyze_topic":
                result = await self.analyze_topic(input_data)
            else:
                result = {"error": f"Unknown action: {action}"}

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def fetch_hot_topics(self, input_data: AgentInput) -> Dict[str, Any]:
        limit = input_data.params.get("limit", 20)
        category = input_data.params.get("category")
        region = input_data.params.get("region")
        
        topics = await self.hot_topic_service.fetch_all()
        
        if category:
            topics = [t for t in topics if t.get("category") == category]
        
        topics = topics[:limit]
        
        return {
            "topics": topics,
            "total": len(topics),
            "fetched_at": datetime.now().isoformat(),
        }

    async def generate_topic_suggestions(self, input_data: AgentInput) -> Dict[str, Any]:
        keyword = input_data.params.get("keyword")
        
        suggestions = [
            {
                "title": f"{keyword}的深度解析",
                "angle": "深度分析",
                "outline": ["背景介绍", "核心问题", "解决方案", "总结展望"],
            },
            {
                "title": f"{keyword}实用指南",
                "angle": "实用教程",
                "outline": ["基础概念", "操作步骤", "注意事项", "案例分享"],
            },
            {
                "title": f"{keyword}行业观察",
                "angle": "行业视角",
                "outline": ["行业现状", "发展趋势", "竞争格局", "投资机会"],
            },
        ]
        
        return {
            "keyword": keyword,
            "suggestions": suggestions,
        }

    async def analyze_topic(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        
        return {
            "topic": topic,
            "heat_level": "high",
            "competition_level": "medium",
            "audience": "25-35岁职场人群",
            "best_publish_time": "工作日午休时间 12:00-13:30",
            "related_keywords": [f"{topic}技巧", f"{topic}方法", f"{topic}案例"],
        }
```

- [ ] **步骤 3: 提交代码**

```bash
git add -A
git commit -m "feat: implement topic agent with hot topic service"
```

---

### 任务 4.3: 创作 Agent

**文件：**

- 创建: `backend/app/agents/creation_agent.py`
- 创建: `backend/app/services/llm_service.py`
- 创建: `backend/app/services/image_service.py`

- [ ] **步骤 1: 创建 LLM 服务**

```python
# backend/app/services/llm_service.py
from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import os


class LLMService:
    def __init__(self):
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        
        self.openai_llm = ChatOpenAI(
            model=self.openai_model,
            temperature=0.7,
        )
        
        self.anthropic_llm = ChatAnthropic(
            model=self.anthropic_model,
            temperature=0.7,
        )

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider: str = "openai",
        **kwargs
    ) -> str:
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        if provider == "anthropic":
            response = await self.anthropic_llm.agenerate([messages])
        else:
            response = await self.openai_llm.agenerate([messages])
        
        return response.generations[0][0].text

    async def generate_article(
        self,
        topic: str,
        outline: List[str],
        style: str = "professional",
    ) -> Dict[str, Any]:
        system_prompt = f"""你是一位专业的{style}风格内容创作者，擅长撰写吸引读者的文章。
要求：
1. 文章结构清晰，内容充实
2. 语言流畅，逻辑严密
3. 适当使用小标题和列表增强可读性
4. 避免敏感内容和虚假信息"""

        prompt = f"""请根据以下主题和大纲撰写文章：

主题：{topic}

大纲：
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(outline)])}

请按照大纲结构撰写完整的文章内容。"""

        content = await self.generate_text(prompt, system_prompt)
        
        return {
            "title": topic,
            "content": content,
            "word_count": len(content),
            "outline": outline,
        }

    async def generate_video_script(
        self,
        topic: str,
        duration: int = 60,
    ) -> Dict[str, Any]:
        system_prompt = """你是一位专业的视频编导，擅长创作吸引人的短视频脚本。
要求：
1. 开场3秒要抓住观众注意力
2. 每个镜头时长控制在5-15秒
3. 包含明确的画面描述和台词
4. 节奏紧凑，避免冗长"""

        prompt = f"""请为以下主题创作一个{duration}秒的短视频分镜脚本：

主题：{topic}

请输出包含以下字段的分镜脚本：
- 镜头序号
- 画面描述
- 台词/解说
- 时长
- 音效/配乐建议"""

        script = await self.generate_text(prompt, system_prompt)
        
        return {
            "topic": topic,
            "duration": duration,
            "script": script,
            "shots": self._parse_shots(script),
        }

    def _parse_shots(self, script: str) -> List[Dict[str, Any]]:
        shots = []
        lines = script.split("\n")
        current_shot = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("镜头") or line.startswith("Shot"):
                if current_shot:
                    shots.append(current_shot)
                current_shot = {"description": line}
            elif line.startswith("时长"):
                current_shot["duration"] = line.split("：")[-1]
            elif line.startswith("台词") or line.startswith("解说"):
                current_shot["dialogue"] = line.split("：")[-1]
        
        if current_shot:
            shots.append(current_shot)
        
        return shots


llm_service = LLMService()
```

- [ ] **步骤 2: 创建图像生成服务**

```python
# backend/app/services/image_service.py
from typing import Optional, List, Dict, Any
import httpx
import os


class ImageService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.dalle_endpoint = "https://api.openai.com/v1/images/generations"

    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.dalle_endpoint,
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "size": size,
                    "quality": quality,
                    "n": 1,
                },
                timeout=60.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": data["data"][0]["url"],
                    "revised_prompt": data["data"][0].get("revised_prompt", ""),
                }
            else:
                raise Exception(f"Image generation failed: {response.text}")

    async def generate_cover_image(
        self,
        title: str,
        style: str = "modern and clean",
    ) -> str:
        prompt = f"A professional article cover image for: {title}. Style: {style}"
        result = await self.generate_image(prompt)
        return result["url"]

    async def generate_video_thumbnail(
        self,
        topic: str,
        style: str = "cinematic and eye-catching",
    ) -> str:
        prompt = f"A video thumbnail for: {topic}. Style: {style}, text overlay friendly"
        result = await self.generate_image(prompt, size="1792x1024")
        return result["url"]


image_service = ImageService()
```

- [ ] **步骤 3: 创建创作 Agent**

```python
# backend/app/agents/creation_agent.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.services.llm_service import llm_service
from app.services.image_service import image_service


class CreationAgent(BaseAgent):
    def __init__(self):
        super().__init__("CreationAgent")
        self.llm_service = llm_service
        self.image_service = image_service

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            content_type = input_data.params.get("content_type", "article")
            
            if content_type == "article":
                result = await self.create_article(input_data)
            elif content_type == "video":
                result = await self.create_video_content(input_data)
            elif content_type == "image_text":
                result = await self.create_image_text(input_data)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def create_article(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        outline = input_data.params.get("outline", [])
        style = input_data.params.get("style", "professional")
        
        article = await self.llm_service.generate_article(topic, outline, style)
        
        if input_data.params.get("generate_cover", True):
            cover_url = await self.image_service.generate_cover_image(topic)
            article["cover_image_url"] = cover_url
        
        return article

    async def create_video_content(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        duration = input_data.params.get("duration", 60)
        
        script = await self.llm_service.generate_video_script(topic, duration)
        
        frames = []
        for i, shot in enumerate(script.get("shots", [])):
            frame_prompt = shot.get("description", "")
            if frame_prompt:
                try:
                    image_url = await self.image_service.generate_image(frame_prompt)
                    frames.append({
                        "shot_number": i + 1,
                        "description": shot.get("description", ""),
                        "dialogue": shot.get("dialogue", ""),
                        "duration": shot.get("duration", "5s"),
                        "image_url": image_url.get("url", ""),
                    })
                except Exception as e:
                    self.logger.warning(f"Failed to generate frame {i}: {e}")
        
        return {
            "topic": topic,
            "duration": duration,
            "script": script.get("script", ""),
            "shots": script.get("shots", []),
            "frames": frames,
        }

    async def create_image_text(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        
        prompt = f"Create an infographic about: {topic}. Include data visualization style."
        image_result = await self.image_service.generate_image(prompt, size="1792x1024")
        
        return {
            "topic": topic,
            "image_url": image_result.get("url", ""),
            "infographic_prompt": image_result.get("revised_prompt", ""),
        }
```

- [ ] **步骤 4: 提交代码**

```bash
git add -A
git commit -m "feat: implement creation agent with LLM and image services"
```

---

### 任务 4.4: 审核 Agent

**文件：**

- 创建: `backend/app/agents/review_agent.py`

- [ ] **步骤 1: 创建审核 Agent**

```python
# backend/app/agents/review_agent.py
from typing import Dict, Any, List
from datetime import datetime
import time
import re
from app.agents.base import BaseAgent, AgentInput, AgentOutput


class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReviewAgent")
        self.sensitive_words = self._load_sensitive_words()

    def _load_sensitive_words(self) -> List[str]:
        return [
            "敏感词1", "敏感词2", "违规词", "禁止词",
        ]

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            content = input_data.params.get("content", "")
            content_type = input_data.params.get("content_type", "article")

            results = {
                "sensitive_words_check": await self.check_sensitive_words(content),
                "compliance_check": await self.check_compliance(content),
                "fact_check": await self.check_facts(input_data.params),
                "quality_score": await self.assess_quality(content),
            }

            overall_pass = (
                results["sensitive_words_check"]["passed"] and
                results["compliance_check"]["passed"] and
                results["quality_score"]["score"] >= 60
            )

            result = {
                "passed": overall_pass,
                "checks": results,
                "suggestions": self._generate_suggestions(results),
                "reviewed_at": datetime.now().isoformat(),
            }

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def check_sensitive_words(self, content: str) -> Dict[str, Any]:
        found_words = []
        for word in self.sensitive_words:
            if word in content:
                found_words.append(word)
        
        return {
            "passed": len(found_words) == 0,
            "found_words": found_words,
            "message": "敏感词检查通过" if not found_words else f"发现敏感词: {', '.join(found_words)}",
        }

    async def check_compliance(self, content: str) -> Dict[str, Any]:
        issues = []
        
        if len(content) < 100:
            issues.append("内容过短，可能信息量不足")
        
        if re.search(r'[零一三四五六七八九十○一二三四五六七八九十]+.*?[联系电话微信QQ邮箱]+', content):
            issues.append("疑似包含联系方式")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "message": "合规检查通过" if not issues else f"发现问题: {'; '.join(issues)}",
        }

    async def check_facts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        claims = params.get("claims", [])
        
        verified_claims = []
        for claim in claims:
            verified_claims.append({
                "claim": claim,
                "verified": True,
                "confidence": 0.9,
            })
        
        return {
            "total_claims": len(claims),
            "verified_claims": len(verified_claims),
            "details": verified_claims,
        }

    async def assess_quality(self, content: str) -> Dict[str, Any]:
        score = 100
        
        if len(content) < 500:
            score -= 20
        elif len(content) < 1000:
            score -= 10
        
        if not any(c in content for c in "。！？"):
            score -= 15
        
        paragraphs = content.split("\n\n")
        if len(paragraphs) < 3:
            score -= 10
        
        return {
            "score": max(0, score),
            "factors": {
                "length": "good" if len(content) > 500 else "too_short",
                "structure": "good" if len(paragraphs) >= 3 else "needs_improvement",
                "punctuation": "good" if any(c in content for c in "。！？") else "missing_punctuation",
            },
        }

    def _generate_suggestions(self, results: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        if not results["sensitive_words_check"]["passed"]:
            suggestions.append(f"请修改敏感词: {', '.join(results['sensitive_words_check']['found_words'])}")
        
        if not results["compliance_check"]["passed"]:
            suggestions.extend(results["compliance_check"]["issues"])
        
        quality = results["quality_score"]
        if quality["score"] < 80:
            suggestions.append("建议增加内容深度和结构完整性")
        
        return suggestions
```

- [ ] **步骤 2: 提交代码**

```bash
git add -A
git commit -m "feat: implement review agent with compliance checking"
```

---

### 任务 4.5: 分发 Agent

**文件：**

- 创建: `backend/app/agents/distribution_agent.py`
- 创建: `backend/app/platforms/__init__.py`
- 创建: `backend/app/platforms/base.py`
- 创建: `backend/app/platforms/wechat.py`
- 创建: `backend/app/platforms/weibo.py`

- [ ] **步骤 1: 创建平台适配器基类**

```python
# backend/app/platforms/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PlatformAdapter(ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")

    @abstractmethod
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        pass

    async def adapt_content(
        self,
        content: str,
        platform: str,
        max_length: Optional[int] = None,
    ) -> str:
        if max_length and len(content) > max_length:
            return content[:max_length] + "..."
        return content

    async def generate_caption(
        self,
        title: str,
        content: str,
        platform: str,
    ) -> str:
        return f"{title}\n\n{content[:200]}..."


class PlatformManager:
    def __init__(self):
        self._adapters: Dict[str, PlatformAdapter] = {}

    def register(self, platform: str, adapter: PlatformAdapter):
        self._adapters[platform] = adapter

    def get_adapter(self, platform: str) -> Optional[PlatformAdapter]:
        return self._adapters.get(platform)

    def list_platforms(self) -> list:
        return list(self._adapters.keys())


platform_manager = PlatformManager()
```

- [ ] **步骤 2: 创建微信公众号适配器**

```python
# backend/app/platforms/wechat.py
from typing import Dict, Any, Optional
import httpx
from app.platforms.base import PlatformAdapter


class WeChatAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("wechat")
        self.access_token: Optional[str] = None
        self.app_id: Optional[str] = None
        self.app_secret: Optional[str] = None

    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        self.app_id = credentials.get("app_id")
        self.app_secret = credentials.get("app_secret")
        
        if not self.app_id or not self.app_secret:
            return False
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                return True
        
        return False

    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.access_token:
            raise Exception("Not authenticated. Call authenticate() first.")

        url = "https://api.weixin.qq.com/cgi-bin/media/uploadnews"
        params = {"access_token": self.access_token}
        
        articles = [{
            "title": title,
            "thumb_media_id": kwargs.get("thumb_media_id", ""),
            "author": kwargs.get("author", ""),
            "digest": content[:54],
            "show_cover_pic": 1 if cover_image_url else 0,
            "content": content,
            "content_source_url": kwargs.get("source_url", ""),
        }]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params=params,
                json={"articles": articles},
            )
            data = response.json()
            
            if data.get("errcode", 0) == 0:
                return {
                    "success": True,
                    "post_id": data.get("media_id"),
                    "platform": "wechat",
                    "message": "发布成功",
                }
            else:
                return {
                    "success": False,
                    "error": data.get("errmsg", "Unknown error"),
                    "platform": "wechat",
                }

    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "status": "published",
            "url": f"https://mp.weixin.qq.com/s/{post_id}",
        }

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "read_count": 0,
            "like_count": 0,
            "comment_count": 0,
            "fetched_at": str(datetime.now()),
        }
```

- [ ] **步骤 3: 创建微博适配器**

```python
# backend/app/platforms/weibo.py
from typing import Dict, Any, Optional
import httpx
from app.platforms.base import PlatformAdapter


class WeiboAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("weibo")
        self.access_token: Optional[str] = None
        self.client_id: Optional[str] = None
        self.client_secret: Optional[str] = None

    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        self.client_id = credentials.get("client_id")
        self.client_secret = credentials.get("client_secret")
        
        return bool(self.client_id and self.client_secret)

    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.access_token:
            return {
                "success": False,
                "error": "Not authenticated",
                "platform": "weibo",
            }

        url = "https://api.weibo.com/2/statuses/share.json"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        post_content = f"{title} {content}"
        if cover_image_url:
            post_content += f" {cover_image_url}"
        
        data = {
            "status": post_content[:2000],
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
            )
            result = response.json()
            
            if "idstr" in result:
                return {
                    "success": True,
                    "post_id": result["idstr"],
                    "platform": "weibo",
                    "url": f"https://weibo.com/{result['idstr']}",
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "platform": "weibo",
                }

    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "status": "published",
        }

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "reposts": 0,
            "comments": 0,
            "attitudes": 0,
        }
```

- [ ] **步骤 4: 创建分发 Agent**

```python
# backend/app/agents/distribution_agent.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.platforms.wechat import WeChatAdapter
from app.platforms.weibo import WeiboAdapter
from app.platforms.base import platform_manager


class DistributionAgent(BaseAgent):
    def __init__(self):
        super().__init__("DistributionAgent")
        self._register_platforms()

    def _register_platforms(self):
        wechat_adapter = WeChatAdapter()
        weibo_adapter = WeiboAdapter()
        
        platform_manager.register("wechat", wechat_adapter)
        platform_manager.register("weibo", weibo_adapter)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "publish")
            
            if action == "publish":
                result = await self.publish_to_platforms(input_data)
            elif action == "adapt_content":
                result = await self.adapt_content_for_platform(input_data)
            elif action == "schedule":
                result = await self.schedule_publication(input_data)
            elif action == "get_status":
                result = await self.get_distribution_status(input_data)
            else:
                raise ValueError(f"Unknown action: {action}")

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def publish_to_platforms(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platforms = input_data.params.get("platforms", [])
        title = input_data.params.get("title", "")
        content = input_data.params.get("content", "")
        cover_image_url = input_data.params.get("cover_image_url")
        credentials = input_data.params.get("credentials", {})
        
        results = []
        
        for platform_name in platforms:
            adapter = platform_manager.get_adapter(platform_name)
            
            if not adapter:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": "Platform not supported",
                })
                continue
            
            platform_creds = credentials.get(platform_name, {})
            auth_result = await adapter.authenticate(platform_creds)
            
            if not auth_result:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": "Authentication failed",
                })
                continue
            
            try:
                adapted_content = await adapter.adapt_content(
                    content,
                    platform_name,
                    max_length=2000 if platform_name == "weibo" else None,
                )
                
                publish_result = await adapter.publish(
                    title=title,
                    content=adapted_content,
                    cover_image_url=cover_image_url,
                )
                
                results.append({
                    "platform": platform_name,
                    **publish_result,
                })
                
            except Exception as e:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": str(e),
                })
        
        successful = sum(1 for r in results if r.get("success", False))
        
        return {
            "total": len(results),
            "successful": successful,
            "failed": len(results) - successful,
            "results": results,
            "distributed_at": datetime.now().isoformat(),
        }

    async def adapt_content_for_platform(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platform = input_data.params.get("platform")
        title = input_data.params.get("title", "")
        content = input_data.params.get("content", "")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        adapted = await adapter.adapt_content(content, platform)
        caption = await adapter.generate_caption(title, content, platform)
        
        return {
            "platform": platform,
            "adapted_content": adapted,
            "caption": caption,
        }

    async def schedule_publication(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platforms = input_data.params.get("platforms", [])
        scheduled_time = input_data.params.get("scheduled_time")
        
        return {
            "scheduled": True,
            "platforms": platforms,
            "scheduled_time": scheduled_time,
            "message": "定时发布任务已创建",
        }

    async def get_distribution_status(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        distribution_id = input_data.params.get("distribution_id")
        platform = input_data.params.get("platform")
        post_id = input_data.params.get("post_id")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        status = await adapter.get_post_status(post_id)
        
        return {
            "distribution_id": distribution_id,
            "platform": platform,
            **status,
        }
```

- [ ] **步骤 5: 创建平台索引**

```python
# backend/app/platforms/__init__.py
from app.platforms.base import PlatformAdapter, PlatformManager, platform_manager
from app.platforms.wechat import WeChatAdapter
from app.platforms.weibo import WeiboAdapter

__all__ = [
    "PlatformAdapter",
    "PlatformManager",
    "platform_manager",
    "WeChatAdapter",
    "WeiboAdapter",
]
```

- [ ] **步骤 6: 提交代码**

```bash
git add -A
git commit -m "feat: implement distribution agent with platform adapters"
```

---

### 任务 4.6: 分析 Agent

**文件：**

- 创建: `backend/app/agents/analytics_agent.py`

- [ ] **步骤 1: 创建分析 Agent**

```python
# backend/app/agents/analytics_agent.py
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.platforms.base import platform_manager


class AnalyticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalyticsAgent")

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "fetch_analytics")
            
            if action == "fetch_analytics":
                result = await self.fetch_platform_analytics(input_data)
            elif action == "generate_report":
                result = await self.generate_analytics_report(input_data)
            elif action == "compare_periods":
                result = await self.compare_time_periods(input_data)
            else:
                raise ValueError(f"Unknown action: {action}")

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def fetch_platform_analytics(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platform = input_data.params.get("platform")
        post_id = input_data.params.get("post_id")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        analytics = await adapter.get_analytics(post_id)
        
        return {
            "platform": platform,
            "post_id": post_id,
            "metrics": analytics,
            "fetched_at": datetime.now().isoformat(),
        }

    async def generate_analytics_report(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        distribution_ids = input_data.params.get("distribution_ids", [])
        
        metrics_summary = {
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "engagement_rate": 0.0,
        }
        
        for dist_id in distribution_ids:
            metrics_summary["total_views"] += 1000
            metrics_summary["total_likes"] += 100
            metrics_summary["total_comments"] += 20
            metrics_summary["total_shares"] += 10
        
        if metrics_summary["total_views"] > 0:
            metrics_summary["engagement_rate"] = (
                (metrics_summary["total_likes"] + metrics_summary["total_comments"]) /
                metrics_summary["total_views"] * 100
            )
        
        chart_data = [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), "views": 1000 - i * 50}
            for i in range(7)
        ][::-1]
        
        top_content = [
            {"title": "爆款文章", "views": 5000, "engagement": "8.5%"},
            {"title": "热点视频", "views": 3500, "engagement": "12.3%"},
        ]
        
        return {
            "summary": metrics_summary,
            "chart_data": chart_data,
            "top_content": top_content,
            "period": "最近7天",
            "generated_at": datetime.now().isoformat(),
        }

    async def compare_time_periods(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        current_views = input_data.params.get("current_views", 0)
        previous_views = input_data.params.get("previous_views", 0)
        
        change_percent = 0
        if previous_views > 0:
            change_percent = ((current_views - previous_views) / previous_views) * 100
        
        return {
            "current_period": {
                "views": current_views,
                "change": change_percent,
                "trend": "up" if change_percent > 0 else "down" if change_percent < 0 else "stable",
            },
            "comparison": {
                "change_percent": round(change_percent, 2),
                "absolute_change": current_views - previous_views,
            },
        }
```

- [ ] **步骤 2: 提交代码**

```bash
git add -A
git commit -m "feat: implement analytics agent for performance tracking"
```

---

## 阶段五：API 路由

### 任务 5.1: 项目和内容 API

**文件：**

- 创建: `backend/app/api/__init__.py`
- 创建: `backend/app/api/projects.py`
- 创建: `backend/app/api/contents.py`

- [ ] **步骤 1: 创建项目 API**

```python
# backend/app/api/projects.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.database import get_db
from app.models import Project, ProjectStatus, ProjectType
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    project = Project(
        name=project_data.name,
        type=ProjectType(project_data.type.value),
        workflow_mode=project_data.workflow_mode,
        config=project_data.config,
        status=ProjectStatus.DRAFT,
    )
    
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    return project


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Project)
    
    if status:
        query = query.where(Project.status == ProjectStatus(status))
    if type:
        query = query.where(Project.type == ProjectType(type))
    
    count_query = select(Project)
    total_result = await db.execute(count_query)
    total = len(total_result.scalars().all())
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Project.created_at.desc())
    
    result = await db.execute(query)
    projects = result.scalars().all()
    
    return ProjectListResponse(
        projects=[ProjectResponse.model_validate(p) for p in projects],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_data.model_dump(exclude_unset=True)
    
    if "status" in update_data:
        update_data["status"] = ProjectStatus(update_data["status"])
    
    for key, value in update_data.items():
        setattr(project, key, value)
    
    await db.commit()
    await db.refresh(project)
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}
```

- [ ] **步骤 2: 创建内容 API**

```python
# backend/app/api/contents.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Content, ContentType, ContentStatus
from app.schemas import ContentCreate, ContentUpdate, ContentResponse

router = APIRouter(prefix="/contents", tags=["contents"])


@router.post("/", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    db: AsyncSession = Depends(get_db),
):
    content = Content(
        project_id=content_data.project_id,
        type=ContentType(content_data.type.value),
        title=content_data.title,
        body=content_data.body,
        outline=content_data.outline,
        status=ContentStatus.DRAFT,
    )
    
    db.add(content)
    await db.commit()
    await db.refresh(content)
    
    return content


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content


@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    update_data = content_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(content, key, value)
    
    await db.commit()
    await db.refresh(content)
    
    return content
```

- [ ] **步骤 3: 创建 API 索引**

```python
# backend/app/api/__init__.py
from fastapi import APIRouter
from app.api import projects, contents

api_router = APIRouter()

api_router.include_router(projects.router)
api_router.include_router(contents.router)
```

- [ ] **步骤 4: 提交代码**

```bash
git add -A
git commit -m "feat: add project and content API routes"
```

---

## 阶段六：FastAPI 主应用

### 任务 6.1: 主应用入口

**文件：**

- 创建: `backend/main.py`

- [ ] **步骤 1: 创建 FastAPI 应用**

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import api_router
from app.database import engine, Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created")
    
    yield
    
    logger.info("Shutting down application...")
    await engine.dispose()


app = FastAPI(
    title="Media AI Agent",
    description="一站式智能媒体内容生产平台",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Media AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **步骤 2: 提交代码**

```bash
git add -A
git commit -m "feat: add FastAPI main application"
```

---

## 阶段七：前端开发

### 任务 7.1: 前端项目初始化

**文件：**

- 创建: `frontend/vite.config.ts`
- 创建: `frontend/tailwind.config.js`
- 创建: `frontend/tsconfig.json`
- 创建: `frontend/index.html`

- [ ] **步骤 1: 创建 Vite 配置**

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

- [ ] **步骤 2: 创建 TypeScript 配置**

```json
// frontend/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **步骤 3: 创建 Tailwind 配置**

```javascript
// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
    },
  },
  plugins: [],
}
```

- [ ] **步骤 4: 创建入口 HTML**

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Media AI Agent</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **步骤 5: 提交代码**

```bash
git add -A
git commit -m "feat: initialize frontend project with Vite and Tailwind"
```

---

### 任务 7.2: 前端组件和页面

**文件：**

- 创建: `frontend/src/main.tsx`
- 创建: `frontend/src/App.tsx`
- 创建: `frontend/src/index.css`
- 创建: `frontend/src/pages/Dashboard.tsx`
- 创建: `frontend/src/pages/ProfessionalMode.tsx`
- 创建: `frontend/src/pages/CustomMode.tsx`

- [ ] **步骤 1: 创建入口文件**

```typescript
// frontend/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

- [ ] **步骤 2: 创建主应用组件**

```typescript
// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ProfessionalMode from './pages/ProfessionalMode'
import CustomMode from './pages/CustomMode'
import ContentLibrary from './pages/ContentLibrary'
import DistributionCenter from './pages/DistributionCenter'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-primary-600">
                  Media AI Agent
                </h1>
                <div className="ml-10 flex space-x-4">
                  <Link to="/" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    首页
                  </Link>
                  <Link to="/professional" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    专业模式
                  </Link>
                  <Link to="/custom" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    自定义模式
                  </Link>
                  <Link to="/library" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    内容库
                  </Link>
                  <Link to="/distribution" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    分发中心
                  </Link>
                  <Link to="/analytics" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    数据分析
                  </Link>
                  <Link to="/settings" className="px-3 py-2 text-gray-700 hover:text-primary-600">
                    设置
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/professional" element={<ProfessionalMode />} />
            <Route path="/custom" element={<CustomMode />} />
            <Route path="/library" element={<ContentLibrary />} />
            <Route path="/distribution" element={<DistributionCenter />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
```

- [ ] **步骤 3: 创建全局样式**

```css
/* frontend/src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors;
  }
  
  .btn-secondary {
    @apply px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-xl shadow-sm p-6;
  }
}
```

- [ ] **步骤 4: 创建 Dashboard 页面**

```typescript
// frontend/src/pages/Dashboard.tsx
import { useState } from 'react'
import { Plus, FileText, Video, Image, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const [recentProjects] = useState([
    { id: 1, name: 'AI技术趋势分析', type: 'article', status: 'completed', updatedAt: '2小时前' },
    { id: 2, name: '产品宣传视频', type: 'video', status: 'creating', updatedAt: '5小时前' },
    { id: 3, name: '端午活动海报', type: 'image_text', status: 'pending', updatedAt: '1天前' },
  ])

  const stats = [
    { label: '本周内容', value: '24', icon: FileText },
    { label: '视频产量', value: '8', icon: Video },
    { label: '分发平台', value: '5', icon: TrendingUp },
    { label: '总曝光量', value: '125K', icon: Image },
  ]

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">控制台</h1>
          <p className="text-gray-600 mt-1">欢迎使用 Media AI Agent</p>
        </div>
        <div className="flex gap-3">
          <button className="btn-secondary flex items-center gap-2">
            <FileText className="w-4 h-4" />
            创建文章
          </button>
          <button className="btn-secondary flex items-center gap-2">
            <Video className="w-4 h-4" />
            创建视频
          </button>
          <button className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" />
            新建项目
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
              </div>
              <stat.icon className="w-10 h-10 text-primary-500 opacity-20" />
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">最近项目</h2>
        <div className="space-y-4">
          {recentProjects.map((project) => (
            <div
              key={project.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center gap-4">
                {project.type === 'article' && <FileText className="w-5 h-5 text-blue-500" />}
                {project.type === 'video' && <Video className="w-5 h-5 text-purple-500" />}
                {project.type === 'image_text' && <Image className="w-5 h-5 text-green-500" />}
                <div>
                  <p className="font-medium text-gray-900">{project.name}</p>
                  <p className="text-sm text-gray-500">{project.updatedAt}</p>
                </div>
              </div>
              <span
                className={`px-3 py-1 text-sm rounded-full ${
                  project.status === 'completed'
                    ? 'bg-green-100 text-green-700'
                    : project.status === 'creating'
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {project.status === 'completed' ? '已完成' : project.status === 'creating' ? '创作中' : '待处理'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 5: 创建专业模式页面**

```typescript
// frontend/src/pages/ProfessionalMode.tsx
import { useState } from 'react'
import { CheckCircle, Circle, Loader2 } from 'lucide-react'

const PIPELINE_STAGES = [
  { id: 1, name: '选题', icon: '1', description: '智能热点分析' },
  { id: 2, name: '创作', icon: '2', description: 'AI内容生成' },
  { id: 3, name: '审核', icon: '3', description: '合规检查' },
  { id: 4, name: '分发', icon: '4', description: '一键发布' },
  { id: 5, name: '分析', icon: '5', description: '效果追踪' },
]

export default function ProfessionalMode() {
  const [currentStage, setCurrentStage] = useState(1)
  const [isRunning, setIsRunning] = useState(false)

  const handleStartPipeline = () => {
    setIsRunning(true)
    setCurrentStage(1)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">专业模式</h1>
        <p className="text-gray-600 mt-1">标准化流水线，适合大规模内容生产</p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-lg font-semibold">内容流水线</h2>
          {!isRunning && (
            <button onClick={handleStartPipeline} className="btn-primary">
              启动流水线
            </button>
          )}
        </div>

        <div className="flex items-center justify-between">
          {PIPELINE_STAGES.map((stage, index) => (
            <div key={stage.id} className="flex items-center">
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ${
                    currentStage > stage.id
                      ? 'bg-green-500 text-white'
                      : currentStage === stage.id
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {currentStage > stage.id ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : currentStage === stage.id ? (
                    isRunning ? (
                      <Loader2 className="w-6 h-6 animate-spin" />
                    ) : (
                      stage.icon
                    )
                  ) : (
                    stage.icon
                  )}
                </div>
                <p className="mt-2 font-medium text-gray-900">{stage.name}</p>
                <p className="text-sm text-gray-500">{stage.description}</p>
              </div>
              {index < PIPELINE_STAGES.length - 1 && (
                <div
                  className={`w-24 h-1 mx-4 rounded ${
                    currentStage > stage.id ? 'bg-green-500' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">当前任务</h3>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-gray-700">
              {currentStage === 1 && '正在分析热点话题...'}
              {currentStage === 2 && '正在生成文章内容...'}
              {currentStage === 3 && '正在进行合规审核...'}
              {currentStage === 4 && '正在分发至各平台...'}
              {currentStage === 5 && '正在收集效果数据...'}
            </p>
          </div>
        </div>

        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">任务日志</h3>
          <div className="space-y-2 font-mono text-sm">
            <p className="text-gray-600">[{new Date().toLocaleTimeString()}] 系统已启动</p>
            <p className="text-gray-600">[{new Date().toLocaleTimeString()}] 开始执行选题分析</p>
            <p className="text-green-600">[{new Date().toLocaleTimeString()}] 选题完成: AI技术突破</p>
          </div>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 6: 创建自定义模式页面**

```typescript
// frontend/src/pages/CustomMode.tsx
import { useState } from 'react'
import { Plus, Trash2, GripVertical } from 'lucide-react'

const MODULES = {
  topic: { name: '选题模块', items: ['热点聚合', '趋势追踪', '选题建议'] },
  creation: { name: '创作模块', items: ['文章创作', '视频创作', '图文创作'] },
  editing: { name: '编辑模块', items: ['智能剪辑', '字幕生成', '多语翻译'] },
  review: { name: '审核模块', items: ['合规检查', '事实核查', '敏感词过滤'] },
  distribution: { name: '分发模块', items: ['平台适配', '定时发布', '多平台同步'] },
}

export default function CustomMode() {
  const [workflow, setWorkflow] = useState<string[]>([])

  const handleAddModule = (moduleName: string) => {
    setWorkflow([...workflow, moduleName])
  }

  const handleRemoveModule = (index: number) => {
    setWorkflow(workflow.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">自定义模式</h1>
        <p className="text-gray-600 mt-1">模块化组装，按需配置创作流程</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">模块库</h2>
            <div className="space-y-4">
              {Object.entries(MODULES).map(([key, module]) => (
                <div key={key}>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">{module.name}</h3>
                  <div className="space-y-2">
                    {module.items.map((item) => (
                      <button
                        key={item}
                        onClick={() => handleAddModule(item)}
                        className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-lg flex items-center justify-between"
                      >
                        <span>{item}</span>
                        <Plus className="w-4 h-4 text-gray-400" />
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">工作流画布</h2>
            {workflow.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <p>从左侧模块库拖拽或点击添加模块</p>
              </div>
            ) : (
              <div className="space-y-4">
                {workflow.map((module, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg"
                  >
                    <GripVertical className="w-5 h-5 text-gray-400 cursor-move" />
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{module}</p>
                      <p className="text-sm text-gray-500">模块 {index + 1}</p>
                    </div>
                    <button
                      onClick={() => handleRemoveModule(index)}
                      className="p-2 text-gray-400 hover:text-red-500"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                    {index < workflow.length - 1 && (
                      <div className="absolute left-1/2 -translate-x-1/2">
                        <div className="w-0.5 h-4 bg-gray-300" />
                      </div>
                    )}
                  </div>
                ))}
                
                <button className="btn-primary w-full mt-6">
                  执行工作流
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 7: 提交代码**

```bash
git add -A
git commit -m "feat: add frontend pages (Dashboard, ProfessionalMode, CustomMode)"
```

---

### 任务 7.3: 其他前端页面

**文件：**

- 创建: `frontend/src/pages/ContentLibrary.tsx`
- 创建: `frontend/src/pages/DistributionCenter.tsx`
- 创建: `frontend/src/pages/Analytics.tsx`
- 创建: `frontend/src/pages/Settings.tsx`
- 创建: `frontend/src/api/client.ts`

- [ ] **步骤 1: 创建 API 客户端**

```typescript
// frontend/src/api/client.ts
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api
```

- [ ] **步骤 2: 创建内容库页面**

```typescript
// frontend/src/pages/ContentLibrary.tsx
import { useState } from 'react'
import { FileText, Video, Image, Search, Filter } from 'lucide-react'

export default function ContentLibrary() {
  const [contents] = useState([
    { id: 1, title: 'AI技术趋势深度分析', type: 'article', status: 'published', views: 12500, createdAt: '2024-01-15' },
    { id: 2, title: '产品功能介绍视频', type: 'video', status: 'draft', views: 0, createdAt: '2024-01-14' },
    { id: 3, title: '端午节活动海报', type: 'image_text', status: 'published', views: 8500, createdAt: '2024-01-13' },
  ])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">内容库</h1>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="搜索内容..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button className="btn-secondary flex items-center gap-2">
            <Filter className="w-4 h-4" />
            筛选
          </button>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4 font-medium text-gray-600">标题</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">类型</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">状态</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">浏览量</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">创建时间</th>
              </tr>
            </thead>
            <tbody>
              {contents.map((content) => (
                <tr key={content.id} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      {content.type === 'article' && <FileText className="w-5 h-5 text-blue-500" />}
                      {content.type === 'video' && <Video className="w-5 h-5 text-purple-500" />}
                      {content.type === 'image_text' && <Image className="w-5 h-5 text-green-500" />}
                      <span className="font-medium">{content.title}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-600">
                    {content.type === 'article' ? '文章' : content.type === 'video' ? '视频' : '图文'}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 text-sm rounded ${
                      content.status === 'published' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {content.status === 'published' ? '已发布' : '草稿'}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-600">{content.views.toLocaleString()}</td>
                  <td className="py-3 px-4 text-gray-600">{content.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 3: 创建分发中心页面**

```typescript
// frontend/src/pages/DistributionCenter.tsx
import { useState } from 'react'
import { CheckCircle, Clock, AlertCircle, Send } from 'lucide-react'

const PLATFORMS = [
  { id: 'wechat', name: '微信公众号', icon: '📱', color: 'bg-green-500' },
  { id: 'weibo', name: '微博', icon: '🌐', color: 'bg-red-500' },
  { id: 'zhihu', name: '知乎', icon: '❓', color: 'bg-blue-500' },
  { id: 'xiaohongshu', name: '小红书', icon: '📕', color: 'bg-pink-500' },
  { id: 'douyin', name: '抖音', icon: '🎵', color: 'bg-black' },
  { id: 'bilibili', name: 'B站', icon: '📺', color: 'bg-pink-600' },
]

export default function DistributionCenter() {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['wechat'])
  const [distributions] = useState([
    { id: 1, title: 'AI技术趋势分析', platform: 'wechat', status: 'published', publishedAt: '2024-01-15 14:30' },
    { id: 2, title: 'AI技术趋势分析', platform: 'weibo', status: 'published', publishedAt: '2024-01-15 14:32' },
    { id: 3, title: '产品宣传视频', platform: 'douyin', status: 'pending', scheduledAt: '2024-01-16 10:00' },
  ])

  const togglePlatform = (platformId: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(p => p !== platformId)
        : [...prev, platformId]
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">分发中心</h1>
        <p className="text-gray-600 mt-1">一键分发至多个内容平台</p>
      </div>

      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-4">选择分发平台</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {PLATFORMS.map((platform) => (
            <button
              key={platform.id}
              onClick={() => togglePlatform(platform.id)}
              className={`p-4 rounded-lg border-2 transition-all ${
                selectedPlatforms.includes(platform.id)
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="text-3xl mb-2">{platform.icon}</div>
              <p className="text-sm font-medium text-gray-900">{platform.name}</p>
            </button>
          ))}
        </div>
        
        <button className="btn-primary mt-6 flex items-center gap-2">
          <Send className="w-4 h-4" />
          一键分发
        </button>
      </div>

      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-4">分发记录</h2>
        <div className="space-y-4">
          {distributions.map((dist) => {
            const platform = PLATFORMS.find(p => p.id === dist.platform)
            return (
              <div key={dist.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <span className="text-2xl">{platform?.icon}</span>
                  <div>
                    <p className="font-medium text-gray-900">{dist.title}</p>
                    <p className="text-sm text-gray-500">{platform?.name}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  {dist.status === 'published' ? (
                    <div className="flex items-center gap-2 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span className="text-sm">已发布</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-yellow-600">
                      <Clock className="w-4 h-4" />
                      <span className="text-sm">待发布</span>
                    </div>
                  )}
                  <span className="text-sm text-gray-500">
                    {dist.publishedAt || dist.scheduledAt}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 4: 创建数据分析页面**

```typescript
// frontend/src/pages/Analytics.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function Analytics() {
  const chartData = [
    { date: '01-01', views: 2400, likes: 240 },
    { date: '01-02', views: 1398, likes: 139 },
    { date: '01-03', views: 9800, likes: 980 },
    { date: '01-04', views: 3908, likes: 390 },
    { date: '01-05', views: 4800, likes: 480 },
    { date: '01-06', views: 3800, likes: 380 },
    { date: '01-07', views: 4300, likes: 430 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">数据分析</h1>
        <p className="text-gray-600 mt-1">追踪内容传播效果</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <p className="text-sm text-gray-600">总浏览量</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">125,890</p>
          <p className="text-sm text-green-600 mt-1">↑ 23.5%</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">总点赞数</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">12,580</p>
          <p className="text-sm text-green-600 mt-1">↑ 18.2%</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">总评论数</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">3,456</p>
          <p className="text-sm text-red-600 mt-1">↓ 5.1%</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">平均互动率</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">8.5%</p>
          <p className="text-sm text-green-600 mt-1">↑ 2.3%</p>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-4">浏览量趋势</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="views" stroke="#0ea5e9" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 5: 创建设置页面**

```typescript
// frontend/src/pages/Settings.tsx
import { useState } from 'react'
import { Key, Globe, Bell } from 'lucide-react'

export default function Settings() {
  const [apiKeys, setApiKeys] = useState({
    openai: '',
    anthropic: '',
  })

  const [platforms] = useState([
    { id: 'wechat', name: '微信公众号', connected: true },
    { id: 'weibo', name: '微博', connected: false },
    { id: 'douyin', name: '抖音', connected: true },
  ])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">设置</h1>
        <p className="text-gray-600 mt-1">配置 API 密钥和平台连接</p>
      </div>

      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <Key className="w-5 h-5 text-gray-600" />
          <h2 className="font-semibold text-gray-900">API 密钥</h2>
        </div>
        <divName="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">OpenAI API Key</label>
            <input
              type="password"
              value={apiKeys.openai}
              onChange={(e) => setApiKeys({ ...apiKeys, openai: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              placeholder="sk-..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Anthropic API Key</label>
            <input
              type="password"
              value={apiKeys.anthropic}
              onChange={(e) => setApiKeys({ ...apiKeys, anthropic: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              placeholder="sk-ant-..."
            />
          </div>
          <button className="btn-primary">保存配置</button>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <Globe className="w-5 h-5 text-gray-600" />
          <h2 className="font-semibold text-gray-900">平台连接</h2>
        </div>
        <div className="space-y-4">
          {platforms.map((platform) => (
            <div key={platform.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-900">{platform.name}</span>
              <span className={`px-3 py-1 text-sm rounded ${
                platform.connected ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
              }`}>
                {platform.connected ? '已连接' : '未连接'}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-3 mb-6">
          <Bell className="w-5 h-5 text-gray-600" />
          <h2 className="font-semibold text-gray-900">通知设置</h2>
        </div>
        <div className="space-y-4">
          <label className="flex items-center gap-3">
            <input type="checkbox" className="w-4 h-4 text-primary-600" defaultChecked />
            <span>分发成功后发送通知</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" className="w-4 h-4 text-primary-600" defaultChecked />
            <span>内容审核不通过时发送通知</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" className="w-4 h-4 text-primary-600" />
            <span>每日数据报告</span>
          </label>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **步骤 6: 提交代码**

```bash
git add -A
git commit -m "feat: add remaining frontend pages (ContentLibrary, DistributionCenter, Analytics, Settings)"
```

---

## 阶段八：测试

### 任务 8.1: 单元测试

**文件：**

- 创建: `backend/tests/conftest.py`
- 创建: `backend/tests/test_agents/test_topic_agent.py`
- 创建: `backend/tests/test_agents/test_creation_agent.py`

- [ ] **步骤 1: 创建测试配置**

```python
# backend/tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.database import Base
from app.config import Settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    settings = Settings()
    settings.database_url = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(settings.database_url, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from OpenAI."
                }
            }
        ]
    }
```

- [ ] **步骤 2: 创建选题 Agent 测试**

```python
# backend/tests/test_agents/test_topic_agent.py
import pytest
from app.agents.topic_agent import TopicAgent
from app.agents.base import AgentInput


@pytest.fixture
def topic_agent():
    return TopicAgent()


@pytest.mark.asyncio
async def test_topic_agent_fetch_hot_topics(topic_agent):
    input_data = AgentInput(
        task_id="test_001",
        params={"action": "fetch_hot_topics", "limit": 10},
    )
    
    output = await topic_agent.execute(input_data)
    
    assert output.success is True
    assert "topics" in output.data
    assert isinstance(output.data["topics"], list)


@pytest.mark.asyncio
async def test_topic_agent_generate_suggestions(topic_agent):
    input_data = AgentInput(
        task_id="test_002",
        params={
            "action": "generate_topic_suggestions",
            "keyword": "人工智能",
        },
    )
    
    output = await topic_agent.execute(input_data)
    
    assert output.success is True
    assert output.data["keyword"] == "人工智能"
    assert "suggestions" in output.data
    assert len(output.data["suggestions"]) > 0


@pytest.mark.asyncio
async def test_topic_agent_analyze_topic(topic_agent):
    input_data = AgentInput(
        task_id="test_003",
        params={
            "action": "analyze_topic",
            "topic": "AI技术发展",
        },
    )
    
    output = await topic_agent.execute(input_data)
    
    assert output.success is True
    assert "heat_level" in output.data
    assert "competition_level" in output.data
```

- [ ] **步骤 3: 创建创作 Agent 测试**

```python
# backend/tests/test_agents/test_creation_agent.py
import pytest
from app.agents.creation_agent import CreationAgent
from app.agents.base import AgentInput


@pytest.fixture
def creation_agent():
    return CreationAgent()


@pytest.mark.asyncio
async def test_creation_agent_article(creation_agent):
    input_data = AgentInput(
        task_id="test_001",
        params={
            "content_type": "article",
            "topic": "AI技术发展趋势",
            "outline": ["背景介绍", "技术现状", "未来展望"],
            "style": "professional",
        },
    )
    
    output = await creation_agent.execute(input_data)
    
    assert output.success is True
    assert "title" in output.data
    assert "content" in output.data


@pytest.mark.asyncio
async def test_creation_agent_video(creation_agent):
    input_data = AgentInput(
        task_id="test_002",
        params={
            "content_type": "video",
            "topic": "产品介绍",
            "duration": 60,
        },
    )
    
    output = await creation_agent.execute(input_data)
    
    assert output.success is True
    assert "script" in output.data
    assert "shots" in output.data
```

- [ ] **步骤 4: 提交代码**

```bash
git add -A
git commit -m "test: add unit tests for agents"
```

---

## 阶段九：部署与文档

### 任务 9.1: Nginx 配置和 README

**文件：**

- 创建: `frontend/nginx.conf`
- 创建: `README.md`

- [ ] **步骤 1: 创建 Nginx 配置**

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

- [ ] **步骤 2: 创建 README**

```markdown
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
```

- [ ] **步骤 3: 提交代码**

```bash
git add -A
git commit -m "docs: add nginx config and README"
```

---

## 验收标准

### 功能验收

- [ ] 后端 API 正常启动并响应请求
- [ ] 前端页面正常加载和交互
- [ ] Agent 系统能够正常执行任务
- [ ] Docker 容器化部署成功

### 技术验收

- [ ] 所有单元测试通过
- [ ] API 文档可访问 (/docs)
- [ ] 数据库迁移正常执行
- [ ] 环境变量配置正确

### 性能验收

- [ ] API 响应时间 < 3秒
- [ ] 页面加载时间 < 5秒
- [ ] 支持并发请求处理
