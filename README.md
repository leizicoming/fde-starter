# fde-starter

电子信息应届的 FDE 入门练习：先打通「读本地材料 → 调用大模型 → 写出可用结果」，再做成带依据的设备手册问答。

仓库分两部分：

- `first/`：把一段文本压成三句话总结
- `manual-qa/`：根据本地手册回答现场问题，格式为结论、手册原文、现场建议

## 环境

- Windows + Python 3.9+
- 建议使用仓库外或本地虚拟环境（`.venv` 已忽略，不上传）

```powershell
cd E:\NJAU\FDE
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install openai httpx