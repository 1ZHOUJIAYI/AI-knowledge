import json
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
print("加载语义大模型中...")
model = SentenceTransformer('all-MiniLM-L6-v2')


def process_triples():
    with open('data/raw_triples.json', 'r', encoding='utf-8') as f:
        raw_triples = json.load(f)

    all_entities = list(set([t['subject'] for t in raw_triples] + [t['object'] for t in raw_triples]))
    if not all_entities: return

    embeddings = model.encode(all_entities, convert_to_tensor=True)
    entity_map = {}
    processed = set()

    for i in range(len(all_entities)):
        if i in processed: continue
        cosine_scores = util.cos_sim(embeddings[i], embeddings)[0]
        # 保持 0.85 的黄金融合比例
        similar_indices = torch.where(cosine_scores > 0.85)[0].tolist()
        canonical = all_entities[i]
        for idx in similar_indices:
            entity_map[all_entities[idx]] = canonical
            processed.add(idx)

    processed_triples = []
    for t in raw_triples:
        new_t = {
            "subject": entity_map.get(t['subject'], t['subject']),
            "predicate": t['predicate'].lower(),
            "object": entity_map.get(t['object'], t['object'])
        }
        # 核心修正：取消长度限制，只要主宾语不完全一样就保留！
        if new_t['subject'] != new_t['object'] and len(new_t['subject']) > 1 and len(new_t['object']) > 1:
            processed_triples.append(new_t)

    df = pd.DataFrame(processed_triples)
    df.to_csv('data/refined_triples.csv', index=False)
    print(f"✅ 清洗完成，最终保留 {len(df)} 条长句关系！")


if __name__ == "__main__":
    process_triples()