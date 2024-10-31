import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from typing import Literal

load_dotenv()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.hybrid_command(description="Sync Commands! (Legacy Version)")
async def legacysync(ctx: commands.Context):
    await ctx.send("Syncing...", ephemeral=True)
    await bot.tree.sync()

@bot.hybrid_command(description="Sync Commands!")
@app_commands.describe(option  = "Choose How You Want to Sync")
async def sync(ctx: commands.Context, option: Literal['Global', 'Local']):
    await ctx.send(f"Syncing {option}ly...", ephemeral=True)
    if str == 'Global':
        await bot.tree.sync(guild=ctx.guild)
    else:
        await bot.tree.sync()

@bot.hybrid_command(description="Scrape any Website!")
@app_commands.describe(url  = "Enter the URL")
async def scrape(ctx: commands.Context, url: str):
    try:
        parsed_url = urlparse(url)
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            page_content = response.content
            soup = bs(page_content, 'html.parser')
            text = soup.get_text()

            filename = "scraped_text.txt"
            with open(filename, "w", encoding='utf-8') as file:
                file.write(text)

            await ctx.send(file=discord.File(filename))
        else:
            await ctx.send(f"Failed to retrieve webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"An error occurred: {e}")

@bot.event
async def on_ready():
    print("Web Scraper is Up and Ready!")

bot.run(os.getenv("TOKEN"))