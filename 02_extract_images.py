import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
output_dir = "./output/images"
os.makedirs(output_dir, exist_ok=True)

client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))

with open("./input/sample.pdf", "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=f,
        output=["figures"],
    )
    result = poller.result()

operation_id = poller.details["operation_id"]
image_files = []

for idx, figure in enumerate(result.figures or []):
    figure_bytes = b"".join(
        client.get_analyze_result_figure(
            model_id=result.model_id,
            result_id=operation_id,
            figure_id=figure.id,
        )
    )
    filename = f"{output_dir}/image_{idx+1}.png"
    with open(filename, "wb") as img:
        img.write(figure_bytes)
    image_files.append(filename)

print("Extracted images:", image_files)
