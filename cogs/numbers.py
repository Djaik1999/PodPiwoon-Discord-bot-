import requests
import discord
from discord.ext import commands
from typing import Optional
import re


class Numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cog loaded')

    @commands.command()
    async def facts(self, ctx, number='1', type: Optional[str] = 'trivia'):
        # Types - trivia, date, math, year
        if type == 'date':
            if not re.match(r'^\d{2}/\d{2}$', number):
                await ctx.channel.send(f"Строка для type='date', должна иметь вид месяц/день (пример: 09/11 - 11 сентября)")
            else:
                response = requests.get(f"http://numbersapi.com/{number}/{type}")
                embed = discord.Embed(description=response.text)
                await ctx.channel.send(embed=embed)
        elif not number.isnumeric():
            await ctx.channel.send(f"number - должен быть числом")

        response = requests.get(f"http://numbersapi.com/{number}/{type}")
        embed = discord.Embed(description=response.text)
        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Numbers(bot))