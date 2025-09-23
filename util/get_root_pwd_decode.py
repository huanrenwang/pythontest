import time

import paramiko


# 脚本使用之前，需要先安装paramiko, pip install paramiko

def ssh_linux(hostname, username, password, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, port=port, username=username, password=password)
    except Exception:
        print('连接失败')
        print('连接失败')
    return client


def get_linux_info(hostname, username, password, cmd, port=22):
    """
    远程登录linux获取要取得的信息
    :param hostname: ip.
    :param port: 远程连接端口，ssh为22.
    :param username: 用户名.
    :param password: 密码.
    :param cmd: 输入的linux命令.
    :return: 输入命令stout打印的所有信息.
    """
    ssh = ssh_linux(hostname, username, password, port)
    invoke_linux = ssh.invoke_shell()
    invoke_linux.send(cmd + '\n')
    time.sleep(1)
    info_linux = invoke_linux.recv(1024).decode("utf-8")
    ssh.close()
    return info_linux


if __name__ == '__main__':
    # 获取平台root密码信息
    hostname = '10.8.100.1'
    username = 'ops'
    password = 'ycxx123#'
    cmd = 'cat cipher/root_login_password'
    linux_info = get_linux_info(hostname, username, password, cmd)
    # 处理信息获取到root的密码信息
    root_pwd_encode_info = linux_info[:-18].splitlines()[6]
    # 调用可以解密的平台进行解密
    hostname = '124.222.76.251'
    username = 'root'
    password = '6789@jkl'
    cmd = f'echo -n  "{root_pwd_encode_info}" | base64 -d | openssl enc -aes-256-ecb -a -d -pass pass:"QWEasd123" ' \
          f'-nosalt 2>/dev/null'
    linux_info = get_linux_info(hostname, username, password, cmd)[:-24].splitlines()
    root_pwd_decode_info = linux_info[-1]
    print(root_pwd_decode_info)

