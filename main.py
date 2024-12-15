from pyrogram import Client, filters, idle
from utils import config
from utils.helpers import create_connection
from pyrogram.types import Message

# DataBase Config
try:
    with create_connection() as database:
        with database.cursor(dictionary=True) as con:
            # Text List
            con.execute('SELECT * FROM pv_text')
            allResult = con.fetchall()
            for res in allResult:
                config.LIST_PV_TEXT.append(str(res['content']))

            con.execute('SELECT * FROM group_text')
            allResult = con.fetchall()
            for res in allResult:
                config.LIST_GROUP_TEXT.append(str(res['content']))

            con.execute('SELECT * FROM tags')
            allResult = con.fetchall()
            for res in allResult:
                config.LIST_TAGS.append(str(res['content']))

            con.execute('SELECT * FROM requests')
            allResult = con.fetchall()
            for res in allResult:
                config.LIST_REQUEST.append(str(res['content']))

except Exception as error:
    print(f'SQL Error: {error}')
    exit()

# App Config
app = Client(config.API_NAME, api_id=config.API_ID, api_hash=config.API_HASH)


# ADMIN
@app.on_message(filters.text & filters.incoming & filters.private & filters.user([config.ADMIN_ID]) & filters.regex('(?i)^راهنمات$'))
async def admin_handler(client: Client, message: Message):
    await client.send_message(config.ADMIN_ID, 'salam')


# GROUP
@app.on_message(filters.text & filters.incoming & filters.group)
async def group_handler(client: Client, message: Message):
    chat_id = message.chat.id
    username = message.chat.username
    msg_id = message.id
    msg = message.text
    id_from_user = message.from_user.id
    username_from_user = message.from_user.username
    for req in config.LIST_REQUEST:
        if req in msg:
            for tag in config.LIST_TAGS:
                if tag in msg:
                    text = (f'GROUP REQUEST\n'
                            f'GROUP: {username}\n'
                            f'Massage: {msg}\n\n'
                            f'From (id): {id_from_user}\n'
                            f'From: {username_from_user}')
                    await client.send_message(config.ADMIN_ID, text)
                    return

# CHANNEL
@app.on_message(filters.text & filters.channel)
async def channel_handler(client: Client, message: Message):
    chat_id = message.chat.id
    username = message.chat.username
    msg_id = message.id
    msg = message.text
    username_from_user = message.from_user.username
    for req in config.LIST_REQUEST:
        if req in msg:
            for tag in config.LIST_TAGS:
                if tag in msg:
                    text = (f'CHANNEL REQUEST\n'
                            f'Massage: {msg}\n\n'
                            f'From (id): {chat_id}\n'
                            f'From: {username}')
                    await client.send_message(config.ADMIN_ID, text)
                    return


# App Start
app.start(), print("Manager Running ..."), app.send_message(config.ADMIN_ID, "ربات روشن شد :)"), idle(), app.stop()
