import os
from groq import Groq
import base64
import cv2
import json  # Import json for parsing the response


os.environ['GROQ_API_KEY'] = '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'


def main():
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
                    {"type": "text", 
                     "text": """
                        Please extract the following fields from the insurance claim form image. Ensure that the values are returned in the exact format specified below.

                        Fields to extract:
                        1. Policy No. (Alphanumeric characters, max length 30)
                        2. SL No./Certificate No. (Digits only, 10-15 characters)
                        3. Company/TPA ID No. (Alphanumeric, 10-15 characters)
                        4. Name (Full name, first name and last name)
                        5. Address (Complete address, with street and city)
                        6. City (City name, full form, no abbreviations)

                        The output should follow this **exact JSON** format, with **double quotes** and no extra spaces:
                        {
                            "Policy No.": "IJKLEFGHIJKL1234567890ABXZ",
                            "SL No./Certificate No.": "12345321342",
                            "Company/TPA ID No.": "eweZGK4321",
                            "Name": "Sohaib Shamsi",
                            "Address": "1209 35th Cross Block Jayanagar",
                            "City": "Karachi"
                        }
                         
                        If a field is missing or unreadable, return an empty string for that field. 
                        Do not include any extra characters like single quotes or extra spaces.
                    """},
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

    # Extracting the fields and structuring them in the desired format
    extracted_data = completion.choices[0].message.content
    
    # Try parsing the extracted data as JSON
    try:
        data = json.loads(extracted_data)  # Attempt to parse the string as JSON
    except json.JSONDecodeError:
        print("Error parsing response as JSON:", extracted_data)  # Print error and raw response
        data = {}

    formatted_data = format_extracted_data(data)
    
    return formatted_data


def format_extracted_data(data):
    # Map the extracted data into the required format
    formatted_json = {
        "Policy No.": data.get("Policy No.", ""),
        "SL No./Certificate No.": data.get("SL No./Certificate No.", ""),
        "Company/TPA ID No.": data.get("Company/TPA ID No.", ""),
        "Name": data.get("Name", ""),
        "Address": data.get("Address", ""),
        "City": data.get("City", "")
    }
    
    return formatted_json


if __name__ == "__main__":
    print(main())
