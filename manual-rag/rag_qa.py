import os
from pathlib import Path

import httpx
from openai import OpenAI

api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("没有读到 API Key")

http_client = httpx.Client(trust_env=False, timeout=60.0)
client = OpenAI(
    api_key=api_key,
    base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
    http_client=http_client,
)

here = Path(__file__).resolve().parent
manual_dir = here.parent / "tractor-manuals"
question_path = here / "question.txt"

if not manual_dir.exists():
    raise SystemExit("缺少 manuals 文件夹")
if not question_path.exists():
    raise SystemExit("缺少 question.txt")

question = question_path.read_text(encoding="utf-8").strip()
if not question:
    raise SystemExit("question.txt 为空")

docs = []
for p in sorted(manual_dir.glob("*.txt")):
    text = p.read_text(encoding="utf-8").strip()
    if text:
        docs.append((p.name, text))

if not docs:
    raise SystemExit("manuals 里没有文本")

def score(question_text, doc_text):
    q = set(question_text.lower())
    d = set(doc_text.lower())
    # 中文按字重叠 + 几个关键词加权
    overlap = len(q & d)
    keywords = ["振动", "峰值", "CH1", "CH2", "越障", "圈数", "感应", "速度", "故障"]
    bonus = sum(4 for k in keywords if k in question_text and k in doc_text)
    return overlap + bonus

ranked = sorted(docs, key=lambda item: score(question, item[1]), reverse=True)
top = ranked[:2]

print("检索到的手册段落：")
for name, text in top:
    print(f"- {name}: {text[:40]}...")

context = "\n\n".join(f"[{name}]\n{text}" for name, text in top)

resp = client.chat.completions.create(
    model=os.environ.get("LLM_MODEL", "deepseek-chat"),
    messages=[
        {
            "role": "system",
            "content": (
                "你是设备现场助手。只能根据检索到的手册段落回答。\n"
                "格式：\n"
                "1) 结论\n"
                "2) 依据：抄检索段落原句，并写出来自哪个文件\n"
                "3) 现场建议：只能写段落能推出的检查；推不出写「手册未记载」\n"
                "禁止使用检索结果之外的知识。"
            ),
        },
        {
            "role": "user",
            "content": f"检索结果：\n{context}\n\n问题：\n{question}",
        },
    ],
)

answer = resp.choices[0].message.content.strip()
print("\n回答：\n")
print(answer)

out = here / "answer.txt"
out.write_text(answer + "\n", encoding="utf-8")
print("\n已写入", out)