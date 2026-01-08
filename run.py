# -*- coding: utf-8 -*-
import sys
import os
import io

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    # 设置标准输出编码为UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from app import create_app
from config import Config
from dotenv import load_dotenv
import atexit

# 加载.env文件
load_dotenv()

app = create_app(Config)

if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    
    # 使用Token模式启动ngrok（如果配置了token）
    try:
        from pyngrok import ngrok
        import time
        
        # 从环境变量获取ngrok token
        ngrok_auth_token = os.environ.get('NGROK_AUTH_TOKEN', '').strip()
        
        if not ngrok_auth_token:
            print("\n" + "="*70)
            print("ℹ️  未设置NGROK_AUTH_TOKEN，将使用免费模式")
            print("="*70)
            print("提示：如需使用固定地址，请在 .env 文件中设置 NGROK_AUTH_TOKEN")
            print("获取token: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("="*70 + "\n")
            use_token = False
        else:
            use_token = True
            print("\n" + "="*70)
            print("🚀 正在启动Ngrok固定地址隧道（Token模式）...")
            print("="*70)
        
        # 只检查并关闭当前端口的隧道（如果有），不关闭其他隧道
        def check_and_close_port_tunnel():
            """只检查并关闭当前端口的隧道，确保完全关闭"""
            closed_count = 0
            max_cleanup_attempts = 3
            
            for cleanup_attempt in range(max_cleanup_attempts):
                try:
                    tunnels = ngrok.get_tunnels()
                    if not tunnels:
                        break
                    
                    # 只查找指向当前端口的隧道
                    port_tunnels = []
                    for tunnel in tunnels:
                        try:
                            # 检查隧道配置的本地地址是否匹配当前端口
                            tunnel_addr = tunnel.config.get('addr', '')
                            # 匹配格式: "localhost:5000", "127.0.0.1:5000", "5000" 等
                            if (f':{port}' in str(tunnel_addr) or 
                                tunnel_addr == str(port) or
                                tunnel_addr == f'localhost:{port}' or
                                tunnel_addr == f'127.0.0.1:{port}'):
                                port_tunnels.append(tunnel)
                        except:
                            pass
                    
                    if not port_tunnels:
                        break
                    
                    if cleanup_attempt == 0:
                        print(f"🔍 发现 {len(port_tunnels)} 个指向端口 {port} 的隧道，正在关闭...")
                    
                    for tunnel in port_tunnels:
                        try:
                            if tunnel.public_url:
                                ngrok.disconnect(tunnel.public_url)
                                closed_count += 1
                                if cleanup_attempt == 0:
                                    print(f"   ✓ 已关闭隧道: {tunnel.public_url}")
                        except Exception as e:
                            pass
                    
                    # 等待隧道完全关闭
                    time.sleep(1)
                    
                except Exception as e:
                    break
            
            if closed_count > 0:
                print(f"✓ 已关闭 {closed_count} 个指向端口 {port} 的隧道")
                time.sleep(1)  # 额外等待确保完全释放
        
        # 如果使用token模式，设置认证token
        if use_token:
            try:
                ngrok.set_auth_token(ngrok_auth_token)
                print("✓ Ngrok认证token已设置")
            except Exception as e:
                error_msg = str(e)
                if "invalid" in error_msg.lower() or "ERR_NGROK_107" in error_msg:
                    print(f"\n❌ Ngrok认证token无效！")
                    print(f"   您提供的token: {ngrok_auth_token[:20]}...")
                    print(f"\n   可能的原因：")
                    print(f"   1. Token已过期或被重置")
                    print(f"   2. Token是团队账号的，但您已被移除")
                    print(f"   3. Token已被撤销")
                    print(f"\n   解决方案：")
                    print(f"   1. 访问 https://dashboard.ngrok.com/get-started/your-authtoken 获取新token")
                    print(f"   2. 更新 .env 文件中的 NGROK_AUTH_TOKEN")
                    print(f"   3. 或者删除 .env 文件中的 NGROK_AUTH_TOKEN 行，使用免费模式\n")
                    raise Exception("Ngrok认证失败，请检查token或使用免费模式")
                else:
                    print(f"⚠️  设置ngrok token失败: {str(e)}")
                    print("   继续使用未认证模式\n")
                    use_token = False
        
        # 检查是否已经有指向当前端口的隧道（处理Flask reloader的情况）
        def find_existing_tunnel():
            """查找已存在的指向当前端口的隧道"""
            try:
                tunnels = ngrok.get_tunnels()
                if tunnels:
                    for tunnel in tunnels:
                        try:
                            tunnel_addr = tunnel.config.get('addr', '')
                            # 匹配格式: "localhost:5000", "127.0.0.1:5000", "5000" 等
                            if (f':{port}' in str(tunnel_addr) or 
                                tunnel_addr == str(port) or
                                tunnel_addr == f'localhost:{port}' or
                                tunnel_addr == f'127.0.0.1:{port}'):
                                return tunnel
                        except:
                            pass
            except:
                pass
            return None
        
        # 先检查是否已有隧道（Flask reloader 时会重用现有隧道）
        existing_tunnel = find_existing_tunnel()
        
        if existing_tunnel:
            # 如果已有隧道，直接使用（Flask reloader 的情况）
            tunnel = existing_tunnel
            public_url = tunnel.public_url
            print(f"✓ 检测到现有隧道，直接使用: {public_url}")
            print("   (Flask debug模式reloader，重用现有隧道)")
        else:
            # 没有现有隧道，先清理可能残留的隧道
            check_and_close_port_tunnel()
            
            # 创建ngrok隧道
            if use_token:
                print("\n🚀 正在创建固定地址隧道...")
            else:
                print("\n🚀 正在创建免费模式隧道...")
            
            # 创建ngrok隧道，确保只创建一个
            max_retries = 3
            public_url = None
            tunnel = None  # 初始化隧道变量
            use_https = True  # 优先使用HTTPS
        
            for attempt in range(max_retries):
                try:
                    # 在每次尝试前，再次检查是否已有隧道（可能其他进程已创建）
                    existing_tunnel = find_existing_tunnel()
                    if existing_tunnel:
                        tunnel = existing_tunnel
                        public_url = tunnel.public_url
                        print(f"✓ 检测到现有隧道，直接使用: {public_url}")
                        break
                    
                    # 在每次尝试前，再次检查并关闭可能存在的隧道
                    if attempt > 0:
                        check_and_close_port_tunnel()
                    
                    # 尝试创建隧道（优先HTTPS，如果失败则尝试HTTP）
                    if use_https:
                        try:
                            tunnel = ngrok.connect(str(port), bind_tls=True)
                            public_url = tunnel.public_url
                            print(f"✓ 已创建HTTPS隧道: {public_url}")
                            break
                        except Exception as https_error:
                            https_error_msg = str(https_error)
                            # 如果HTTPS失败且不是端点已存在的错误，尝试HTTP
                            if "already online" not in https_error_msg and "ERR_NGROK_334" not in https_error_msg:
                                print(f"   ⚠️  HTTPS隧道创建失败，尝试HTTP模式...")
                                use_https = False
                                # 继续到HTTP尝试
                            else:
                                # 如果是端点已存在的错误，尝试查找现有隧道
                                existing_tunnel = find_existing_tunnel()
                                if existing_tunnel:
                                    tunnel = existing_tunnel
                                    public_url = tunnel.public_url
                                    print(f"✓ 端点已存在，使用现有隧道: {public_url}")
                                    break
                                raise https_error
                    
                    # 如果HTTPS失败或已切换，尝试HTTP
                    if not use_https or (attempt == max_retries - 1 and tunnel is None):
                        tunnel = ngrok.connect(str(port), bind_tls=False)
                        public_url = tunnel.public_url
                        print(f"✓ 已创建HTTP隧道: {public_url}")
                        break
                        
                except Exception as e:
                    error_msg = str(e)
                    
                    # 检查是否是会话限制错误
                    if "ERR_NGROK_108" in error_msg or "limited to" in error_msg.lower() or "simultaneous" in error_msg.lower():
                        print(f"\n❌ Ngrok 会话数限制错误！")
                        print("=" * 70)
                        print("   您的账户已达到同时会话数限制（免费版限制为 3 个）")
                        print("\n   解决方案：")
                        print("   1. 运行清理脚本: python cleanup_ngrok.py")
                        print("   2. 访问 https://dashboard.ngrok.com/agents 手动关闭不需要的会话")
                        print("   3. 等待几分钟后重试")
                        print("   4. 或使用 ngrok.yml 配置文件统一管理多个端点")
                        print("=" * 70)
                        raise Exception("Ngrok 会话数限制，请先清理现有会话")
                    
                    if "already online" in error_msg or "ERR_NGROK_334" in error_msg:
                        # 端点已存在，尝试查找现有隧道
                        existing_tunnel = find_existing_tunnel()
                        if existing_tunnel:
                            tunnel = existing_tunnel
                            public_url = tunnel.public_url
                            print(f"✓ 端点已存在，使用现有隧道: {public_url}")
                            break
                        
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 3
                            print(f"   ⚠️  端点仍在使用中，等待 {wait_time} 秒后重试 ({attempt + 1}/{max_retries})...")
                            time.sleep(wait_time)
                            # 再次尝试关闭当前端口的隧道
                            check_and_close_port_tunnel()
                        else:
                            # 最后一次尝试失败
                            raise Exception(f"无法创建隧道: 端点仍在使用中，请手动清理或等待后重试")
                    else:
                        # 其他错误，如果是最后一次尝试且还没尝试HTTP，尝试HTTP
                        if attempt == max_retries - 1 and use_https:
                            print(f"   ⚠️  创建隧道失败，最后尝试HTTP模式...")
                            try:
                                check_and_close_port_tunnel()
                                tunnel = ngrok.connect(str(port), bind_tls=False)
                                public_url = tunnel.public_url
                                print(f"✓ 已创建HTTP隧道: {public_url}")
                                break
                            except Exception as e2:
                                raise Exception(f"无法创建隧道: {str(e2)}")
                        else:
                            raise e
        
        # 验证只创建了一个隧道
        if tunnel:
            try:
                tunnels = ngrok.get_tunnels()
                port_tunnels = [t for t in tunnels if t.public_url == public_url]
                if len(port_tunnels) != 1:
                    print(f"⚠️  警告: 检测到多个隧道指向端口 {port}，正在清理...")
                    check_and_close_port_tunnel()
                    # 重新获取当前隧道
                    tunnels = ngrok.get_tunnels()
                    port_tunnels = [t for t in tunnels if t.public_url == public_url]
                    if len(port_tunnels) != 1:
                        print(f"⚠️  警告: 隧道数量异常，但将继续运行")
            except:
                pass
        
        if public_url and tunnel:
            # 最终验证：确保只创建了一个指向当前端口的隧道
            try:
                final_tunnels = ngrok.get_tunnels()
                port_tunnels_count = 0
                for t in final_tunnels:
                    try:
                        tunnel_addr = t.config.get('addr', '')
                        if (f':{port}' in str(tunnel_addr) or 
                            tunnel_addr == str(port) or
                            tunnel_addr == f'localhost:{port}' or
                            tunnel_addr == f'127.0.0.1:{port}'):
                            port_tunnels_count += 1
                    except:
                        pass
                
                if port_tunnels_count > 1:
                    print(f"\n⚠️  警告: 检测到 {port_tunnels_count} 个指向端口 {port} 的隧道")
                    print("   正在清理多余的隧道...")
                    check_and_close_port_tunnel()
                    # 只保留当前隧道
                    final_tunnels = ngrok.get_tunnels()
                    for t in final_tunnels:
                        if t.public_url != public_url:
                            try:
                                tunnel_addr = t.config.get('addr', '')
                                if (f':{port}' in str(tunnel_addr) or 
                                    tunnel_addr == str(port) or
                                    tunnel_addr == f'localhost:{port}' or
                                    tunnel_addr == f'127.0.0.1:{port}'):
                                    if t.public_url and isinstance(t.public_url, str):
                                        ngrok.disconnect(t.public_url)
                            except:
                                pass
            except:
                pass
            
            print("\n" + "="*70)
            if use_token:
                print("✅ Ngrok 固定地址隧道已成功启动！")
                print("="*70)
                print(f"🌐 公网访问地址（固定）: {public_url}")
                print(f"🔗 本地访问地址: http://{host}:{port}")
                print("="*70)
                print("\n📋 使用说明：")
                print("   - 使用token模式，地址相对固定（取决于您的ngrok计划）")
                print("   - 将公网地址分享给其他用户即可访问")
                print("   - 按 Ctrl+C 停止服务器和隧道")
                print("   - 此项目只占用一个ngrok隧道，不影响其他项目")
                print("="*70 + "\n")
            else:
                print("✅ Ngrok 免费隧道已成功启动！")
                print("="*70)
                print(f"🌐 公网访问地址: {public_url}")
                print(f"🔗 本地访问地址: http://{host}:{port}")
                print("="*70)
                print("\n📋 使用说明：")
                print("   - 将公网地址分享给其他用户即可访问")
                print("   - 免费版地址每次重启都会变化")
                print("   - 如需固定地址，请在 .env 文件中设置 NGROK_AUTH_TOKEN")
                print("   - 按 Ctrl+C 停止服务器和隧道")
                print("   - 此项目只占用一个ngrok隧道，不影响其他项目")
                print("="*70 + "\n")
            
            # 注册退出时只关闭当前创建的隧道
            current_tunnel_url = public_url
            current_tunnel = tunnel  # 保存隧道对象
            
            def close_current_tunnel():
                try:
                    if current_tunnel_url and isinstance(current_tunnel_url, str):
                        ngrok.disconnect(current_tunnel_url)
                        print(f"\n✓ 已关闭当前隧道: {current_tunnel_url}")
                except:
                    # 如果断开连接失败，尝试通过隧道对象关闭
                    try:
                        if current_tunnel and hasattr(current_tunnel, 'public_url') and current_tunnel.public_url:
                            tunnel_url = current_tunnel.public_url
                            if isinstance(tunnel_url, str):
                                ngrok.disconnect(tunnel_url)
                                print(f"\n✓ 已关闭当前隧道")
                    except:
                        pass
            
            atexit.register(close_current_tunnel)
        else:
            raise Exception("无法创建ngrok隧道")
            
    except ImportError:
        print("\n⚠️  提示: pyngrok 未安装，仅使用本地模式")
        print("   如需公网访问，请运行: pip install pyngrok")
        print("   然后重新运行此脚本\n")
    except Exception as e:
        print(f"\n⚠️  警告: 启动ngrok失败: {str(e)}")
        print("   继续使用本地模式运行")
        print(f"   本地访问地址: http://{host}:{port}\n")
    
    # 从配置中读取debug模式设置
    # 默认关闭debug模式，避免Flask reloader导致ngrok重复创建问题
    # 如需开启，在.env文件中设置 FLASK_DEBUG=True
    debug_mode = app.config.get('DEBUG', False)
    
    if debug_mode:
        print("\n" + "="*70)
        print("⚠️  调试模式已开启")
        print("="*70)
        print("   - 代码修改后会自动重载")
        print("   - 显示详细错误信息")
        print("   - 注意：Flask reloader可能导致ngrok隧道重复创建")
        print("   - 如果遇到ngrok错误，建议关闭调试模式（设置FLASK_DEBUG=False）")
        print("="*70 + "\n")
    
    app.run(debug=debug_mode, host=host, port=port)

