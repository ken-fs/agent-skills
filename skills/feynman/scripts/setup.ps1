# 飞书多维表格集成 - PowerShell 配置脚本
# 用于引导用户完成环境变量配置

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "飞书多维表格集成 - 快速配置向导" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "本脚本将帮助你配置飞书多维表格集成所需的环境变量。" -ForegroundColor White
Write-Host ""
Write-Host "你需要准备以下信息：" -ForegroundColor Yellow
Write-Host "  1. 飞书应用 ID (App ID)" -ForegroundColor Gray
Write-Host "  2. 飞书应用密钥 (App Secret)" -ForegroundColor Gray
Write-Host "  3. 多维表格 App Token" -ForegroundColor Gray
Write-Host "  4. 表格 Table ID" -ForegroundColor Gray
Write-Host ""
Write-Host "如果还没有这些信息，请先参考配置指南：" -ForegroundColor Yellow
Write-Host "  references\feishu-setup-guide.md" -ForegroundColor Gray
Write-Host ""

$continue = Read-Host "准备好了吗？按回车继续，或输入 'N' 取消"
if ($continue -eq 'N' -or $continue -eq 'n') {
    Write-Host "已取消配置。" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始配置环境变量" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 读取配置信息
do {
    $appId = Read-Host "请输入飞书应用 ID (cli_xxxxx)"
    if ([string]::IsNullOrWhiteSpace($appId)) {
        Write-Host "[错误] App ID 不能为空" -ForegroundColor Red
    }
} while ([string]::IsNullOrWhiteSpace($appId))

do {
    $appSecret = Read-Host "请输入飞书应用密钥"
    if ([string]::IsNullOrWhiteSpace($appSecret)) {
        Write-Host "[错误] App Secret 不能为空" -ForegroundColor Red
    }
} while ([string]::IsNullOrWhiteSpace($appSecret))

do {
    $appToken = Read-Host "请输入多维表格 App Token (bascnxxxxx)"
    if ([string]::IsNullOrWhiteSpace($appToken)) {
        Write-Host "[错误] App Token 不能为空" -ForegroundColor Red
    }
} while ([string]::IsNullOrWhiteSpace($appToken))

do {
    $tableId = Read-Host "请输入表格 Table ID (tblxxxxx)"
    if ([string]::IsNullOrWhiteSpace($tableId)) {
        Write-Host "[错误] Table ID 不能为空" -ForegroundColor Red
    }
} while ([string]::IsNullOrWhiteSpace($tableId))

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "配置摘要" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "FEISHU_APP_ID: " -NoNewline -ForegroundColor Gray
Write-Host $appId -ForegroundColor Green
Write-Host "FEISHU_APP_SECRET: " -NoNewline -ForegroundColor Gray
Write-Host "$($appSecret.Substring(0, [Math]::Min(10, $appSecret.Length)))..." -ForegroundColor Green
Write-Host "FEISHU_BITABLE_APP_TOKEN: " -NoNewline -ForegroundColor Gray
Write-Host $appToken -ForegroundColor Green
Write-Host "FEISHU_BITABLE_TABLE_ID: " -NoNewline -ForegroundColor Gray
Write-Host $tableId -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "确认以上信息正确吗？(Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "已取消配置。" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择配置方式" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 仅在当前会话中设置（临时，关闭 PowerShell 后失效）" -ForegroundColor Gray
Write-Host "2. 设置为用户环境变量（永久，推荐）" -ForegroundColor Yellow
Write-Host ""

$configType = Read-Host "请选择 (1 或 2)"

if ($configType -eq '1') {
    # 临时设置
    Write-Host ""
    Write-Host "[设置中] 正在设置临时环境变量..." -ForegroundColor Yellow

    $env:FEISHU_APP_ID = $appId
    $env:FEISHU_APP_SECRET = $appSecret
    $env:FEISHU_BITABLE_APP_TOKEN = $appToken
    $env:FEISHU_BITABLE_TABLE_ID = $tableId

    Write-Host "[完成] 环境变量已设置（当前会话）" -ForegroundColor Green
    Write-Host ""
    Write-Host "注意：这些变量仅在当前 PowerShell 窗口有效。" -ForegroundColor Yellow
    Write-Host "      关闭窗口后将失效。" -ForegroundColor Yellow

} elseif ($configType -eq '2') {
    # 永久设置
    Write-Host ""
    Write-Host "[设置中] 正在设置用户环境变量..." -ForegroundColor Yellow

    try {
        [Environment]::SetEnvironmentVariable("FEISHU_APP_ID", $appId, "User")
        [Environment]::SetEnvironmentVariable("FEISHU_APP_SECRET", $appSecret, "User")
        [Environment]::SetEnvironmentVariable("FEISHU_BITABLE_APP_TOKEN", $appToken, "User")
        [Environment]::SetEnvironmentVariable("FEISHU_BITABLE_TABLE_ID", $tableId, "User")

        # 同时在当前会话中设置
        $env:FEISHU_APP_ID = $appId
        $env:FEISHU_APP_SECRET = $appSecret
        $env:FEISHU_BITABLE_APP_TOKEN = $appToken
        $env:FEISHU_BITABLE_TABLE_ID = $tableId

        Write-Host "[完成] 用户环境变量已设置" -ForegroundColor Green
        Write-Host ""
        Write-Host "注意：已在当前会话和用户环境变量中设置。" -ForegroundColor Green
        Write-Host "      新开的终端窗口将自动应用这些设置。" -ForegroundColor Green

    } catch {
        Write-Host "[错误] 设置环境变量失败：$($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }

} else {
    Write-Host ""
    Write-Host "[错误] 无效的选择" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试配置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$testNow = Read-Host "是否立即运行配置检查工具？(Y/N)"

if ($testNow -eq 'Y' -or $testNow -eq 'y') {
    Write-Host ""
    Write-Host "[运行中] 正在检查配置..." -ForegroundColor Yellow
    Write-Host ""

    # 检查 Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "[检查] Python: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "[错误] 未找到 Python，请先安装 Python 3.7+" -ForegroundColor Red
        Write-Host "       下载地址: https://www.python.org/downloads/" -ForegroundColor Gray
        exit 1
    }

    # 检查 requests 库
    $requestsCheck = python -c "import requests" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[安装中] 正在安装 requests 库..." -ForegroundColor Yellow
        pip install requests
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[错误] requests 库安装失败" -ForegroundColor Red
            exit 1
        }
    }

    # 运行配置检查
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $scriptDir

    python check_config.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "🎉 配置完成！" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "你现在可以使用以下命令：" -ForegroundColor White
        Write-Host "  python save_to_feishu.py --test     # 测试保存功能" -ForegroundColor Gray
        Write-Host "  python example_usage.py             # 查看使用示例" -ForegroundColor Gray
        Write-Host ""
        Write-Host "或者在 Claude Code 中使用：" -ForegroundColor White
        Write-Host "  /feynman [概念名称]" -ForegroundColor Yellow
        Write-Host ""

    } else {
        Write-Host ""
        Write-Host "[失败] 配置检查未通过，请根据上述错误信息进行修复。" -ForegroundColor Red
        Write-Host ""
        Write-Host "常见问题：" -ForegroundColor Yellow
        Write-Host "  1. 应用未授权访问多维表格" -ForegroundColor Gray
        Write-Host "  2. 表格字段名不匹配（必须是：标题、内容、创建时间）" -ForegroundColor Gray
        Write-Host "  3. App ID 或 Secret 错误" -ForegroundColor Gray
        Write-Host ""
        Write-Host "详细配置指南：" -ForegroundColor Yellow
        Write-Host "  ..\references\feishu-setup-guide.md" -ForegroundColor Gray
    }

} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "配置完成" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "环境变量已设置。" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步：" -ForegroundColor Yellow
    Write-Host "  1. 运行配置检查：python check_config.py" -ForegroundColor Gray
    Write-Host "  2. 查看使用指南：Get-Content ..\README.md" -ForegroundColor Gray
    Write-Host "  3. 运行使用示例：python example_usage.py" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
