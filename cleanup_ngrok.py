"""
清理所有 ngrok 进程和会话的脚本
用于解决 ngrok 会话数限制问题
"""
import os
import sys
import time
import subprocess
import platform

# 修复 Windows 控制台编码问题
if platform.system() == "Windows":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def kill_ngrok_processes():
    """强制关闭所有 ngrok 进程"""
    print("=" * 70)
    print("🔍 正在检查 ngrok 进程...")
    print("=" * 70)
    
    system = platform.system()
    killed_count = 0
    
    try:
        if system == "Windows":
            # Windows 系统
            try:
                # 查找所有 ngrok 进程
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq ngrok.exe", "/FO", "CSV"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if "ngrok.exe" in result.stdout:
                    lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                    pids = []
                    for line in lines:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) > 1:
                                pid = parts[1].strip('"')
                                if pid.isdigit():
                                    pids.append(pid)
                    
                    if pids:
                        print(f"   发现 {len(pids)} 个 ngrok 进程: {', '.join(pids)}")
                        for pid in pids:
                            try:
                                subprocess.run(
                                    ["taskkill", "/F", "/PID", pid],
                                    capture_output=True,
                                    check=False
                                )
                                print(f"   ✓ 已终止进程 PID: {pid}")
                                killed_count += 1
                            except Exception as e:
                                print(f"   ⚠️  无法终止进程 {pid}: {e}")
                    else:
                        print("   ✓ 未发现 ngrok 进程")
                else:
                    print("   ✓ 未发现 ngrok 进程")
                    
            except Exception as e:
                print(f"   ⚠️  检查进程时出错: {e}")
        
        elif system in ["Linux", "Darwin"]:  # Linux 或 macOS
            try:
                result = subprocess.run(
                    ["pgrep", "-f", "ngrok"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    print(f"   发现 {len(pids)} 个 ngrok 进程: {', '.join(pids)}")
                    for pid in pids:
                        try:
                            subprocess.run(
                                ["kill", "-9", pid],
                                capture_output=True,
                                check=False
                            )
                            print(f"   ✓ 已终止进程 PID: {pid}")
                            killed_count += 1
                        except Exception as e:
                            print(f"   ⚠️  无法终止进程 {pid}: {e}")
                else:
                    print("   ✓ 未发现 ngrok 进程")
                    
            except Exception as e:
                print(f"   ⚠️  检查进程时出错: {e}")
        
        time.sleep(1)  # 等待进程完全关闭
        
    except Exception as e:
        print(f"   ❌ 清理进程时出错: {e}")
    
    return killed_count

def cleanup_ngrok_tunnels():
    """清理所有 ngrok 隧道（通过 API）"""
    print("\n" + "=" * 70)
    print("🔍 正在检查 ngrok 隧道...")
    print("=" * 70)
    
    try:
        from pyngrok import ngrok
        
        try:
            tunnels = ngrok.get_tunnels()
            if tunnels:
                print(f"   发现 {len(tunnels)} 个活动隧道")
                for tunnel in tunnels:
                    try:
                        if tunnel.public_url:
                            ngrok.disconnect(tunnel.public_url)
                            print(f"   ✓ 已关闭隧道: {tunnel.public_url}")
                    except Exception as e:
                        print(f"   ⚠️  关闭隧道失败: {e}")
            else:
                print("   ✓ 未发现活动隧道")
        except Exception as e:
            print(f"   ⚠️  获取隧道列表失败: {e}")
        
        # 尝试关闭所有 ngrok 进程
        try:
            ngrok.kill()
            print("   ✓ 已调用 ngrok.kill()")
        except Exception as e:
            print(f"   ⚠️  调用 ngrok.kill() 失败: {e}")
            
    except ImportError:
        print("   ℹ️  pyngrok 未安装，跳过隧道清理")
    except Exception as e:
        print(f"   ⚠️  清理隧道时出错: {e}")

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧹 Ngrok 清理工具")
    print("=" * 70)
    print("此工具将关闭所有 ngrok 进程和会话")
    print("=" * 70 + "\n")
    
    # 清理隧道
    cleanup_ngrok_tunnels()
    
    # 强制关闭进程
    killed_count = kill_ngrok_processes()
    
    print("\n" + "=" * 70)
    if killed_count > 0:
        print(f"✅ 清理完成！已终止 {killed_count} 个 ngrok 进程")
    else:
        print("✅ 清理完成！未发现需要清理的进程")
    print("=" * 70)
    print("\n💡 提示：")
    print("   - 如果问题仍然存在，请访问 https://dashboard.ngrok.com/agents")
    print("   - 在 ngrok 控制台手动关闭不需要的会话")
    print("   - 等待几分钟后重试")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

