import paramiko
import os


def connect_remote():
    host = '123.123.123.123'
    port = 22
    name = 'abc'
    password = '123456'

    # 创建SSH对象
    ssh_client = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机, 第一次登录的认证信息
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh_client.connect(hostname=host, port=port, username=name, password=password)

    transport = paramiko.Transport((host, port))
    transport.connect(username=name, password=password)
    return ssh_client, transport


if __name__ == '__main__':
    local_dir = 'E:/markdown/blog/'
    remote_dir = r'/usr/local/blog/source/_posts/'

    print("=== sftp python v0.1 ===")
    print(" 连接服务器... ")
    ssh, sftp = connect_remote()
    print(" 连接成功 ")
    print(" 1.查看博客路径")
    print(" 2.上传Post文章")
    print(" 3.下载Post文章")
    print(" 4.按q退出")

    while 1:
        answer = input()
        if answer == 'q':
            # 关闭连接
            ssh.close()
            sftp.close()
            exit(0)

        if int(answer) == 1:
            stdin, stdout, stderr = ssh.exec_command('ls ' + remote_dir)
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            print(result.decode())

        elif int(answer) == 2:
            # basedir 根目录, sub_directory 根目录下所有文件夹, sub_file 根目录下所有文件
            for basedir, sub_directory, sub_file in os.walk(local_dir):
                for i in sub_file:
                    print(i)
            file = input("which file want to upload?\n")
            sftp_client = paramiko.SFTPClient.from_transport(sftp)
            print(local_dir + file + '.md', remote_dir + file + '.md')
            sftp_client.put(local_dir + file + '.md', remote_dir + file + '.md')
            print("ok!\n")

        elif int(answer) == 3:
            stdin, stdout, stderr = ssh.exec_command('ls ' + remote_dir)
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            print(result.decode())

            file = input("which file want to download?\n")
            sftp_client = paramiko.SFTPClient.from_transport(sftp)
            sftp_client.get(remote_dir + file + '.md', local_dir + file + '.md')
            print("ok!\n")
