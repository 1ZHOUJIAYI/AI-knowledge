import spacy
import json
import os
from tqdm import tqdm

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("❌ 找不到英文模型！请在终端运行: python -m spacy download en_core_web_sm")
    exit()


def extract_relationships(text):
    doc = nlp(text)
    relationships = []

    for sent in doc.sents:
        subject = ""
        relation = ""
        obj = ""

        for token in sent:
            # 寻找核心谓语动词
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                relation = token.lemma_  # 使用动词原形

                # 狂野提取法：抓取主语的整棵语法树（保留所有从句和修饰语）
                for left in token.lefts:
                    if left.dep_ in ["nsubj", "nsubjpass"]:
                        subject = "".join([w.text + " " for w in left.subtree]).strip()

                # 狂野提取法：抓取宾语的整棵语法树
                for right in token.rights:
                    if right.dep_ in ["attr", "dobj", "pobj", "ccomp"]:
                        obj = "".join([w.text + " " for w in right.subtree]).strip()

        if subject and relation and obj:
            relationships.append({
                "subject": subject,
                "predicate": relation,
                "object": obj
            })

    return relationships


def process():
    input_file = 'data/raw_docs.json'
    if not os.path.exists(input_file):
        print("❌ 找不到原始数据文件 data/raw_docs.json")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        docs = json.load(f)

    all_results = []
    for doc in tqdm(docs, desc="全量语法树抽取中"):
        triples = extract_relationships(doc['content'])
        for t in triples:
            t['source'] = doc['title']
            all_results.append(t)

    with open('data/raw_triples.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4)
    print(f"✅ 提取完成，爆发式获取了 {len(all_results)} 条关系！")


if __name__ == "__main__":
    process()