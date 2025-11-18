import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")


def gen_mermaid(image_path, diagram_type):

    client = AzureOpenAI(
        api_key=OPENAI_KEY,
        azure_endpoint=OPENAI_ENDPOINT,
        api_version=OPENAI_API_VERSION,
    )

    with open(image_path, "rb") as imgf:
        img_b64 = base64.b64encode(imgf.read()).decode("utf-8")

    prompt = f"""
あなたはソフトウェア設計の専門家です。
画像を解析し、推定される図をMermaid形式に変換してください。

図の種別: {diagram_type}

ルール:
- 図に存在する要素のみ記述すること
- 不明な要素は省略し、推測しないこと
- mermaidコードのみ出力し、余計な説明は不要
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    image_files_and_types = [
        ("./output/images/image_1.png", "flowchart"),
        ("./output/images/image_2.png", "flowchart"),
    ]

    for image_path, diagram_type in image_files_and_types:
        mermaid_code = gen_mermaid(image_path, diagram_type)
        print(f"Generated Mermaid for {image_path}:\n{mermaid_code}\n")

        with open(f"{image_path}_diagram.mmd", "w", encoding="utf-8") as f:
            f.write(mermaid_code)
