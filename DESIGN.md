# Hermes CLI 管理工具 - 设计文档

## 1. 项目概述

**名称**: hermes_cli.py
**语言**: Python 3.9+
**依赖**: 仅使用 Python 标准库
**用途**: Hermes Agent 一站式安装与管理工具
**版本**: v1.0
**更新日期**: 2026-05-29
**启动命令**: `hc`

### 1.1 启动配置

**命令**: `hc`（Hermes CLI 缩写）

**安装方式**: 符号链接
```bash
# 脚本安装时自动创建
sudo ln -sf /path/to/hermes_cli.py /usr/local/bin/hc
sudo chmod +x /usr/local/bin/hc
```

**兼容性**:
| 系统 | 支持 |
|------|------|
| Ubuntu/Debian | ✅ |
| CentOS/RHEL | ✅ |
| AlmaLinux/Rocky | ✅ |
| Fedora | ✅ |
| macOS | ✅ |
| Alpine Linux | ✅ |
| Arch Linux | ✅ |
| FreeBSD | ✅ |
| Windows (WSL) | ✅ |

**使用方式**:
```bash
# 直接输入即可启动
hc
```

## 2. 功能清单

### 2.1 安装与更新
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 安装 Hermes | 官方脚本安装 | `curl ... \| bash` |
| 更新 Hermes | 检查并更新 | `hermes update` |
| 卸载 Hermes | 完全卸载 | `hermes uninstall` |

### 2.2 服务管理
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| Gateway 管理 | 消息网关管理 | `hermes gateway` |
| Dashboard 管理 | Web 仪表板 | `hermes dashboard` |
| Proxy 管理 | 订阅代理 | `hermes proxy` |

### 2.3 配置管理
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 设置向导 | 完整配置向导 | `hermes setup` |
| 模型管理 | 选择/切换模型 | `hermes model` |
| 工具配置 | 启用/禁用工具 | `hermes tools` |
| 认证管理 | API Key 管理 | `hermes auth` |
| Secrets 管理 | Bitwarden 集成 | `hermes secrets` |
| 配置查看 | 显示当前配置 | `hermes config show` |

### 2.4 功能模块
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 技能管理 | 浏览/安装/发布技能 | `hermes skills` |
| 技能包管理 | 技能包组管理 | `hermes bundles` |
| 记忆管理 | 配置记忆系统 | `hermes memory` |
| MCP 管理 | MCP 服务器配置 | `hermes mcp` |
| 插件管理 | 安装/启用插件 | `hermes plugins` |
| LSP 管理 | 语言服务器协议 | `hermes lsp` |

### 2.5 自动化与任务
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 定时任务 | 管理定时任务 | `hermes cron` |
| Kanban 任务 | 多代理任务管理 | `hermes kanban` |
| Webhook 管理 | 事件驱动激活 | `hermes webhook` |
| ntfy 推送 | 推送通知 | `hermes send` |

### 2.6 会话与数据
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 终端对话 | 启动交互式对话 | `hermes` |
| 会话管理 | 浏览/导出会话 | `hermes sessions` |
| 备份 | 备份配置和数据 | `hermes backup` |
| 恢复 | 从备份恢复 | `hermes import` |

### 2.7 诊断与调试
| 功能 | 说明 | 对应命令 |
|------|------|----------|
| 健康检查 | 诊断配置问题 | `hermes doctor` |
| 状态查看 | 显示系统状态 | `hermes status` |
| 日志查看 | 查看运行日志 | `hermes logs` |
| 配置转储 | 导出配置信息 | `hermes dump` |
| 安全审计 | 依赖安全检查 | `hermes security audit` |

## 3. 菜单结构

### 3.1 主菜单
```
┌─────────────────────────────────────────────────────────┐
│              Hermes Agent 管理工具 v1.0                  │
├─────────────────────────────────────────────────────────┤
│  运行状态 : ● 运行中    当前版本 : v0.15.2               │
├─────────────────────────────────────────────────────────┤
│  【安装与更新】                                          │
│  1.  安装 Hermes Agent                                  │
│  2.  更新 Hermes                                        │
│  3.  卸载 Hermes                                        │
├─────────────────────────────────────────────────────────┤
│  【服务管理】                                            │
│  4.  Gateway 管理                                       │
│  5.  Dashboard 管理 (Web 仪表板)                        │
│  6.  Proxy 管理 (订阅代理)                              │
├─────────────────────────────────────────────────────────┤
│  【配置管理】                                            │
│  7.  运行设置向导 (hermes setup)                        │
│  8.  模型管理 (hermes model)                            │
│  9.  工具配置 (hermes tools)                            │
│  10. 认证管理 (hermes auth)                             │
│  11. Secrets 管理 (Bitwarden)                           │
├─────────────────────────────────────────────────────────┤
│  【功能模块】                                            │
│  12. 技能管理 (hermes skills)                           │
│  13. 技能包管理 (hermes bundles)                        │
│  14. 记忆管理 (hermes memory)                           │
│  15. MCP 服务器管理 (hermes mcp)                        │
│  16. 插件管理 (hermes plugins)                          │
│  17. LSP 管理 (语言服务器协议)                          │
├─────────────────────────────────────────────────────────┤
│  【自动化与任务】                                        │
│  18. 定时任务管理 (hermes cron)                         │
│  19. Kanban 任务管理 (hermes kanban)                    │
│  20. Webhook 管理 (hermes webhook)                      │
│  21. ntfy 推送通知                                      │
├─────────────────────────────────────────────────────────┤
│  【会话与数据】                                          │
│  22. 终端对话 UI (hermes)                               │
│  23. 会话管理 (hermes sessions)                         │
│  24. 备份 Hermes                                        │
│  25. 恢复 Hermes                                        │
├─────────────────────────────────────────────────────────┤
│  【诊断与调试】                                          │
│  26. 健康检查 (hermes doctor)                           │
│  27. 查看状态 (hermes status)                           │
│  28. 查看日志 (hermes logs)                             │
│  29. 转储配置 (hermes dump)                             │
│  30. 安全审计 (hermes security audit)                   │
├─────────────────────────────────────────────────────────┤
│  0. 退出                                                │
└─────────────────────────────────────────────────────────┘
```

### 3.2 二级菜单

#### Gateway 管理
```
1. 启动 Gateway
2. 停止 Gateway
3. 重启 Gateway
4. 查看状态
5. 配置消息平台 (setup)
6. 安装为系统服务
7. 卸载系统服务
0. 返回
```

#### Dashboard 管理
```
1. 启动 Dashboard
2. 查看状态
0. 返回
```

#### Proxy 管理
```
1. 启动代理 (start)
2. 查看状态 (status)
3. 列出提供商 (providers)
0. 返回
```

#### 模型管理
```
1. 交互式选择模型
2. 添加新提供商
3. 查看当前模型
0. 返回
```

#### 工具配置
```
1. 交互式配置工具
2. 查看已启用工具
0. 返回
```

#### 认证管理
```
1. 交互式管理
2. 列出凭证 (list)
3. 添加凭证 (add)
4. 移除凭证 (remove)
5. 重置凭证 (reset)
6. 查看状态 (status)
0. 返回
```

#### Secrets 管理
```
1. Bitwarden 设置 (setup)
2. 查看状态 (status)
3. 同步密钥 (sync)
4. 禁用 (disable)
0. 返回
```

#### 技能管理
```
1. 浏览技能 (browse)
2. 搜索技能 (search)
3. 安装技能 (install)
4. 列出已安装 (list)
5. 检查更新 (check)
6. 更新技能 (update)
7. 卸载技能 (uninstall)
8. 配置技能 (config)
0. 返回
```

#### 技能包管理
```
1. 列出技能包 (list)
2. 创建技能包 (create)
3. 查看技能包 (show)
4. 删除技能包 (delete)
0. 返回
```

#### 记忆管理
```
1. 设置记忆提供商 (setup)
2. 查看状态 (status)
0. 返回
```

#### MCP 管理
```
1. 添加 MCP 服务器
2. 列出服务器
3. 移除服务器
4. 运行 Hermes 作为 MCP 服务器
0. 返回
```

#### 插件管理
```
1. 安装插件
2. 列出插件
3. 启用插件
4. 禁用插件
5. 移除插件
0. 返回
```

#### LSP 管理
```
1. 查看状态 (status)
2. 列出服务器 (list)
3. 安装服务器 (install)
4. 安装全部 (install-all)
5. 重启 (restart)
0. 返回
```

#### 定时任务管理
```
1. 列出任务 (list)
2. 创建任务 (create)
3. 编辑任务 (edit)
4. 暂停任务 (pause)
5. 恢复任务 (resume)
6. 立即运行 (run)
7. 删除任务 (remove)
8. 查看状态 (status)
0. 返回
```

#### Kanban 任务管理
```
1. 列出任务 (list)
2. 创建任务 (create)
3. 查看任务 (show)
4. 完成任务 (complete)
5. 阻塞任务 (block)
6. 取消阻塞 (unblock)
7. 归档任务 (archive)
8. 创建 Swarm 图 (swarm)
9. 调度器状态 (dispatch)
10. 看板管理 (boards)
0. 返回
```

#### Webhook 管理
```
1. 订阅 Webhook (subscribe)
2. 列出订阅 (list)
3. 移除订阅 (remove)
4. 测试订阅 (test)
0. 返回
```

#### ntfy 推送通知
```
1. 配置 ntfy
2. 测试推送
3. 查看状态
0. 返回
```

#### 会话管理
```
1. 列出会话 (list)
2. 导出会话 (export)
3. 清理会话 (prune)
4. 重命名会话 (rename)
5. 删除会话 (delete)
0. 返回
```

#### 日志查看
```
1. Agent 日志
2. Gateway 日志
3. 错误日志
4. 列出所有日志
5. 实时跟踪 (follow)
0. 返回
```

#### 诊断与调试
```
1. 健康检查 (doctor)
2. 查看状态 (status)
3. 转储配置 (dump)
4. 安全审计 (security audit)
5. 查看日志
0. 返回
```

## 4. 技术架构

### 4.1 目录结构
```
my-hermes-cli/
├── DESIGN.md              # 本文档
├── hermes_cli.py          # 主脚本
├── hermes_manager.sh      # 旧版参考
└── kejilion.sh            # 旧版参考
```

### 4.2 代码结构
```python
#!/usr/bin/env python3
"""Hermes Agent 管理工具"""

# === 导入区 ===
import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from typing import Optional, Tuple, List

# === 常量区 ===
HERMES_HOME = Path.home() / ".hermes"
CONFIG_FILE = HERMES_HOME / "config.yaml"
INSTALL_SCRIPT = "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh"
VERSION = "1.0"

# === 颜色定义 ===
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'  # No Color

# === 基础工具函数 ===
def run_cmd(cmd: str, check: bool = True) -> Tuple[int, str, str]:
    """执行 shell 命令"""
    pass

def run_interactive(cmd: str) -> int:
    """执行交互式命令"""
    pass

def check_installed() -> bool:
    """检查 Hermes 是否已安装"""
    pass

def get_version() -> str:
    """获取当前版本"""
    pass

def get_latest_version() -> str:
    """获取最新版本"""
    pass

def get_gateway_status() -> str:
    """获取 Gateway 状态"""
    pass

def detect_os() -> str:
    """检测操作系统"""
    pass

def check_disk_space(path: str = "/", required_gb: int = 2) -> bool:
    """检查磁盘空间"""
    pass

def detect_cn() -> bool:
    """检测是否国内环境"""
    pass

def refresh_path():
    """刷新 PATH 环境变量"""
    pass

# === 安装模块 ===
def install_dependencies():
    """安装系统依赖"""
    pass

def install_hermes():
    """安装 Hermes"""
    pass

def setup_gateway():
    """配置 Gateway 服务"""
    pass

def uninstall_hermes():
    """卸载 Hermes"""
    pass

# === 服务管理模块 ===
def gateway_management():
    """Gateway 管理"""
    pass

def dashboard_management():
    """Dashboard 管理"""
    pass

def proxy_management():
    """Proxy 管理"""
    pass

# === 配置管理模块 ===
def setup_wizard():
    """设置向导"""
    pass

def model_management():
    """模型管理"""
    pass

def tools_config():
    """工具配置"""
    pass

def auth_management():
    """认证管理"""
    pass

def secrets_management():
    """Secrets 管理"""
    pass

# === 功能模块 ===
def skills_management():
    """技能管理"""
    pass

def bundles_management():
    """技能包管理"""
    pass

def memory_management():
    """记忆管理"""
    pass

def mcp_management():
    """MCP 管理"""
    pass

def plugins_management():
    """插件管理"""
    pass

def lsp_management():
    """LSP 管理"""
    pass

# === 自动化与任务模块 ===
def cron_management():
    """定时任务管理"""
    pass

def kanban_management():
    """Kanban 任务管理"""
    pass

def webhook_management():
    """Webhook 管理"""
    pass

def ntfy_management():
    """ntfy 推送通知"""
    pass

# === 会话与数据模块 ===
def terminal_chat():
    """终端对话"""
    pass

def sessions_management():
    """会话管理"""
    pass

def backup_hermes():
    """备份 Hermes"""
    pass

def import_hermes():
    """恢复 Hermes"""
    pass

# === 诊断模块 ===
def health_check():
    """健康检查"""
    pass

def show_status():
    """显示状态"""
    pass

def view_logs():
    """查看日志"""
    pass

def dump_config():
    """转储配置"""
    pass

def security_audit():
    """安全审计"""
    pass

# === UI 模块 ===
def show_header():
    """显示头部信息"""
    pass

def show_main_menu():
    """显示主菜单"""
    pass

def show_submenu(title: str, options: List[Tuple[str, str]]):
    """显示子菜单"""
    pass

def handle_choice(choice: str):
    """处理用户选择"""
    pass

def prompt_continue():
    """提示按任意键继续"""
    pass

def clear_screen():
    """清屏"""
    pass

# === 主入口 ===
def main():
    """主函数"""
    pass

if __name__ == "__main__":
    main()
```

## 5. 用户流程

### 5.1 首次安装流程
```
运行脚本
    ↓
检测环境 (OS/磁盘/网络)
    ↓
检测国内环境 → 配置镜像加速
    ↓
选择 "1. 安装 Hermes"
    ↓
安装系统依赖 (Python3, curl, jq, git)
    ↓
执行官方安装脚本
    ↓
配置 PATH 环境变量
    ↓
运行 hermes setup 向导
    ↓
安装完成
```

### 5.2 日常使用流程
```
运行脚本
    ↓
显示状态 (版本/运行状态)
    ↓
显示菜单
    ↓
用户选择功能
    ↓
执行对应 hermes 命令
    ↓
返回菜单
```

## 6. 交互设计

### 6.1 快捷操作

| 操作 | 方式 | 示例 |
|------|------|------|
| 选择功能 | 输入数字 | `1`、`2`、`3` |
| 返回上级 | 输入 `0` 或 `b` 或 `back` | |
| 退出脚本 | 输入 `q` 或 `quit` 或 `exit` | |
| 中断操作 | 按 `Ctrl+C` | |
| 清屏 | 输入 `c` 或 `clear` | |
| 搜索功能 | 输入 `/` + 关键词 | `/model`、`/skill` |

### 6.2 回退/取消机制

| 场景 | 操作 |
|------|------|
| 输入错误 | 按 `Enter` 重新输入 |
| 不想选择 | 输入 `0` 返回上一级 |
| 中断操作 | 按 `Ctrl+C` 返回主菜单 |
| 取消输入 | 按 `Esc` 或空输入按回车 |

### 6.3 输入提示格式

**主菜单提示**:
```
┌─────────────────────────────────────────────────────────┐
│  输入数字选择功能，0=返回，q=退出，/=搜索                │
└─────────────────────────────────────────────────────────┘
请选择 [0-30]:
```

**子菜单提示**:
```
请选择 [0-3]:
```

### 6.4 错误处理

```
请选择 [0-30]: abc
❌ 无效输入，请输入数字 (0-30)

请选择 [0-30]: 99
❌ 选项不存在，请输入 0-30 之间的数字

请选择 [0-30]:
（空输入，重新显示菜单）
```

### 6.5 输入函数设计

```python
def get_input(prompt: str, valid_range: tuple = None, allow_commands: bool = True) -> str:
    """
    获取用户输入，支持快捷命令和回退
    
    Args:
        prompt: 输入提示
        valid_range: 有效数字范围 (min, max)
        allow_commands: 是否允许快捷命令
    
    Returns:
        str: 用户输入
        'back': 用户请求返回
        'quit': 用户请求退出
        'search:xxx': 搜索命令
    """
    while True:
        try:
            user_input = input(prompt).strip().lower()
            
            # 空输入
            if not user_input:
                continue
            
            # 快捷命令
            if allow_commands:
                if user_input in ('0', 'b', 'back'):
                    return 'back'
                if user_input in ('q', 'quit', 'exit'):
                    return 'quit'
                if user_input in ('c', 'clear'):
                    clear_screen()
                    continue
            
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
                        print(f"❌ 选项不存在，请输入 {valid_range[0]}-{valid_range[1]} 之间的数字")
                        continue
                except ValueError:
                    print("❌ 无效输入，请输入数字")
                    continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n")
            return 'back'
        except EOFError:
            return 'quit'
```

### 6.6 交互流程示例

```
╔═══════════════════════════════════════════════════════════╗
║              Hermes Agent 管理工具 v1.0                   ║
╠═══════════════════════════════════════════════════════════╣
║  运行状态 : ● 运行中    当前版本 : v0.15.2                ║
╠═══════════════════════════════════════════════════════════╣
║  【安装与更新】                                            ║
║  1.  安装 Hermes Agent                                    ║
║  2.  更新 Hermes                                          ║
║  3.  卸载 Hermes                                          ║
╠═══════════════════════════════════════════════════════════╣
║  ...                                                      ║
╠═══════════════════════════════════════════════════════════╣
║  0. 退出                                                  ║
╚═══════════════════════════════════════════════════════════╝
┌───────────────────────────────────────────────────────────┐
│  输入数字选择功能，0=返回，q=退出，/=搜索                  │
└───────────────────────────────────────────────────────────┘
请选择 [0-30]: 8

┌───────────────────────────────────────────────────────────┐
│                      模型管理                              │
├───────────────────────────────────────────────────────────┤
│  1. 交互式选择模型                                        │
│  2. 添加新提供商                                          │
│  3. 查看当前模型                                          │
├───────────────────────────────────────────────────────────┤
│  0. 返回                                                  │
└───────────────────────────────────────────────────────────┘
请选择 [0-3]: 0

（返回主菜单）

请选择 [0-30]: /skill
（搜索包含 skill 的功能）

请选择 [0-30]: q
（退出脚本）
```

## 7. 技术细节

### 6.1 命令执行方式
```python
# 交互式命令（继承终端）
def run_interactive(cmd: str) -> int:
    """用于需要用户输入的命令，如 hermes model, hermes setup"""
    return subprocess.run(cmd, shell=True).returncode

# 非交互式命令（捕获输出）
def run_capture(cmd: str) -> Tuple[int, str, str]:
    """用于获取命令输出，如 hermes status, hermes doctor"""
    result = subprocess.run(
        cmd, shell=True,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr

# 后台命令
def run_background(cmd: str) -> subprocess.Popen:
    """用于后台运行的命令，如 hermes gateway start"""
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

### 6.2 国内镜像配置
```python
PYPI_MIRRORS = {
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "huawei": "https://repo.huaweicloud.com/repository/pypi/simple/",
}

GH_PROXY = "https://ghproxy.com/"
```

### 6.3 版本检测
```python
def get_version() -> str:
    """优先从 dist-info 读取，避免启动 hermes CLI"""
    # 1. 尝试从 METADATA 文件读取
    hermes_home = Path.home() / ".hermes"
    venv_dir = hermes_home / "hermes-agent" / "venv"
    
    if venv_dir.exists():
        for metadata in venv_dir.glob("lib/python*/site-packages/hermes_agent-*.dist-info/METADATA"):
            try:
                with open(metadata, 'r') as f:
                    for line in f:
                        if line.startswith("Version:"):
                            return "v" + line.split(":")[1].strip()
            except:
                pass
    
    # 2. 兜底执行 hermes --version
    try:
        result = subprocess.run(
            ["hermes", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return "未安装"
```

### 6.4 Gateway 状态检测
```python
def get_gateway_status() -> str:
    """获取 Gateway 运行状态"""
    # 1. 检查 systemd 服务
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "hermes-gateway.service"],
            capture_output=True, text=True
        )
        if result.stdout.strip() == "active":
            return "运行中"
    except:
        pass
    
    # 2. 检查进程
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
```

## 7. 输出格式

### 7.1 颜色方案

```python
class Colors:
    """终端颜色定义"""
    BLUE = '\033[38;5;39m'      # 亮蓝色 - ASCII 艺术字
    GREEN = '\033[38;5;82m'     # 绿色 - 运行中、成功
    RED = '\033[38;5;196m'      # 红色 - 已停止、错误
    YELLOW = '\033[38;5;214m'   # 黄色 - 警告
    CYAN = '\033[38;5;45m'      # 青色 - 信息
    WHITE = '\033[38;5;255m'    # 白色 - 标题
    GRAY = '\033[38;5;245m'     # 灰色 - 帮助文字
    RESET = '\033[0m'           # 重置颜色
```

### 7.2 ASCII 艺术字

```python
HERMESCLI_ASCII = """
\033[38;5;39m    ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗ ██████╗██╗     ██╗
    ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██║     ██║
    ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗██║     ██║     ██║
    ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║██║     ██║     ██║
    ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║╚██████╗███████╗██║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝\033[0m
"""
```

### 7.3 主菜单样式（无边框设计）

```
    ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗ ██████╗██╗     ██╗
    ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██║     ██║
    ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗██║     ██║     ██║
    ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║██║     ██║     ██║
    ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║╚██████╗███████╗██║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝

    Hermes Agent 管理工具 v1.0
    ─────────────────────────────────────────────────────────────────────────

      运行状态: [运行中]    当前版本: v0.15.2
      安装路径: ~/.hermes

    ─────────────────────────────────────────────────────────────────────────

      安装与更新                      服务管理
       1. 安装 Hermes                  4. Gateway 管理
       2. 更新 Hermes                  5. Dashboard 管理
       3. 卸载 Hermes                  6. Proxy 管理

      配置管理                        功能模块
       7. 运行设置向导                 12. 技能管理
       8. 模型管理                     13. 技能包管理
       9. 工具配置                     14. 记忆管理
      10. 认证管理                     15. MCP 服务器管理
      11. Secrets 管理                 16. 插件管理
                                      17. LSP 管理

      自动化与任务                    会话与数据
      18. 定时任务管理                 22. 终端对话 UI
      19. Kanban 任务管理              23. 会话管理
      20. Webhook 管理                 24. 备份 Hermes
      21. ntfy 推送通知                25. 恢复 Hermes

      诊断与调试
      26. 健康检查                     29. 转储配置
      27. 查看状态                     30. 安全审计
      28. 查看日志

    ─────────────────────────────────────────────────────────────────────────
      0=返回  q=退出  Ctrl+C=中断  /=搜索
    ─────────────────────────────────────────────────────────────────────────
      请选择 [0-30]:
```

### 7.4 子菜单样式（无边框设计）

```
    ██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗ ██████╗██╗     ██╗
    ██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██║     ██║
    ███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗██║     ██║     ██║
    ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║██║     ██║     ██║
    ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║╚██████╗███████╗██║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝

    Gateway 管理
    ─────────────────────────────────────────────────────────────────────────

      当前状态: [运行中]    PID: 12345

    ─────────────────────────────────────────────────────────────────────────

       1. 启动 Gateway
       2. 停止 Gateway
       3. 重启 Gateway
       4. 查看状态
       5. 配置消息平台
       6. 安装为系统服务
       7. 卸载系统服务

    ─────────────────────────────────────────────────────────────────────────
       0. 返回主菜单
    ─────────────────────────────────────────────────────────────────────────
      请选择 [0-7]:
```

### 7.5 状态显示

```
      运行状态: [运行中]    当前版本: v0.15.2
      安装路径: ~/.hermes
      配置文件: ~/.hermes/config.yaml
```

### 7.6 操作反馈

**成功**:
```
      ✅ Gateway 已成功启动
         PID: 12345
```

**错误**:
```
      ❌ Gateway 启动失败
         原因: 端口 8080 已被占用
```

**警告**:
```
      ⚠️  Hermes 未安装
         请先选择 "1. 安装 Hermes" 进行安装
```

## 8. 错误处理

### 8.1 常见错误场景
| 场景 | 处理方式 |
|------|----------|
| Hermes 未安装 | 提示先安装，引导到安装选项 |
| 命令执行失败 | 显示错误信息，提示可能原因 |
| 网络连接失败 | 提示检查网络，建议配置代理 |
| 磁盘空间不足 | 提示清理空间 |
| 权限不足 | 提示使用 sudo 或检查权限 |
| 命令不存在 | 提示更新 Hermes 版本 |

### 8.2 错误信息格式
```
❌ 错误: Hermes 未安装
   请先选择 "1. 安装 Hermes" 进行安装
```

```
⚠️ 警告: Gateway 未运行
   请先选择 "4. Gateway 管理" → "1. 启动 Gateway"
```

```
✅ 成功: Hermes 已更新到 v0.15.2
```

## 9. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-05-29 | 初始版本，包含 30 个功能模块 |

## 10. 参考资源

- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/)
- [CLI 命令参考](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
- [Skills Hub](https://agentskills.io)
