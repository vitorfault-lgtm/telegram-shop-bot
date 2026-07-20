from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    buttons = [
        "Fluorite Keys", "Android Keys",
        "Full iOS Panel", "Full Android Panel",
        "GBox", "Esign",
        "Monite Key", "Migul iOS Panel",
        "Support", "Profile"
    ]
    
    for button in buttons:
        builder.button(text=button)
        
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True)
