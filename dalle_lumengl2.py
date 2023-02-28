import requests
from PIL import Image
from io import BytesIO
from luma.gl import gl, GLFWApp

# Set up the API endpoint
url = "https://api.openai.com/v1/images/generations"

# Prompt the user for input
prompt = input("Enter a prompt: ")

# Set up the request headers and body
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY" # Replace with your actual API key
}

data = {
    "model": "image-alpha-001", # Use the DALL-E 2 model
    "prompt": prompt,
    "num_images": 1, # Generate one image
    "size": "512x512", # Set the image size
    "response_format": "url" # Request the image URL in the response
}

# Send the API request and retrieve the response
response = requests.post(url, headers=headers, json=data).json()

# Extract the URL of the generated image from the response
image_url = response["data"][0]["url"]

# Download the image from the URL
image_data = requests.get(image_url).content

# Convert the image data to a PIL Image object
image = Image.open(BytesIO(image_data))

# Initialize the GLFWApp and set up the 3D visualization
app = GLFWApp()

with app:
    # Create a texture from the PIL Image
    texture = gl.Texture.from_image(image)
    
    # Set up the 3D model and render it
    with gl.MatrixStack.projection(45, app.aspect, 0.1, 1000):
        with gl.MatrixStack.modelview():
            gl.glTranslatef(0, 0, -10)
            gl.glRotatef(app.time * 50, 0, 1, 0)
            gl.glRotatef(app.time * 30, 1, 0, 0)
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture.id)
            gl.glBegin(gl.GL_QUADS)
            gl.glTexCoord2f(0, 0)
            gl.glVertex3f(-1, -1, 0)
            gl.glTexCoord2f(1, 0)
            gl.glVertex3f(1, -1, 0)
            gl.glTexCoord2f(1, 1)
            gl.glVertex3f(1, 1, 0)
            gl.glTexCoord2f(0, 1)
            gl.glVertex3f(-1, 1, 0)
            gl.glEnd()

    # Run the GLFWApp main loop
    app.run()
