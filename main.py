import os
from groq import Groq
import base64
import cv2


os.environ['GROQ_API_KEY'] = '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'


def main ():
    # Load image
    image = cv2.imread('./form-1.png')  # Provide the correct image path

    # Step 1: Convert to Grayscale (reduces complexity)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Thresholding (to make text more distinct)
    _, threshold_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

    # Step 3: Noise Removal (GaussianBlur)
    blurred_image = cv2.GaussianBlur(threshold_image, (5, 5), 0)

    # Step 4: Resize (optional - adjust based on the image's content)
    resized_image = cv2.resize(blurred_image, (1200, 800))

    # Step 5: Save or continue to the next step (base64 encoding)
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Save the processed image (optional to check the result)
    cv2.imwrite("processed_image.png", resized_image)

    # Now encode the processed image to Base64
    _, buffer = cv2.imencode('.png', resized_image)
    base64_image = base64.b64encode(buffer).decode('utf-8')

    # The base64_image is now ready to be sent to the Groq API
    # print(base64_image)  # You can now send this Base64 string in your API request

    client = Groq()

    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",  # Use the correct model ID
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract field name & its respective value pairs from the form and return in JSON format."},
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


    return completion.choices[0].message.content


if __name__ == "__main__":
    print(main())

