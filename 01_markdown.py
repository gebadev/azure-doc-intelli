from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)

# 解析対象ファイル
file_path = "./input/sample.pdf"

with open(file_path, "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",  # レイアウト解析用の定義済みモデル
        body=f,
        output_content_format="markdown",
    )

result = poller.result()
with open("./output/result.md", "w", encoding="utf-8") as wf:
    wf.write(result.content)
