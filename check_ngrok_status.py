"""
检查当前 ngrok 状态脚本
用于查看当前运行的 ngrok 进程和会话
"""
import os
import sys
import subprocess
import platform
from datetime import datetime

# 修复 Windows 控制台编码问题
if platform.system() == "Windows":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def check_ngrok_processes():
    """检查 ngrok 进程"""
    print("=" * 70)
    print("📊 Ngrok 状态检查")
    print("=" * 70)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    system = platform.system()
    process_count = 0
    
    print("🔍 进程检查:")
    print("-" * 70)
    
    try:
        if system == "Windows":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq ngrok.exe", "/FO", "CSV"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if "ngrok.exe" in result.stdout:
                lines = result.stdout.strip().split('\n')[1:]
                processes = []
                for line in lines:
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            pid = parts[1].strip('"')
                            mem = parts[4].strip('"') if len(parts) > 4 else "N/A"
                            if pid.isdigit():
                                processes.append({"pid": pid, "memory": mem})
                                process_count += 1
                
                if processes:
                    print(f"   发现 {process_count} 个 ngrok 进程:")
                    for proc in processes:
                        print(f"   - PID: {proc['pid']}, 内存: {proc['memory']}")
                else:
                    print("   ✓ 未发现 ngrok 进程")
            else:
                print("   ✓ 未发现 ngrok 进程")
                
        elif system in ["Linux", "Darwin"]:
            result = subprocess.run(
                ["pgrep", "-f", "ngrok"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                process_count = len(pids)
                print(f"   发现 {process_count} 个 ngrok 进程:")
                for pid in pids:
                    print(f"   - PID: {pid}")
            else:
                print("   ✓ 未发现 ngrok 进程")
                
    except Exception as e:
        print(f"   ⚠️  检查进程时出错: {e}")
    
    return process_count

def check_ngrok_tunnels():
    """检查 ngrok 隧道"""
    print("\n🔍 隧道检查:")
    print("-" * 70)
    
    try:
        from pyngrok import ngrok
        
        try:
            tunnels = ngrok.get_tunnels()
            if tunnels:
                print(f"   发现 {len(tunnels)} 个活动隧道:")
                for i, tunnel in enumerate(tunnels, 1):
                    print(f"\n   隧道 {i}:")
                    print(f"   - 公网地址: {tunnel.public_url}")
                    print(f"   - 本地地址: {tunnel.config.get('addr', 'N/A')}")
                    print(f"   - 协议: {tunnel.proto}")
            else:
                print("   ✓ 未发现活动隧道")
        except Exception as e:
            print(f"   ⚠️  获取隧道列表失败: {e}")
            print(f"   错误信息: {str(e)}")
            
    except ImportError:
        print("   ℹ️  pyngrok 未安装，无法检查隧道")
        print("   安装命令: pip install pyngrok")
    except Exception as e:
        print(f"   ⚠️  检查隧道时出错: {e}")

def check_ngrok_config():
    """检查 ngrok 配置"""
    print("\n🔍 配置检查:")
    print("-" * 70)
    
    # 检查配置文件
    config_file = "ngrok.yml"
    if os.path.exists(config_file):
        print(f"   ✓ 发现配置文件: {config_file}")
    else:
        print(f"   ⚠️  未发现配置文件: {config_file}")
    
    # 检查环境变量
    auth_token = os.environ.get('NGROK_AUTH_TOKEN', '')
    if auth_token:
        print(f"   ✓ NGROK_AUTH_TOKEN 已设置 (长度: {len(auth_token)})")
    else:
        print("   ⚠️  NGROK_AUTH_TOKEN 未设置 (将使用免费模式)")

def main():
    """主函数"""
    process_count = check_ngrok_processes()
    check_ngrok_tunnels()
    check_ngrok_config()
    
    print("\n" + "=" * 70)
    print("📋 总结:")
    print("-" * 70)
    print(f"   - 运行中的进程数: {process_count}")
    
    if process_count >= 3:
        print("\n   ⚠️  警告: 检测到 3 个或更多进程，可能已达到会话限制！")
        print("   建议:")
        print("   1. 运行 python cleanup_ngrok.py 清理所有进程")
        print("   2. 访问 https://dashboard.ngrok.com/agents 手动关闭会话")
        print("   3. 使用 ngrok.yml 配置文件统一管理多个端点")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

