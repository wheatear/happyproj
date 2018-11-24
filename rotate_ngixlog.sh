#!/usr/bin/env bash

#!/bin/bash
#设置日志文件存放目录
LOG_HOME="/data/web/happyproj/log"

#备分文件名称
LOG_PATH_BAK="nginx_$(date -d yesterday +%Y%m%d)".log

#重命名日志文件
mv ${LOG_HOME}/nginx.log ${LOG_HOME}/${LOG_PATH_BAK}.log

#向nginx主进程发信号重新打开日志
kill -USR1 `cat /data/svr/nginx/logs/nginx.pid`
