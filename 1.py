import os
import jieba
import jieba.analyse
import networkx as nx
import csv  # 新增：用于导出 CSV 文件

# ==========================================
# 1. 读取本地文本文件
# ==========================================
file_path = r"D:\AI知识工程\新建 文本文档.txt"
# 新增：定义输出文件的路径 (和你的文本文档在同一个文件夹下)
output_csv_path = r"D:\AI知识工程\知识图谱三元组_导出结果.csv"

print(f"正在尝试读取文件: {file_path}")

try:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="gbk") as f:
            content = f.read()

    print(f"✅ 成功读取文件，共 {len(content)} 个字符。\n")
except FileNotFoundError:
    print(f"❌ 找不到文件，请确认路径是否正确: {file_path}")
    exit()

if len(content.strip()) == 0:
    print("❌ 提取失败：文本内容为空，请确保文本文档里有文字并已保存！")
    exit()

# ==========================================
# 2. 关键词提取
# ==========================================
print("--- [步骤 2: 关键词提取] ---")
keywords = jieba.analyse.extract_tags(content, topK=20)
print(f"提取出的核心关键词: {keywords}\n")

# ==========================================
# 3. 实体消歧与对齐
# ==========================================
print("--- [步骤 3: 实体消歧] ---")
knowledge_base_mapping = {
    "图灵": "艾伦·图灵",
    "艾伦": "艾伦·图灵",
    "人工智能": "人工智能",
    "AI": "人工智能"
}

standard_entities = set()
for kw in keywords:
    if kw in knowledge_base_mapping:
        standard_entities.add(knowledge_base_mapping[kw])
    else:
        standard_entities.add(kw)

print(f"处理后的标准实体池: {list(standard_entities)[:10]} ...\n")

# ==========================================
# 4. 关系抽取
# ==========================================
print("--- [步骤 4: 关系抽取] ---")
extracted_triples = []
sentences = content.replace("\n", "。").replace("！", "。").replace("？", "。").split("。")

for sentence in sentences:
    if not sentence.strip():
        continue

    if "包括" in sentence or "包含" in sentence or "有" in sentence:
        for entity in standard_entities:
            if entity in sentence and len(entity) > 1:
                extracted_triples.append((entity, "涉及", "相关概念"))

    if "用于" in sentence or "提出" in sentence or "发明" in sentence or "是" in sentence:
        for entity in standard_entities:
            if entity in sentence and len(entity) > 1:
                extracted_triples.append((entity, "关联", "某项事物"))

extracted_triples = list(set(extracted_triples))

for t in extracted_triples[:10]:
    print(f"提炼三元组: [{t[0]}] --({t[1]})--> [{t[2]}]")

print(f"共提炼出 {len(extracted_triples)} 个关系。\n")

# ==========================================
# 5. 构建图谱
# ==========================================
print("--- [步骤 5: 知识图谱落库] ---")
kg = nx.DiGraph()
for subject, relation, obj in extracted_triples:
    kg.add_edge(subject, obj, label=relation)
print("✅ 图谱网络在内存中构建完成！\n")

# ==========================================
# 6. 导出结果到文件 (新增步骤)
# ==========================================
print("--- [步骤 6: 导出数据] ---")
if len(extracted_triples) > 0:
    # 使用 utf-8-sig 编码，确保用 Excel 打开时中文不会乱码
    with open(output_csv_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["主体 (Subject)", "关系 (Relation)", "客体 (Object)"])
        # 批量写入数据
        writer.writerows(extracted_triples)
    print(f"🎉 成功！所有三元组数据已导出至文件：\n   👉 {output_csv_path}")
else:
    print("⚠️ 没有提取到任何三元组，因此未生成导出文件。请尝试修改步骤4中的匹配规则。")