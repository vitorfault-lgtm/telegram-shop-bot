from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from bot.states.shop import ShopStates
import os

router = Router()

ADMIN_ID = 6516079642 

# --- Coupon Logic Add Kiya Hai ---
def get_discounted_price(coupon, original_price):
    coupons = {
        "VFG100OFF": 100,
        "VITOR500G": 500,
        "GIVEAWAY500": 500,
        "FAN1000": 1000,
        "VISHI1500": 1500
    }
    discount = coupons.get(coupon.upper(), 0)
    final_price = max(original_price - discount, 0)
    return final_price, discount

# --- 1. Main Bottom Menu (As It Is) ---
def get_custom_menu():
    buttons = [
        [KeyboardButton(text="Fluorite Keys"), KeyboardButton(text="Android Keys")],
        [KeyboardButton(text="Full iOS Panel"), KeyboardButton(text="Full Android Panel")],
        [KeyboardButton(text="GBox"), KeyboardButton(text="Esign")],
        [KeyboardButton(text="Monite Key"), KeyboardButton(text="Migul iOS Panel")],
        [KeyboardButton(text="Profile"), KeyboardButton(text="Support")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- 2. Master Product Database (As It Is) ---
PRODUCT_DB = {
    "fl_7d": {"name": "Fluorite 7 Day Key", "price": 900},
    "fl_1m": {"name": "Fluorite 1 Month Key", "price": 1500},
    "and_7d": {"name": "Android 7 Day Key", "price": 600},
    "and_1m": {"name": "Android 1 Month Key", "price": 1000},
    "and_fs": {"name": "Android Full Season Key", "price": 2000},
    "ios_p1": {"name": "Full iOS Panel (Standard)", "price": 3000},
    "ios_p2": {"name": "Full iOS Panel (VIP Access)", "price": 4500},
    "and_p1": {"name": "Full Android Panel (Standard)", "price": 2000},
    "and_p2": {"name": "Full Android Panel (Root Pack)", "price": 3500},
    "gbox_6m": {"name": "GBox 6 Month Access", "price": 1000},
    "gbox_1y": {"name": "GBox 1 Year Premium", "price": 1500},
    "esign_1y": {"name": "Esign 1 Year Certificate", "price": 800},
    "esign_vip": {"name": "Esign 1 Year (VIP Instant Anti-Revoke)", "price": 1200},
    "mon_7d": {"name": "Monite 7 Day Key", "price": 600},
    "mon_31d": {"name": "Monite 31 Day Key", "price": 1000},
    "mig_full": {"name": "Migul Full iOS Panel", "price": 1500},
    "mig_pro": {"name": "Migul iOS Panel + Injection Kit", "price": 2500}
}

# --- 3. Main Reply Trigger Handlers (As It Is) ---
@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✨ Welcome to the Shop! Choose a product category from below to view pricing options:", reply_markup=get_custom_menu())

@router.message(F.text == "Fluorite Keys")
async def handle_fluorite(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy 7 Day Key (900 INR)", callback_data="buy_fl_7d")],
        [InlineKeyboardButton(text="🛒 Buy 1 Month Key (1500 INR)", callback_data="buy_fl_1m")]
    ])
    await message.answer("💎 **Fluorite Keys Options:**\nSelect the specific tier you want to buy below:", reply_markup=kb)

@router.message(F.text == "Android Keys")
async def handle_android_keys(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy 7 Day Key (600 INR)", callback_data="buy_and_7d")],
        [InlineKeyboardButton(text="🛒 Buy 1 Month Key (1000 INR)", callback_data="buy_and_1m")],
        [InlineKeyboardButton(text="🛒 Buy Full Season Key (2000 INR)", callback_data="buy_and_fs")]
    ])
    await message.answer("🤖 **Android Keys Options:**\nSelect the options below to proceed:", reply_markup=kb)

@router.message(F.text == "Full iOS Panel")
async def handle_full_ios(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy Full iOS Panel (3000 INR)", callback_data="buy_ios_p1")],
        [InlineKeyboardButton(text="🛒 Buy VIP iOS Panel (4500 INR)", callback_data="buy_ios_p2")]
    ])
    await message.answer("🍏 **Full iOS Panel Subscriptions:**\nChoose your license access duration/tier:", reply_markup=kb)

@router.message(F.text == "Full Android Panel")
async def handle_full_android(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy Full Android Panel (2000 INR)", callback_data="buy_and_p1")],
        [InlineKeyboardButton(text="🛒 Buy Root Pack Bundle (3500 INR)", callback_data="buy_and_p2")]
    ])
    await message.answer("🤖 **Full Android Panel Subscriptions:**\nSelect the package structure you want:", reply_markup=kb)

@router.message(F.text == "GBox")
async def handle_gbox(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy GBox 6 Month (1000 INR)", callback_data="buy_gbox_6m")],
        [InlineKeyboardButton(text="🛒 Buy GBox 1 Year (1500 INR)", callback_data="buy_gbox_1y")]
    ])
    await message.answer("📦 **GBox Premium Subscriptions:**\nSelect preferred runtime variant:", reply_markup=kb)

@router.message(F.text == "Esign")
async def handle_esign(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy Standard 1 Year (800 INR)", callback_data="buy_esign_1y")],
        [InlineKeyboardButton(text="🛒 Buy VIP Anti-Revoke (1200 INR)", callback_data="buy_esign_vip")]
    ])
    await message.answer("✍️ **Esign Certificate Licenses:**\nChoose the certificate policy option:", reply_markup=kb)

@router.message(F.text == "Monite Key")
async def handle_monite(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy 7 Day Key (600 INR)", callback_data="buy_mon_7d")],
        [InlineKeyboardButton(text="🛒 Buy 31 Days Key (1000 INR)", callback_data="buy_mon_31d")]
    ])
    await message.answer("🛡️ **Monite Key Licensing:**\nSelect your operation runtime validation:", reply_markup=kb)

@router.message(F.text == "Migul iOS Panel")
async def handle_migul(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy Full iOS Panel (1500 INR)", callback_data="buy_mig_full")],
        [InlineKeyboardButton(text="🛒 Buy Panel + Injector Kit (2500 INR)", callback_data="buy_mig_pro")]
    ])
    await message.answer("🔥 **Migul iOS Panel Offers:**\nSelect the setup configuration layout below:", reply_markup=kb)

@router.message(F.text == "Support")
async def handle_support(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Open Direct Chat", url="https://t.me/vitor_fault")]
    ])
    await message.answer("👨‍💻 **Support Center**\n\nFor any pre-sales queries, dynamic key replacements, or payment technical issues, feel free to reach out to the administrator directly.", reply_markup=kb)

@router.message(F.text == "Profile")
async def handle_profile(message: Message):
    profile_text = (
        f"👤 **Your Account Profile**\n\n"
        f"🔹 **Name:** {message.from_user.full_name}\n"
        f"🆔 **Telegram ID:** `{message.from_user.id}`\n"
        f"🌐 **Username:** @{message.from_user.username if message.from_user.username else 'N/A'}\n"
        f"💰 **Preferred Currency:** INR (Indian Rupee)\n"
        f"🎖️ **Account Status:** Active Client"
    )
    await message.answer(profile_text)

# --- 4. Updated E-Commerce Workflow (Coupons Added) ---
@router.callback_query(F.data.startswith("buy_"))
async def process_buy_button(callback: CallbackQuery, state: FSMContext):
    product_code = callback.data.split("buy_")[1]
    item_data = PRODUCT_DB[product_code]
    name = item_data["name"]
    price = item_data["price"]
    await state.update_data(current_product=name, base_price=price, final_price=price)
    
    coupon_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟️ Apply Coupon Code", callback_data="apply_coupon")],
        [InlineKeyboardButton(text="➡️ Skip & Continue to Payment", callback_data="proceed_payment")]
    ])
    await callback.message.edit_text(f"📦 **Product Selection Confirmed:**\n\n🔹 **Item:** {name}\n💰 **Price:** {price} INR\n\nDo you have an active coupon/promotional code to apply?", reply_markup=coupon_kb)
    await callback.answer()

@router.callback_query(F.data == "apply_coupon")
async def ask_coupon(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Please type and send your coupon code directly in this chat:")
    await state.set_state(ShopStates.waiting_for_coupon)
    await callback.answer()

@router.message(ShopStates.waiting_for_coupon)
async def process_coupon(message: Message, state: FSMContext):
    user_code = message.text.strip().upper()
    data = await state.get_data()
    final_p, discount = get_discounted_price(user_code, data['base_price'])
    
    if discount > 0:
        await state.update_data(final_price=final_p)
        msg = f"✅ **Coupon {user_code} Applied!**\n💰 **New Updated Balance:** {final_p} INR"
    else:
        msg = f"❌ **Invalid or Expired Coupon!**\n💰 **Current Balance:** {data['base_price']} INR"

    payment_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Proceed to Payment Portal", callback_data="proceed_payment")]
    ])
    await message.answer(msg, reply_markup=payment_kb)

@router.callback_query(F.data == "proceed_payment")
async def show_payment_gateway(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    qr_text = (
        f"📲 **SECURE UPI GATEWAY INSTANCE**\n\n"
        f"📦 **Order Pack:** {data['current_product']}\n"
        f"🔺 **Net Payable Amount:** {data.get('final_price', data['base_price'])} INR\n\n"
        f"📌 **UPI ID:** `bharatpe.8y0l1s2n7z76332@fbpe` (Tap to Copy)\n\n"
        f"👉 **How to Pay:**\nComplete the transfer and click below to upload your screenshot."
    )
    screenshot_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Upload Payment Screenshot", callback_data="upload_ss")]
    ])
    await callback.message.edit_text(qr_text, reply_markup=screenshot_kb)
    await callback.answer()

@router.callback_query(F.data == "upload_ss")
async def ask_screenshot(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🖼️ Please send the photo/screenshot of your payment confirmation now:")
    await state.set_state(ShopStates.waiting_for_screenshot)
    await callback.answer()

@router.message(ShopStates.waiting_for_screenshot, F.photo)
async def handle_payment_screenshot(message: Message, state: FSMContext, bot: Bot):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve Order", callback_data=f"admin_approve_{message.from_user.id}"),
         InlineKeyboardButton(text="❌ Reject Order", callback_data=f"admin_reject_{message.from_user.id}")]
    ])
    await bot.send_photo(chat_id=ADMIN_ID, photo=photo_id, caption=f"🔔 **Incoming Purchase!**\nUser: {message.from_user.full_name}\nProduct: {data['current_product']}\nAmount: {data.get('final_price', data['base_price'])} INR", reply_markup=admin_kb)
    await message.answer("⏳ **Please wait for 10 minutes.** Our system is verifying your payment.")
    await state.clear()

@router.callback_query(F.data.startswith("admin_approve_"))
async def admin_approve(callback: CallbackQuery, bot: Bot):
    client_id = int(callback.data.split("admin_approve_")[1])
    await bot.send_message(chat_id=client_id, text="🎉 **Payment Verified Successfully!**\nHere is your key: `FV-SH1-VAND-SH19-0726-OK`")
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n🟢 **ORDER STATE: DELIVERED**")
    await callback.answer("Order Approved!")

@router.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery, bot: Bot):
    client_id = int(callback.data.split("admin_reject_")[1])
    await bot.send_message(chat_id=client_id, text="❌ **Payment Audit Failed!** Please contact support.")
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n🔴 **ORDER STATE: REJECTED**")
    await callback.answer("Order Rejected!")