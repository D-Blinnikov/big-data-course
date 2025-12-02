import sys
from sys import stdin
from collections import defaultdict

test_data  = [
  "быть   1337112293   0.14285714285714285\t1",
  "быть\t1337112294\t0.14285714285714285\t1",
  "быть\t1337112295\t0.14285714285714285\t1",
  "детей\t1293336984\t0.14285714285714285\t1",
  "заботиться\t1293336984\t0.14285714285714285\t1",
  "каналу\t1337112293\t0.14285714285714285\t1",
  "пищевой\t1337112293\t0.14285714285714285\t1",
  "приучить\t1293336984\t0.14285714285714285\t1",
  "способов\t1293336984\t0.14285714285714285\t1",
  "телеграм\t1337112293\t0.14285714285714285\t1",
  "технолог\t1337112293\t0.14285714285714285\t1",
  "фанатизма\t1293336984\t0.14285714285714285\t1",
  "химик\t1293336984\t0.14285714285714285\t1",
  "химик\t1337112293\t0.14285714285714285\t1",
  "вами\t1337112293\t0.14285714285714285\t1",
  "экологии\t1293336984\t0.14285714285714285\t1"
]




current_word = None
channel_tfs = {}
total_docs = 0
doc_set = set()



for line in stdin:
# for line in test_data:
    line = line.strip()
    if not line:
        continue
    try:
        word, channel_id, tf_str, one = line.split('\t')
        tf = float(tf_str)
        if current_word != word:
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