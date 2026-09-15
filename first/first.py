import os
import httpx
from openai import OpenAI

api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("没有读到 API Key。请先设置 $env:DEEPSEEK_API_KEY")

# 不使用系统代理，避免校园网 SSL 被掐断
http_client = httpx.Client(trust_env=False, timeout=60.0)

client = OpenAI(
    api_key=api_key,
    base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
    http_client=http_client,
)

here = os.path.dirname(os.path.abspath(__file__))
in_path = os.path.join(here, "input.txt")

if not os.path.exists(in_path):
    raise SystemExit("请先在同目录创建 input.txt，把要总结的文字贴进去。")

with open(in_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    raise SystemExit("input.txt 是空的。")

resp = client.chat.completions.create(
    model=os.environ.get("LLM_MODEL", "deepseek-chat"),
    messages=[
        {
            "role": "system",
            "content": "把用户输入压缩成恰好三句话的中文总结，不要编号，不要额外解释。",
        },
        {"role": "user", "content": text},
    ],
)

summary = resp.choices[0].message.content.strip()
print("\n三句话总结：\n")
print(summary)

out_path = os.path.join(here, "summary_output.txt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(summary + "\n")
print("\n已写入", out_path)