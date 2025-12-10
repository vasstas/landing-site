import paramiko

HOST = "94.249.192.193"
USER = "ubuntu"
PASSWORD = "m4qy62MQ"

def fix_permissions():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD)
    
    commands = [
        "usermod -aG landing ubuntu",
        "chown -R landing:landing /srv/landing",
        "chmod -R 775 /srv/landing"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        stdin, stdout, stderr = client.exec_command(f"echo {PASSWORD} | sudo -S {cmd}")
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(f"STDERR: {err}")
            
    client.close()

if __name__ == "__main__":
    fix_permissions()
