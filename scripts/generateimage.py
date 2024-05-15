from PIL import Image
import base64
import io

# Create a large image (e.g., 8000x8000 pixels)
img = Image.new('RGB', (38000, 38000), color = (73, 109, 137))

# Save to a bytes buffer
buffer = io.BytesIO()
img.save(buffer, format="PNG")
byte_data = buffer.getvalue()

# Base64 encode
encoded_string = base64.b64encode(byte_data).decode('utf-8')

# Create data URI
data_uri = 'data:image/png;base64,' + encoded_string
print(data_uri)