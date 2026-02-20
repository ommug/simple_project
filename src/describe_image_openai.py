"""
Using the openAI's image upload feature, the class will describe the imaga and return the description
"""

import openai
import os

class DescribeImageOpenAI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



    def image_raw_path_to_http_url(self, image_path: str) -> str:

        """
        [(https://storage.googleapis.com/amt-creator-media-cache/instagram/posts/post-pics/3580899939209067616.jpg)
        """
        if image_path.startswith("gs://"):
            return image_path.replace("gs://", "https://storage.googleapis.com/")
        elif image_path.startswith("gc://"):
            return image_path.replace("gc://", "https://storage.googleapis.com/")

    def describe_image(self, image_path: str) -> str:
        """
        Convert the image path to HTTP URL and use OpenAI's vision model to describe it.
        Returns a detailed description of the image.
        """
        # Convert the image path (e.g., gs://...) to an HTTP URL
        image_url = self.image_raw_path_to_http_url(image_path)
        
        # Create a comprehensive prompt for describing the image
        prompt = """Please provide a detailed and comprehensive description of this image. 
        Include information about:
        - The main subjects, objects, or people visible in the image
        - The setting, environment, or background
        - Colors, lighting, and overall mood or atmosphere
        - Any text, symbols, or notable details
        - The composition and visual style
        - Any actions or activities taking place
        
        Be specific and descriptive, as if describing the image to someone who cannot see it."""
        
        # Use Chat Completions API with vision capabilities
        # Use the public HTTP URL directly for the vision API
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        description = response.choices[0].message.content
        return description

    
