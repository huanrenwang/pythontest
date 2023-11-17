import base64
import OpenSSL
import time
import paramiko
import subprocess
import yaml
import pymysql
import pandas as pd


# 脚本使用之前，需要先安装paramiko, pip install paramiko
def ssh_linux(hostname, username, password, port):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, port=port, username=username, password=password)
    except Exception:
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


def get_linux_root_pwd(hostname, username, password, cmd) -> str:
    root_ = get_linux_info(hostname, username, password, cmd, port=22)[:-18].splitlines()[6]
    root_ = f'{root_}'
    return get_openssl_pass(root_, "QWEasd123")


def get_openssl_pass(cipher, pwd):
    ciphertext = cipher
    openssl_pass = pwd

    # Base64解码
    decoded_bytes = base64.b64decode(ciphertext)

    # 将解码后的字节写入到一个临时文件中
    with open('tmp_input.bin', 'wb') as f:
        f.write(decoded_bytes)

    # 使用subprocess执行openssl命令进行解密
    command = ['openssl', 'enc', '-aes-256-ecb', '-a', '-d', '-pass', 'pass:' + openssl_pass, '-nosalt', '-in',
               'tmp_input.bin',
               '-out', 'tmp_output.bin']
    subprocess.run(command, check=True)

    # 读取解密后的结果
    with open('tmp_output.bin', 'rb') as f:
        decrypted_bytes = f.read().rstrip()

    # 删除临时文件
    subprocess.run(['rm', 'tmp_input.bin', 'tmp_output.bin'], check=True)

    # 将解密后的字节转换为字符串
    decrypted_string = decrypted_bytes.decode('utf-8')

    return decrypted_string


def read_yaml_file_remote(host, name, pwd, yaml_path, yaml_key, port=22) -> str:

    client = ssh_linux(host, name, pwd, port)
    stdin, stdout, stderr = client.exec_command(f'cat {yaml_path}')
    yaml_content = stdout.read().decode("utf-8")
    client.close()
    return yaml.safe_load(yaml_content).get(yaml_key)


class DataBase(object):

    def __init__(self, host, port, user, pwd):
        self.db = None
        self.cursor = None
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def conn(self):
        try:
            self.db = pymysql.connect(host=self.host, user=self.user, port=self.port, password=self.pwd)
        except Exception as e:
            print('连接失败')
            print(e)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


#查询实操题资源
def get_practic_list(host, port, user, pwd):

    sql = ''' select a.resource_id env_hash,b.name,a.title from bc.oj_practice_operation a, bc.oj_practice_set b 
    where a.practice_set_id = b.resource_id and a.dynamic_env = 1;'''

    with DataBase(host, port, user, pwd) as db:
        db.conn()
        pratic_list = db.get_list(sql)

    return pratic_list


def write_practic_list_to_csv(host, port, user, pwd):

    practic_list = get_practic_list(host, port, user, pwd)

    data = pd.DataFrame(practic_list)
    filename = 'practice.csv'
    data.to_csv(filename, mode='w', index=False)


if __name__ == '__main__':

    hostname = '10.8.100.1'
    username = 'ops'
    password = 'ycxx123#'
    cmd = 'cat cipher/root_login_password'
    root_pwd = get_linux_root_pwd(hostname, username, password, cmd)
    yaml_path = '/opt/docker_build/01build_docker_compose_mariadb.yml'
    yaml_content = read_yaml_file_remote(hostname, "root", root_pwd, yaml_path, "services")
    root_pwd_database = yaml_content.get("mariadb").get("environment")[1][20:]
    write_practic_list_to_csv(hostname, 9306, "root", root_pwd_database)


