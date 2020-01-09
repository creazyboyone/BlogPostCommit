import paramiko
import os
import time


def connect_remote():
    host = '123.123.123.123'
    port = 22
    name = 'abc'
    key = paramiko.RSAKey.from_private_key_file('C:/Users/feng8/.ssh/id_rsa_feng')

    # 创建SSH对象
    ssh_client = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机, 第一次登录的认证信息
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh_client.connect(hostname=host, port=port, username=name, pkey=key)

    transport = paramiko.Transport((host, port))
    transport.connect(username=name, pkey=key)
    return ssh_client, transport


def execute_command(c):
    stdin, stdout, stderr = ssh.exec_command(c)
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    return result.decode()


if __name__ == '__main__':
    local_dir = 'E:/markdown/blog/'
    remote_dir = r'/usr/local/blog/source/_posts/'
    local_img_dir = 'E:/markdown/blog_image/'
    remote_img_dir = r'/usr/local/nginx/html/down/image/blog/'

    print("=== sftp python v0.1 ===")
    print(" 连接服务器... ")
    ssh, sftp = connect_remote()
    print(" 连接成功~")
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
            print(execute_command('ls ' + remote_dir))

        elif int(answer) == 2:
            index = 1
            files = []
            # basedir 根目录, sub_directory 根目录下所有文件夹, sub_file 根目录下所有文件
            for basedir, sub_directory, sub_file in os.walk(local_dir):
                for value in sub_file:
                    print(str(index) + '.' + value, end='  ')
                    files.append(value)
                    if index % 5 == 0:
                        print(end='\n')
                    index = index + 1
            print('\n')
            dex = input("which file want to upload?\n")
            file = files[int(dex) - 1]
            print(execute_command('rm ' + remote_dir + file))
            time.sleep(1)
            sftp_client = paramiko.SFTPClient.from_transport(sftp)
            sftp_client.put(local_dir + file, remote_dir + file)

            # md上传完后，有图片就上传图片
            file = file[:-3]
            if os.path.exists(local_img_dir + file):
                execute_command('mkdir ' + remote_img_dir + file)
                for basedir, sub_directory, sub_file in os.walk(local_img_dir + file):
                    for i in sub_file:
                        sftp_client.put(local_img_dir + file + '/' + i, remote_img_dir + file + '/' + i)
            print("ok!\n")

        elif int(answer) == 3:
            print(execute_command('ls ' + remote_dir))

            file = input("which file want to download?\n")
            sftp_client = paramiko.SFTPClient.from_transport(sftp)
            sftp_client.get(remote_dir + file + '.md', local_dir + file + '.md')
            print("ok!\n")
