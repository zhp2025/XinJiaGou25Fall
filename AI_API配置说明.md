# AI 模型 API 配置说明

## 概述

AICove 平台支持**5个 AI 模型提供商**，用于以下功能：
- **AI 实验室**：与多个 AI 模型进行对话
- **AI 搜索**：智能语义搜索
- **AI 助教**：基于 RAG 的智能问答

## 支持的模型提供商

1. **阿里云通义千问** (DashScope)
   - 模型：`qwen-turbo`、`qwen-plus`、`qwen-max`
   - 密钥：`DASHSCOPE_API_KEY`
   - 文档：https://help.aliyun.com/zh/model-studio/

2. **DeepSeek**
   - 模型：`deepseek-chat`
   - 密钥：`DEEPSEEK_API_KEY`
   - 官网：https://www.deepseek.com/

3. **Kimi** (Moonshot AI)
   - 模型：`moonshot-v1-8k`
   - 密钥：`KIMI_API_KEY`
   - 官网：https://platform.moonshot.cn/

4. **Google Gemini**
   - 模型：`gemini-pro`
   - 密钥：`GEMINI_API_KEY`
   - 官网：https://makersuite.google.com/app/apikey

5. **OpenAI**
   - 模型：`gpt-3.5-turbo`、`gpt-4`
   - 密钥：`OPENAI_API_KEY`
   - 官网：https://platform.openai.com/api-keys

## 快速配置

### 1. 创建 .env 文件

在项目根目录（与 `run.py` 同级）创建 `.env` 文件：

```env
# AI 模型 API 配置（至少配置一个即可使用）
DASHSCOPE_API_KEY=your-aliyun-api-key-here      # 阿里云通义千问
DEEPSEEK_API_KEY=your-deepseek-api-key-here      # DeepSeek
KIMI_API_KEY=your-kimi-api-key-here              # Kimi (Moonshot AI)
GEMINI_API_KEY=your-gemini-api-key-here          # Google Gemini
OPENAI_API_KEY=your-openai-api-key-here          # OpenAI

# Flask 配置
SECRET_KEY=your-secret-key-here
```

**注意**：您不需要配置所有密钥，只需配置您要使用的模型提供商的密钥即可。系统会根据配置的密钥动态显示可用的模型。

### 2. 获取 API 密钥

#### 阿里云 DashScope

1. 访问 [DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 登录阿里云账号
3. 创建 API Key
4. 将 API Key 复制到 `.env` 文件中的 `DASHSCOPE_API_KEY`

#### DeepSeek

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 将 API Key 复制到 `.env` 文件中的 `DEEPSEEK_API_KEY`

#### Kimi (Moonshot AI)

1. 访问 [Moonshot AI 平台](https://platform.moonshot.cn/)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 将 API Key 复制到 `.env` 文件中的 `KIMI_API_KEY`

#### Google Gemini

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用 Google 账号登录
3. 创建 API Key
4. 将 API Key 复制到 `.env` 文件中的 `GEMINI_API_KEY`

#### OpenAI

1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录 OpenAI 账号
3. 创建 API Key
4. 将 API Key 复制到 `.env` 文件中的 `OPENAI_API_KEY`

### 3. 安装依赖

#### 安装所有依赖（推荐）

```bash
pip install -r requirements.txt
```

#### 按需安装 AI 模型依赖

根据您要使用的模型，选择性安装对应的依赖包：

**核心依赖（必需）：**
```bash
pip install Flask==3.0.0 Flask-Login==0.6.3 Werkzeug==3.0.1 python-dotenv==1.0.0 requests==2.31.0
```

**AI 模型依赖（按需安装）：**
```bash
# 阿里云通义千问
pip install dashscope==1.17.0

# OpenAI
pip install openai==1.3.0

# Google Gemini
pip install google-generativeai==0.3.1

# DeepSeek 和 Kimi（使用 requests，已包含在核心依赖中，无需额外安装）
```

**依赖包说明：**
- `dashscope`：阿里云通义千问 SDK
- `openai`：OpenAI 官方 SDK
- `google-generativeai`：Google Gemini SDK
- `requests`：DeepSeek 和 Kimi 使用 REST API（已包含在核心依赖中）

## 功能说明

### AI 实验室

- **位置**：`/ai-lab` > AI 游乐场
- **功能**：与多个 AI 模型进行实时对话
- **可用模型**（根据配置的 API 密钥动态显示）：
  - **阿里云**：通义千问 Turbo / Plus / Max
  - **DeepSeek**：DeepSeek Chat
  - **Kimi**：Moonshot v1-8k
  - **Gemini**：Gemini Pro
  - **OpenAI**：GPT-3.5 Turbo / GPT-4

### AI 搜索

- **位置**：搜索页面 > AI 搜索标签
- **功能**：使用 AI 分析搜索意图，提取关键词，返回更相关的搜索结果
- **特点**：智能理解用户意图，即使关键词不准确也能找到相关内容

### AI 助教

- **位置**：`/community/ai-assistant`
- **功能**：基于 RAG 技术的智能问答系统
- **特点**：专门针对 AI 学习问题优化，提供专业且易懂的回答

## 模型标识格式

系统使用统一的模型标识格式：`provider-model`

例如：
- `aliyun-qwen-turbo`
- `deepseek-chat`
- `kimi-moonshot-v1-8k`
- `gemini-pro`
- `openai-gpt-3.5-turbo`

## 动态模型列表

- 模型选择器会根据 `.env` 中配置的密钥**动态显示**可用模型
- 只显示已配置密钥的模型
- 如果未配置任何密钥，会显示提示信息

## API 端点

- `GET /api/models` - 获取可用模型列表（无需登录）
- `POST /api/ai-chat` - 发送消息到指定模型（需要登录）
- `POST /api/ai-assistant` - AI 助教问答（需要登录）

## 错误处理

如果 API 密钥未配置或配置错误：

1. **AI 实验室**：会显示错误提示，提示配置 API 密钥
2. **AI 搜索**：会自动回退到普通关键词搜索
3. **AI 助教**：会显示错误信息

## 测试

配置完成后，可以：

1. 登录系统（使用测试账号：`testuser` / `test123`）
2. 访问 AI 实验室，尝试与模型对话
3. 使用 AI 搜索功能
4. 在 AI 助教中提问

## 注意事项

1. **API 费用**：使用 AI 功能会产生费用，请关注各提供商的账户余额
2. **速率限制**：注意各 API 的调用频率限制
3. **安全性**：不要将 `.env` 文件提交到版本控制系统
4. **密钥管理**：定期更换 API 密钥，确保安全
5. **至少配置一个密钥**：系统需要至少一个 API 密钥才能使用 AI 功能

## 故障排查

### 问题：API 调用失败

**可能原因**：
- API 密钥未配置或配置错误
- 网络连接问题
- API 余额不足

**解决方法**：
1. 检查 `.env` 文件中的 API 密钥是否正确
2. 确认 API 密钥有效且有余额
3. 检查网络连接
4. 查看终端或浏览器控制台的错误信息

### 问题：模块导入错误

**解决方法**：

根据错误信息安装对应的依赖包：

```bash
# 如果缺少 dashscope（阿里云）
pip install dashscope==1.17.0

# 如果缺少 openai
pip install openai==1.3.0

# 如果缺少 google-generativeai（Gemini）
pip install google-generativeai==0.3.1

# 如果缺少 requests（DeepSeek 和 Kimi）
pip install requests==2.31.0

# 或者安装所有依赖
pip install -r requirements.txt
```

### 问题：API 返回错误

查看终端或浏览器控制台的错误信息，常见错误：
- `Invalid API Key`：API 密钥无效
- `Insufficient Balance`：余额不足
- `Rate Limit Exceeded`：超过调用频率限制

## 更多信息

- [DashScope 官方文档](https://help.aliyun.com/zh/model-studio/)
- [通义千问模型说明](https://help.aliyun.com/zh/model-studio/developer-reference/model-introduction)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Gemini API 文档](https://ai.google.dev/docs)

