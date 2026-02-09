@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Feynman 飞书集成测试（专业版）
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或未加入 PATH
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖库...
python -c "import requests" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  requests 库未安装，正在安装...
    pip install requests
)

echo.
echo [3/3] 运行飞书集成测试...
echo.
python feishu_bitable_pro.py --test

echo.
echo ========================================
pause
