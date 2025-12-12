# AICove - AI 学习与探索平台

AICove 是一个综合性 AI 学习与探索平台，旨在为用户提供 AI 知识普及、资源获取、实践体验与社区交流的一站式服务。

## ✨ 功能特性

### 核心模块

1. **主页** (`/`)
   - 英雄区展示平台定位
   - 新手引导（可跳过）
   - 功能快捷入口（热门科普、最新资讯、热门大模型、站内搜索）
   - 热门内容展示

2. **AI 基础** (`/ai-basics`)
   - 核心概念：AI 相关术语卡片展示
   - 学习路径：小白入门、职场应用、学生进阶三条路径
   - AI 发展史：时间轴可视化展示

3. **AI 实验室** (`/ai-lab`)
   - AI 游乐场：支持多个大模型 API 的沙盒体验
   - 模型透视：神经网络工作机制可视化演示
   - 支持模型：阿里云通义千问、DeepSeek、Kimi、Gemini、OpenAI

4. **应用场景** (`/applications`)
   - 案例库：按行业分类展示 AI 应用案例
   - AI 工具箱：实用工具测评与推荐

5. **伦理与未来** (`/ethics`)
   - 专题讨论：AI 安全、偏见与公平、就业、隐私等话题
   - 支持用户评论与点赞

6. **资源中心** (`/resources`)
   - AI 术语表：A-Z 索引，支持搜索
   - 推荐阅读：书籍、论文、期刊、课程推荐

7. **社区** (`/community`)
   - AI 助教：基于 RAG 技术的站内智能问答
   - 问答论坛：用户生成内容社区
   - 关于我们、隐私政策、使用指南

8. **站内搜索** (`/search`)
   - 普通搜索：关键词匹配
   - 高级检索：多条件筛选
   - AI 搜索：智能语义理解

## 🛠️ 技术栈

- **后端**：Flask (Python 3.8+)
- **前端**：HTML, CSS, JavaScript
- **认证**：Flask-Login (Session-based)
- **AI 服务**：阿里云 DashScope、DeepSeek、Kimi、Gemini、OpenAI
- **数据存储**：模拟数据（内存，当前版本）

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

#### 方式一：安装所有依赖（推荐）

```bash
pip install -r requirements.txt
```

这将安装所有核心依赖和 AI 模型依赖。

#### 方式二：仅安装核心依赖（最小安装）

如果暂时不需要 AI 功能，可以只安装核心依赖：

```bash
pip install Flask==3.0.0 Flask-Login==0.6.3 Werkzeug==3.0.1 python-dotenv==1.0.0 requests==2.31.0
```

#### 方式三：按需安装 AI 模型依赖

根据您要使用的 AI 模型，选择性安装：

```bash
# 核心依赖（必需）
pip install Flask==3.0.0 Flask-Login==0.6.3 Werkzeug==3.0.1 python-dotenv==1.0.0 requests==2.31.0

# 阿里云通义千问（如果使用）
pip install dashscope==1.17.0

# OpenAI（如果使用）
pip install openai==1.3.0

# Google Gemini（如果使用）
pip install google-generativeai==0.3.1
```

**注意**：DeepSeek 和 Kimi 使用 `requests` 库（已包含在核心依赖中），无需额外安装。

### 3. 配置环境变量（可选但推荐）

在项目根目录（与 `run.py` 同级）创建 `.env` 文件：

```env
# AI 模型 API 配置（至少配置一个以使用 AI 功能）
DASHSCOPE_API_KEY=your-aliyun-api-key-here      # 阿里云通义千问
DEEPSEEK_API_KEY=your-deepseek-api-key-here      # DeepSeek
KIMI_API_KEY=your-kimi-api-key-here              # Kimi (Moonshot AI)
GEMINI_API_KEY=your-gemini-api-key-here          # Google Gemini
OPENAI_API_KEY=your-openai-api-key-here          # OpenAI

# Flask 配置
SECRET_KEY=your-secret-key-here
```

**获取 API Key：**
- 阿里云：访问 [DashScope 控制台](https://dashscope.console.aliyun.com/)
- DeepSeek：访问 [DeepSeek 官网](https://www.deepseek.com/)
- Kimi：访问 [Moonshot AI](https://platform.moonshot.cn/)
- Gemini：访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
- OpenAI：访问 [OpenAI Platform](https://platform.openai.com/api-keys)

详细配置说明请查看 `AI_API配置说明.md`

### 4. 准备 Logo（可选）

将 `AICove.jpg` 文件放在项目根目录（与 `config.py` 同级）。如果文件不存在，logo 会自动隐藏。

### 5. 运行应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动。

## 👤 测试账号

- 管理员：账号 `admin` / 密码 `admin123`
- 测试用户：账号 `testuser` / 密码 `test123`

**注意**：密码已加密存储，登录时自动验证。您也可以使用注册功能创建新账号。

## 📁 项目结构

```
AICove/
├── app/
│   ├── __init__.py          # Flask 应用工厂（无数据库）
│   ├── routes.py            # 路由定义（使用模拟数据）
│   ├── mock_data.py         # 模拟数据（包含用户、文章、工具等）
│   ├── ai_service.py        # AI 服务模块（多模型支持）
│   ├── models.py            # 数据库模型（预留，当前未使用）
│   ├── templates/           # HTML 模板
│   │   ├── base.html        # 基础模板
│   │   ├── index.html       # 首页
│   │   ├── ai_basics.html   # AI基础
│   │   ├── ai_lab.html      # AI实验室
│   │   ├── applications.html # 应用场景
│   │   ├── ethics.html      # 伦理与未来
│   │   ├── resources.html   # 资源中心
│   │   ├── search.html      # 搜索页面
│   │   ├── community.html   # 社区
│   │   ├── profile.html     # 个人中心
│   │   ├── login.html       # 登录页面
│   │   ├── register.html    # 注册页面
│   │   ├── forgot_password.html # 找回密码
│   │   └── ...              # 其他模板
│   └── static/             # 静态文件
│       ├── css/
│       │   └── style.css    # 主样式文件（包含动画样式）
│       ├── js/
│       │   └── main.js      # 主JavaScript文件
│       └── uploads/         # 用户上传文件（头像等）
│           └── avatars/
├── config.py               # 配置文件
├── run.py                  # 应用入口
├── AICove.jpg             # Logo（需手动添加）
├── requirements.txt       # Python 依赖
├── README.md              # 项目说明
└── AI_API配置说明.md      # AI API 配置详细说明
```

## 📝 当前状态

### ✅ 已实现

- ✅ 所有功能页面和路由
- ✅ 动态路由支持（浏览器前进/返回）
- ✅ 用户认证（Session-based）
- ✅ 多模型 AI 支持
- ✅ 响应式设计
- ✅ 动画效果
- ✅ 用户个人中心（收藏、点赞、消息、设置）
- ✅ 密码加密存储
- ✅ 二级密码/安全问题支持

### ⚠️ 注意事项

- **数据存储**：当前版本使用模拟数据（内存中），所有数据修改都是临时的，刷新页面会恢复
- **注册功能**：已实现，支持账号注册（账号、昵称、邮箱、密码、二级问题等）
- **数据持久化**：发帖、评论等功能会返回成功消息，但数据不会持久化（重启应用后恢复）

## 🔄 后续接入数据库

当数据库准备好后，需要：

1. **安装数据库依赖**：
   ```bash
   pip install Flask-SQLAlchemy==3.1.1 PyMySQL==1.1.0 cryptography==41.0.7
   ```
   
   或者取消注释 `requirements.txt` 中的数据库相关依赖，然后运行：
   ```bash
   pip install -r requirements.txt
   ```

2. **恢复数据库模型**：
   - 取消注释 `app/models.py` 中的模型定义
   - 在 `app/__init__.py` 中初始化数据库

3. **修改路由**：
   - 将 `app/routes.py` 中的模拟数据查询替换为数据库查询
   - 将 `app/mock_data.py` 中的数据迁移到数据库

4. **更新配置**：
   - 在 `config.py` 中配置数据库连接
   - 运行 `init_db.py` 初始化数据库（如果存在）

## 🔧 开发说明

### 添加新功能

1. 在 `app/routes.py` 中添加路由
2. 在 `app/templates/` 中创建模板文件
3. 在 `app/static/` 中添加静态资源
4. 如需数据模型，在 `app/mock_data.py` 中添加模拟数据

### API 接口

主要 API 端点：

**认证相关：**
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册
- `GET /auth/forgot-password` - 找回密码页面
- `POST /auth/forgot-password` - 找回密码
- `GET /api/auth/security-question` - 根据用户名获取二级问题
- `GET /api/auth/check-first-login` - 检查是否首次登录

**AI 相关：**
- `POST /api/ai-chat` - AI 聊天
- `POST /api/ai-assistant` - AI 助教
- `GET /api/models` - 获取可用模型列表

**论坛相关：**
- `POST /api/forum/post` - 创建论坛帖子
- `POST /api/forum/<id>/comment` - 添加评论
- `POST /api/forum/<id>/like` - 点赞/取消点赞帖子
- `POST /api/forum/<id>/favorite` - 收藏/取消收藏帖子

**伦理专题相关：**
- `POST /api/ethics/<id>/like` - 点赞/取消点赞伦理专题
- `POST /api/ethics/<id>/favorite` - 收藏/取消收藏伦理专题
- `POST /api/ethics/<id>/comment` - 添加评论

**文章相关：**
- `POST /api/article/<id>/favorite` - 收藏/取消收藏文章

**个人中心相关：**
- `GET /profile` - 个人中心页面
- `GET /api/profile/favorites` - 获取收藏列表
- `GET /api/profile/likes` - 获取点赞记录
- `GET /api/profile/messages` - 获取消息列表
- `POST /api/profile/username` - 更新昵称
- `POST /api/profile/password` - 修改密码（需验证二级问题）
- `POST /api/profile/security` - 修改二级密码（需验证当前答案）
- `POST /api/profile/avatar` - 上传头像
- `POST /api/profile/interests` - 更新兴趣领域

## 📚 相关文档

- `AI_API配置说明.md` - AI 模型 API 详细配置说明
- `requirements.txt` - Python 依赖列表

## ⚠️ 注意事项

1. **生产环境配置**：
   - 修改 `config.py` 中的 `SECRET_KEY`
   - 配置环境变量（API 密钥等）
   - 关闭调试模式：`app.run(debug=False, ...)`

2. **AI API 费用**：
   - 使用 AI 功能会产生费用，请关注各提供商的账户余额
   - 注意 API 调用频率限制

3. **安全性**：
   - 不要将 `.env` 文件提交到版本控制系统
   - 定期更换 API 密钥
   - 生产环境使用 HTTPS

## 📄 许可证

本项目仅供学习和研究使用。

## 📞 联系方式

如有问题或建议，请联系：contact@aicove.com
