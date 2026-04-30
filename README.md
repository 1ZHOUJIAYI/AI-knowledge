AI Knowledge Graph 

这是一个基于 Python 的端到端知识图谱自动化构建工具。本项目能够从非结构化的纯文本中自动提取实体关系（三元组），通过深度学习模型进行语义融合与清洗，并最终生成带有高级筛选、节点动态大小和物理引擎交互的网页版图谱。

本项目按数据流向分为核心代码与生成产物两部分：

核心代码模块 (Core Scripts)
main.py`：项目的总控入口。依次调度数据采集、知识抽取、语义清洗和可视化四大阶段，支持一键运行全流程。
`config.py`：全局配置文件。用于设置目标搜索主题、最大爬取篇数等核心参数
`scraper.py`：数据采集模块。负责抓取相关百科的长文本语料，内置了离线备用数据机制以应对网络连接不稳定。
`extractor.py`：知识抽取模块。依托 `spaCy` 的 NLP 句法树分析，通过“子树提取法”从复杂长句中贪婪匹配并抽取“主语-谓语-宾语”三元组。
`processor.py`：语义清洗模块。引入 `sentence-transformers` 模型，通过计算余弦相似度自动识别并合并指代一致的实体节点，剔除冗余关系。
`visualize.py`：图谱渲染模块。基于 `pyvis`，将清洗后的关系表转化为带有下拉点选、侧边栏筛选、节点权重动态缩放的 HTML 交互页面。

数据与产物 (Data & Outputs)
`raw_docs.json`：数据源头。存放爬虫抓取或本地加载的原始分段长文本。
`raw_triples.json`：初步提取产物。存放 NLP 模型暴力提取出的海量、未经清洗的原始实体关系字典。
`refined_triples.csv`：深度清洗产物。经过大模型语义融合、去重后得到的高质量核心关系表，是最终图谱的底层数据支撑。
`turing_graph_ultimate.html`：最终展示成品。纯前端交互式知识图谱，双击即可在任意浏览器中打开体验。


 安装环境依赖
请确保本地已安装 Python 3.9+，并在终端运行以下命令安装所需的基础库：
```bash
pip install spacy pandas pyvis sentence-transformers beautifulsoup4 requests
