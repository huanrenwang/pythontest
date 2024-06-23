#!/bin/bash  
# 遍历某个目录下的所有文件并且把disk 和disk1打包成tar包并且拷贝到固定的路径下  
# 获取当前脚本的绝对路径  
script_path=$(realpath "$0")  
  
# 获取当前脚本所在的目录路径  
dirname=$(dirname "$script_path")  
  
# 使用basename命令获取目录名称  
basename=$(basename "$dirname")  
  
# 输出目录名称  
#echo "当前脚本所在的目录名称是：$basename"
#tar -cvf "$basename".tar info disk disk1
#echo "$basename打包成功"
#sleep 1
cp "$dirname/$basename"".tar" /home/ftp/
#sleep 1
time.sleep(1)
