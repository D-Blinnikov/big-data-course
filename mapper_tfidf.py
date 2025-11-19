#!/usr/bin/env python3
# mapper_tfidf.py — финальная версия (без stderr-хака)

import sys
import math
import os

# Берём общее количество документов из переменной окружения
# Мы передадим её через -cmdenv TOTAL_DOCS=XXXXXX в run_step2
total_docs = int(os.getenv("TOTAL_DOCS", "1"))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        word, channel_id, tf_str, df_str = line.split('\t')
        tf = float(tf_str)
        df = int(df_str)

        # Сглаженный IDF: log(N / (df + 1))
        idf = math.log(total_docs / (df + 1))
        tfidf = tf * idf

        print(f"{channel_id}\t{word}\t{tfidf:.6f}")
    except Exception as e:
        continue  # молча пропускаем битые строки