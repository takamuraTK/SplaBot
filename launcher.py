from discord.ext import commands
import requests
import json

from requests.api import get
import config
import discord

endpoint = config.ENDPOINT
bot = commands.Bot(command_prefix="!sp ")


def get_now_info(rule_type):
    """
    rule_type:
    - regular
    - gachi
    - league
    """
    url = f"{endpoint}/{rule_type}/now"
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    result = response_dict["result"]
    return result


def get_parse_content(rule, maps_list):
    maps = '・'.join(maps_list)
    content = f"ルール：{rule}\nステージ：{maps}"
    return content


@bot.event
async def on_ready():
    print("on ready")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command()
async def now(ctx):
    result_regular = get_now_info("regular")
    result_gachi = get_now_info("gachi")
    result_league = get_now_info("league")

    embed = discord.Embed()
    embed.color = discord.Color.purple()
    embed.title = "現在のステージ情報はこちらです"
    # Regular
    regular_content = get_parse_content(
        result_regular[0]["rule"], result_regular[0]["maps"])
    embed.add_field(name="レギュラーマッチ", value=regular_content, inline=False)
    # Gachi
    gachi_content = get_parse_content(
        result_gachi[0]["rule"], result_gachi[0]["maps"])
    embed.add_field(name="ガチマッチ", value=gachi_content, inline=False)
    # League
    league_content = get_parse_content(
        result_league[0]["rule"], result_league[0]["maps"])
    embed.add_field(name="リーグマッチ", value=league_content, inline=False)
    await ctx.send(embed=embed)


bot.run(config.TOKEN)
