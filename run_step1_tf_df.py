# run_step1_tf_df.py
# Запуск первой джобы: TF + DF

import os
from dotenv import load_dotenv
from utils import run

load_dotenv()

NAME_NODE             = os.getenv("NAME_NODE")
CODE_DIR_IN_CONTAINER = os.getenv("CODE_DIR_IN_CONTAINER")
INPUT_DOCS            = os.getenv("INPUT_DOCS")
TFIDF_STEP1           = os.getenv("TFIDF_STEP1")  # фиксированный путь

def main():
    print("Запуск Step 1 →", TFIDF_STEP1)

    streaming_cmd = (
        "hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar "
        f"-files {CODE_DIR_IN_CONTAINER}/mapper_tf.py,{CODE_DIR_IN_CONTAINER}/reducer_df.py "
        "-mapper 'python3 mapper_tf.py' "
        "-reducer 'python3 reducer_df.py' "
        f"-input {INPUT_DOCS} "
        f"-output {TFIDF_STEP1} "
        "-cmdenv PYTHONIOENCODING=utf-8"
    )

    run(f"docker exec {NAME_NODE} sh -c \"{streaming_cmd}\"")

    print(f"\nStep 1 завершён! Результат в {TFIDF_STEP1}")
    print("Первые 20 строк результата (TF + DF):")
    run(f"docker exec {NAME_NODE} hdfs dfs -cat {TFIDF_STEP1}/part-00000 | head -n 20")

    print("\nТеперь можно запускать Step 2 — он сам найдёт данные")

if __name__ == "__main__":
    main()