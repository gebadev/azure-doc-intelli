from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
from dotenv import load_dotenv

load_dotenv()

vision_endpoint = os.getenv("VISION_ENDPOINT")
vision_key = os.getenv("VISION_KEY")

vision_client = ComputerVisionClient(
    vision_endpoint, CognitiveServicesCredentials(vision_key)
)


def classify_image(file):
    with open(file, "rb") as image_stream:
        result = vision_client.analyze_image_in_stream(
            image_stream, visual_features=["Tags", "Description"]
        )

    tags = [t.name for t in result.tags]

    # ルールベース判定
    if any(t in tags for t in ["flowchart", "diagram", "process"]):
        return "flowchart"
    elif any(t in tags for t in ["database", "table", "schema"]):
        return "er"
    elif any(t in tags for t in ["screen", "interface", "ui"]):
        return "screenshot"
    else:
        return "unknown"


image_files = [
    "./output/images/image_1.png",
    "./output/images/image_2.png",
]
for file in image_files:
    label = classify_image(file)
    print(file, "=>", label)
