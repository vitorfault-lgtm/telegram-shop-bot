from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from bot.states.shop import ShopStates
import os

router = Router()

ADMIN_ID = 6516079642  # Your actual Telegram ID from .env

# --- 1. Main Bottom Menu (Reply Keyboard) ---
def get_custom_menu():
    buttons = [
        [KeyboardButton(text="Fluorite Keys"), KeyboardButton(text="Android Keys")],
        [KeyboardButton(text="Full iOS Panel"), KeyboardButton(text="Full Android Panel")],
        [KeyboardButton(text="GBox"), KeyboardButton(text="Esign")],
        [KeyboardButton(text="Monite Key"), KeyboardButton(text="Migul iOS Panel")],
        [KeyboardButton(text="Profile"), KeyboardButton(text="Support")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- 2. Master Product Database (Mapping all 8+ categories smoothly) ---
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

# --- 3. Main Reply Trigger Handlers ---
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

# --- 4. Unified E-Commerce Workflow (Coupons, QR Generation & Approval) ---
@router.callback_query(F.data.startswith("buy_"))
async def process_buy_button(callback: CallbackQuery, state: FSMContext):
    product_code = callback.data.split("buy_")[1]
    
    if product_code not in PRODUCT_DB:
        await callback.answer("❌ Error: Invalid Item Selected.", show_alert=True)
        return
        
    item_data = PRODUCT_DB[product_code]
    name = item_data["name"]
    price = item_data["price"]
    
    await state.update_data(current_product=name, base_price=price, final_price=price)
    
    coupon_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟️ Apply Coupon Code", callback_data="apply_coupon")],
        [InlineKeyboardButton(text="➡️ Skip & Continue to Payment", callback_data="proceed_payment")]
    ])
    
    await callback.message.edit_text(
        f"📦 **Product Selection Confirmed:**\n\n🔹 **Item:** {name}\n💰 **Price:** {price} INR\n\nDo you have an active coupon/promotional code to apply?",
        reply_markup=coupon_kb
    )
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
    
    if user_code == "DISCOUNT10":
        discount = int(data['base_price'] * 0.10)
        final_p = data['base_price'] - discount
        await state.update_data(final_price=final_p, applied_coupon=user_code)
        msg = f"✅ **Coupon Code Successfully Applied!** You received a 10% instant discount.\n💰 **New Updated Balance:** {final_p} INR"
    else:
        final_p = data['base_price']
        msg = f"❌ **Invalid or Expired Coupon!** Proceeding with the default original valuation.\n💰 **Current Balance:** {final_p} INR"

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
        f"🔺 **Net Payable Amount:** {data['final_price']} INR\n\n"
        f"📌 **UPI ID:** `bharatpe.8y0l1s2n7z76332@fbpe` (Tap to Copy)\n\n"
        f"👉 **How to Pay:**\n"
        f"1. Scan the QR Code attached above or copy the UPI ID.\n"
        f"2. Complete the transfer of exactly **{data['final_price']} INR**.\n"
        f"3. Take a clear screenshot of the successful transaction confirmation screen.\n\n"
        f"⚠️ **Crucial:** Once completed, click the button below to upload your transaction validation record."
    )
              
    screenshot_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Upload Payment Screenshot", callback_data="upload_ss")]
    ])
    
    await callback.message.delete()
    
    # 🎯 FIX: Changed .jpg to .png as per your requirement
    qr_filename = "my_qr.png"
    
    if os.path.exists(qr_filename):
        try:
            with open(qr_filename, "rb") as image_file:
                photo_bytes = image_file.read()
                photo_payload = BufferedInputFile(photo_bytes, filename=qr_filename)
                
                await bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=photo_payload,
                    caption=qr_text,
                    reply_markup=screenshot_kb
                )
        except Exception as e:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f"⚠️ **Error reading file:** Please check image health.\n\n{qr_text}",
                reply_markup=screenshot_kb
            )
    else:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"⚠️ **Error:** `{qr_filename}` file not found in project folder!\n\n{qr_text}",
            reply_markup=screenshot_kb
        )
        
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
    
    user_info = f"👤 **Client:** {message.from_user.full_name} (@{message.from_user.username})\n🆔 **User ID:** `{message.from_user.id}`"
    
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Approve Order", callback_data=f"admin_approve_{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Reject Order", callback_data=f"admin_reject_{message.from_user.id}")
        ]
    ])
    
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=f"🔔 **Incoming Store Purchase Request!**\n\n{user_info}\n📦 **Product:** {data['current_product']}\n💰 **Transferred:** {data['final_price']} INR",
        reply_markup=admin_kb
    )
    
    await message.answer("⏳ **Please wait for 10 minutes to approve your payment.**\nOur automated confirmation protocol is verifying the ledger receipt transaction.")
    await state.clear()

# --- 5. Admin Live Approval Engine ---
@router.callback_query(F.data.startswith("admin_approve_"))
async def admin_approve(callback: CallbackQuery, bot: Bot):
    client_id = int(callback.data.split("admin_approve_")[1])
    delivered_stock = "🔑 `STOCK-LICENSE-KEY: FV-SH1-VAND-SH19-0726-OK`"
    
    await bot.send_message(
        chat_id=client_id,
        text=f"🎉 **Payment Verified Successfully!**\nThank you for choosing us. Here is your ordered license asset:\n\n{delivered_stock}\n\n*Keep this safe. For configuration help, check out @vitor_fault*"
    )
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n🟢 **ORDER STATE: COMPLETED & DELIVERED**")
    await callback.answer("Order successfully processed and keys dispatched!", show_alert=True)

@router.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery, bot: Bot):
    client_id = int(callback.data.split("admin_reject_")[1])
    
    await bot.send_message(
        chat_id=client_id,
        text="❌ **Payment Audit Verification Failed!**\nThe verification agent rejected your proof of purchase file. If this is an error, please establish direct contact with support at @vitor_fault."
    )
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n🔴 **ORDER STATE: AUDIT REJECTED / DISMISS**")
    await callback.answer("Order rejected. Client notified.", show_alert=True)