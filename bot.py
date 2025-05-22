import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart

# ✅ Token
API_TOKEN = '7617255159:AAFEL818SQifnaVdHoc_IIrsk1SasPaEZLs'

# Kanal va adminlar
CHANNELS = ['@school299']
ADMINS = ['@Avazxoja1', '@schoolGulhayo']

# Boshlang‘ich ovozlar (sizga 100 ta)
candidates = {
    "Shukurullaxo'djayev Avazxo'ja": 400,
    "Abduvaliyev Jamilbek": 10,
    "Xayriddinov Shoxjahon": 42,
    "Shomirova Sabriya": 300,
    "Maxmudjonov Diyorbek": 44,
    "Ergasheva Jasmina": 169,
    "Abdusattorova Roziya": 100,
    "Toxirjonov Xojakbar": 34,
    "Baxtiyorov Muhammadali": 40,
    "Komiljonov Abdurasul": 2,
}

# Kim ovoz berdi
user_votes = {}

# Bot holati
class VoteStates(StatesGroup):
    waiting_for_vote = State()

# Obuna tekshirish
async def check_subscription(bot: Bot, user_id: int) -> bool:
    for channel in CHANNELS:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            return False
    return True

# Tugma yasash
def vote_keyboard():
    kb = InlineKeyboardBuilder()
    for name, count in candidates.items():
        kb.button(text=f"{name} ({count} ta ovoz)", callback_data=f"vote:{name}")
    kb.adjust(1)
    return kb.as_markup()

# /start komandasi
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    if not await check_subscription(bot, message.from_user.id):
        channels_list = "\n".join([f"{ch}" for ch in CHANNELS])
        await message.answer(
            f"❗️ Ovoz berishdan oldin quyidagi kanal(lar)ga obuna bo‘ling:\n{channels_list}"
        )
        return
    await message.answer(
        "Assalomu alaykum! Yil o‘quvchisi uchun ovoz berish botiga xush kelibsiz!\n\nIltimos, nomzodlardan birini tanlang:",
        reply_markup=vote_keyboard()
    )
    await state.set_state(VoteStates.waiting_for_vote)

# Ovoz berish
async def vote_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    data = callback.data.split(":")
    candidate = data[1]

    if user_id in user_votes:
        await callback.answer("❌ Siz allaqachon ovoz bergansiz!", show_alert=True)
        return

    candidates[candidate] += 1
    user_votes[user_id] = candidate

    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"👤 {user_name} -> 🗳 {candidate}")
        except:
            pass

    await callback.message.edit_text(
        f"✅ Siz {candidate} uchun ovoz berdingiz.\n\nRahmat!",
    )
    await state.clear()

# Asosiy funksiya
async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())
    dp.callback_query.register(vote_handler, F.data.startswith("vote:"), VoteStates.waiting_for_vote)

    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

# Ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())

