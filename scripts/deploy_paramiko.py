import paramiko
import os
import sys
import time

HOST = "94.249.192.193"
USER = "ubuntu"
PASSWORD = "m4qy62MQ"
REMOTE_PATH = "/srv/landing"

# Files and directories to sync
SYNC_ITEMS = [
    "landing_site",
    "templates",
    "locale",
    "static",
    "pages",
    "scripts",
    "requirements.txt",
    "manage.py"
]

def create_remote_dir(sftp, remote_dir):
    """Recursively create remote directories."""
    dirs = remote_dir.split('/')
    path = ""
    for d in dirs:
        if not d: continue
        path += "/" + d
        try:
            sftp.stat(path)
        except IOError:
            sftp.mkdir(path)

def upload_dir(sftp, local_dir, remote_dir):
    """Recursively upload a directory."""
    create_remote_dir(sftp, remote_dir)
    for item in os.listdir(local_dir):
        if item.startswith('.') or item == '__pycache__':
            continue
            
        local_path = os.path.join(local_dir, item)
        remote_path = os.path.join(remote_dir, item)
        
        if os.path.isfile(local_path):
            print(f"Uploading {local_path} to {remote_path}")
            sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            upload_dir(sftp, local_path, remote_path)

def deploy():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, username=USER, password=PASSWORD)
        print("Connected successfully.")
        
        sftp = client.open_sftp()
        
        print("Starting file upload...")
        for item in SYNC_ITEMS:
            local_path = os.path.abspath(item)
            remote_item_path = f"{REMOTE_PATH}/{item}"
            
            if os.path.isfile(local_path):
                print(f"Uploading {item}...")
                sftp.put(local_path, remote_item_path)
            elif os.path.isdir(local_path):
                print(f"Uploading directory {item}...")
                upload_dir(sftp, local_path, remote_item_path)
        
        print("File upload complete.")
        sftp.close()
        
        # Run commands
        shell = client.invoke_shell()
        
        # Wait for initial prompt
        time.sleep(1)
        while shell.recv_ready():
            shell.recv(1024)

        commands = [
            f"echo {PASSWORD} | sudo -S chown -R landing:landing /srv/landing",
            f"echo {PASSWORD} | sudo -S -u landing bash -c 'cd /srv/landing && source .venv/bin/activate && pip install -r requirements.txt'",
            f"echo {PASSWORD} | sudo -S -u landing bash -c 'cd /srv/landing && source .venv/bin/activate && python manage.py migrate'",
            f"echo {PASSWORD} | sudo -S -u landing bash -c 'cd /srv/landing && source .venv/bin/activate && python manage.py collectstatic --noinput'",
            f"echo {PASSWORD} | sudo -S -u landing bash -c 'cd /srv/landing && source .venv/bin/activate && python manage.py compilemessages --ignore=.venv'",
            f"echo {PASSWORD} | sudo -S systemctl restart gunicorn"
        ]

        for cmd in commands:
            print(f"Executing: {cmd}")
            shell.send(cmd + "\n")
            time.sleep(2)
            
            # Read output
            while True:
                if shell.recv_ready():
                    data = shell.recv(4096).decode('utf-8', errors='replace')
                    print(data, end="")
                    if data.strip().endswith("$") or data.strip().endswith("#"):
                        break
                else:
                    time.sleep(0.5)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    deploy()
