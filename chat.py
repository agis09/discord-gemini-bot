import google.generativeai as genai
import os
import discord
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv(override=True)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.0-pro-vision-latest")

chat = None


def init_chat():
    global chat
    chat = model.start_chat()
    response = chat.send_message(
        content="You are a excellent chat bot. Please chat me in Japanese!"
    )


@client.event
async def on_ready():
    # init_chat()
    print(f"{client.user.name} is online!")


@client.event
async def on_message(message):
    print(f"Message received from {message.author}")
    if message.author == client.user or not (str(client.user.id) in message.content):
        return

    content = message.content.strip()
    content = content.replace(f"<@{str(client.user.id)}> ", "")
    print(f"content: {content}")
    attachments = message.attachments

    if content == "reflesh":
        init_chat()
        await message.reply("refleshed chat !!!!")

    elif attachments:
        print(attachments)
        img_url = attachments[0].url
        res = requests.get(img_url)
        img = Image.open(BytesIO(res.content))
        response = model.generate_content([img, content])

        await message.reply(response.text)

    else:
        # response = chat.send_message(content=[img, content])
        print(response.text)
        await message.reply(response.text)


def download_image(url, timeout=10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if "image" not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content


client.run(os.environ["DISCORD_API_TOKEN"])
