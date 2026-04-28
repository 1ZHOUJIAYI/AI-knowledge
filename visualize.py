# visualize.py
import pandas as pd
from pyvis.network import Network
import os

def generate_interactive_graph():
    input_file = 'data/refined_triples.csv'
    if not os.path.exists(input_file):
        print("❌ 找不到数据文件！")
        return

    df = pd.read_csv(input_file)

    # 🚀 开启高级交互菜单
    net = Network(
        height="850px",
        width="100%",
        bgcolor="#111111",
        font_color="white",
        directed=True,
        select_menu=True,  # 下拉选择节点
        filter_menu=True   # 多维边栏筛选
    )

    # 设置物理引擎让图谱舒展
    net.force_atlas_2based(
        gravity=-80,
        central_gravity=0.01,
        spring_length=200,
        spring_strength=0.05,
        damping=0.4
    )

    # 计算节点的度（用于调整大小）
    node_weights = {}
    for _, row in df.iterrows():
        s, o = str(row['subject']), str(row['object'])
        node_weights[s] = node_weights.get(s, 0) + 1
        node_weights[o] = node_weights.get(o, 0) + 1

    for _, row in df.iterrows():
        subj, obj, pred = str(row['subject']), str(row['object']), str(row['predicate'])

        # 图灵相关节点标为青色，其他为橙色
        subj_color = "#00f2ff" if "Turing" in subj or "Alan" in subj else "#ff6600"
        obj_color = "#00f2ff" if "Turing" in obj or "Alan" in obj else "#ffbb00"

        net.add_node(
            subj, label=subj,
            title=f"Entity: {subj} | Links: {node_weights.get(subj)}",
            size=15 + node_weights.get(subj, 1) * 3, color=subj_color
        )
        net.add_node(
            obj, label=obj,
            title=f"Entity: {obj} | Links: {node_weights.get(obj)}",
            size=15 + node_weights.get(obj, 1) * 3, color=obj_color
        )
        net.add_edge(subj, obj, label=pred, title=f"Relation: {pred}", color="#555555")

    output_path = "turing_graph_ultimate.html"
    net.save_graph(output_path)
    print(f"🎉 终极版图谱生成成功！请打开: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_interactive_graph()