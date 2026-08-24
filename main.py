import os
import discord
from discord import app_commands
from discord.ext import commands

# 🆔 ID เซิร์ฟเวอร์ของคุณ
GUILD_ID = 1529780061975089152

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

MY_GUILD = discord.Object(id=GUILD_ID)

@bot.event
async def on_ready():
    print(f'🐱 บอทแมวกลม ออนไลน์แล้ว! (ID: {bot.user.id})')
    try:
        bot.tree.copy_global_to(guild=MY_GUILD)
        synced = await bot.tree.sync(guild=MY_GUILD)
        print(f"✅ ซิงค์ {len(synced)} คำสั่งเข้าเซิร์ฟเวอร์เรียบร้อย!")
    except Exception as e:
        print(f"❌ ซิงค์คำสั่งไม่ผ่าน: {e}")

# -------------------- คำสั่ง Slash Commands --------------------

@bot.tree.command(name="เข้ามา", description="ให้น้องแมวกลมเข้าไป AFK ในห้องเสียง")
async def come_in(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("❌ เข้าห้องเสียงก่อนนะ!", ephemeral=True)
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

# -------------------- รันบอท --------------------
TOKEN = os.getenv('TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: ไม่พบ TOKEN ใน Environment Variables")

