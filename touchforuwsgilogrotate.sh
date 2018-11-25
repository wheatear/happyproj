#!/bin/bash

#DIR=`echo $(cd "$(dirname "$0")"; pwd)`       #获取当前目录
LOGDIR="/data/web/happyproj/log"                   #log目录

sourcelogpath="${LOGDIR}/uwsgi.log"            #log源地址
touchfile="${LOGDIR}/.touchforlogrotat"       #需要touch的文件

DATE=`date -d "yesterday" +"%Y%m%d"`
destlogpath="${LOGDIR}/uwsgi_${DATE}.log"     #重命名后的文件
mv $sourcelogpath $destlogpath

touch $touchfile                            # 更新文件时间戳
