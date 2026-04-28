# main.py
import scraper
import extractor
import processor
import visualize
import os


def main():
    print("=== 🚀 开始构建【原始贪婪提取 + Pro交互渲染】图谱 ===")

    print("\n>>> 阶段 1: 数据采集 (带防断网离线保护) <<<")
    scraper.scrape_and_save()

    print("\n>>> 阶段 2: 知识抽取 (贪婪动词匹配) <<<")
    extractor.process()

    print("\n>>> 阶段 3: 语义处理 (温和清洗) <<<")
    processor.process_triples()

    print("\n>>> 阶段 4: 图谱渲染 (高级组件加载) <<<")
    visualize.generate_interactive_graph()

    print("\n" + "=" * 50)
    print("✅ 全部完成！请在左侧文件树双击打开 [turing_graph_ultimate.html]")
    print("=" * 50)


if __name__ == "__main__":
    main()