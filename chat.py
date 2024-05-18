import google.generativeai as genai
import os
import discord
from dotenv import load_dotenv

load_dotenv(override=True)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-latest")

chat = None


def init_chat():
    global chat
    chat = model.start_chat()
    response = chat.send_message(
        # content="You are an excellent software engineer. Please think logically and answer my questions STEP BY STEP with evidence. If you are unclear about a question or need additional information, please ask. Please think in English and answer in Japanese.",
        content="You are a excellent chat bot. Please chat me in Japanese!"
    )


@client.event
async def on_ready():
    init_chat()
    print(f"{client.user.name} is online!")


@client.event
async def on_message(message):
    print(f"Message received from {message.author}: {message.content}")
    if message.author == client.user or not (str(client.user.id) in message.content):
        return

    content = message.content.strip()
    content = content.replace(f"<@{str(client.user.id)}> ", "")
    print(f"content: {content}")

    if content == "reflesh":
        init_chat()
        await message.reply("refleshed chat !!!!")

    else:
        response = chat.send_message(content=content)
        await message.reply(response.text)


client.run(os.environ["DISCORD_API_TOKEN"])
