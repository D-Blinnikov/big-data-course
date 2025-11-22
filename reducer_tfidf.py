#!/usr/bin/env python3
# reducer_tfidf.py — финальная рабочая версия с L2-нормализацией и env-настройками

import sys
import os
import math

test_data = [
"1337112293\tаааа\t0.000004",
"1337112293\tааааа\t0.000009",
"1337112293\tаамилопектин\t0.000004",
"1337112293\tаассивно\t0.000004",
"1337112293\tабакумов\t0.000004",
"1293336984\tаббревиатура\t0.000009",
"1337112293\tаббревиатура\t0.000014",
"1293336984\tаббревиатуру\t0.000005",
"1293336984\tаббревиатуры\t0.000009",
"1337112293\tаббревиатуры\t0.000007",
"1293336984\tабдулла\t0.000005",
"1337112293\tабзац\t0.000004",
"1293336984\tабонемент\t0.000022",
"1293336984\tабонементе\t0.000005",
"1293336984\tабонементом\t0.000005",
"1293336984\tабонентская\t0.000005",
"1337112293\tаборты\t0.000004",
"1337112293\tабразивы\t0.000009",
"1293336984\tабрамченко\t0.000033",
"1337112293\tабрау\t0.000004"
]

# === НАСТРОЙКИ ЧЕРЕЗ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===
# MAX_TERMS       = int(os.getenv("MAX_TERMS", "8000"))      # топ-N терминов в векторе
# MIN_TFIDF       = float(os.getenv("MIN_TFIDF", "-0.7"))    # отсечка слабых слов
# ENABLE_L2_NORM  = os.getenv("ENABLE_L2_NORM", "1") == "1"  # нормализация вектора (ОБЯЗАТЕЛЬНО!)
# # =================================================

# current_channel = None
# terms = {}

# def output_vector(channel_id: str, terms_dict: dict):
#     """Собирает, сортирует, фильтрует, нормализует и выводит TF-IDF вектор канала"""
#     if not terms_dict:
#         return

#     # Сортируем по убыванию TF-IDF
#     sorted_terms = sorted(terms_dict.items(), key=lambda x: -x[1])

#     # Берём только топ MAX_TERMS
#     top_terms = sorted_terms[:MAX_TERMS]

#     if ENABLE_L2_NORM:
#         # L2-нормализация: делаем вектор единичной длины
#         norm = math.sqrt(sum(v * v for _, v in top_terms))
#         if norm > 0:
#             items = [f"{word}:{value / norm:.6f}" for word, value in top_terms]
#         else:
#             items = [f"{word}:{value:.6f}" for word, value in top_terms]
#     else:
#         items = [f"{word}:{value:.6f}" for word, value in top_terms]

#     print(f"{channel_id}\t{' '.join(items)}")

# === Основной цикл ===
# # for line in sys.stdin:
# for line in test_data:
#     line = line.strip()
#     if not line:
#         continue

#     try:
#         channel_id, word, tfidf_str = line.split('\t')
#         tfidf = float(tfidf_str)

#         # Отсекаем шум по порогу
#         # if tfidf < MIN_TFIDF:
#             # continue

#         if current_channel != channel_id:
#             # Выводим предыдущий канал
#             if current_channel is not None:
#                 output_vector(current_channel, terms)

#             current_channel = channel_id
#             terms = {}

#         terms[word] = tfidf

#     except Exception as e:
#         # Молча пропускаем битые строки
#         continue

# # Не забываем последний канал
# if current_channel is not None:
#     output_vector(current_channel, terms)

# Настройки
# MAX_TERMS       = int(os.getenv("MAX_TERMS", "8000"))
# MIN_TFIDF       = float(os.getenv("MIN_TFIDF", "0.00"))   # поставь 0.07, а не 0.0!
# ENABLE_L2_NORM  = os.getenv("ENABLE_L2_NORM", "1") == "1"

# current_channel = None
# terms = {}

# def flush_channel():
#     if not terms or current_channel is None:
#         return

#     # Сортируем по убыванию TF-IDF (чтобы топ-термы были первыми)
#     sorted_terms = sorted(terms.items(), key=lambda x: -x[1])

#     # Применяем порог MIN_TFIDF (очень важно!)
#     filtered = [(w, v) for w, v in sorted_terms if v >= MIN_TFIDF]

#     # Берём только топ MAX_TERMS
#     top_terms = filtered[:MAX_TERMS]

#     if not top_terms:
#         return  # ничего не выводим, если после фильтрации пусто

#     if ENABLE_L2_NORM:
#         norm = math.sqrt(sum(v * v for _, v in top_terms))
#         if norm > 0:
#             items = [f"{w}:{v/norm:.6f}" for w, v in top_terms]
#         else:
#             items = [f"{w}:{v:.6f}" for w, v in top_terms]
#     else:
#         items = [f"{w}:{v:.6f}" for w, v in top_terms]

#     print(f"{current_channel}\t{' '.join(items)}")
#     # ← ВАЖНО: после вывода очищаем, чтобы не было дублирования!
#     terms.clear()

# # === Основной цикл ===
# # for line in sys.stdin:
# for line in test_data:
#     line = line.strip()
#     if not line:
#         continue

#     parts = line.split('\t')
#     if len(parts) != 3:
#         continue

#     channel_id, word, tfidf_str = parts
#     try:
#         tfidf = float(tfidf_str)
#     except:
#         continue

#     # ФИЛЬТР ОТРИЦАТЕЛЬНЫХ И СЛАБЫХ ВЕСОВ — ОБЯЗАТЕЛЬНО!
#     if tfidf < MIN_TFIDF:
#         continue

#     if current_channel != channel_id:
#         # Смена канала — выводим предыдущий и начинаем новый
#         if current_channel is not None:
#             flush_channel()
#         current_channel = channel_id
#         terms = {}   # ← полностью новый словарь!

#     terms[word] = tfidf

# # Не забываем последний канал
# if current_channel is not None:
#     flush_channel()



MAX_TERMS       = int(os.getenv("MAX_TERMS", "8000"))
MIN_TFIDF       = float(os.getenv("MIN_TFIDF", "0.00"))
ENABLE_L2_NORM  = os.getenv("ENABLE_L2_NORM", "1") == "1"

# Глобальный словарь: channel_id → список пар (word, tfidf)
vectors = {}

# for line in test_data:
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split('\t')
    if len(parts) != 3:
        continue

    channel_id, word, tfidf_str = parts
    try:
        tfidf = float(tfidf_str)
    except:
        continue

    if tfidf < MIN_TFIDF:
        continue

    # ← ТОЧНО КАК ТЫ СКАЗАЛ:
    if channel_id not in vectors:
        vectors[channel_id] = []
    vectors[channel_id].append((word, tfidf))

# === Выводим все каналы ===
for channel_id, term_list in vectors.items():
    # Сортируем по убыванию tfidf
    term_list.sort(key=lambda x: -x[1])
    top_terms = term_list[:MAX_TERMS]

    if ENABLE_L2_NORM:
        norm = math.sqrt(sum(v*v for _, v in top_terms))
        if norm > 0:
            items = [f"{w}:{v/norm:.6f}" for w, v in top_terms]
        else:
            items = [f"{w}:{v:.6f}" for w, v in top_terms]
    else:
        items = [f"{w}:{v:.6f}" for w, v in top_terms]

    print(f"{channel_id}\t{' '.join(items)}")