import subprocess

def run(cmd):
    print(f"==> {cmd}")
    subprocess.run(cmd, shell=True, check=True)