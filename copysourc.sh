#!/bin/bash

for item in /mnt/mali/images2/*; do
    if [ -d "$item" ]; then
        
        basename=$(basename "$item")
        echo "$item"
        cd "$item" 
        # echo "包名称为$basename"
        # tar -cvf "$basename".tar info disk disk1
        # echo "$item路径下打包成功"
        sleep 1
        cp "$item/$basename"".tar" /home/ftp/
        echo "copy $basename完成"
    else
        echo "$item is not a directory"
    fi
done
echo "所有脚本都已经执行完成"
