@echo off
setlocal enabledelayedexpansion
chcp 65001
:: 使用方法：
:: check_pr.bat <PullRequest_ID>

REM 判断参数个数是否为1
if "%~2"=="" (
    if not "%~1"=="" (
        set "BRANCH_NAME=%~1"
        echo 参数正确，BRANCH_NAME=%BRANCH_NAME%
    ) else (
        echo 错误：没有提供参数
        exit /b 1
    )
) else (
    echo 错误：只能提供一个参数，当前提供了多个参数
    exit /b 1
)

:: 根据其 ID 号获取对该拉取请求的引用，在该过程中创建一个新分支
git fetch origin pull/%BRANCH_NAME%/head:%BRANCH_NAME%

:: 切换到基于此拉取请求的新分支：
git switch %BRANCH_NAME%