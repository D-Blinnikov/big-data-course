import os
import time
from utils import run 

NAME_NODE = "hadoop-namenode-1"



def main():
    project_dir = os.getcwd()  # используем текущую директорию
    print("Работаем из:", project_dir)

    # 1. Остановка контейнеров
    run("docker-compose down")

    # 2. Поднятие чистых контейнеров
    run("docker-compose up -d")

    print("Ожидание запуска контейнеров...")
    time.sleep(5)

    # 3–4. Копирование файлов в контейнер
    run(f"docker cp ./data {NAME_NODE}:/tmp/")
    run(f"docker cp ./code {NAME_NODE}:/tmp/")
    run(f"docker cp ./mapper_tf.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./reducer_df.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./mapper_tfidf.py {NAME_NODE}:/tmp/")
    run(f"docker cp ./reducer_tfidf.py {NAME_NODE}:/tmp/")

    # 5. Команды HDFS внутри контейнера
    hdfs_cmds = [
        "hdfs dfs -mkdir -p /user/hadoop/input",
        "hdfs dfs -put /tmp/data/file1.txt /user/hadoop/input/",
        "hdfs dfs -put /tmp/data/file2.txt /user/hadoop/input/",
        "hdfs dfs -put /tmp/data/file3.txt /user/hadoop/input/"
    ]

    for cmd in hdfs_cmds:
        run(f"docker exec {NAME_NODE} {cmd}")

    print("Hadoop запущен.")

if __name__ == "__main__":
    main()
