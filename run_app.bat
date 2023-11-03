@echo off
docker run crashserver
timeout /t 2 >nul
for /f "tokens=*" %%i in ('docker ps -l -q') do set container_id=%%i
echo server container id: %container_id%
echo to stop server run the following command: docker kill %container_id%
