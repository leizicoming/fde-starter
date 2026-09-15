import os
import httpx
from openai import OpenAI

api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("没有读到 API Key。请先设置 $env:DEEPSEEK_API_KEY")

http_client = httpx.Client(trust_env=False, timeout=60.0)

client = OpenAI(
    api_key=api_key,
    base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
    http_client=http_client,
)

here = os.path.dirname(os.path.abspath(__file__))
manual_path = os.path.join(here, "manual.txt")
question_path = os.path.join(here, "question.txt")

if not os.path.exists(manual_path):
    raise SystemExit("缺少 manual.txt")
if not os.path.exists(question_path):
    raise SystemExit("缺少 question.txt")

with open(manual_path, "r", encoding="utf-8") as f:
    manual = f.read().strip()
with open(question_path, "r", encoding="utf-8") as f:
    question = f.read().strip()

if not manual or not question:
    raise SystemExit("manual.txt 或 question.txt 是空的")

resp = client.chat.completions.create(
    model=os.environ.get("LLM_MODEL", "deepseek-chat"),
    messages=[
        {
            "role": "system",
            "content": (
                "你是设备现场助手。必须只根据手册回答。\n"
"格式严格如下：\n"
"1) 结论：一句话\n"
"2) 依据：原文抄手册里相关的一句或几句\n"
"3) 现场建议：只写手册能推出的检查项；推不出就写「手册未记载」\n"
"禁止编造手册里没有的部件或数值。"
            ),
        },
        {
            "role": "user",
            "content": f"手册：\n{manual}\n\n问题：\n{question}",
        },
    ],
)

answer = resp.choices[0].message.content.strip()
print("\n回答：\n")
print(answer)

out_path = os.path.join(here, "answer.txt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(answer + "\n")
print("\n已写入", out_path)