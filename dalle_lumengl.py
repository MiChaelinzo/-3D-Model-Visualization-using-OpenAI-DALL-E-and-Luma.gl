import requests
from PIL import Image
from io import BytesIO
from luma.gl import gl, GLFWApp

# Set the OpenAI API endpoint and your API key
API_ENDPOINT = "https://api.openai.com/v1/images/generations"
API_KEY = "YOUR_API_KEY"

# Set the text prompt and model parameters
prompt = "3D model of a red cube on a green plane"
model = "image-alpha-001"
size = "512x512"

# Send the API request to generate the image
response = requests.post(
    API_ENDPOINT,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    },
    json={
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": size,
        "response_format": "url",
    },
)

# Check if the request was successful
if response.status_code == 200:
    # Get the URL of the generated image from the response
    image_url = response.json()["data"][0]["url"]

    # Download and display the image using Pillow
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image.show()

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
else:
    # Display the error message if the request failed
    print(f"Error: {response.text}")


