import re
import sys
import json
import paramiko

import Servers
from Secrets import Secrets


#  Result data - key is server name, value is an object with captured information
result = {}


# Return true if the param is an instance of string
# The method handles this correctly for python 2 and 3.
def isstring(param):
    if (sys.version_info >= (3, 0)):
        return isinstance(param, str)  # python 3
    else:
        return isinstance(param, basestring)  # python 2


def add_info(server_name, key, value):
    global result

    # create initial empty object if it does not exist and set its desc.
    result.setdefault(server_name, {})

    # check if value exists for a key and convert to array of values if multiple values added to a key
    existing_val = result[server_name].get(key, None)
    if existing_val is None:
        result[server_name][key] = value
    elif isstring(existing_val):
        result[server_name][key] = [existing_val, value]
    elif isinstance(existing_val, list):
        existing_val.append(value)
    else:
        print "Error adding value to a key", key, value

    # print key, value


def get_os_info(ssh, server_name):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uname -a;lsb_release -a;cat /etc/issue.net; cat /etc/*release")
    out = ssh_stdout.read()
    err = ssh_stderr.read()
    if "Oracle Linux Server release 6.10" in out:
        os_ver = "Oracle Linux 6.10"
    elif "Oracle Linux Server release 7.6" in out:
        os_ver = "Oracle Linux 7.6"
    elif "Oracle Linux Server release 7.7" in out:
        os_ver = "Oracle Linux 7.7"
    elif "Red Hat Enterprise Linux Server release 6.8" in out:
        os_ver = "RedHat 6.8"
    elif "Red Hat Enterprise Linux Server release 6.10" in out:
        os_ver = "RedHat 6.10"
    elif "Red Hat Enterprise Linux Server release 6.7" in out:
        os_ver = "RedHat 6.7"
    elif "Red Hat Enterprise Linux Server release 6.3" in out:
        os_ver = "RedHat 6.3"
    elif "SUSE Linux Enterprise Server 10" in out:
        os_ver = "SLES 10"
    elif "SUSE Linux Enterprise Server 11" in out:
        os_ver = "SLES 11"
    else:
        print "==================================================================================================="
        print "Server>", server_name
        print err
        print "-----------"
        print out
        print "---------------------------------------------------------------------------------------------------"
        os_ver = err

    add_info(server_name, 'os_version', os_ver)


def get_open_ssl_info(ssh, server_name):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("openssl version")
    out = ssh_stdout.read()
    # sys.stdout.write(server_name + "," + server_desc + "," + out)
    add_info(server_name, 'openssl_version', out.strip())


def get_apache_info(ssh, server_name):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("find /opt/apache -name httpd -type f 2>&1 | grep -v  'Permission denied' | grep -v 'No such file or directory'")

    for line in ssh_stdout:
        httpd = line.strip()
        ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh.exec_command(httpd + " -v | grep 'Server version:'")
        apache_ver = ssh_stdout2.read().strip()[16:]
        add_info(server_name, 'apache_version', apache_ver)


docker_versio_rex = re.compile('Version:\s*(\S+)', re.MULTILINE)


def get_docker_info(ssh, server_name):
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cd /fdc/logs; tree -h -I *.gz -D | grep -v html")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("docker version;docker images")

    #  docker images
    # Cannot connect to the Docker daemon. Is the docker daemon running on this host?

    out = ssh_stdout.read()
    err = ssh_stderr.read()

    if "command not found" in err:
        print "Server>,", "{0:<10}".format(server_name), ",", "{0:<28}".format(","), ", Err"

    elif "Version:" in out:
        match = docker_versio_rex.search(out)
        docker_version = match.group(1)

        if "REPOSITORY" in out :
            run_status = " and running"
        else:
            run_status = ", but NOT running"

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("docker-compose")
        out = ssh_stdout.read()
        err = ssh_stderr.read()
        # print err
        if "Define and run multi-container applications with Docker." not in err:
            run_status += " (docker-compose missing)"

        print "Server>,", "{0:<10}".format(server_name), ",", ", Docker version:", "{0:<10}".format(docker_version), ", OK - Docker installed" + run_status
    else:
        print "==================================================================================================="
        print "Server>", server_name
        print err
        print "-----------"
        print out
        print "---------------------------------------------------------------------------------------------------"


# Blocking call to ssh.exec_command
def exec_command(ssh, cmd):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    exit_status = ssh_stdout.channel.recv_exit_status()
    if exit_status != 0:
        print("Error running command:", cmd)


for server in Servers.servers:
    server_name = server["name"]


    if "WSV" in server["cluster"] and any(s in server["environment"] for s in ("UAT", "SIT")):
    # if server["name"] in ("n5cvwb993", "n5cvwb995"):

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server_name, username=Secrets.user_name, key_filename="c:\work\Keys\private.key")

            # check for the locked account
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uname")
            if "expired" in ssh_stderr.read():
                print server_name, ", Password change required!!!!!!!!!!!!!!!!!!!"
            else:

                print server_name

                get_os_info(ssh, server_name)
                get_open_ssl_info(ssh, server_name)
                # get_docker_info(ssh, server_name)
                get_apache_info(ssh, server_name)

            ssh.close()
        except:
            print server_name, ", Errorrrrrrrrrrrrrrrrrrrrrrr"
            raise

print
print json.dumps(result, indent=2)
