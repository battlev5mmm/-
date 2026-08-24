import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

# 🔑 ใส่ ID ของคุณ (Discord User ID) เพื่อใช้คำสั่ง /sync
OWNER_ID = 123456789012345678  # <--- เปลี่ยนเป็นเลข ID ของคุณ

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CAT_SOUNDS = [
    "https://www.myinstants.com/media/sounds/meow_1.mp3",
    "https://www.myinstants.com/media/sounds/cat-meow-sound-effect_1.mp3",
    "https://www.myinstants.com/media/sounds/meow-sound-effect.mp3"
]

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

@bot.event
async def on_ready():
    # ไม่มีการ sync อัตโนมัติอีกต่อไป
    print(f'🐱 บอทแมวกลม พร้อมใช้งานแล้ว! (ID: {bot.user.id})')

# -------------------- คำสั่ง --------------------

@bot.tree.command(name="เข้ามา", description="ให้น้องแมวกลมเข้าไป AFK ในห้องเสียง")
async def come_in(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("❌ เข้าห้องเสียงก่อนนะมนุษย์!", ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild__id=interaction.guild.id)

    if voice_client:
        await voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect(self_deaf=True)
    
    await interaction.response.send_message("🐾 เมี้ยว~ น้องแมวกลมมานั่ง AFK แล้ว!")

@bot.tree.command(name="ออก", description="ให้น้องแมวกลมออกจากห้องเสียง")
async def go_out(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild__id=interaction.guild.id)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await interaction.response.send_message("👋 บายๆ เมี้ยว!")
    else:
        await interaction.response.send_message("❌ น้องไม่ได้อยู่ในห้องเสียงนะ", ephemeral=True)

@bot.tree.command(name="เสียงแมว", description="สุ่มเปิดเสียงแมวจากคลัง 1 ครั้ง")
async def cat_sound(interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild__id=interaction.guild.id)
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("❌ ดึงน้องแมวเข้าห้องเสียงก่อนสั่งร้องนะ!", ephemeral=True)
        return

    selected_sound = random.choice(CAT_SOUNDS)

    try:
        if voice_client.is_playing():
            voice_client.stop()
        source = discord.FFmpegPCMAudio(selected_sound, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await interaction.response.send_message("🐈 Meow~ (ส่งเสียงแมว 1 ครั้ง)")
    except Exception as e:
        await interaction.response.send_message(f"❌ เล่นเสียงไม่ได้: {e}", ephemeral=True)

# -------------------- คำสั่งซิงค์ (เฉพาะเจ้าของ) --------------------
@bot.tree.command(name="sync", description="ซิงค์ Slash Command (เฉพาะเจ้าของ)")
async def sync_commands(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ เฉพาะเจ้าของบอทเท่านั้นที่ใช้ได้", ephemeral=True)
        return
    await bot.tree.sync()
    await interaction.response.send_message("✅ ซิงค์คำสั่งเรียบร้อย!", ephemeral=True)

# -------------------- รันบอท --------------------
TOKEN = os.getenv('TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: ไม่พบ TOKEN ใน Environment Variables")
