#!/bin/bash  
  
# 获取当前脚本的绝对路径  
script_path=$(realpath "$0")  
  
# 获取当前脚本所在的目录路径  
dirname=$(dirname "$script_path")  
  
# 使用basename命令获取目录名称  
basename=$(basename "$dirname")  
basename=$(basename "$dirname1")
  
# 输出目录名称  
#echo "当前脚本所在的目录名称是：$basename"
#tar -cvf "$basename".tar info disk disk1
#echo "$basename打包成功"
#sleep 1
cp "$dirname/$basename"".tar" /home/ftp/

