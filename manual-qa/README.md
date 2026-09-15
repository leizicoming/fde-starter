# 设备手册问答（FDE 入门练习）

电子信息应届练习项目：把本地试验规程和现场问题交给大模型，生成「结论 + 手册原文 + 现场建议」，并写入文件。

## 场景

试验台操作时出现「越障没有振动峰值」。  
目标不是闲聊，而是根据手册给出可执行的检查顺序，手册没有的内容不编造。

## 文件

- `manual.txt`：本地手册（短文本即可）
- `question.txt`：现场问题
- `qa.py`：读取上述文件，调用大模型，写出 `answer.txt`
- `answer.txt`：生成结果

## 环境

- Python 3.9+
- 依赖：`openai`、`httpx`（在上级目录虚拟环境 `E:\NJAU\FDE\.venv` 中已安装）

## 运行

PowerShell：

```powershell
cd E:\NJAU\FDE
.\.venv\Scripts\Activate.ps1
cd manual-qa

$env:DEEPSEEK_API_KEY="你的key"
$env:LLM_BASE_URL="https://api.siliconflow.cn/v1"
$env:LLM_MODEL="Qwen/Qwen2.5-7B-Instruct"

python qa.py