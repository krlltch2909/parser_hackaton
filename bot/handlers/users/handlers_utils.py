import logging
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from loader import bot


logger = logging.getLogger(f"root.{__name__}")


async def try_delete_cancel_message(state: FSMContext) -> None:
    state_data = await state.get_data()
    
    if cancel_message_exists(state_data):        
        existing_cancel_message_id = state_data["existing_cancel_message_id"]
        user_id = state.user
        try:
            await bot.delete_message(user_id, existing_cancel_message_id)
            del state_data["existing_cancel_message_id"]
            await state.set_data(state_data)
        except MessageToDeleteNotFound:
            logger.error("can't delete cancel message")


def cancel_message_exists(state_data: dict) -> bool:
    return "existing_cancel_message_id" in state_data
