# -*- coding: utf-8 -*-
def ssh(host,username,password,port,root_pwd,cmd):
    import paramiko
    import time
    #import pdb
    #pdb.set_trace()
    #python -m pdb ssh_with_root.py
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        ssh.send('su - \n')
        buff=''
        while not buff.endswith('Password: '):
            resp = ssh.recv(99999999)
            resp = str(resp, encoding='utf-8')
            buff +=resp
            ssh.send(root_pwd)
            ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(999999999)
            resp = str(resp, encoding='utf-8')
            buff +=resp
            ssh.send(cmd)
            ssh.send('\n')
            time.sleep(3)
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(999999999)
            resp = str(resp, encoding='utf-8')
            buff +=resp
        s.close()
        result = buff
    else:
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
    return result

if __name__=="__main__":
    sys_ip = "134.0.84.230"
    username = "euser"
    password = "emerUs3r!"
    root_pwd = "n0kiaTas!"
    cmds = "kubectl exec -it netconf-server-586ff9fc4d-nmzkk bash;confd_cli -u admin -g restoreEng;"
    test= ssh(sys_ip,username,password,22,root_pwd,cmds)
    print(test)
