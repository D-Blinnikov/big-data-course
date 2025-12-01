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


MAX_TERMS       = int(os.getenv("MAX_TERMS", "8000"))
MIN_TFIDF       = float(os.getenv("MIN_TFIDF", "0.00"))
ENABLE_L2_NORM  = os.getenv("ENABLE_L2_NORM", "0") == "0"

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

    if channel_id not in vectors:
        vectors[channel_id] = []
    vectors[channel_id].append((word, tfidf))

for channel_id, term_list in vectors.items():
    term_list.sort(key=lambda x: -x[1])
    top_terms = term_list[:MAX_TERMS]

    if ENABLE_L2_NORM:
        norm = math.sqrt(sum(v*v for _, v in top_terms))
        if norm > 0:
            items = [f"{w}:{v/norm:.20f}" for w, v in top_terms]
        else:
            items = [f"{w}:{v:.20f}" for w, v in top_terms]
    else:
        items = [f"{w}:{v:.6f}" for w, v in top_terms]

    print(f"{channel_id}\t{' '.join(items)}")