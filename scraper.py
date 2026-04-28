# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os


def fetch_wikipedia_content(url):
    print(f"正在尝试抓取: {url}")
    try:
        # 设置超时时间为 10 秒
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 50:
                paragraphs.append(text)
        return " ".join(paragraphs)
    except Exception as e:
        print(f"⚠️ 网络连接失败 ({e})。")
        return None


def scrape_and_save():
    if not os.path.exists('data'):
        os.makedirs('data')

    url = "https://en.wikipedia.org/wiki/Alan_Turing"
    content = fetch_wikipedia_content(url)

    # 【双保险机制】：如果维基百科连不上，自动使用内置的一大段高质量英文长文
    if not content:
        print("💡 启动离线备用大数据库，确保图谱节点丰富...")
        content = """Alan Mathison Turing was an English mathematician, computer scientist, logician, cryptanalyst, philosopher, and theoretical biologist. Turing was highly influential in the development of theoretical computer science, providing a formalisation of the concepts of algorithm and computation with the Turing machine, which can be considered a model of a general-purpose computer. He is widely considered to be the father of theoretical computer science and artificial intelligence.
        During the Second World War, Turing worked for the Government Code and Cypher School at Bletchley Park, Britain's codebreaking centre that produced Ultra intelligence. For a time he led Hut 8, the section that was responsible for German naval cryptanalysis. Here, he devised a number of techniques for speeding the breaking of German ciphers, including improvements to the pre-war Polish bombe method, an electromechanical machine that could find settings for the Enigma machine.
        Turing played a crucial role in cracking intercepted coded messages that enabled the Allies to defeat the Axis powers in many crucial engagements, including the Battle of the Atlantic.
        After the war, Turing worked at the National Physical Laboratory, where he designed the Automatic Computing Engine (ACE), one of the first designs for a stored-program computer. In 1948, Turing joined Max Newman's Computing Machine Laboratory, at the Victoria University of Manchester, where he helped develop the Manchester computers and became interested in mathematical biology. He wrote a paper on the chemical basis of morphogenesis and predicted oscillating chemical reactions such as the Belousov–Zhabotinsky reaction, first observed in the 1960s."""

    # 伪装成分段文档
    paragraphs = [p.strip() for p in content.split('\n') if len(p) > 20]
    docs = [{"title": f"Paragraph_{i}", "content": p} for i, p in enumerate(paragraphs)]

    with open('data/raw_docs.json', 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=4)
    print(f"✅ 成功保存 {len(docs)} 个文本块用于提取！")


if __name__ == "__main__":
    scrape_and_save()