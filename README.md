# AICove - 学习与探索平台

AICove 是一个综合性学习与探索平台，旨在为用户提供知识普及、资源获取、实践体验与社区交流的一站式服务。

## ✨ 功能特性

### 核心模块

1. **主页** (`/`)
   - 英雄区展示平台定位
   - 新手引导（可跳过）
   - 功能快捷入口（热门科普、最新资讯、热门工具、站内搜索）
   - 热门内容展示

2. **基础学习** (`/ai-basics`)
   - 核心概念：按文字、图片、视频、知识图谱分类展示，卡片对齐美观
   - 学习路径：小白入门、职场应用、学生进阶三条路径
   - 发展史：时间轴可视化展示（框内滚动）

3. **实验室** (`/ai-lab`)
   - **工具集**：多功能工具集
     - 图像生成：优化图像生成提示词
     - 写作助手：文章、文案创作与优化
     - 翻译工具：多语言翻译
     - 编程助手：代码编写、调试、优化（支持多轮对话和代码下载）
     - PPT制作：自动生成PPT内容并下载
   - **模型透视**：神经网络工作机制可视化演示
     - 神经网络工作机制：交互式可视化
     - 词向量空间：语义关系可视化

4. **应用场景** (`/applications`)
   - 案例库：按行业分类展示应用案例
   - 工具箱：实用工具测评与推荐

5. **伦理与未来** (`/ethics`)
   - 专题讨论：安全、偏见与公平、就业、隐私等话题
   - 支持用户评论与点赞

6. **资源中心** (`/resources`)
   - AI术语表：A-Z 索引，支持搜索和字母筛选
   - 推荐阅读：书籍、论文、期刊推荐
   - 课程推荐：YouTube课程推荐（吴恩达、何凯明等）

7. **社区** (`/community`)
   - 智能助教：基于 RAG 技术的站内智能问答
   - 问答论坛：用户生成内容社区，支持论坛内容搜索、点赞、收藏、回复
   - 关于我们：联系地点、联系方式等信息
   - 隐私政策、使用指南

8. **站内搜索** (`/search`)
   - 普通搜索：关键词匹配
   - 高级检索：多条件筛选
   - 智能搜索：语义理解

## 🛠️ 技术栈

- **后端**：Flask (Python 3.8+)
- **前端**：HTML, CSS, JavaScript
- **认证**：Flask-Login (Session-based)，强制登录访问
- **数据存储**：MySQL数据库（支持从mock_data导入）

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- pip

### 2. 克隆项目

```bash
git clone <repository-url>
cd IA
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件（可以参考 `.env.example` 文件）：

```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，填写你的配置信息
# Windows: notepad .env
# Linux/Mac: nano .env
```

`.env` 文件内容示例：

```env
# Flask配置
SECRET_KEY=your-secret-key-here-change-in-production

# 数据库配置
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=IA

# AI服务API密钥（可选，只有需要使用对应AI服务时才需要配置）
DASHSCOPE_API_KEY=your-dashscope-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key
KIMI_API_KEY=your-kimi-api-key
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
VOLC_SEEDREAM_API_KEY=your-volc-seedream-api-key
```

**重要提示**：
- `SECRET_KEY`：用于Flask会话加密，生产环境必须修改为随机字符串
- `DB_PASSWORD`：填写你的MySQL数据库密码
- AI服务API密钥：只有需要使用对应AI服务时才需要配置，不配置也不影响基本功能

### 5. 初始化数据库

**方式一：使用Python脚本（推荐，一键完成）**

```bash
# 一键初始化（创建数据库、插入数据、启动服务器）
python db_utils.py init
```

该命令会自动执行：
1. 创建数据库（如果不存在）
2. 创建数据库结构（表、索引、视图等）
3. 插入初始数据（包含默认用户）
4. 启动Web服务器

**方式二：分步执行**

```bash
# 1. 创建数据库结构
python db_utils.py create

# 2. 插入初始数据
python db_utils.py insert

# 3. 启动服务器
python run.py
```

**方式三：使用SQL脚本**

```bash
# 1. 创建数据库（如果不存在）
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS IA CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 导入数据库结构
mysql -u root -p IA < init_schema.sql

# 3. 导入初始数据
mysql -u root -p IA < insert_mock_data.sql

# 4. 启动服务器
python run.py
```

**注意**：当前版本默认使用MySQL数据库，数据会持久化存储。

### 6. 运行应用

如果使用 `python db_utils.py init`，服务器会自动启动。

否则，手动启动：

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动。

### 7. 使用Ngrok进行公网部署（自动启用）

应用默认会自动启用Ngrok免费隧道，让其他用户可以远程访问您的网站：

```bash
# 直接运行即可（自动创建ngrok隧道）
python run.py
```

**说明：**
- 系统会自动使用Ngrok免费模式，无需任何配置
- 免费版地址每次重启都会变化，启动时会显示在控制台
- 如果未安装pyngrok，会提示安装，但不影响本地运行
- 公网地址会在启动时自动显示，可直接分享给其他用户

**安装pyngrok（如果未安装）：**
```bash
pip install pyngrok
```

**注意事项：**
- 免费版ngrok有连接数限制，但足够个人使用
- 地址每次重启都会变化，需要重新分享
- 按 Ctrl+C 停止服务器时会自动关闭ngrok隧道

### 8. 使用固定地址模式（可选）

如果您在 `.env` 文件中设置了 `NGROK_AUTH_TOKEN`，可以使用固定地址模式：

```bash
# 使用token模式启动（固定地址）
python run.py
```

**获取Ngrok认证Token：**

1. 访问 https://dashboard.ngrok.com/signup 注册账号（免费）
2. 登录后访问 https://dashboard.ngrok.com/get-started/your-authtoken
3. 复制您的authtoken
4. 在 `.env` 文件中添加：
   ```env
   NGROK_AUTH_TOKEN=你的token
   ```

**两种模式对比：**

| 特性 | 免费模式 | Token模式 |
|------|-------------------|--------------------------------|
| 配置 | 无需配置 | 需要设置NGROK_AUTH_TOKEN |
| 地址 | 每次重启变化 | 相对固定（取决于ngrok计划） |
| 费用 | 完全免费 | 免费版可用 |
| 适用场景 | 测试、开发 | 需要固定地址的场景 |

**注意：**
- 免费版ngrok地址每次重启都会变化
- 如需固定地址，请使用ngrok付费版或设置authtoken
- 公网地址会在启动时显示在控制台

## 👤 默认账号

系统初始化后会创建以下账号：

- **超级管理员**：账号 `superadmin` / 密码 `superadmin123`
- **管理员**：账号 `admin` / 密码 `admin123`
- **普通用户**：账号 `user` / 密码 `user123`

**注意**：首次登录后请及时修改密码。

## 📁 项目结构

```
AICove/
├── app/
│   ├── __init__.py          # Flask应用工厂
│   ├── routes.py            # 路由定义
│   ├── models.py            # 数据库模型
│   ├── mock_data.py         # 模拟数据
│   ├── ai_service.py        # AI服务模块
│   ├── tagging_system.py    # 标记体系模块
│   ├── category_utils.py    # 分类工具函数
│   ├── templates/           # HTML模板
│   └── static/              # 静态文件
│       ├── css/
│       ├── js/
│       └── uploads/
│           ├── avatars/     # 用户头像
│           ├── articles/    # 文章图片
│           └── generated/   # AI生成的文件
├── images/                  # 图片资源
│   ├── cases/               # 案例图片
│   ├── resources/           # 资源封面
│   └── tools/               # 工具图标
├── config.py               # 配置文件
├── run.py                  # 应用入口
├── db_utils.py             # 数据库工具脚本（包含创建、插入、初始化等功能）
├── init_schema.sql         # 数据库结构SQL脚本
├── insert_mock_data.sql    # 初始数据SQL脚本
├── requirements.txt        # Python依赖
└── README.md              # 项目说明
```

## 📝 文件命名规范

### 用户头像文件
- **路径**: `app/static/uploads/avatars/`
- **命名格式**: `avatar_{user_id}_{timestamp}.{ext}`
- **示例**: `avatar_1_20241230_143022.jpg`

### 核心概念
- 核心概念不再使用本地图片存储
- 支持文字、视频和知识图谱等交互式内容

### 文章封面图片
- **路径**: `app/static/uploads/articles/`
- **命名格式**: `article_{article_id}_{timestamp}.{ext}`
- **示例**: `article_1_20241230_140000.jpg`

### 案例图片
- **路径**: `images/cases/`
- **命名格式**: `case_{case_id}_{case_title_slug}.{ext}`
- **示例**: `case_1_ai_medical_diagnosis.jpg`

### 资源封面图片
- **路径**: `images/resources/`
- **命名格式**: `resource_{resource_id}_{resource_title_slug}.{ext}`
- **示例**: `resource_1_deep_learning_book.jpg`

### 工具图标
- **路径**: `images/tools/`
- **命名格式**: `tool_{tool_id}_{tool_name_slug}.{ext}`
- **示例**: `tool_1_chatgpt.png`

### 生成的文件（代码、PPT等）
- **路径**: `app/static/uploads/generated/`
- **命名格式**: `{type}_{user_id}_{timestamp}.{ext}`
- **类型**: `code_`, `ppt_`, `document_`
- **示例**: `code_1_20241230_150000.py`, `ppt_2_20241230_151500.pptx`

### 通用规则
1. **字符限制**: 文件名使用小写字母、数字、下划线和连字符
2. **长度限制**: 文件名（不含路径和扩展名）不超过100个字符
3. **唯一性**: 通过ID和时间戳确保文件名唯一
4. **扩展名**: 保留原始扩展名，支持常见图片格式（jpg, jpeg, png, gif, webp）和文档格式
5. **特殊字符**: 避免使用空格、中文和其他特殊字符（除了下划线和连字符）

## 🖼️ 图片资源说明

### 图片存储位置

- 用户上传文件：`app/static/uploads/`（头像、文章封面等）
- 系统资源图片：`images/`（案例、资源、工具等）

### 图片要求

- **分辨率**：建议宽度800-1200px
- **格式**：JPG（照片类）或PNG（图表类）
- **文件大小**：建议小于500KB
- **内容**：清晰、专业、与内容相关
- **版权**：确保图片可合法使用

### 核心概念

核心概念支持交互式内容：
- **文字**：概念定义和说明
- **视频**：使用YouTube链接，在概念详情页显示
- **知识图谱**：支持JSON格式存储

## 🔧 开发说明

### 添加新功能

1. 在 `app/routes.py` 中添加路由
2. 在 `app/templates/` 中创建模板文件
3. 在 `app/static/` 中添加静态资源
4. 如需数据模型，在 `app/models.py` 中添加模型定义

### API 接口

主要 API 端点：

**认证相关：**
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册
- `GET /auth/forgot-password` - 找回密码页面
- `POST /auth/forgot-password` - 找回密码

**个人中心相关：**
- `GET /profile` - 个人中心页面
- `GET /api/profile/favorites` - 获取收藏列表
- `GET /api/profile/likes` - 获取点赞记录
- `GET /api/profile/messages` - 获取消息列表
- `POST /api/profile/username` - 更新昵称
- `POST /api/profile/password` - 修改密码
- `POST /api/profile/avatar` - 上传头像

## 📝 当前状态

### ✅ 已实现

- ✅ 所有功能页面和路由
- ✅ 用户认证（Session-based，强制登录访问）
- ✅ 数据库支持（支持从mock_data导入）
- ✅ 响应式设计
- ✅ 用户个人中心（收藏、点赞、消息、设置）
- ✅ 头像下拉菜单（收藏、消息功能）
- ✅ 密码加密存储
- ✅ 二级密码/安全问题支持
- ✅ 多功能工具集
- ✅ 论坛内容搜索功能
- ✅ 论坛点赞、收藏、回复功能（基于真实数据）
- ✅ 核心概念页面分类展示（文字、图片、视频、知识图谱）
- ✅ 标记体系管理
- ✅ 统一的分类筛选系统
- ✅ 分页功能（资源中心、论坛、应用场景、伦理页面）
- ✅ 关于我们页面

### ⚠️ 注意事项

- **数据存储**：当前版本使用MySQL数据库，数据会持久化存储
- **注册功能**：已实现，支持账号注册
- **文件上传**：用户上传的文件存储在 `app/static/uploads/` 目录
- **敏感信息**：所有API配置、数据库配置等敏感信息存储在 `.env` 文件中，不会暴露在前端代码中

## ⚠️ 安全说明

1. **生产环境配置**：
   - 修改 `config.py` 中的 `SECRET_KEY`
   - 配置环境变量
   - 关闭调试模式：`app.run(debug=False, ...)`

2. **安全性**：
   - 不要将 `.env` 文件提交到版本控制系统
   - 定期更换密钥
   - 生产环境使用 HTTPS
   - API密钥和数据库配置不会暴露在前端代码中

3. **数据库备份**：
   - 定期备份数据库
   - 保护数据库连接信息

## 📄 许可证

本项目仅供学习和研究使用。

## 📞 联系方式

如有问题或建议，请联系：contact@aicove.com
