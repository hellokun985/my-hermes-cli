#!/bin/bash
# Hermes CLI 管理工具安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# GitHub 仓库信息
REPO="hellokun985/my-hermes-cli"
RAW_URL="https://raw.githubusercontent.com/${REPO}/main"
SCRIPT_NAME="hermes_cli.py"
INSTALL_PATH="/usr/local/bin/hc"

echo -e "${BLUE}"
echo "    ██╗  ██╗ ██████╗ "
echo "    ██║  ██║██╔════╝ "
echo "    ███████║██║      "
echo "    ██╔══██║██║      "
echo "    ██║  ██║╚██████╗ "
echo "    ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${BLUE}Hermes CLI 管理工具安装程序${NC}"
echo "────────────────────────────────────────────"

# 检查是否已安装
if [ -f "$INSTALL_PATH" ]; then
    echo -e "${YELLOW}⚠️  检测到已安装 Hermes CLI${NC}"
    read -p "是否重新安装？(y/n): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "已取消安装"
        exit 0
    fi
fi

# 检查依赖
echo -e "${BLUE}检查依赖...${NC}"

if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ 未找到 curl，正在安装...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y curl
    elif command -v yum &> /dev/null; then
        sudo yum install -y curl
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y curl
    elif command -v brew &> /dev/null; then
        brew install curl
    else
        echo -e "${RED}❌ 无法自动安装 curl，请手动安装${NC}"
        exit 1
    fi
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 python3，请先安装 Python 3.9+${NC}"
    exit 1
fi

# 检查 Python 版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
python_major=$(echo "$python_version" | cut -d. -f1)
python_minor=$(echo "$python_version" | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 9 ]); then
    echo -e "${RED}❌ Python 版本过低: $python_version，需要 Python 3.9+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $python_version${NC}"

# 下载脚本
echo -e "${BLUE}正在下载 Hermes CLI...${NC}"

TEMP_FILE=$(mktemp)
if ! curl -fsSL "${RAW_URL}/${SCRIPT_NAME}" -o "$TEMP_FILE"; then
    echo -e "${RED}❌ 下载失败，请检查网络连接${NC}"
    rm -f "$TEMP_FILE"
    exit 1
fi

echo -e "${GREEN}✅ 下载完成${NC}"

# 安装脚本
echo -e "${BLUE}正在安装到 ${INSTALL_PATH}...${NC}"

if [ -w "$(dirname "$INSTALL_PATH")" ]; then
    cp "$TEMP_FILE" "$INSTALL_PATH"
    chmod +x "$INSTALL_PATH"
else
    sudo cp "$TEMP_FILE" "$INSTALL_PATH"
    sudo chmod +x "$INSTALL_PATH"
fi

rm -f "$TEMP_FILE"

# 验证安装
if [ -f "$INSTALL_PATH" ] && [ -x "$INSTALL_PATH" ]; then
    echo -e "${GREEN}✅ 安装成功！${NC}"
    echo ""
    echo "────────────────────────────────────────────"
    echo -e "  使用方法: ${BLUE}hc${NC}"
    echo -e "  查看版本: ${BLUE}hc --version${NC}"
    echo -e "  安装路径: ${BLUE}${INSTALL_PATH}${NC}"
    echo "────────────────────────────────────────────"
    echo ""
    
    # 测试运行
    read -p "是否现在运行 Hermes CLI？(y/n): " run_now
    if [ "$run_now" = "y" ] || [ "$run_now" = "Y" ]; then
        exec "$INSTALL_PATH"
    fi
else
    echo -e "${RED}❌ 安装失败${NC}"
    exit 1
fi
