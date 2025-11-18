import subprocess
from datetime import datetime

NAME_NODE = "hadoop-namenode-1"

def run(cmd):
    print(f"==> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/user/hadoop/output_{timestamp}"

    streaming_cmd = (
        "hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar "
        "-files /tmp/code/mapper.py,/tmp/code/reducer.py "
        "-mapper 'python3 mapper.py' "
        "-reducer 'python3 reducer.py' "
        "-input /user/hadoop/input/* "
        f"-output {output_dir}"
    )

    run(f"docker exec {NAME_NODE} sh -c \"{streaming_cmd}\"")

    run(f"docker exec {NAME_NODE} sh -c \"hdfs dfs -cat {output_dir}/part-00000\"")

if __name__ == "__main__":
    main()
