from PIL import Image
import io, base64

def compress_incoming_image_file(uploaded_file, quality=30):
  img = Image.open(uploaded_file)
  buf = io.BytesIO()
  img.save(buf, format="JPEG", quality=quality)
  buf.seek(0)

  return buf.read()

def image_to_base64(image_file):
  return base64.b64encode(image_file)