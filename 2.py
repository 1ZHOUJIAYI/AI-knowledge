import os
import jieba
import jieba.analyse
import json

# ==========================================
# 1. 路径设置与文件读取
# ==========================================
file_path = r"D:\AI知识工程\新建 文本文档.txt"
output_json_path = r"D:\AI知识工程\知识标注结果.json"

print(f"正在读取文件: {file_path}")

try:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="gbk") as f:
            content = f.read()
    print(f"✅ 读取成功，文本长度: {len(content)}")
except Exception as e:
    print(f"❌ 读取失败: {e}")
    exit()

# ==========================================
# 2. 关键词提取 (Mention Extraction)
# ==========================================
print("--- [步骤 2: 提取提及词候选] ---")
# 提取前 30 个核心关键词作为 Mention 候选
keywords = jieba.analyse.extract_tags(content, topK=30)

# ==========================================
# 3. 实体消歧映射 (Entity Disambiguation)
# ==========================================
print("--- [步骤 3: 实体消歧与对齐] ---")
# 这里定义消歧字典：将文本中的各种写法对齐到标准库标签
disambiguation_kb = {
    "图灵": "艾伦·图灵",
    "艾伦": "艾伦·图灵",
    "人工智能": "人工智能",
    "AI": "人工智能",
    "恩尼格玛": "恩尼格玛密码机",
    "计算机": "通用计算机"
}

# ==========================================
# 4. 位置计算与结果提炼
# ==========================================
print("--- [步骤 4: 计算位置并构建结果] ---")
results = []

# 使用 jieba.tokenize 得到词语及其在文本中的起止位置 (start, end)
# mode='search' 会进行更细粒度的切分，适合提取位置
tokens = jieba.tokenize(content)

for tk in tokens:
    word = tk[0]
    start = tk[1]
    end = tk[2]

    # 检查当前切分出的词是否在我们提取的关键词名单中
    if word in keywords:
        # 进行消歧：如果在字典里就映射，否则保留原词作为标签
        standard_label = disambiguation_kb.get(word, word)

        # 构建 JSON 条目
        item = {
            "mention": word,  # 文本中的原始写法
            "label": standard_label,  # 消歧后的标准标签
            "start": start,  # 开始索引
            "end": end  # 结束索引
        }
        results.append(item)

# ==========================================
# 5. 导出为 JSON 文件
# ==========================================
print("--- [步骤 5: 导出 JSON 数据] ---")
try:
    with open(output_json_path, 'w', encoding='utf-8') as jf:
        # ensure_ascii=False 保证中文不被编码成 \uXXXX
        # indent=4 让输出的 JSON 文件具有缩进，方便阅读
        json.dump(results, jf, ensure_ascii=False, indent=4)
    print(f"🎉 导出成功！\n👉 文件路径: {output_json_path}")
    print(f"💡 共计标注了 {len(results)} 个实体位置信息。")
except Exception as e:
    print(f"❌ 导出 JSON 失败: {e}")