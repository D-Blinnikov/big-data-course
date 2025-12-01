import os
import time
from utils import run 

NAME_NODE = "hadoop-namenode-1"



def main():
    project_dir = os.getcwd() 
    print("Работаем из:", project_dir)

    run("docker-compose down")

    run("docker-compose up -d")

    print("Ожидание запуска контейнеров...")
    time.sleep(5)



    run(f"docker cp ./mapper_count_docs.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./reducer_count_docs.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./mapper_tf.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./reducer_df.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./mapper_tfidf.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./reducer_tfidf.py {NAME_NODE}:/tmp/")

    hdfs_cmds = [
        "hdfs dfs -mkdir -p /user/hadoop/input",
    ]

    for cmd in hdfs_cmds:
        run(f"docker exec {NAME_NODE} {cmd}")

    print("Hadoop запущен.")

if __name__ == "__main__":
    main()
