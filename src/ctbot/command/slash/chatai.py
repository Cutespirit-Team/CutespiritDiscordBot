import openai
import os
import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def prompt(input_str):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = f"Human: {input_str} \n AI:",
        temperature = 0.9,
        max_tokens = 999,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0.6,
        stop = [" Human:", " AI:"]
    )
    res = response['choices'][0]['text']
    return res



class SlashChatai(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    @cog_slash_managed(description='OpenAI GPT-3')
    async def chatai(self, ctx, msg):
        await ctx.defer()
        await ctx.send(prompt(msg))
