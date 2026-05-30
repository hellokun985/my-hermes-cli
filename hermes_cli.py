#!/usr/bin/env python3
"""
Hermes Agent 管理工具
启动命令: hc
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from typing import Optional, Tuple, List

# === 版本信息 ===
VERSION = "1.1"
SCRIPT_NAME = "hermes_cli.py"
GITHUB_REPO = "https://github.com/hellokun985/my-hermes-cli"
RAW_URL = f"https://raw.githubusercontent.com/hellokun985/my-hermes-cli/main/{SCRIPT_NAME}"

# === 路径常量 ===
HERMES_HOME = Path.home() / ".hermes"
CONFIG_FILE = HERMES_HOME / "config.yaml"
INSTALL_SCRIPT = "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh"
SCRIPT_PATH = Path(__file__).resolve()

# === 颜色定义 ===
class Colors:
    """终端颜色定义"""
    BLUE = '\033[38;5;39m'
    GREEN = '\033[38;5;82m'
    RED = '\033[38;5;196m'
    YELLOW = '\033[38;5;214m'
    CYAN = '\033[38;5;45m'
    WHITE = '\033[38;5;255m'
    GRAY = '\033[38;5;245m'
    RESET = '\033[0m'

# === ASCII 艺术字 ===
HERMESCLI_ASCII = f"""{Colors.BLUE}
    ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗ ██████╗██╗     ██╗
    ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██║     ██║
    ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗██║     ██║     ██║
    ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║██║     ██║     ██║
    ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║╚██████╗███████╗██║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝{Colors.RESET}
"""

# === 基础工具函数 ===

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_interactive(cmd: str) -> int:
    """执行交互式命令（继承终端）"""
    return subprocess.run(cmd, shell=True).returncode

def run_capture(cmd: str) -> Tuple[int, str, str]:
    """执行非交互式命令（捕获输出）"""
    result = subprocess.run(
        cmd, shell=True,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr

def check_installed() -> bool:
    """检查 Hermes 是否已安装"""
    return shutil.which('hermes') is not None

def get_version() -> str:
    """获取当前版本"""
    if not check_installed():
        return "未安装"
    
    # 优先从 dist-info 读取
    venv_dir = HERMES_HOME / "hermes-agent" / "venv"
    if venv_dir.exists():
        for metadata in venv_dir.glob("lib/python*/site-packages/hermes_agent-*.dist-info/METADATA"):
            try:
                with open(metadata, 'r') as f:
                    for line in f:
                        if line.startswith("Version:"):
                            return "v" + line.split(":")[1].strip()
            except:
                pass
    
    # 兜底执行 hermes --version
    try:
        result = subprocess.run(
            ["hermes", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return "未知版本"

def get_gateway_status() -> str:
    """获取 Gateway 运行状态"""
    # 检查 systemd 服务
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "hermes-gateway.service"],
            capture_output=True, text=True
        )
        if result.stdout.strip() == "active":
            return "运行中"
    except:
        pass
    
    # 检查进程
    try:
        result = subprocess.run(
            ["pgrep", "-f", "hermes.*gateway.*run"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return "运行中"
    except:
        pass
    
    return "已停止"

def refresh_path():
    """刷新 PATH 环境变量"""
    hermes_bin = HERMES_HOME / "hermes-agent" / "venv" / "bin"
    if hermes_bin.exists() and str(hermes_bin) not in os.environ.get('PATH', ''):
        os.environ['PATH'] = str(hermes_bin) + ':' + os.environ.get('PATH', '')

# === 输入函数 ===

def get_input(prompt: str = "请选择", valid_range: tuple = None) -> str:
    """
    获取用户输入，支持快捷命令和回退
    
    Returns:
        str: 用户输入
        'back': 用户请求返回
        'quit': 用户请求退出
        'search:xxx': 搜索命令
    """
    while True:
        try:
            user_input = input(f"      {prompt}: ").strip().lower()
            
            # 空输入
            if not user_input:
                continue
            
            # 快捷命令
            if user_input in ('0', 'b', 'back'):
                return 'back'
            if user_input in ('q', 'quit', 'exit'):
                return 'quit'
            if user_input in ('c', 'clear'):
                clear_screen()
                return 'clear'
            
            # 搜索命令
            if user_input.startswith('/'):
                search_keyword = user_input[1:]
                return f'search:{search_keyword}'
            
            # 数字验证
            if valid_range:
                try:
                    num = int(user_input)
                    if valid_range[0] <= num <= valid_range[1]:
                        return str(num)
                    else:
                        print(f"      {Colors.RED}❌ 选项不存在，请输入 {valid_range[0]}-{valid_range[1]} 之间的数字{Colors.RESET}")
                        continue
                except ValueError:
                    print(f"      {Colors.RED}❌ 无效输入，请输入数字{Colors.RESET}")
                    continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n")
            return 'back'
        except EOFError:
            return 'quit'

# === 自更新功能 ===

def get_remote_version() -> Optional[str]:
    """获取远程版本号（使用 GitHub API 避免 CDN 缓存）"""
    try:
        import urllib.request
        import base64
        import json
        
        # 使用 GitHub API 获取最新版本
        api_url = "https://api.github.com/repos/hellokun985/my-hermes-cli/contents/VERSION"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'hermes-cli'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            version = base64.b64decode(data['content']).decode('utf-8').strip()
            return version
    except:
        # 如果 API 失败，尝试使用 raw URL
        try:
            import urllib.request
            version_url = f"https://raw.githubusercontent.com/hellokun985/my-hermes-cli/main/VERSION"
            req = urllib.request.Request(version_url, headers={'User-Agent': 'hermes-cli'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8').strip()
        except:
            return None

def update_from_github() -> bool:
    """从 GitHub 更新脚本（使用 API 避免 CDN 缓存）"""
    try:
        import urllib.request
        import base64
        import json
        
        print_info("正在检查更新...")
        
        # 使用 GitHub API 获取最新版本
        api_url = "https://api.github.com/repos/hellokun985/my-hermes-cli/contents/hermes_cli.py"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'hermes-cli'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            new_content = base64.b64decode(data['content']).decode('utf-8')
        
        # 从下载内容中提取版本号
        remote_version = None
        for line in new_content.split('\n'):
            if line.startswith('VERSION'):
                remote_version = line.split('"')[1]
                break
        
        if not remote_version:
            print_error("无法获取远程版本信息")
            return False
        
        if remote_version == VERSION:
            print_info(f"当前已是最新版本 v{VERSION}")
            return False
        
        print_info(f"发现新版本: v{remote_version}，正在下载...")
        
        # 备份当前版本
        backup_path = SCRIPT_PATH.with_suffix('.py.bak')
        shutil.copy2(SCRIPT_PATH, backup_path)
        print_info(f"已备份当前版本")
        
        # 写入新版本
        with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # 设置执行权限
        SCRIPT_PATH.chmod(0o755)
        
        print_success(f"更新成功！v{VERSION} -> v{remote_version}")
        print_info("请重新运行脚本以使用新版本")
        return True
    except Exception as e:
        print_error(f"更新失败: {e}")
        return False

def self_update():
    """脚本更新"""
    clear_screen()
    print_header("脚本更新", show_ascii=True)
    print_separator()
    
    # 显示版本信息
    print(f"\n      当前版本: {Colors.WHITE}v{VERSION}{Colors.RESET}")
    print(f"      脚本路径: {SCRIPT_PATH}")
    
    # 检查远程版本
    remote_version = get_remote_version()
    if remote_version:
        if remote_version != VERSION:
            print(f"      远程版本: {Colors.GREEN}v{remote_version} (有更新){Colors.RESET}")
        else:
            print(f"      远程版本: {Colors.GREEN}v{remote_version} (已是最新){Colors.RESET}")
    else:
        print(f"      远程版本: {Colors.GRAY}无法获取{Colors.RESET}")
    
    print_separator()
    
    # 检查是否有更新
    if not remote_version or remote_version == VERSION:
        print_info("当前已是最新版本，无需更新")
        prompt_continue()
        return
    
    # 确认更新
    print_warning(f"发现新版本 v{remote_version}，是否更新？")
    confirm = input("      输入 y 确认更新: ").strip().lower()
    
    if confirm == 'y':
        update_from_github()
    
    prompt_continue()

# === UI 组件 ===

def print_header(title: str, show_ascii: bool = True):
    """打印头部"""
    if show_ascii:
        print(HERMESCLI_ASCII)
    print(f"    {Colors.WHITE}{title} v{VERSION}{Colors.RESET}")
    print("    " + "─" * 70)

def print_status():
    """打印状态信息"""
    status = get_gateway_status()
    version = get_version()
    status_color = Colors.GREEN if status == "运行中" else Colors.RED
    print(f"\n      运行状态: [{status_color}{status}{Colors.RESET}]    当前版本: {version}")
    print(f"      安装路径: {HERMES_HOME}")

def print_separator():
    """打印分隔线"""
    print(f"\n    {Colors.GRAY}{'─' * 70}{Colors.RESET}")

def print_section_header(icon: str, title: str):
    """打印版块标题"""
    print(f"\n    {Colors.CYAN}{icon} {title}{Colors.RESET}")
    print(f"    {Colors.GRAY}{'─' * 70}{Colors.RESET}")

def print_menu_item(num: int, name: str, width: int = 35):
    """打印菜单项"""
    print(f"      {Colors.WHITE}{num:>2}.{Colors.RESET} {name:<{width}}")

def print_two_columns(left_title: str, left_items: list, 
                      right_title: str, right_items: list,
                      left_start: int = 1, right_start: int = 1,
                      left_icon: str = "▸", right_icon: str = "▸"):
    """打印双列菜单"""
    print(f"\n    {Colors.CYAN}{left_icon} {left_title:<32}{right_icon} {right_title}{Colors.RESET}")
    print(f"    {Colors.GRAY}{'─' * 70}{Colors.RESET}")
    max_len = max(len(left_items), len(right_items))
    for i in range(max_len):
        left_num = left_start + i if i < len(left_items) else ""
        left_name = left_items[i] if i < len(left_items) else ""
        right_num = right_start + i if i < len(right_items) else ""
        right_name = right_items[i] if i < len(right_items) else ""
        
        left_part = f"{left_num:>2}. {left_name:<30}" if left_name else " " * 34
        right_part = f"{right_num:>2}. {right_name}" if right_name else ""
        print(f"      {Colors.WHITE}{left_part}{Colors.RESET}{right_part}")

def print_single_column(title: str, items: list, start_num: int = 1, icon: str = "▸"):
    """打印单列菜单"""
    print(f"\n    {Colors.CYAN}{icon} {title}{Colors.RESET}")
    print(f"    {Colors.GRAY}{'─' * 70}{Colors.RESET}")
    for i, item in enumerate(items, start_num):
        print(f"      {Colors.WHITE}{i:>2}.{Colors.RESET} {item}")

def print_help():
    """打印帮助信息"""
    print(f"\n    {Colors.GRAY}{'─' * 70}{Colors.RESET}")
    print(f"      {Colors.GRAY}0=返回  q=退出  Ctrl+C=中断  /=搜索{Colors.RESET}")
    print(f"    {Colors.GRAY}{'─' * 70}{Colors.RESET}")

def print_success(message: str):
    """打印成功消息"""
    print(f"\n      {Colors.GREEN}✅ {message}{Colors.RESET}\n")

def print_error(message: str):
    """打印错误消息"""
    print(f"\n      {Colors.RED}❌ {message}{Colors.RESET}\n")

def print_warning(message: str):
    """打印警告消息"""
    print(f"\n      {Colors.YELLOW}⚠️  {message}{Colors.RESET}\n")

def print_info(message: str):
    """打印信息消息"""
    print(f"\n      {Colors.CYAN}ℹ️  {message}{Colors.RESET}\n")

def prompt_continue():
    """提示按任意键继续"""
    input(f"\n      {Colors.GRAY}按 Enter 键继续...{Colors.RESET}")

# === 检查函数 ===

def check_hermes_installed() -> bool:
    """检查 Hermes 是否已安装，未安装则提示"""
    if not check_installed():
        print_warning("Hermes 未安装，请先选择 '1. 安装 Hermes' 进行安装")
        prompt_continue()
        return False
    return True

# === 安装与更新模块 ===

def install_hermes():
    """安装 Hermes"""
    print_header("安装 Hermes Agent", show_ascii=False)
    print_separator()
    
    if check_installed():
        print_warning("Hermes 已安装，是否重新安装？")
        choice = input("      输入 y 确认重新安装: ").strip().lower()
        if choice != 'y':
            return
    
    print_info("正在安装 Hermes Agent...")
    print("      这可能需要几分钟时间，请耐心等待。\n")
    
    # 执行安装脚本
    cmd = f'curl -fsSL {INSTALL_SCRIPT} | bash'
    result = run_interactive(cmd)
    
    if result == 0:
        refresh_path()
        print_success("Hermes Agent 安装成功！")
        
        # 提示配置
        print_info("接下来将运行配置向导...")
        run_interactive("hermes setup")
    else:
        print_error("安装失败，请检查网络连接后重试")

def update_hermes():
    """更新 Hermes"""
    if not check_hermes_installed():
        return
    
    print_header("更新 Hermes", show_ascii=False)
    print_separator()
    print_info("正在检查更新...")
    
    result = run_interactive("hermes update")
    
    if result == 0:
        print_success("更新完成！")
    else:
        print_error("更新失败")

def uninstall_hermes():
    """卸载 Hermes"""
    if not check_hermes_installed():
        return
    
    print_header("卸载 Hermes", show_ascii=False)
    print_separator()
    
    print_warning("确定要卸载 Hermes 吗？")
    print("      此操作将删除所有配置和数据。\n")
    choice = input("      输入 y 确认卸载: ").strip().lower()
    
    if choice == 'y':
        result = run_interactive("hermes uninstall")
        if result == 0:
            print_success("Hermes 已卸载")
        else:
            print_error("卸载失败")
    else:
        print_info("已取消卸载")

# === 服务管理模块 ===

def gateway_management():
    """Gateway 管理"""
    while True:
        clear_screen()
        print_header("Gateway 管理", show_ascii=True)
        
        status = get_gateway_status()
        status_color = Colors.GREEN if status == "运行中" else Colors.RED
        print(f"\n      当前状态: [{status_color}{status}{Colors.RESET}]")
        
        print_separator()
        print_single_column("操作选项", [
            "启动 Gateway",
            "停止 Gateway",
            "重启 Gateway",
            "查看状态",
            "配置消息平台",
            "安装为系统服务",
            "卸载系统服务"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-7]", (0, 7))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes gateway start")
            prompt_continue()
        elif choice == '2':
            run_interactive("hermes gateway stop")
            prompt_continue()
        elif choice == '3':
            run_interactive("hermes gateway restart")
            prompt_continue()
        elif choice == '4':
            run_interactive("hermes gateway status")
            prompt_continue()
        elif choice == '5':
            run_interactive("hermes gateway setup")
            prompt_continue()
        elif choice == '6':
            run_interactive("hermes gateway install")
            prompt_continue()
        elif choice == '7':
            run_interactive("hermes gateway uninstall")
            prompt_continue()

def dashboard_management():
    """Dashboard 管理"""
    while True:
        clear_screen()
        print_header("Dashboard 管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "启动 Dashboard",
            "查看状态"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-2]", (0, 2))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes dashboard")
            prompt_continue()
        elif choice == '2':
            run_interactive("hermes status")
            prompt_continue()

def proxy_management():
    """Proxy 管理"""
    while True:
        clear_screen()
        print_header("Proxy 管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "启动代理",
            "查看状态",
            "列出提供商"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-3]", (0, 3))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes proxy start")
            prompt_continue()
        elif choice == '2':
            run_interactive("hermes proxy status")
            prompt_continue()
        elif choice == '3':
            run_interactive("hermes proxy providers")
            prompt_continue()

# === 配置管理模块 ===

def setup_wizard():
    """设置向导"""
    if not check_hermes_installed():
        return
    run_interactive("hermes setup")
    prompt_continue()

def model_management():
    """模型管理"""
    if not check_hermes_installed():
        return
    run_interactive("hermes model")
    prompt_continue()

def tools_config():
    """工具配置"""
    if not check_hermes_installed():
        return
    run_interactive("hermes tools")
    prompt_continue()

def auth_management():
    """认证管理"""
    while True:
        clear_screen()
        print_header("认证管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "交互式管理",
            "列出凭证",
            "添加凭证",
            "移除凭证",
            "重置凭证",
            "查看状态"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-6]", (0, 6))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes auth")
        elif choice == '2':
            run_interactive("hermes auth list")
        elif choice == '3':
            provider = input("      输入提供商名称: ").strip()
            if provider:
                run_interactive(f"hermes auth add {provider}")
        elif choice == '4':
            provider = input("      输入提供商名称: ").strip()
            if provider:
                run_interactive(f"hermes auth remove {provider}")
        elif choice == '5':
            provider = input("      输入提供商名称: ").strip()
            if provider:
                run_interactive(f"hermes auth reset {provider}")
        elif choice == '6':
            provider = input("      输入提供商名称: ").strip()
            if provider:
                run_interactive(f"hermes auth status {provider}")
        prompt_continue()

def secrets_management():
    """Secrets 管理"""
    while True:
        clear_screen()
        print_header("Secrets 管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "Bitwarden 设置",
            "查看状态",
            "同步密钥",
            "禁用"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-4]", (0, 4))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes secrets bitwarden setup")
        elif choice == '2':
            run_interactive("hermes secrets bitwarden status")
        elif choice == '3':
            run_interactive("hermes secrets bitwarden sync")
        elif choice == '4':
            run_interactive("hermes secrets bitwarden disable")
        prompt_continue()

# === 功能模块 ===

def skills_management():
    """技能管理"""
    while True:
        clear_screen()
        print_header("技能管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "浏览技能",
            "搜索技能",
            "安装技能",
            "列出已安装",
            "检查更新",
            "更新技能",
            "卸载技能",
            "配置技能"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-8]", (0, 8))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes skills browse")
        elif choice == '2':
            keyword = input("      输入搜索关键词: ").strip()
            if keyword:
                run_interactive(f"hermes skills search {keyword}")
        elif choice == '3':
            skill = input("      输入技能名称: ").strip()
            if skill:
                run_interactive(f"hermes skills install {skill}")
        elif choice == '4':
            run_interactive("hermes skills list")
        elif choice == '5':
            run_interactive("hermes skills check")
        elif choice == '6':
            run_interactive("hermes skills update")
        elif choice == '7':
            skill = input("      输入技能名称: ").strip()
            if skill:
                run_interactive(f"hermes skills uninstall {skill}")
        elif choice == '8':
            run_interactive("hermes skills config")
        prompt_continue()

def bundles_management():
    """技能包管理"""
    while True:
        clear_screen()
        print_header("技能包管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "列出技能包",
            "创建技能包",
            "查看技能包",
            "删除技能包"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-4]", (0, 4))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes bundles list")
        elif choice == '2':
            name = input("      输入技能包名称: ").strip()
            if name:
                run_interactive(f"hermes bundles create {name}")
        elif choice == '3':
            name = input("      输入技能包名称: ").strip()
            if name:
                run_interactive(f"hermes bundles show {name}")
        elif choice == '4':
            name = input("      输入技能包名称: ").strip()
            if name:
                run_interactive(f"hermes bundles delete {name}")
        prompt_continue()

def memory_management():
    """记忆管理"""
    while True:
        clear_screen()
        print_header("记忆管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "设置记忆提供商",
            "查看状态"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-2]", (0, 2))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes memory setup")
        elif choice == '2':
            run_interactive("hermes memory status")
        prompt_continue()

def mcp_management():
    """MCP 管理"""
    while True:
        clear_screen()
        print_header("MCP 服务器管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "添加 MCP 服务器",
            "列出服务器",
            "移除服务器",
            "运行 Hermes 作为 MCP 服务器"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-4]", (0, 4))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes mcp add")
        elif choice == '2':
            run_interactive("hermes mcp list")
        elif choice == '3':
            server = input("      输入服务器名称: ").strip()
            if server:
                run_interactive(f"hermes mcp remove {server}")
        elif choice == '4':
            run_interactive("hermes mcp serve")
        prompt_continue()

def plugins_management():
    """插件管理"""
    while True:
        clear_screen()
        print_header("插件管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "安装插件",
            "列出插件",
            "启用插件",
            "禁用插件",
            "移除插件"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-5]", (0, 5))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            plugin = input("      输入插件名称: ").strip()
            if plugin:
                run_interactive(f"hermes plugins install {plugin}")
        elif choice == '2':
            run_interactive("hermes plugins list")
        elif choice == '3':
            plugin = input("      输入插件名称: ").strip()
            if plugin:
                run_interactive(f"hermes plugins enable {plugin}")
        elif choice == '4':
            plugin = input("      输入插件名称: ").strip()
            if plugin:
                run_interactive(f"hermes plugins disable {plugin}")
        elif choice == '5':
            plugin = input("      输入插件名称: ").strip()
            if plugin:
                run_interactive(f"hermes plugins remove {plugin}")
        prompt_continue()

def lsp_management():
    """LSP 管理"""
    while True:
        clear_screen()
        print_header("LSP 管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "查看状态",
            "列出服务器",
            "安装服务器",
            "安装全部",
            "重启"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-5]", (0, 5))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes lsp status")
        elif choice == '2':
            run_interactive("hermes lsp list")
        elif choice == '3':
            server = input("      输入服务器 ID: ").strip()
            if server:
                run_interactive(f"hermes lsp install {server}")
        elif choice == '4':
            run_interactive("hermes lsp install-all")
        elif choice == '5':
            run_interactive("hermes lsp restart")
        prompt_continue()

# === 自动化与任务模块 ===

def cron_management():
    """定时任务管理"""
    while True:
        clear_screen()
        print_header("定时任务管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "列出任务",
            "创建任务",
            "编辑任务",
            "暂停任务",
            "恢复任务",
            "立即运行",
            "删除任务",
            "查看状态"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-8]", (0, 8))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes cron list")
        elif choice == '2':
            run_interactive("hermes cron create")
        elif choice == '3':
            run_interactive("hermes cron edit")
        elif choice == '4':
            job_id = input("      输入任务 ID: ").strip()
            if job_id:
                run_interactive(f"hermes cron pause {job_id}")
        elif choice == '5':
            job_id = input("      输入任务 ID: ").strip()
            if job_id:
                run_interactive(f"hermes cron resume {job_id}")
        elif choice == '6':
            job_id = input("      输入任务 ID: ").strip()
            if job_id:
                run_interactive(f"hermes cron run {job_id}")
        elif choice == '7':
            job_id = input("      输入任务 ID: ").strip()
            if job_id:
                run_interactive(f"hermes cron remove {job_id}")
        elif choice == '8':
            run_interactive("hermes cron status")
        prompt_continue()

def kanban_management():
    """Kanban 任务管理"""
    while True:
        clear_screen()
        print_header("Kanban 任务管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "列出任务",
            "创建任务",
            "查看任务",
            "完成任务",
            "阻塞任务",
            "取消阻塞",
            "归档任务",
            "创建 Swarm 图",
            "调度器状态",
            "看板管理"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-10]", (0, 10))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes kanban list")
        elif choice == '2':
            title = input("      输入任务标题: ").strip()
            if title:
                run_interactive(f'hermes kanban create "{title}"')
        elif choice == '3':
            task_id = input("      输入任务 ID: ").strip()
            if task_id:
                run_interactive(f"hermes kanban show {task_id}")
        elif choice == '4':
            task_id = input("      输入任务 ID: ").strip()
            if task_id:
                run_interactive(f"hermes kanban complete {task_id}")
        elif choice == '5':
            task_id = input("      输入任务 ID: ").strip()
            if task_id:
                reason = input("      输入阻塞原因: ").strip()
                run_interactive(f'hermes kanban block {task_id} "{reason}"')
        elif choice == '6':
            task_id = input("      输入任务 ID: ").strip()
            if task_id:
                run_interactive(f"hermes kanban unblock {task_id}")
        elif choice == '7':
            task_id = input("      输入任务 ID: ").strip()
            if task_id:
                run_interactive(f"hermes kanban archive {task_id}")
        elif choice == '8':
            run_interactive("hermes kanban swarm")
        elif choice == '9':
            run_interactive("hermes kanban dispatch --dry-run")
        elif choice == '10':
            run_interactive("hermes kanban boards list")
        prompt_continue()

def webhook_management():
    """Webhook 管理"""
    while True:
        clear_screen()
        print_header("Webhook 管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "订阅 Webhook",
            "列出订阅",
            "移除订阅",
            "测试订阅"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-4]", (0, 4))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            name = input("      输入订阅名称: ").strip()
            if name:
                run_interactive(f"hermes webhook subscribe {name}")
        elif choice == '2':
            run_interactive("hermes webhook list")
        elif choice == '3':
            name = input("      输入订阅名称: ").strip()
            if name:
                run_interactive(f"hermes webhook remove {name}")
        elif choice == '4':
            name = input("      输入订阅名称: ").strip()
            if name:
                run_interactive(f"hermes webhook test {name}")
        prompt_continue()

def ntfy_management():
    """ntfy 推送通知"""
    while True:
        clear_screen()
        print_header("ntfy 推送通知", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "配置 ntfy",
            "测试推送",
            "查看状态"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-3]", (0, 3))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes setup gateway")
        elif choice == '2':
            message = input("      输入测试消息: ").strip()
            if message:
                run_interactive(f'hermes send --to ntfy "{message}"')
        elif choice == '3':
            run_interactive("hermes status")
        prompt_continue()

# === 会话与数据模块 ===

def terminal_chat():
    """终端对话"""
    if not check_hermes_installed():
        return
    print_info("进入终端对话，输入 /exit 退出")
    run_interactive("hermes")

def sessions_management():
    """会话管理"""
    while True:
        clear_screen()
        print_header("会话管理", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "列出会话",
            "导出会话",
            "清理会话",
            "重命名会话",
            "删除会话"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-5]", (0, 5))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes sessions list")
        elif choice == '2':
            run_interactive("hermes sessions export")
        elif choice == '3':
            run_interactive("hermes sessions prune")
        elif choice == '4':
            session_id = input("      输入会话 ID: ").strip()
            if session_id:
                new_name = input("      输入新名称: ").strip()
                if new_name:
                    run_interactive(f'hermes sessions rename {session_id} "{new_name}"')
        elif choice == '5':
            session_id = input("      输入会话 ID: ").strip()
            if session_id:
                run_interactive(f"hermes sessions delete {session_id}")
        prompt_continue()

def backup_hermes():
    """备份 Hermes"""
    print_header("备份 Hermes", show_ascii=False)
    print_separator()
    print_info("正在备份...")
    
    result = run_interactive("hermes backup")
    
    if result == 0:
        print_success("备份完成！")
    else:
        print_error("备份失败")
    prompt_continue()

def import_hermes():
    """恢复 Hermes"""
    print_header("恢复 Hermes", show_ascii=False)
    print_separator()
    
    zip_file = input("      输入备份文件路径: ").strip()
    if zip_file:
        print_warning("恢复将覆盖现有配置，确定继续吗？")
        choice = input("      输入 y 确认: ").strip().lower()
        if choice == 'y':
            result = run_interactive(f"hermes import {zip_file}")
            if result == 0:
                print_success("恢复完成！")
            else:
                print_error("恢复失败")
    prompt_continue()

# === 诊断模块 ===

def health_check():
    """健康检查"""
    if not check_hermes_installed():
        return
    print_header("健康检查", show_ascii=False)
    print_separator()
    
    result = run_interactive("hermes doctor")
    
    if result == 0:
        print_success("健康检查通过！")
    else:
        print_warning("发现问题，请查看上方输出")
    prompt_continue()

def show_status():
    """查看状态"""
    if not check_hermes_installed():
        return
    print_header("系统状态", show_ascii=False)
    print_separator()
    
    run_interactive("hermes status --all")
    prompt_continue()

def view_logs():
    """查看日志"""
    while True:
        clear_screen()
        print_header("查看日志", show_ascii=True)
        print_separator()
        
        print_single_column("操作选项", [
            "Agent 日志",
            "Gateway 日志",
            "错误日志",
            "列出所有日志",
            "实时跟踪"
        ])
        print_separator()
        print("       0. 返回主菜单")
        print_separator()
        
        choice = get_input("请选择 [0-5]", (0, 5))
        
        if choice == 'back':
            break
        elif choice == 'quit':
            sys.exit(0)
        elif choice == '1':
            run_interactive("hermes logs agent")
        elif choice == '2':
            run_interactive("hermes logs gateway")
        elif choice == '3':
            run_interactive("hermes logs errors")
        elif choice == '4':
            run_interactive("hermes logs list")
        elif choice == '5':
            log_type = input("      输入日志类型 (agent/gateway/errors): ").strip()
            if log_type:
                run_interactive(f"hermes logs {log_type} -f")
        prompt_continue()

def dump_config():
    """转储配置"""
    if not check_hermes_installed():
        return
    print_header("配置转储", show_ascii=False)
    print_separator()
    
    run_interactive("hermes dump")
    prompt_continue()

def security_audit():
    """安全审计"""
    if not check_hermes_installed():
        return
    print_header("安全审计", show_ascii=False)
    print_separator()
    
    run_interactive("hermes security audit")
    prompt_continue()

# === 主菜单 ===

def show_main_menu():
    """显示主菜单"""
    clear_screen()
    print_header("Hermes Agent 管理工具")
    print_status()
    print_separator()
    
    # 版块1: 安装与更新 / 服务管理
    print_two_columns(
        "安装与更新", ["安装 Hermes", "更新 Hermes", "卸载 Hermes"],
        "服务管理", ["Gateway 管理", "Dashboard 管理", "Proxy 管理"],
        1, 4,
        "📦", "🔧"
    )
    
    # 版块2: 配置管理 / 功能模块
    print_two_columns(
        "配置管理", ["运行设置向导", "模型管理", "工具配置", "认证管理", "Secrets 管理"],
        "功能模块", ["技能管理", "技能包管理", "记忆管理", "MCP 服务器管理", "插件管理", "LSP 管理"],
        7, 12,
        "⚙️ ", "🎯"
    )
    
    # 版块3: 自动化与任务 / 会话与数据
    print_two_columns(
        "自动化与任务", ["定时任务管理", "Kanban 任务管理", "Webhook 管理", "ntfy 推送通知"],
        "会话与数据", ["终端对话 UI", "会话管理", "备份 Hermes", "恢复 Hermes"],
        18, 22,
        "🤖", "📱"
    )
    
    # 版块4: 诊断与调试
    print_two_columns(
        "诊断与调试", ["健康检查", "查看状态", "查看日志", "转储配置", "安全审计"],
        "系统工具", ["脚本更新"],
        26, 31,
        "🔍", "🔄"
    )
    
    print_help()

def main():
    """主函数"""
    refresh_path()
    
    while True:
        show_main_menu()
        choice = get_input("请选择 [0-31]", (0, 31))
        
        if choice == 'quit':
            print_info("感谢使用，再见！")
            sys.exit(0)
        elif choice == 'clear':
            continue
        
        # 安装与更新
        elif choice == '1':
            install_hermes()
        elif choice == '2':
            update_hermes()
        elif choice == '3':
            uninstall_hermes()
        
        # 服务管理
        elif choice == '4':
            gateway_management()
        elif choice == '5':
            dashboard_management()
        elif choice == '6':
            proxy_management()
        
        # 配置管理
        elif choice == '7':
            setup_wizard()
        elif choice == '8':
            model_management()
        elif choice == '9':
            tools_config()
        elif choice == '10':
            auth_management()
        elif choice == '11':
            secrets_management()
        
        # 功能模块
        elif choice == '12':
            skills_management()
        elif choice == '13':
            bundles_management()
        elif choice == '14':
            memory_management()
        elif choice == '15':
            mcp_management()
        elif choice == '16':
            plugins_management()
        elif choice == '17':
            lsp_management()
        
        # 自动化与任务
        elif choice == '18':
            cron_management()
        elif choice == '19':
            kanban_management()
        elif choice == '20':
            webhook_management()
        elif choice == '21':
            ntfy_management()
        
        # 会话与数据
        elif choice == '22':
            terminal_chat()
        elif choice == '23':
            sessions_management()
        elif choice == '24':
            backup_hermes()
        elif choice == '25':
            import_hermes()
        
        # 诊断与调试
        elif choice == '26':
            health_check()
        elif choice == '27':
            show_status()
        elif choice == '28':
            view_logs()
        elif choice == '29':
            dump_config()
        elif choice == '30':
            security_audit()
        
        # 系统工具
        elif choice == '31':
            self_update()

if __name__ == "__main__":
    main()
