# Ngrok 使用说明

## 问题说明

您遇到的错误是由于 **ngrok 免费账户同时会话数限制**导致的。免费版 ngrok 账户最多只能同时运行 3 个 agent 会话。

## 解决方案

### 方案一：使用清理脚本（推荐，快速解决）

运行清理脚本，强制关闭所有 ngrok 进程和会话：

```bash
python cleanup_ngrok.py
```

这个脚本会：
- 关闭所有活动的 ngrok 隧道
- 强制终止所有 ngrok 进程
- 清理所有会话

### 方案二：检查当前状态

在清理之前，可以先检查当前状态：

```bash
python check_ngrok_status.py
```

这个脚本会显示：
- 当前运行的 ngrok 进程数量
- 活动的隧道信息
- 配置状态

### 方案三：手动清理

1. **访问 ngrok 控制台**
   - 打开 https://dashboard.ngrok.com/agents
   - 手动关闭不需要的会话

2. **使用系统命令关闭进程**
   - Windows: `taskkill /F /IM ngrok.exe`
   - Linux/macOS: `pkill -9 ngrok`

### 方案四：使用配置文件（推荐，长期解决）

使用 `ngrok.yml` 配置文件可以同时运行多个端点，但只占用一个会话。

#### 1. 使用配置文件启动（需要安装 ngrok CLI）

```bash
# 安装 ngrok CLI（如果未安装）
# 下载地址: https://ngrok.com/download

# 使用配置文件启动所有端点
ngrok start --all

# 或启动指定端点
ngrok start web
```

#### 2. 配置文件说明

`ngrok.yml` 文件已创建，包含以下配置：

- **web**: HTTPS 端点（端口 5000）
- **web-http**: HTTP 端点（端口 5000）

#### 3. 修改配置

如果需要修改端口或添加新端点，编辑 `ngrok.yml`：

```yaml
tunnels:
  web:
    proto: http
    addr: 5000  # 修改为您的端口
    bind_tls: true
```

## 改进的 run.py

`run.py` 已经改进，现在会：

1. **自动清理**：启动前自动关闭所有现有隧道和进程
2. **错误检测**：检测会话限制错误并给出明确提示
3. **强制关闭**：使用系统命令强制关闭所有 ngrok 进程
4. **更好的错误处理**：提供详细的错误信息和解决方案

## 使用建议

### 日常使用

1. **启动应用前**：如果遇到会话限制错误，先运行 `python cleanup_ngrok.py`
2. **定期检查**：使用 `python check_ngrok_status.py` 检查状态
3. **使用配置文件**：如果需要多个端点，使用 `ngrok.yml` 配置文件

### 避免问题

1. **不要同时运行多个 `run.py`**：每次只运行一个实例
2. **正确关闭应用**：使用 Ctrl+C 正常关闭，不要直接关闭终端
3. **定期清理**：如果长时间运行，定期检查并清理不需要的会话

## 文件说明

- `cleanup_ngrok.py`: 清理所有 ngrok 进程和会话的脚本
- `check_ngrok_status.py`: 检查当前 ngrok 状态的脚本
- `ngrok.yml`: ngrok 配置文件（用于统一管理多个端点）
- `run.py`: 改进后的主启动文件（已增强清理功能）

## 常见错误

### ERR_NGROK_108: 会话数限制

**原因**：已达到同时会话数上限（免费版 3 个）

**解决**：
1. 运行 `python cleanup_ngrok.py`
2. 访问 https://dashboard.ngrok.com/agents 手动关闭会话
3. 等待几分钟后重试

### ERR_NGROK_334: 端点已在线

**原因**：端点仍在远程服务器上

**解决**：
1. 运行 `python cleanup_ngrok.py`
2. 等待 2-3 分钟后重试
3. 如果问题持续，访问控制台手动关闭

### 心跳超时

**原因**：网络连接不稳定或进程异常

**解决**：
1. 检查网络连接
2. 运行 `python cleanup_ngrok.py` 清理
3. 重新启动应用

## 升级到付费计划

如果需要更多同时会话，可以考虑升级到 ngrok 付费计划：
- 访问 https://dashboard.ngrok.com/billing/choose-a-plan
- 付费计划可以移除会话数限制

## 技术支持

如果问题仍然存在：
1. 检查 ngrok 控制台：https://dashboard.ngrok.com/agents
2. 查看 ngrok 日志
3. 确认网络连接正常

