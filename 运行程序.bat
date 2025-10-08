@echo off
chcp 65001 > nul

echo 正在启动陈狗模型检测代码执行器...
start "" "%~dp0\dist\陈狗模型检测代码执行器.exe"

REM 可选：等待几秒后自动关闭批处理窗口
ping 127.0.0.1 -n 3 > nul