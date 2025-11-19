#!/usr/bin/env python3
# reducer_df.py
import sys
from sys import stdin
from collections import defaultdict

current_word = None
channel_tfs = {}
total_docs = 0
doc_set = set()

for line in stdin:
    line = line.strip()
    if not line:
        continue
    try:
        word, channel_id, tf_str, one = line.split('\t')
        tf = float(tf_str)
        if current_word != word:
            # выводим предыдущее слово
            if current_word:
                df = len(channel_tfs)
                for ch_id, ch_tf in channel_tfs.items():
                    print(f"{current_word}\t{ch_id}\t{ch_tf}\t{df}")
                channel_tfs.clear()
            current_word = word
        channel_tfs[channel_id] = tf
        doc_set.add(channel_id)
    except:
        continue

# последнее слово
if current_word:
    df = len(channel_tfs)
    for ch_id, ch_tf in channel_tfs.items():
        print(f"{current_word}\t{ch_id}\t{ch_tf}\t{df}")

total_docs = len(doc_set)
print(f"_stats_\ttotal_docs\t{total_docs}\t1", file=sys.stderr)