# run_count_docs.py
# Запуск джобы подсчета количества документов

import os
from dotenv import load_dotenv
from utils import run

load_dotenv()

NAME_NODE             = os.getenv("NAME_NODE")
CODE_DIR_IN_CONTAINER = os.getenv("CODE_DIR_IN_CONTAINER")
INPUT_DOCS            = os.getenv("INPUT_DOCS")
DOC_COUNT_OUTPUT      = os.getenv("DOC_COUNT_OUTPUT", "/user/hadoop/tfidf_doc_count")

def main():
    print("Запуск шага подсчета количества документов →", DOC_COUNT_OUTPUT)

    # Удаляем предыдущий вывод, чтобы Hadoop не жаловался
    run(f"docker exec {NAME_NODE} hdfs dfs -rm -r -f {DOC_COUNT_OUTPUT}")

    streaming_cmd = (
        "hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar "
        f"-files {CODE_DIR_IN_CONTAINER}/mapper_count_docs.py,{CODE_DIR_IN_CONTAINER}/reducer_count_docs.py "
        "-mapper 'python3 mapper_count_docs.py' "
        "-reducer 'python3 reducer_count_docs.py' "
        f"-input {INPUT_DOCS} "
        f"-output {DOC_COUNT_OUTPUT} "
        "-cmdenv PYTHONIOENCODING=utf-8"
    )

    run(f"docker exec {NAME_NODE} sh -c \"{streaming_cmd}\"")

    print(f"\nРезультат в {DOC_COUNT_OUTPUT}")
    print("----------------------------")
    print("Общее количество документов:")
    run(f"docker exec {NAME_NODE} hdfs dfs -cat {DOC_COUNT_OUTPUT}/part-*")
    print("----------------------------")

if __name__ == '__main__':
    main()
