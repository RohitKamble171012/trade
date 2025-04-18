import hashlib
import time
from server import blockchain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

# Initialize Groq
llm = ChatGroq(
    temperature=0.9,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

template = """
You are a helpful assistant. From the following list of colors:

{color_list}

Randomly choose one color and return only the name of that color.
Return only the name of that color.
Do not return any other text or explanation.
"""

prompt = PromptTemplate(template=template)
runnable_chain = prompt | llm

common_colors_hex = {
    "White": "#FFFFFF", "Black": "#000000", "Red": "#FF0000", "Green": "#00FF00",
    "Blue": "#0000FF", "Yellow": "#FFFF00", "Orange": "#FFA500", "Purple": "#800080",
    "Pink": "#FFC0CB", "Gray": "#808080", "Light Gray": "#D3D3D3", "Dark Gray": "#A9A9A9",
    "Brown": "#A52A2A", "Cyan": "#00FFFF", "Magenta": "#FF00FF", "Navy": "#000080",
    "Olive": "#808000", "Maroon": "#800000", "Teal": "#008080", "Lime": "#BFFF00",
    "Indigo": "#4B0082", "Coral": "#FF7F50", "Turquoise": "#40E0D0", "Salmon": "#FA8072",
    "Gold": "#FFD700", "Beige": "#F5F5DC", "Mint": "#98FF98", "Lavender": "#E6E6FA",
    "Sky Blue": "#87CEEB", "Crimson": "#DC143C", "Slate Gray": "#708090",
    "Periwinkle": "#CCCCFF", "Sea Green": "#2E8B57", "Chartreuse": "#7FFF00",
    "Hot Pink": "#FF69B4", "Peach": "#FFE5B4", "Khaki": "#F0E68C", "Plum": "#DDA0DD",
    "Azure": "#F0FFFF", "Snow": "#FFFAFA", "Ivory": "#FFFFF0"
}

common_colors = list(common_colors_hex.keys())

def pick_ai_color():
    response = runnable_chain.invoke({"color_list": common_colors})
    return response.content.strip()

def get_hex(color_name):
    return common_colors_hex.get(color_name)

def hex_from_hash(hash_str):
    return f"#{hash_str[:6]}"

def generate_new_color(previous_hex):
    hash_object = hashlib.sha256(previous_hex.encode())
    new_hash = hash_object.hexdigest()
    return hex_from_hash(new_hash)

def run_color_loop(start_color_hex, duration_seconds=4 * 60 * 60, interval_seconds=180):
    start_time = time.time()
    current_hex = start_color_hex

    while time.time() - start_time < duration_seconds:
        blockchain.add_block({"color": current_hex})
        print(f"Added block with color: {current_hex}")
        current_hex = generate_new_color(current_hex)
        time.sleep(interval_seconds)

def main_loop():
    while True:
        base_color_name = pick_ai_color()
        base_color_hex = get_hex(base_color_name)

        print(f"\n🌈 New 4-Hour Cycle Started with AI Color: {base_color_name} ({base_color_hex})\n")
        run_color_loop(base_color_hex)

if __name__ == "__main__":
    main_loop()
