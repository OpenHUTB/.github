
rem conda create -n mkdocs python=3.10 -y
rem conda activate mkdocs
rem conda activate mkdocs

:: 启动mkdocs虚拟环境（注意替换为本地的anaconda3目录、虚拟环境名为mkdocs）
%WINDIR%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'D:\hutb\Build\dependencies\prerequisites\miniconda3\shell\condabin\conda-hook.ps1' ; conda activate 'D:\hutb\Build\dependencies\prerequisites\miniconda3' "; conda activate mkdocs; mkdocs serve --livereload;
