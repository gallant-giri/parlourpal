import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- Your Project Details ---
project_id = "image-gen-demo-epsilon"
location = "us-central1"

# Initialize Vertex AI for your project
vertexai.init(project=project_id, location=location)

# Load the Imagen model
# model = ImageGenerationModel.from_pretrained("imagegeneration@006")
# model = ImageGenerationModel.from_pretrained("gemini-2.0-flash-preview-image-generation")
model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")



# --- Define what you want to create ---
prompt_text = """Create a luxurious, festive Deepwali-themed poster for "Diamond Beauty Parlour". Feature a glamorous Indian woman with radiant, glowing skin, flawless festive makeup, and intricately styled traditional hair. She should be dressed in an elegant saree or lehenga in rich festive colors (deep red, pink, or gold), adorned with subtle diamond jewelry to reflect the brand name.

Surround her with sparkling diyas (oil lamps), rangoli patterns, soft bokeh lights, and elegant beauty elements like lipstick, makeup brushes, compact mirror, and floral decor. Use rich and warm lighting, creating a glow-from-within ambiance with luxurious tones—gold, magenta, rose-pink, and crimson.

Integrate this promotional text in a stylish, artistic font:
"💎 Diamond Beauty Parlour – This Deepwali, Glow Like Never Before! 💇‍♀️💅💖✨ 50% OFF on All Services!"

Below that, in clean, smaller font:
🕒 11:00 AM – 8:00 PM | 📞 +91 123456789

At the bottom, clearly show the location:
📍 Sector 35, Navanagar, Bagalkot

Design should feel festive, elegant, and professional—perfectly formatted for use as a WhatsApp status, Instagram/Facebook story or post, with soft shadows, modern layout, and diamond-inspired accents subtly integrated throughout."""


print(f"Generating image for prompt: '{prompt_text}'...")

# Generate the image using the model's default safety settings
images = model.generate_images(
    prompt=prompt_text,
    number_of_images=1,
)

# --- THIS IS THE CRUCIAL CHECK ---
# It prevents the crash.
if images:
    # If the list is NOT empty, save the first image
    image_filename = "parlor5.png"
    images[0].save(location=image_filename)
    print(f"Success! 🖼️  You can now see the image '{image_filename}' in your folder.")
else:
    # If the list IS empty, print a helpful error message instead of crashing
    print("⚠️ No image was generated. The model's safety filter likely blocked the prompt for your project.")
    print("Try a simpler prompt like 'A colorful bird in a garden'.")