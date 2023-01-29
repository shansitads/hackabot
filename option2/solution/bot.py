import config
import discord
from responses import handle_response


async def send_message(message, user_message, is_private):
    try:
        response = handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    # api keys in config.py (not committed)
    TOKEN = config.token_id

    # bot permissions (set on https://discord.com/developers/applications)
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # when bot is online
    @client.event
    async def on_ready():
        print(f'{client.user} is ready')

    # when message is set in chat
    @client.event
    async def on_message(message):
        # bot shouldn't respond to itself
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        print(user_message)
        channel = str(message.channel)

        print(f'{username} said: {user_message} [{channel}]')

        # messages starting with '~' will start private chat with bot
        if user_message[0] == '~':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)