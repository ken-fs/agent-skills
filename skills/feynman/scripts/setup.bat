@echo off
REM 飞书多维表格集成 - Windows 快速配置脚本
REM 用于引导用户完成环境变量配置

echo ========================================
echo 飞书多维表格集成 - 快速配置向导
echo ========================================
echo.

echo 本脚本将帮助你配置飞书多维表格集成所需的环境变量。
echo.
echo 你需要准备以下信息：
echo   1. 飞书应用 ID (App ID)
echo   2. 飞书应用密钥 (App Secret)
echo   3. 多维表格 App Token
echo   4. 表格 Table ID
echo.
echo 如果还没有这些信息，请先参考配置指南：
echo   references\feishu-setup-guide.md
echo.

pause

echo.
echo ========================================
echo 开始配置环境变量
echo ========================================
echo.

REM 读取 App ID
:input_app_id
set /p FEISHU_APP_ID="请输入飞书应用 ID (cli_xxxxx): "
if "%FEISHU_APP_ID%"=="" (
    echo [错误] App ID 不能为空
    goto input_app_id
)

REM 读取 App Secret
:input_app_secret
set /p FEISHU_APP_SECRET="请输入飞书应用密钥: "
if "%FEISHU_APP_SECRET%"=="" (
    echo [错误] App Secret 不能为空
    goto input_app_secret
)

REM 读取 App Token
:input_app_token
set /p FEISHU_BITABLE_APP_TOKEN="请输入多维表格 App Token (bascnxxxxx): "
if "%FEISHU_BITABLE_APP_TOKEN%"=="" (
    echo [错误] App Token 不能为空
    goto input_app_token
)

REM 读取 Table ID
:input_table_id
set /p FEISHU_BITABLE_TABLE_ID="请输入表格 Table ID (tblxxxxx): "
if "%FEISHU_BITABLE_TABLE_ID%"=="" (
    echo [错误] Table ID 不能为空
    goto input_table_id
)

echo.
echo ========================================
echo 配置摘要
echo ========================================
echo.
echo FEISHU_APP_ID: %FEISHU_APP_ID%
echo FEISHU_APP_SECRET: %FEISHU_APP_SECRET:~0,10%...
echo FEISHU_BITABLE_APP_TOKEN: %FEISHU_BITABLE_APP_TOKEN%
echo FEISHU_BITABLE_TABLE_ID: %FEISHU_BITABLE_TABLE_ID%
echo.

set /p confirm="确认以上信息正确吗？(Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo 已取消配置。
    pause
    exit /b 1
)

echo.
echo ========================================
echo 选择配置方式
echo ========================================
echo.
echo 1. 仅在当前会话中设置（临时，关闭窗口后失效）
echo 2. 设置为用户环境变量（永久，推荐）
echo.
set /p config_type="请选择 (1 或 2): "

if "%config_type%"=="1" (
    REM 临时设置
    echo.
    echo [设置中] 正在设置临时环境变量...
    setx FEISHU_APP_ID "%FEISHU_APP_ID%" >nul 2>&1
    setx FEISHU_APP_SECRET "%FEISHU_APP_SECRET%" >nul 2>&1
    setx FEISHU_BITABLE_APP_TOKEN "%FEISHU_BITABLE_APP_TOKEN%" >nul 2>&1
    setx FEISHU_BITABLE_TABLE_ID "%FEISHU_BITABLE_TABLE_ID%" >nul 2>&1

    echo [完成] 环境变量已设置（当前会话）
    echo.
    echo 注意：这些变量仅在当前命令行窗口有效。
    echo       关闭窗口后将失效。
) else if "%config_type%"=="2" (
    REM 永久设置
    echo.
    echo [设置中] 正在设置用户环境变量...
    setx FEISHU_APP_ID "%FEISHU_APP_ID%" >nul
    setx FEISHU_APP_SECRET "%FEISHU_APP_SECRET%" >nul
    setx FEISHU_BITABLE_APP_TOKEN "%FEISHU_BITABLE_APP_TOKEN%" >nul
    setx FEISHU_BITABLE_TABLE_ID "%FEISHU_BITABLE_TABLE_ID%" >nul

    if errorlevel 1 (
        echo [错误] 设置环境变量失败，请检查权限
        pause
        exit /b 1
    )

    echo [完成] 用户环境变量已设置
    echo.
    echo 注意：需要重新打开命令行窗口才能生效。
) else (
    echo.
    echo [错误] 无效的选择
    pause
    exit /b 1
)

echo.
echo ========================================
echo 测试配置
echo ========================================
echo.
set /p test_now="是否立即运行配置检查工具？(Y/N): "

if /i "%test_now%"=="Y" (
    echo.
    echo [运行中] 正在检查配置...
    echo.

    REM 检查 Python 是否可用
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [错误] 未找到 Python，请先安装 Python 3.7+
        echo        下载地址: https://www.python.org/downloads/
        pause
        exit /b 1
    )

    REM 检查 requests 库
    python -c "import requests" >nul 2>&1
    if errorlevel 1 (
        echo [安装中] 正在安装 requests 库...
        pip install requests
        if errorlevel 1 (
            echo [错误] requests 库安装失败
            pause
            exit /b 1
        )
    )

    REM 运行配置检查
    cd /d "%~dp0"
    python check_config.py

    if errorlevel 1 (
        echo.
        echo [失败] 配置检查未通过，请根据上述错误信息进行修复。
        echo.
        echo 常见问题：
        echo   1. 应用未授权访问多维表格
        echo   2. 表格字段名不匹配
        echo   3. App ID 或 Secret 错误
        echo.
        echo 详细配置指南：
        echo   ..\references\feishu-setup-guide.md
    ) else (
        echo.
        echo ========================================
        echo 🎉 配置完成！
        echo ========================================
        echo.
        echo 你现在可以使用以下命令：
        echo   python save_to_feishu.py --test     # 测试保存功能
        echo   python example_usage.py             # 查看使用示例
        echo.
        echo 或者在 Claude Code 中使用：
        echo   /feynman [概念名称]
        echo.
    )
) else (
    echo.
    echo ========================================
    echo 配置完成
    echo ========================================
    echo.
    echo 环境变量已设置。
    echo.
    echo 下一步：
    echo   1. 重新打开命令行窗口（如果选择了永久设置）
    echo   2. 运行配置检查：python check_config.py
    echo   3. 查看使用指南：type ..\README.md
    echo.
)

pause
