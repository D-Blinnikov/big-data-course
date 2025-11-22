# tg_search.py
# Запуск: python tg_search.py
# Автоматически скачивает вектора из Hadoop и даёт бесконечный поиск

import os
import glob
import re
import math
from collections import defaultdict, Counter
from dotenv import load_dotenv
from utils import run

load_dotenv()

NAME_NODE         = os.getenv("NAME_NODE", "hadoop-namenode-1")
TFIDF_FINAL       = os.getenv("TFIDF_FINAL", "/user/hadoop/tfidf_final")
LOCAL_VECTORS_DIR = "tg_vectors_cache"

vectors = {}
norms   = {}

def download_vectors_if_needed():
    os.makedirs(LOCAL_VECTORS_DIR, exist_ok=True)

    existing = glob.glob(f"{LOCAL_VECTORS_DIR}/part-*")
    if existing:
        print(f"Найдено {len(existing)} part-файлов в кэше")
        choice = input("Обновить вектора из Hadoop? (y/n, по умолчанию n): ").strip().lower()
        if choice != 'y':
            return
    else:
        print("Векторов нет в кэше → скачиваю из Hadoop...")

    print(f"Скачиваю свежие вектора из {TFIDF_FINAL} ...")

    # САМАЯ НАДЁЖНАЯ КОНСТРУКЦИЯ — используем bash -c и правильное экранирование
    copy_cmd = (
        "bash -c "
        "\"find " + TFIDF_FINAL + " -name 'part-*' -exec cp '{}' /tmp/ \\;\""
    )
    run(f"docker exec {NAME_NODE} {copy_cmd}")

    # Очищаем локальный кэш
    run(f"rm -rf {LOCAL_VECTORS_DIR}/*")

    # Копируем все part-файлы (шаблон раскрывается локально — работает на Windows!)
    run(f"docker cp {NAME_NODE}:/tmp/part-* {LOCAL_VECTORS_DIR}/")

    # Чистим временные файлы в контейнере
    run(f"docker exec {NAME_NODE} bash -c \"rm -f /tmp/part-*\"")

    new_files = glob.glob(f"{LOCAL_VECTORS_DIR}/part-*")
    if not new_files:
        print("ОШИБКА: файлы не скачались!")
        print("Проверь вручную:")
        run(f"docker exec {NAME_NODE} ls -l {TFIDF_FINAL}/")
        exit(1)

    print(f"Успешно скачано {len(new_files)} файлов")

def load_vectors():
    global vectors, norms
    vectors.clear()
    norms.clear()

    files = glob.glob(f"{LOCAL_VECTORS_DIR}/part-*")
    if not files:
        print("ОШИБКА: нет part-файлов в кэше!")
        print("Запусти полный пайплайн или принудительно обнови вектора (y при вопросе)")
        exit(1)

    print(f"Загружаю {len(files)} part-файлов в память...")
    count = 0
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ch_id, vec_str = line.split("\t", 1)
                    vec = {}
                    for term in vec_str.split():
                        if ':' not in term:
                            continue
                        word, val = term.rsplit(":", 1)
                        vec[word] = float(val)
                    vectors[ch_id] = vec
                    norm = math.sqrt(sum(v*v for v in vec.values())) or 1.0
                    norms[ch_id] = norm
                    count += 1
                except:
                    continue
    print(f"Готово! Загружено {count:,} каналов")

def search(query: str, top_n=20):
    words = re.findall(r'[а-яА-ЯёЁa-zA-Z]{2,}', query.lower())
    if not words:
        print("Нет подходящих слов в запросе")
        return

    qvec = Counter(words)
    qnorm = math.sqrt(sum(c*c for c in qvec.values())) or 1.0

    scores = defaultdict(float)
    for ch_id, vec in vectors.items():
        dot = sum(vec.get(w, 0.0) * cnt for w, cnt in qvec.items())
        scores[ch_id] = dot / (norms[ch_id] * qnorm)

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_n]

    print(f"\nЗапрос: «{query}» → топ-{len(ranked)}\n")
    for i, (ch_id, score) in enumerate(ranked, 1):
        print(f"{i:2}. {score:.4f} → https://t.me/c/{ch_id}")

if __name__ == "__main__":
    print("Telegram-каналы поисковик по TF-IDF")
    print("=" * 60)

    download_vectors_if_needed()
    load_vectors()

    print("\n" + "=" * 60)
    print("ГОТОВО! Вводи запросы (пустая строка = выход)")
    print("=" * 60)

    while True:
        try:
            q = input("\n➤ ").strip()
            if not q:
                print("Пока!")
                break
            search(q)
        except KeyboardInterrupt:
            print("\nПока!")
            break