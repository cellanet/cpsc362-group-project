import discord
from messages import reply_message

async def send_message(message, user_message, is_private):
    try:
        response = reply_message(user_message)

        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    token = 'MTA4MTQ0NjY4NTc2NDQ5MzM0Mg.GhWQTK.IGuLfnuzc7TdHb1GEL0kHclZnK3QPVtZ8D00fs'
    client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' {channel}")

        if user_message[0] == '!':
            user_message = user_message[1]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(token)
