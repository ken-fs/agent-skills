@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   配置飞书环境变量
echo ========================================
echo.

echo [1/4] 设置 FEISHU_APP_ID...
setx FEISHU_APP_ID "cli_a90846c997795bc4"
if %errorlevel% equ 0 (
    echo ✓ FEISHU_APP_ID 设置成功
) else (
    echo ✗ FEISHU_APP_ID 设置失败
)

echo.
echo [2/4] 设置 FEISHU_APP_SECRET...
setx FEISHU_APP_SECRET "JdXarMiUhwCgbrp97OjUhdp28IJvuQ6k"
if %errorlevel% equ 0 (
    echo ✓ FEISHU_APP_SECRET 设置成功
) else (
    echo ✗ FEISHU_APP_SECRET 设置失败
)

echo.
echo [3/4] 设置 FEISHU_BITABLE_APP_TOKEN...
setx FEISHU_BITABLE_APP_TOKEN "DLMfbXCvNaGsbksuqKPcoVBFnZK"
if %errorlevel% equ 0 (
    echo ✓ FEISHU_BITABLE_APP_TOKEN 设置成功
) else (
    echo ✗ FEISHU_BITABLE_APP_TOKEN 设置失败
)

echo.
echo [4/4] 设置 FEISHU_BITABLE_TABLE_ID...
setx FEISHU_BITABLE_TABLE_ID "tblAJ5G6R4YoRnGH"
if %errorlevel% equ 0 (
    echo ✓ FEISHU_BITABLE_TABLE_ID 设置成功
) else (
    echo ✗ FEISHU_BITABLE_TABLE_ID 设置失败
)

echo.
echo ========================================
echo   环境变量配置完成！
echo ========================================
echo.
echo ⚠️ 重要提示:
echo   请关闭当前所有终端窗口，重新打开新的终端
echo   环境变量才会生效！
echo.
echo 下一步:
echo   1. 关闭所有 PowerShell/CMD 窗口
echo   2. 重新打开一个新的终端
echo   3. 运行测试: cd %~dp0 ^&^& test_feishu.bat
echo.
pause
