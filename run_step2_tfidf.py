# run_step2_tfidf.py
import os
from datetime import datetime
from utils import run
from dotenv import load_dotenv
import subprocess

load_dotenv()

NAME_NODE             = os.getenv("NAME_NODE", "hadoop-namenode-1")
CODE_DIR_IN_CONTAINER = os.getenv("CODE_DIR_IN_CONTAINER", "/temp")
OUTPUT_BASE_DIR       = os.getenv("OUTPUT_BASE_DIR", "/user/hadoop/tfidf_results")
# STEP1_OUTPUT          = os.getenv("STEP1_OUTPUT")  # ← обязательно укажи в .env после первой джобы!
TFIDF_STEP1           = os.getenv("TFIDF_STEP1")
TFIDF_FINAL           = os.getenv("TFIDF_FINAL")



def get_total_docs():
    cmd = f"hdfs dfs -cat {os.getenv('INPUT_DOCS')} | wc -l"
    result = subprocess.run(
        f"docker exec {NAME_NODE} sh -c \"{cmd}\"",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return int(result.stdout.strip())

def main():
    total_docs = get_total_docs()
    print(f"Общее количество каналов: {total_docs}")

    print(f"Запуск Step 2: {TFIDF_STEP1} → {TFIDF_FINAL}")

    streaming_cmd = (
        "hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar "
        f"-files {CODE_DIR_IN_CONTAINER}/mapper_tfidf.py,{CODE_DIR_IN_CONTAINER}/reducer_tfidf.py "
        "-mapper 'python3 mapper_tfidf.py' "
        "-reducer 'python3 reducer_tfidf.py' "
        f"-input {TFIDF_STEP1} "
        f"-output {TFIDF_FINAL} "
        f"-cmdenv TOTAL_DOCS={total_docs} "
        "-cmdenv MAX_TERMS=8000 "
        "-cmdenv MIN_TFIDF=0.07 "
        "-cmdenv ENABLE_L2_NORM=1 "
        "-cmdenv PYTHONIOENCODING=utf-8"
    )

    run(f"docker exec {NAME_NODE} sh -c \"{streaming_cmd}\"")

    print(f"\nГотово! Финальные вектора в {TFIDF_FINAL}")
    print("Скачивай:")
    print(f"mkdir -p final_vectors && docker cp {NAME_NODE}:{TFIDF_FINAL}/part-* final_vectors/")

if __name__ == "__main__":
    main()