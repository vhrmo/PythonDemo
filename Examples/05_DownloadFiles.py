import os
import paramiko
from Secrets import Secrets


server_name = 'r5cvwb1005'
file_name = '../Data/Servers.json5'


def upload_file():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_name, username=Secrets.user_name, key_filename=Secrets.private_key_file)

        sftp = ssh.open_sftp()
        sftp.put(file_name, os.path.basename(file_name))
        sftp.close()

        ssh.close()
    except Exception as e:
        print e


def download_files():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_name, username=Secrets.user_name, key_filename=Secrets.private_key_file)

        # check for the locked account
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uname")
        if "expired" in ssh_stderr.read():
            print server_name, ", Password change required!!!!!!!!!!!!!!!!!!!"
        else:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('find /fdc/logs -name "access*" | xargs tar --ignore-failed-read -zcf ~/`hostname`-logs.tar.gz')
            print ssh_stderr.read()
            print ssh_stdout.read()

            tar_name = server_name + "-logs.tar.gz"
            sftp = ssh.open_sftp()
            sftp.get(tar_name, os.path.basename(tar_name))
            sftp.close()

            ssh.exec_command("rm ~/*-logs.tar.gz")

        ssh.close()
    except Exception as e:
        print e
        raise e


upload_file()
# download_files()
