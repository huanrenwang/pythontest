# 打开文件
file = open('example.txt', 'r')

# 逐行读取文件内容
for line in file:
    print(line)

# 关闭文件
file.close()
