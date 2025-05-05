import openai
import base64
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read the image
image_path = "C:/Users/Hazel/Documents/projectpractice/fridge.jpg"
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

# Analyze the image
vision_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a photo of a fridge. List the food items you can identify."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=300
)

# Extract the response
fridge_items = vision_response.choices[0].message.content
print("\n🧊 Detected items in fridge:\n")
print(fridge_items)

# Suggest recipes based on those items
recipe_prompt = f"Based on these items in my fridge: {fridge_items.strip()} — what can I cook?"

recipe_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a cooking assistant that suggests recipes from fridge items."},
        {"role": "user", "content": recipe_prompt}
    ],
    max_tokens=400
)

recipe_text = recipe_response.choices[0].message.content
print("\n🍳 Recipe suggestions:\n")
print(recipe_text)

# Try to extract the first recipe title (simplified)
first_line = recipe_text.strip().split('\n')[0]
recipe_name = first_line.strip("•-1234567890. ").strip()

# Generate an image of the recipe
print("\n🖼️ Generating image for:", recipe_name)

image_response = client.images.generate(
    model="dall-e-3",
    prompt=f"A top-down photo of {recipe_name} on a white plate, realistic, natural lighting",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = image_response.data[0].url
print("\n📷 Recipe image URL:\n")
print(image_url)

# Optional: Chat
print("\n💬 Ask your fridge assistant something (or press Enter to skip):")
user_input = input("> ")

if user_input.strip():
    chat_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a fridge and cooking assistant. Respond clearly and helpfully."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=400
    )

    print("\n🤖 GPT says:\n")
    print(chat_response.choices[0].message.content)
else:
    print("Chat skipped.")
