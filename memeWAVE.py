import config
import discord
import urllib.request
import json
import time


client = discord.Client()
old_meme_link = 'http://example.com'


def get_meme_link():
    url = (
        "https://api.vk.com/method/wall.get?domain="
        + config.vk_group
        + "&count=1&offset=1&access_token="
        + config.vk_token
        + "&v=5.126"
    )
    contents = urllib.request.urlopen(url).read()
    json_contents = json.loads(contents)["response"]["items"][0]["attachments"][0]["photo"]["sizes"]
    return json_contents[len(json_contents) - 1]["url"]


async def send_meme(channel):
    global old_meme_link
    new_meme_link = get_meme_link()
    if old_meme_link != new_meme_link:
        await channel.send(new_meme_link)
        old_meme_link = new_meme_link
    time.sleep(config.timeout)


@client.event
async def on_ready():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(),
        name=config.channel_name)
    while True:
        await send_meme(channel)


client.run(config.app_token)