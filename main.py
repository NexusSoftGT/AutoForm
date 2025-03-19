import os
from groq import Groq
import base64

os.environ['GROQ_API_KEY'] = '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'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "./form-1.png"

base64_image = encode_image(image_path)

client = Groq()

completion = client.chat.completions.create(
    model="llama-3.2-90b-vision-preview",  # Use the correct model ID
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract key-value pairs from the form and return in JSON format."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",  # Base64 encoded image
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)


print(completion.choices[0].message.content)
