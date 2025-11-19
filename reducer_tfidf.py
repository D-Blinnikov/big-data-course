#!/usr/bin/env python3
# reducer_tfidf.py — финальная рабочая версия с L2-нормализацией и env-настройками

import sys
import os
import math

# === НАСТРОЙКИ ЧЕРЕЗ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===
MAX_TERMS       = int(os.getenv("MAX_TERMS", "8000"))      # топ-N терминов в векторе
MIN_TFIDF       = float(os.getenv("MIN_TFIDF", "0.07"))    # отсечка слабых слов
ENABLE_L2_NORM  = os.getenv("ENABLE_L2_NORM", "1") == "1"  # нормализация вектора (ОБЯЗАТЕЛЬНО!)
# =================================================

current_channel = None
terms = {}

def output_vector(channel_id: str, terms_dict: dict):
    """Собирает, сортирует, фильтрует, нормализует и выводит TF-IDF вектор канала"""
    if not terms_dict:
        return

    # Сортируем по убыванию TF-IDF
    sorted_terms = sorted(terms_dict.items(), key=lambda x: -x[1])

    # Берём только топ MAX_TERMS
    top_terms = sorted_terms[:MAX_TERMS]

    if ENABLE_L2_NORM:
        # L2-нормализация: делаем вектор единичной длины
        norm = math.sqrt(sum(v * v for _, v in top_terms))
        if norm > 0:
            items = [f"{word}:{value / norm:.6f}" for word, value in top_terms]
        else:
            items = [f"{word}:{value:.6f}" for word, value in top_terms]
    else:
        items = [f"{word}:{value:.6f}" for word, value in top_terms]

    print(f"{channel_id}\t{' '.join(items)}")

# === Основной цикл ===
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        channel_id, word, tfidf_str = line.split('\t')
        tfidf = float(tfidf_str)

        # Отсекаем шум по порогу
        if tfidf < MIN_TFIDF:
            continue

        if current_channel != channel_id:
            # Выводим предыдущий канал
            if current_channel is not None:
                output_vector(current_channel, terms)

            current_channel = channel_id
            terms = {}

        terms[word] = tfidf

    except Exception as e:
        # Молча пропускаем битые строки
        continue

# Не забываем последний канал
if current_channel is not None:
    output_vector(current_channel, terms)