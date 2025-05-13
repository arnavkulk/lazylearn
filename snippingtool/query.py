import os
from dotenv import load_dotenv
from openai import OpenAI
import io
import base64

# Load environment variables
load_dotenv()

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def send_openai_request(img):
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Convert image to base64
        base64_image = encode_image_to_base64(img)
        
        # Prepare the message for the API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Explain this image in detail"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Print the response
        print("\nOpenAI Response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error processing image with OpenAI: {str(e)}")
