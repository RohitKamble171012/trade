from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import time

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq LLM setup
llm = ChatGroq(
    temperature=0.9,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# Common colors HEX map
common_colors_hex = {
    "White": "#FFFFFF",
    "Black": "#000000",
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Orange": "#FFA500",
    "Purple": "#800080",
    "Pink": "#FFC0CB",
    "Gray": "#808080",
    "Light Gray": "#D3D3D3",
    "Dark Gray": "#A9A9A9",
    "Brown": "#A52A2A",
    "Cyan": "#00FFFF",
    "Magenta": "#FF00FF",
    "Navy": "#000080",
    "Olive": "#808000",
    "Maroon": "#800000",
    "Teal": "#008080",
    "Lime": "#BFFF00",
    "Indigo": "#4B0082",
    "Coral": "#FF7F50",
    "Turquoise": "#40E0D0",
    "Salmon": "#FA8072",
    "Gold": "#FFD700",
    "Beige": "#F5F5DC",
    "Mint": "#98FF98",
    "Lavender": "#E6E6FA",
    "Sky Blue": "#87CEEB",
    "Crimson": "#DC143C",
    "Slate Gray": "#708090",
    "Periwinkle": "#CCCCFF",
    "Sea Green": "#2E8B57",
    "Chartreuse": "#7FFF00",
    "Hot Pink": "#FF69B4",
    "Peach": "#FFE5B4",
    "Khaki": "#F0E68C",
    "Plum": "#DDA0DD",
    "Azure": "#F0FFFF",
    "Snow": "#FFFAFA",
    "Ivory": "#FFFFF0",
}

common_colors = list(common_colors_hex.keys())

template = """
You are a helpful assistant. From the following list of colors:

{color_list}

Randomly choose one color and return only the name of that color.
Return only the name of that color.
Do not return any other text or explanation.
"""

prompt = PromptTemplate.from_template(template)
runnable_chain = prompt | llm

def pick_color(color_list):
    response = runnable_chain.invoke({"color_list": color_list})
    return response.content.strip()

def get_hex(color_name):
    return common_colors_hex.get(color_name)

# For standalone test runs
def main():
    color_name = pick_color(common_colors)
    hex_value = get_hex(color_name)
    print(color_name)
    print(hex_value)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(4 * 60 * 60)  # Every 4 hours
