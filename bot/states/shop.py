from aiogram.fsm.state import StatesGroup, State

class ShopStates(StatesGroup):
    waiting_for_coupon = State()
    waiting_for_screenshot = State()
