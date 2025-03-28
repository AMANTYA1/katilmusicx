import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()


    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
(190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
 f"Added By: {requested_by}",
 (255, 255, 255),
 font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")



@Client.on_message(
    command(["play"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer

    lel = await message.reply("🔎 **𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ✌︎✌︎★..**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "@tera_baap_katil"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝐀𝐝 𝐌𝐞 😎 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 💫  𝐅𝐢𝐫𝐬𝐭✌︎✌︎★</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** 🎶 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐉𝐨𝐢𝐧𝐞𝐝 😎 🤟 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩  𝐅𝐨𝐫 𝐏𝐥𝐚𝐲 ▶ 𝐌𝐮𝐬𝐢𝐜 🎸**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>❰𝐅𝐥𝐨𝐨𝐝 😒 𝐖𝐚𝐢𝐭 𝐄𝐫𝐫𝐨𝐫  😔❱</b>\n𝐇𝐞𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 🎸 𝐔𝐬𝐞𝐫𝐁𝐨𝐭 ❤️ 𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐉𝐨𝐢𝐧 𝐘𝐨𝐮𝐫 💫 𝐆𝐫𝐨𝐮𝐩  𝐃𝐮𝐞 𝐓𝐨 𝐇𝐞𝐚𝐯𝐲 𝐉𝐨𝐢𝐧 𝐑𝐞𝐐𝐮𝐞𝐬𝐭 🥀 . 𝐌𝐚𝐤𝐞 𝐒𝐮𝐫𝐞 𝐔𝐬𝐞𝐫𝐁𝐨𝐭 💫 𝐈𝐬 𝐍𝐨𝐭 𝐁𝐚𝐧𝐧𝐞𝐝 😔 𝐈𝐧 𝐆𝐫𝐨𝐮𝐩 🎸  𝐀𝐧𝐝 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧 𝐋𝐚𝐭𝐞𝐫 𝐀𝐧𝐲 𝐇𝐞𝐥𝐩 𝐃𝐦 :- ✨ [༒︎★•亗『Broken』亗•★ ](https://t.me/iam_your_heart4) ❤️🥀 :)")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>Hey {user.first_name}, 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 🎸 𝐔𝐬𝐞𝐫𝐁𝐨𝐭 𝐈𝐬 𝐍𝐨𝐭 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭' 𝐀𝐬𝐤 𝐀𝐝𝐦𝐢𝐧 😎 𝐓𝐨 𝐒𝐞𝐧𝐝 /Play 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 😎 𝐅𝐨𝐫 𝐅𝐢𝐫𝐬𝐭 𝐓𝐢𝐦𝐞 𝐓𝐨 𝐀𝐝𝐝 𝐈𝐭 𝐀𝐧𝐲 𝐇𝐞𝐥𝐩 𝐃𝐦 :- ✨ [༒︎★•亗『Broken』亗•★ ](https://t.me/iam_your_heart4) ❤️🥀 </i>")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❰ ° 𝐒𝐨𝐧𝐠 🎸 ° ❱ 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞'𝐒 𝐀𝐫𝐞𝐧'𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️🥀❌"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/13fba0e9d76c406ae9ce2.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                
               [
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/heartbrokenp3erson1"),
                            
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/FULL_MAS3TI_CLUBS")
               ],
               
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                
               [
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/HEARTBROKEN3PERSON1"),
                            
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/FULL_MAST3I_CLUBS")
               ],
               
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/153087782510223747be6.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                
               [
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/HEARTBROKE3NPERSON1"),
                            
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/FULL_MAST3I_CLUBS")
               ],
               
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❰ ° 𝐒𝐨𝐧𝐠 🎸 ° ❱ 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞'𝐒 𝐀𝐫𝐞𝐧'𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️🥀❌"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "✌𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️"
            )
        await lel.edit("**Processing 🔄 Please Wait !!**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "🌸° 𝐒𝐨𝐧𝐠 🎸 𝐍𝐨𝐭 😒 𝐅𝐨𝐮𝐧𝐝 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 ° 🥀."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                
               [
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/HEARTBROK3ENPERSON1"),
                            
                    InlineKeyboardButton(
                            text="",
                            url=f"https://t.me/FULL_MAST3I_CLUBS")
               ],
               
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❰ ° 𝐒𝐨𝐧𝐠 🎸 ° ❱ 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞'𝐒 𝐀𝐫𝐞𝐧'𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️🥀❌"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**» ⏩ 𝐓𝐑𝐀𝐂𝐊 𝐐𝐔𝐄𝐔𝐄𝐃 𝐀𝐓 {position} **\n➡️ **𝐓𝐈𝐓𝐋𝐄​:** [{title[:65]}]({url})\n🕕 **𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍:** `{duration}` 𝐌𝐈𝐍𝐔𝐓𝐄s\n🥀 **𝐑𝐄𝐐𝐔𝐄𝐒𝐓𝐄𝐃 𝐁𝐘​:** {message.from_user.mention}\n❤️ **𝐏𝐋𝐀𝐘𝐈𝐍𝐆 𝐈𝐍​:** `{message.chat.title}`\n🎥 **𝐒𝐓𝐑𝐄𝐀𝐌 𝐓𝐘𝐏𝐄:** 𝐘𝐎𝐔𝐓𝐔𝐁𝐄 𝐌𝐔𝐒𝐈𝐂\n❰ ★𝐓𝐌𝐂♪♪𝐌𝐔𝐒𝐈𝐂'𝐗✌︎✌︎★ ❱ Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀...\n𝗕𝘆 : @iam_your_heart4".format(position),
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**»▶️ 𝐍𝐎𝐖 𝐏𝐋𝐀𝐘𝐈𝐍𝐆 «**\n➡️ **𝐓𝐈𝐓𝐋𝐄​:** [{title[:65]}]({url})\n🕕 **𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍:** `{duration}` 𝐌𝐈𝐍𝐔𝐓𝐄s\n🥀 **𝐑𝐄𝐐𝐔𝐄𝐒𝐓𝐄𝐃 𝐁𝐘​:** {message.from_user.mention}\n❤️ **𝐏𝐋𝐀𝐘𝐈𝐍𝐆 𝐈𝐍​:** `{message.chat.title}`\n🎥 **𝐒𝐓𝐑𝐄𝐀𝐌 𝐓𝐘𝐏𝐄:** 𝐘𝐎𝐔𝐓𝐔𝐁𝐄 𝐌𝐔𝐒𝐈𝐂\n **Now 😄 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 📀...\n **𝗕𝘆 : BROKEN MR Z".format(
        message.chat.title
        ), )

    os.remove("final.png")
    return await lel.delete()
    
