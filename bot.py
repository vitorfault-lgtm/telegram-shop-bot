import sqlite3
import qrcode
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler
)

# ================= CONFIGURATION =================
TOKEN = "8986448248:AAH5rirPfxkZVVZHNYvWE080-kWHqWnXQck"
UPI_ID = "bharatpe.8y0l1s2n7z76332@fbpe"
ADMIN_ID = 8338184748

# Conversation States
AWAITING_COUPON = 1
AWAITING_KEY_ADD = 2
AWAITING_COUPON_ADD = 3
AWAITING_BLOCK_USER = 4

# ================= DATABASE SETUP =================
def init_db():
    conn = sqlite3.connect("shop_data.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key_code TEXT UNIQUE,
                        status TEXT DEFAULT 'AVAILABLE'
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS coupons (
                        code TEXT PRIMARY KEY,
                        discount INT
                    )''')
                    
    cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_users (
                        user_id TEXT PRIMARY KEY
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INT,
                        item TEXT,
                        amount INT,
                        status TEXT
                    )''')

    default_coupons = [
        ("IOSKEY300D", 300), ("KEYS200D", 200), 
        ("VIPOFF500D", 500), ("PROMO100D", 100), ("SAVE400D", 400)
    ]
    for code, disc in default_coupons:
        cursor.execute("INSERT OR IGNORE INTO coupons VALUES (?, ?)", (code, disc))

    sample_keys = [
        "HGK38YLSF8FN0LIA", "PLM92KSHA71629AL", "OQI1827364510PLA", "ZXM9821736451290",
        "QWE1234567890RTY", "UIO0987654321PAS", "DFG6543210987JKL", "CVB7890123456MNO"
    ]
    for k in sample_keys:
        cursor.execute("INSERT OR IGNORE INTO keys (key_code) VALUES (?)", (k,))

    conn.commit()
    conn.close()

init_db()

# Markdown Escaper
def esc(text):
    if not text:
        return ""
    return str(text).replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')

# ================= KEYBOARDS =================
def get_user_menu():
    kb = [
        [KeyboardButton("💎 Fluorite Keys"), KeyboardButton("🤖 Android Keys")],
        [KeyboardButton("📱 Full iOS Panel"), KeyboardButton("🛠️ Full Android Panel")],
        [KeyboardButton("📦 GBox"), KeyboardButton("✍️ Esign")],
        [KeyboardButton("🔑 Monite Key"), KeyboardButton("👤 Profile")],
        [KeyboardButton("📜 My Orders")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def get_admin_menu():
    kb = [
        [KeyboardButton("📦 Manage Products"), KeyboardButton("📋 Orders")],
        [KeyboardButton("🏷️ Discount Coupon"), KeyboardButton("🚫 Block User")],
        [KeyboardButton("❌ Exit Admin")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def get_payment_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏷️ Apply Discount Coupon", callback_data="prompt_coupon")],
        [InlineKeyboardButton("📸 Upload Payment Screenshot", callback_data="prompt_upload_ss")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="close_payment")]
    ])

# ================= COMMAND / START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    c.execute("SELECT user_id FROM blocked_users WHERE user_id=?", (user_id,))
    if c.fetchone():
        conn.close()
        await update.message.reply_text("🚫 **You are blocked from using this bot.**", parse_mode="Markdown")
        return
    conn.close()

    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("⚡ **Welcome Admin!** Select option from panel:", reply_markup=get_admin_menu())
    else:
        await update.message.reply_text("✨ **Welcome to the Shop!** Choose a product category below:", reply_markup=get_user_menu())

# ================= PHOTO SCREENSHOT FORWARDING TO ADMIN =================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    item_name = context.user_data.get('last_item', 'Fluorite 7 Day Key')
    amount = context.user_data.get('discounted_amount', context.user_data.get('last_amount', 900))

    # Save order in DB
    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, item, amount, status) VALUES (?, ?, ?, ?)", (user.id, item_name, amount, "PENDING"))
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    # User Acknowledgement
    await update.message.reply_text(
        "⏳ **Payment Screenshot Received!**\n\nPlease wait up to **10 minutes** while admin verifies your payment.",
        parse_mode="Markdown"
    )

    # Approve/Reject Buttons for Admin
    admin_btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve Order", callback_data=f"appr_{order_id}_{user.id}"),
            InlineKeyboardButton("❌ Reject Order", callback_data=f"rejc_{order_id}_{user.id}")
        ]
    ])

    username_str = f"(@{esc(user.username)})" if user.username else ""
    full_name = esc(user.first_name)
    if user.last_name:
        full_name += f" {esc(user.last_name)}"

    # Exact format as requested
    admin_caption = (
        f"🔔 **Incoming Store Purchase Request!**\n\n"
        f"👤 **Client:** {full_name} {username_str}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"📦 **Product:** {esc(item_name)}\n"
        f"💰 **Transferred:** {amount} INR"
    )

    # Forwarding Photo + Details to Admin
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=admin_caption,
        parse_mode="Markdown",
        reply_markup=admin_btn
    )

# ================= TEXT HANDLER =================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    c.execute("SELECT user_id FROM blocked_users WHERE user_id=?", (str(user_id),))
    if c.fetchone():
        conn.close()
        await update.message.reply_text("🚫 **You are blocked.**")
        return
    conn.close()

    # Admin Menu Options
    if user_id == ADMIN_ID:
        if text == "📦 Manage Products":
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Key", callback_data="admin_add_key"), InlineKeyboardButton("➖ Remove Key", callback_data="admin_rem_key")]
            ])
            await update.message.reply_text("📦 **Manage Products & Keys Stock:**", reply_markup=kb)
            return

        elif text == "📋 Orders":
            conn = sqlite3.connect("shop_data.db")
            c = conn.cursor()
            c.execute("SELECT order_id, user_id, item, amount, status FROM orders WHERE status='PENDING' ORDER BY order_id DESC LIMIT 5")
            rows = c.fetchall()
            conn.close()

            if not rows:
                await update.message.reply_text("📋 No pending orders right now.", parse_mode="Markdown")
                return

            for r in rows:
                ord_id, u_id, item, amt, st = r
                admin_btn = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Approve Order", callback_data=f"appr_{ord_id}_{u_id}"),
                     InlineKeyboardButton("❌ Reject Order", callback_data=f"rejc_{ord_id}_{u_id}")]
                ])
                msg = (
                    f"📋 **Order #{ord_id}**\n\n"
                    f"👤 **User ID:** `{u_id}`\n"
                    f"📦 **Product:** {esc(item)}\n"
                    f"💰 **Transferred:** {amt} INR\n"
                    f"Status: **{st}**"
                )
                await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=admin_btn)
            return

        elif text == "🏷️ Discount Coupon":
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Coupon", callback_data="admin_add_coupon"), InlineKeyboardButton("➖ Remove Coupon", callback_data="admin_rem_coupon")]
            ])
            await update.message.reply_text("🏷️ **Manage Discount Coupons:**", reply_markup=kb)
            return

        elif text == "🚫 Block User":
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🛑 Enter User ID/Username to Block", callback_data="admin_block_prompt")]])
            await update.message.reply_text("🚫 **Block User Panel:**", reply_markup=kb)
            return

        elif text == "❌ Exit Admin":
            await update.message.reply_text("Returned to User Menu.", reply_markup=get_user_menu())
            return

    # Customer Options
    products = {
        "💎 Fluorite Keys": [("7 Day Key | 900 INR", "pay_Fluorite 7 Day Key_900"), ("1 Month Key | 1500 INR", "pay_Fluorite 1 Month Key_1500")],
        "🤖 Android Keys": [("7 Day Key | 600 INR", "pay_Android 7 Day Key_600"), ("1 Month Key | 1000 INR", "pay_Android 1 Month Key_1000"), ("Full Season Key | 2000 INR", "pay_Android Full Season Key_2000")],
        "📱 Full iOS Panel": [("Full iOS Panel | 3000 INR", "pay_Full iOS Panel_3000")],
        "🛠️ Full Android Panel": [("Full Android Panel | 2000 INR", "pay_Full Android Panel_2000")],
        "📦 GBox": [("GBox 6 Month | 1000 INR", "pay_GBox 6 Month_1000"), ("GBox 1 Year | 1500 INR", "pay_GBox 1 Year_1500")],
        "✍️ Esign": [("Esign 1 Year Certificate | 800 INR", "pay_Esign 1 Year Certificate_800")],
        "🔑 Monite Key": [("7 Day Key | 600 INR", "pay_Monite 7 Day Key_600"), ("31 Days Key | 1000 INR", "pay_Monite 31 Days Key_1000")]
    }

    if text in products:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=data)] for label, data in products[text]])
        await update.message.reply_text(f"Select option for {text}:", reply_markup=kb)

    elif text == "👤 Profile":
        user = update.effective_user
        profile_text = f"👤 **User Profile Info**\n\n• **Name:** {esc(user.first_name)}\n• **Username:** @{esc(user.username) if user.username else 'N/A'}\n• **User ID:** `{user.id}`"
        await update.message.reply_text(profile_text, parse_mode="Markdown")

    elif text == "📜 My Orders":
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("SELECT order_id, item, amount, status FROM orders WHERE user_id=? ORDER BY order_id DESC LIMIT 5", (user_id,))
        rows = c.fetchall()
        conn.close()

        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="close_payment")]])

        if not rows:
            await update.message.reply_text("📜 **Your Order History**\n\nYou haven't placed any orders yet!", parse_mode="Markdown", reply_markup=back_kb)
            return

        orders_msg = "📜 **Your Recent Purchase History:**\n\n"
        for r in rows:
            ord_id, item, amt, status = r
            status_icon = "🟢" if status == "APPROVED" else ("🔴" if status == "REJECTED" else "⏳")
            orders_msg += (
                f"🆔 **Order ID:** #{ord_id}\n"
                f"📦 **Product:** {esc(item)}\n"
                f"💰 **Amount Paid:** ₹{amt}\n"
                f"📌 **Status:** {status_icon} `{status}`\n"
                f"-----------------------------------\n"
            )

        await update.message.reply_text(orders_msg, parse_mode="Markdown", reply_markup=back_kb)

# ================= BUTTON CALLBACK ROUTER =================
async def button_tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "close_payment":
        await query.answer("Returned to Main Menu")
        await query.message.delete()

    elif data == "prompt_upload_ss":
        await query.answer()
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="close_payment")]])
        await query.message.reply_text("📸 **Please share the payment screenshot in the chat now:**", parse_mode="Markdown", reply_markup=kb)

    elif data == "prompt_coupon":
        await query.answer()
        await query.message.reply_text("🏷️ **Please enter your discount coupon code in chat:**", parse_mode="Markdown")
        return AWAITING_COUPON

    elif data == "show_updated_payment":
        await query.answer()
        item_name = context.user_data.get('last_item', 'Product')
        amount = context.user_data.get('discounted_amount', context.user_data.get('last_amount', 0))
        discount = context.user_data.get('discount_saved', 0)
        await send_payment_qr(query.message.chat_id, context, item_name, amount, query.message, discount_applied=discount)

    elif data.startswith("pay_"):
        await query.answer()
        _, item_name, amount = data.split("_")
        context.user_data['last_item'] = item_name
        context.user_data['last_amount'] = int(amount)
        context.user_data['discounted_amount'] = int(amount)
        context.user_data['discount_saved'] = 0
        await send_payment_qr(query.message.chat_id, context, item_name, int(amount), query.message)

    # APPROVE BUTTON ACTION
    elif data.startswith("appr_"):
        _, order_id, user_id = data.split("_")
        
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("SELECT id, key_code FROM keys WHERE status='AVAILABLE' LIMIT 1")
        row = c.fetchone()

        if row:
            key_id, key_code = row
            c.execute("UPDATE keys SET status='SOLD' WHERE id=?", (key_id,))
            c.execute("UPDATE orders SET status='APPROVED' WHERE order_id=?", (order_id,))
            conn.commit()
            conn.close()

            await query.answer(text="Order Approved & Key Sent!", show_alert=True)

            delivery_msg = (
                f"✅ **Payment Approved!**\n\n"
                f"Thank you for your purchase. Here is your Key:\n\n"
                f"🔑 `{key_code}`\n\n"
                f"*(Tap key code to copy)*"
            )
            await context.bot.send_message(chat_id=int(user_id), text=delivery_msg, parse_mode="Markdown")
            
            # Updates message text exactly like the screenshot
            updated_caption = f"{query.message.caption}\n\n🟢 **ORDER STATE: COMPLETED & DELIVERED**"
            await query.edit_message_caption(caption=updated_caption, reply_markup=None, parse_mode="Markdown")
        else:
            conn.close()
            await query.answer(text="⚠️ OUT OF STOCK! Add keys in Admin Menu!", show_alert=True)

    # REJECT BUTTON ACTION
    elif data.startswith("rejc_"):
        _, order_id, user_id = data.split("_")
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("UPDATE orders SET status='REJECTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        await query.answer(text="Order Rejected", show_alert=True)

        rejection_msg = "❌ **Your payment got rejected.** For information please do the right payment on given QR."
        await context.bot.send_message(chat_id=int(user_id), text=rejection_msg, parse_mode="Markdown")
        
        updated_caption = f"{query.message.caption}\n\n🔴 **ORDER STATE: REJECTED & DISMISSED**"
        await query.edit_message_caption(caption=updated_caption, reply_markup=None, parse_mode="Markdown")

    # Admin Management Callbacks
    elif data == "admin_add_key":
        await query.answer()
        await query.message.reply_text("➕ **Send the new key code in chat to add:**", parse_mode="Markdown")
        return AWAITING_KEY_ADD

    elif data == "admin_rem_key":
        await query.answer()
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("SELECT id, key_code FROM keys WHERE status='AVAILABLE' LIMIT 10")
        rows = c.fetchall()
        conn.close()

        if not rows:
            await query.message.reply_text("No keys available in stock.")
            return

        kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"❌ Delete {r[1]}", callback_data=f"delkey_{r[0]}")] for r in rows])
        await query.message.reply_text("Tap key to remove:", reply_markup=kb)

    elif data.startswith("delkey_"):
        await query.answer()
        key_id = data.split("_")[1]
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("DELETE FROM keys WHERE id=?", (key_id,))
        conn.commit()
        conn.close()
        await query.edit_message_text("✅ **Your key is successfully removed!**", parse_mode="Markdown")

    elif data == "admin_add_coupon":
        await query.answer()
        await query.message.reply_text("➕ Send coupon format in chat: `CODE:DISCOUNT` (e.g. `OFF100:100`)", parse_mode="Markdown")
        return AWAITING_COUPON_ADD

    elif data == "admin_rem_coupon":
        await query.answer()
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("SELECT code FROM coupons")
        rows = c.fetchall()
        conn.close()

        kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"❌ Remove {r[0]}", callback_data=f"delcoup_{r[0]}")] for r in rows])
        await query.message.reply_text("Tap coupon code to delete:", reply_markup=kb)

    elif data.startswith("delcoup_"):
        await query.answer()
        code = data.split("_")[1]
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("DELETE FROM coupons WHERE code=?", (code,))
        conn.commit()
        conn.close()
        await query.edit_message_text(f"✅ **Coupon '{code}' removed successfully!**", parse_mode="Markdown")

    elif data == "admin_block_prompt":
        await query.answer()
        await query.message.reply_text("🚫 **Enter User ID or Username in chat to block:**", parse_mode="Markdown")
        return AWAITING_BLOCK_USER

# ================= CONVERSATION INPUT PROCESSORS =================
async def process_user_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()
    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    c.execute("SELECT discount FROM coupons WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()

    if row:
        discount = row[0]
        orig_amount = context.user_data.get('last_amount', 0)
        new_amount = max(0, orig_amount - discount)
        context.user_data['discounted_amount'] = new_amount
        context.user_data['discount_saved'] = discount

        kb = InlineKeyboardMarkup([[InlineKeyboardButton("💳 Proceed to Updated Payment Portal", callback_data="show_updated_payment")]])
        await update.message.reply_text(f"🎉 **Congratulations!** You got **Flat ₹{discount} Discount!**", parse_mode="Markdown", reply_markup=kb)
    else:
        await update.message.reply_text("❌ **Invalid Coupon Code.** Please try again.")
    return ConversationHandler.END

async def process_admin_add_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key_code = update.message.text.strip().upper()
    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO keys (key_code) VALUES (?)", (key_code,))
        conn.commit()
        await update.message.reply_text("✅ **Your key is added successfully!**", parse_mode="Markdown")
    except:
        await update.message.reply_text("⚠️ Key already exists.")
    finally:
        conn.close()
    return ConversationHandler.END

async def process_admin_add_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        code, disc = update.message.text.strip().split(":")
        conn = sqlite3.connect("shop_data.db")
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO coupons VALUES (?, ?)", (code.upper(), int(disc)))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ **Coupon '{code.upper()}' added!**", parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ Invalid format. Use `CODE:AMOUNT`.")
    return ConversationHandler.END

async def process_admin_block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text.strip()
    conn = sqlite3.connect("shop_data.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO blocked_users VALUES (?)", (target,))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"🚫 **User '{target}' blocked!**", parse_mode="Markdown")
    return ConversationHandler.END

# ================= QR PAYMENT SCREEN =================
async def send_payment_qr(chat_id, context, item_name, amount, message_obj=None, discount_applied=0):
    upi_url = f"upi://pay?pa={UPI_ID}&pn=StoreAdmin&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    bio = BytesIO()
    bio.name = 'qr.png'
    qr.save(bio, 'PNG')
    bio.seek(0)

    caption_text = f"📌 **UPI ID:** `{UPI_ID}`\n*(Tap UPI ID to copy)*\n\n"
    if discount_applied > 0:
        caption_text += f"🎉 **Coupon Discount Applied:** Saved ₹{discount_applied}!\n\n"

    caption_text += (
        f"👉 **How to Pay:**\n"
        f"1. Scan the QR Code attached above or copy the UPI ID.\n"
        f"2. Complete the transfer of exactly **{amount} INR**.\n"
        f"3. Take a clear screenshot of the successful transaction confirmation screen.\n\n"
        f"⚠️ **Crucial:** Once completed, send the payment screenshot in this chat."
    )

    if message_obj:
        await message_obj.delete()
        
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=bio,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=get_payment_buttons()
    )

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_tap)],
        states={
            AWAITING_COUPON: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_user_coupon)],
            AWAITING_KEY_ADD: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_admin_add_key)],
            AWAITING_COUPON_ADD: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_admin_add_coupon)],
            AWAITING_BLOCK_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_admin_block_user)],
        },
        fallbacks=[],
        per_message=False
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_tap))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is up and running!")
    app.run_polling()

if __name__ == "__main__":
    main()