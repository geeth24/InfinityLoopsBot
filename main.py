import discord
import os
from discord.ext import commands
import io
import aiohttp
import requests
from bs4 import BeautifulSoup
import random

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")


@bot.command()
async def loop(ctx, arg):
    if arg == "":
        url = "https://www.looperman.com/loops"
    else:
        url = "https://www.looperman.com/loops?keys=" + arg

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    loop_urls = []

    for d in soup.find_all('div', {'rel': True}):
        loop_urls.append(d['rel'])

    if loop_urls:
        rand_loop_url = random.choice(loop_urls)
        print(rand_loop_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(rand_loop_url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                url_spilt = rand_loop_url.split('/')[-1]
                if url_spilt.split('.')[-1] == "mp3":
                    await ctx.send(file=discord.File(data, url_spilt.split('.')[-2] + ".mp3"))
                elif url_spilt.split('.')[-1] == "wav":
                    await ctx.send(file=discord.File(data, url_spilt.split('.')[-2] + ".wav"))

    else:
        await ctx.send("No loops found. Please try a different argument")


bot.run(os.getenv('TOKEN'))
