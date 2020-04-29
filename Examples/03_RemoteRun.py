import paramiko
from Secrets import Secrets


server_name = 'n5cvap1001'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(server_name, username=Secrets.user_name, key_filename=Secrets.private_key_file)

    # check for the locked account
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uname -a;lsb_release -a;cat /etc/issue.net; cat /etc/*release")
    if "expired" in ssh_stderr.read():
        print server_name, ", Password change required!!!!!!!!!!!!!!!!!!!"
    else:
        print ssh_stdout.read()

    ssh.close()
except:
    print server_name, ", Errorrrrrrrrrrrrrrrrrrrrrrr"
    raise
