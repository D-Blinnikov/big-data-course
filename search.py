# tg_search.py — фиксированные вектора длины 10000 (для ML, кластеризации, нейросетей)

import os
import glob
import re
import math
import numpy as np
from collections import Counter
from dotenv import load_dotenv
from utils import run

load_dotenv()

NAME_NODE         = os.getenv("NAME_NODE", "hadoop-namenode-1")
TFIDF_FINAL       = os.getenv("TFIDF_FINAL", "/user/hadoop/tfidf_final")
LOCAL_VECTORS_DIR = "tg_vectors_cache"
VOCAB_SIZE        = 10000  # ← фиксированная длина вектора

# Глобальные структуры
word_to_index = {}
channel_vectors = {}  # ch_id → np.array[VOCAB_SIZE]
channel_norms = {}    # всегда 1.0 (уже нормализованы)

def download_vectors_if_needed():
    os.makedirs(LOCAL_VECTORS_DIR, exist_ok=True)
    
    existing = glob.glob(f"{LOCAL_VECTORS_DIR}/part-*")
    if existing:
        print(f"Найдено {len(existing)} part-файлов в кэше")
        if input("Обновить вектора из Hadoop? (y/n, по умолчанию n): ").strip().lower() != 'y':
            return
    else:
        print("Векторов нет в кэше → скачиваю из Hadoop...")

    print(f"Скачиваю вектора из {TFIDF_FINAL}...")

    # Удаляем старое
    run(f"rm -rf {LOCAL_VECTORS_DIR}/*")

    # 1. Копируем файлы из HDFS во временную папку внутри контейнера
    run(f"docker exec {NAME_NODE} mkdir -p /tmp/tfidf_download")
    run(f"docker exec {NAME_NODE} hdfs dfs -get {TFIDF_FINAL}/part-* /tmp/tfidf_download/")

    # 2. Копируем из контейнера на хост
    run(f"docker cp {NAME_NODE}:/tmp/tfidf_download/. {LOCAL_VECTORS_DIR}/")

    # 3. Чистим за собой
    run(f"docker exec {NAME_NODE} rm -rf /tmp/tfidf_download")

    new_files = glob.glob(f"{LOCAL_VECTORS_DIR}/part-*")
    if not new_files:
        print("ОШИБКА: файлы не скачались!")
        run(f"docker exec {NAME_NODE} hdfs dfs -ls {TFIDF_FINAL}/")
        exit(1)

    print(f"Успешно скачано {len(new_files)} файлов")

def build_vocabulary_and_load_vectors():
    global word_to_index, channel_vectors, channel_norms

    print("Строю глобальный словарь (топ-{} слов)...".format(VOCAB_SIZE))
    word_freq = Counter()
    for filepath in glob.glob(f"{LOCAL_VECTORS_DIR}/part-*"):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                _, vec_str = line.split("\t", 1)
                for term in vec_str.split():
                    if ':' in term:
                        word = term.rsplit(":", 1)[0]
                        word_freq[word] += 1

    top_words = [w for w, _ in word_freq.most_common(VOCAB_SIZE)]
    word_to_index = {word: i for i, word in enumerate(top_words)}
    print(f"Словарь построен: {len(top_words)} слов")

    print(f"Превращаю каналы в вектора длины {VOCAB_SIZE}...")
    count = 0
    for filepath in glob.glob(f"{LOCAL_VECTORS_DIR}/part-*"):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ch_id, vec_str = line.split("\t", 1)
                    vec = np.zeros(VOCAB_SIZE, dtype=np.float32)
                    for term in vec_str.split():
                        if ':' not in term:
                            continue
                        word, val_str = term.rsplit(":", 1)
                        if word in word_to_index:
                            idx = word_to_index[word]
                            vec[idx] = float(val_str)
                    if np.any(vec):
                        norm = np.linalg.norm(vec)
                        if norm > 0:
                            vec = vec / norm
                        channel_vectors[ch_id] = vec
                        channel_norms[ch_id] = 1.0
                        count += 1
                except:
                    continue
    print(f"Готово! Загружено {count:,} каналов как вектора длины {VOCAB_SIZE}")

def search(query: str, top_n=20):
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]{2,}', query.lower())
    if not words:
        print("Нет слов в запросе")
        return

    qvec = np.zeros(VOCAB_SIZE, dtype=np.float32)
    for word in words:
        if word in word_to_index:
            qvec[word_to_index[word]] += 1.0

    if np.all(qvec == 0):
        print("Нет известных слов в запросе")
        return

    qvec = qvec / np.linalg.norm(qvec)

    scores = {}
    for ch_id, vec in channel_vectors.items():
        scores[ch_id] = np.dot(vec, qvec)

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_n]

    print(f"\nЗапрос: «{query}» → топ-{len(ranked)}\n")
    for i, (ch_id, score) in enumerate(ranked, 1):
        print(f"{i:2}. {score:.4f} → https://t.me/c/{ch_id}")

# === ГЛАВНЫЙ БЛОК ===
if __name__ == "__main__":
    print("Telegram-каналы поисковик — фиксированные вектора длины", VOCAB_SIZE)
    print("=" * 70)

    download_vectors_if_needed()
    build_vocabulary_and_load_vectors()

    print("\n" + "=" * 70)
    print(f"ГОТОВО! Загружено {len(channel_vectors):,} каналов")
    print(f"Все вектора имеют длину: {VOCAB_SIZE}")
    print("Вводи запросы — поиск мгновенный!")
    print("=" * 70)

    while True:
        try:
            q = input("\nЗапрос → ").strip()
            if not q:
                print("Пока!")
                break
            search(q)
        except KeyboardInterrupt:
            print("\nПока!")
            break