import config
import discord
import urllib.request
import json
import time


client = discord.Client()


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
    with open('memeLink.json', 'r') as file:
            old_meme_link = json.load(file)
    new_meme_link = get_meme_link()
    if old_meme_link[0][-183:] != new_meme_link[-183:]:
        await channel.send(new_meme_link)
        old_meme_link[0] = new_meme_link
        with open('memeLink.json', 'w') as file:
            json.dump(old_meme_link, file, ensure_ascii=False, indent=4)
    time.sleep(config.timeout)


@client.event
async def on_ready():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(),
        name=config.channel_name)
    while True:
        await send_meme(channel)


client.run(config.app_token)