from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.reply import get_main_menu_keyboard

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("✨ Welcome to the Shop! Choose an option from below:", reply_markup=get_main_menu_keyboard())

@router.message(F.text == "Fluorite Keys")
async def handle_fluorite(message: Message):
    await message.answer("🔹 **Fluorite Keys**\n\n7 day key | 900 INR\n1 month key | 1500 INR")

@router.message(F.text == "Android Keys")
async def handle_android_keys(message: Message):
    await message.answer("🔹 **Android Keys**\n\n7 day key | 600 INR\n1 month key | 1000 INR\nFull season key | 2000 INR")

@router.message(F.text == "Full iOS Panel")
async def handle_full_ios(message: Message):
    await message.answer("🔹 **Full iOS Panel**\n\nFull iOS Panel | 3000 INR")

@router.message(F.text == "Full Android Panel")
async def handle_full_android(message: Message):
    await message.answer("🔹 **Full Android Panel**\n\nFull Android Panel | 2000 INR")

@router.message(F.text == "GBox")
async def handle_gbox(message: Message):
    await message.answer("🔹 **GBox**\n\nGBox 6 month | 1000 INR\nGBox 1 Year | 1500 INR")

@router.message(F.text == "Esign")
async def handle_esign(message: Message):
    await message.answer("🔹 **Esign**\n\nEsign 1 year certificate | 800 INR")

@router.message(F.text == "Monite Key")
async def handle_monite(message: Message):
    await message.answer("🔹 **Monite Key**\n\n7 day key | 600 INR\n31 days key | 1000 INR")

@router.message(F.text == "Migul iOS Panel")
async def handle_migul(message: Message):
    await message.answer("🔹 **Migul iOS Panel**\n\nMigul Full iOS panel | 1500 INR")

@router.message(F.text == "Support")
async def handle_support(message: Message):
    await message.answer("👨‍💻 **Support**\n\nFor any queries or issues, contact: @vitor_fault")

@router.message(F.text == "Profile")
async def handle_profile(message: Message):
    await message.answer(f"👤 **Your Profile**\n\nName: {message.from_user.full_name}\nID: {message.from_user.id}\nCurrency: INR")
