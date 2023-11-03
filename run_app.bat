@echo off
docker run crashserver
@REM timeout /t 2 >nul
@REM for /f %%i in ('docker ps -l -q') do set container_id=%%i
@REM echo server container id: %container_id%
@REM echo to stop the server run the following command: docker kill %container_id%

