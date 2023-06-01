import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from os import getenv
from dotenv import load_dotenv; load_dotenv()

bot_token = getenv('TG_TOKEN')
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

order_info = {}  # Dictionary to store order information


class FollowerOrderStates(StatesGroup):
    USERNAME = State()
    FOLLOWERS_COUNT = State()
    PHONE_NUMBER = State()


class LikeOrderStates(StatesGroup):
    USERNAME = State()
    LIKES_COUNT = State()
    PHONE_NUMBER = State()


class CommentOrderStates(StatesGroup):
    USERNAME = State()
    COMMENTS_COUNT = State()
    COMMENTS_TEXT = State()
    PHONE_NUMBER = State()


@dp.message_handler(Command('start'))
async def start(message: types.Message):
    text = "Welcome to our Instagram services!\n\nAvailable commands:"
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    order_followers_button = types.InlineKeyboardButton("Order Followers", callback_data='order_followers')
    order_likes_button = types.InlineKeyboardButton("Order Likes", callback_data='order_likes')
    order_comments_button = types.InlineKeyboardButton("Order Comments", callback_data='order_comments')
    inline_keyboard_markup.add(order_followers_button, order_likes_button, order_comments_button)

    await message.reply(text, reply_markup=inline_keyboard_markup)


@dp.callback_query_handler(lambda c: c.data == 'order_followers')
async def order_followers(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(user_id, "Please enter your Instagram username:")
    await FollowerOrderStates.USERNAME.set()


@dp.message_handler(state=FollowerOrderStates.USERNAME)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text

    await state.update_data(username=username)

    reply_keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    followers_options = [
        types.InlineKeyboardButton("1000", callback_data='1000'),
        types.InlineKeyboardButton("5000", callback_data='5000'),
        types.InlineKeyboardButton("10000", callback_data='10000')
    ]
    reply_keyboard_markup.add(*followers_options)

    await bot.send_message(message.chat.id, "Choose the number of followers you would like to order:",
                           reply_markup=reply_keyboard_markup)

    await FollowerOrderStates.FOLLOWERS_COUNT.set()


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=FollowerOrderStates.FOLLOWERS_COUNT)
async def process_followers(callback_query: types.CallbackQuery, state: FSMContext):
    followers_count = int(callback_query.data)

    data = await state.get_data()
    user_id = callback_query.from_user.id
    username = data.get('username')

    order_info[user_id] = {'username': username, 'followers': followers_count}

    await bot.send_message(user_id, "Please provide your phone number:")
    await FollowerOrderStates.PHONE_NUMBER.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=FollowerOrderStates.PHONE_NUMBER)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    data = await state.get_data()
    user_id = message.from_user.id

    order_info[user_id]['phone_number'] = phone_number

    await bot.send_message(user_id, f"Order Information:\n\n"
                                    f"Instagram Username: {order_info[user_id]['username']}\n"
                                    f"Number of Followers: {order_info[user_id]['followers']}\n"
                                    f"Phone Number: {order_info[user_id]['phone_number']}\n\n"
                                    f"Please make sure your Instagram profile is public before proceeding.")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'order_likes')
async def order_likes(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(user_id, "Please enter your Instagram username:")
    await LikeOrderStates.USERNAME.set()


@dp.message_handler(state=LikeOrderStates.USERNAME)
async def process_likes_username(message: types.Message, state: FSMContext):
    username = message.text

    await state.update_data(username=username)

    reply_keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    likes_options = [
        types.InlineKeyboardButton("1000", callback_data='1000'),
        types.InlineKeyboardButton("5000", callback_data='5000'),
        types.InlineKeyboardButton("10000", callback_data='10000')
    ]
    reply_keyboard_markup.add(*likes_options)

    await bot.send_message(message.chat.id, "Choose the number of likes you would like to order:",
                           reply_markup=reply_keyboard_markup)

    await LikeOrderStates.LIKES_COUNT.set()


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=LikeOrderStates.LIKES_COUNT)
async def process_likes_count(callback_query: types.CallbackQuery, state: FSMContext):
    likes_count = int(callback_query.data)

    data = await state.get_data()
    user_id = callback_query.from_user.id
    username = data.get('username')

    order_info[user_id] = {'username': username, 'likes': likes_count}

    await bot.send_message(user_id, "Please provide your phone number:")
    await LikeOrderStates.PHONE_NUMBER.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=LikeOrderStates.PHONE_NUMBER)
async def process_likes_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    data = await state.get_data()
    user_id = message.from_user.id

    order_info[user_id]['phone_number'] = phone_number

    await bot.send_message(user_id, f"Order Information:\n\n"
                                    f"Instagram Username: {order_info[user_id]['username']}\n"
                                    f"Number of Likes: {order_info[user_id]['likes']}\n"
                                    f"Phone Number: {order_info[user_id]['phone_number']}\n\n"
                                    f"Please make sure your Instagram profile is public before proceeding.")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'order_comments')
async def order_comments(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(user_id, "Please enter your Instagram username:")
    await CommentOrderStates.USERNAME.set()


@dp.message_handler(state=CommentOrderStates.USERNAME)
async def process_comments_username(message: types.Message, state: FSMContext):
    username = message.text

    await state.update_data(username=username)

    await bot.send_message(message.chat.id, "Enter the number of comments you would like to order:")

    await CommentOrderStates.COMMENTS_COUNT.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=CommentOrderStates.COMMENTS_COUNT)
async def process_comments_count(message: types.Message, state: FSMContext):
    comments_count = message.text

    await state.update_data(comments_count=comments_count)

    await bot.send_message(message.chat.id, "Enter the comments you would like to order, separated by commas:")

    await CommentOrderStates.COMMENTS_TEXT.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=CommentOrderStates.COMMENTS_TEXT)
async def process_comments_text(message: types.Message, state: FSMContext):
    comments_text = message.text

    data = await state.get_data()
    user_id = message.from_user.id
    username = data.get('username')
    comments_count = data.get('comments_count')

    order_info[user_id] = {'username': username, 'comments_count': comments_count, 'comments_text': comments_text}

    await bot.send_message(user_id, "Please provide your phone number:")
    await CommentOrderStates.PHONE_NUMBER.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=CommentOrderStates.PHONE_NUMBER)
async def process_comments_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    data = await state.get_data()
    user_id = message.from_user.id

    order_info[user_id]['phone_number'] = phone_number

    await bot.send_message(user_id, f"Order Information:\n\n"
                                    f"Instagram Username: {order_info[user_id]['username']}\n"
                                    f"Number of Comments: {order_info[user_id]['comments_count']}\n"
                                    f"Comments: {order_info[user_id]['comments_text']}\n"
                                    f"Phone Number: {order_info[user_id]['phone_number']}\n\n"
                                    f"Please make sure your Instagram profile is public before proceeding.")

    await state.finish()

    text = "Order placed successfully!\n\nAvailable commands:"
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    order_followers_button = types.InlineKeyboardButton("Order Followers", callback_data='order_followers')
    order_likes_button = types.InlineKeyboardButton("Order Likes", callback_data='order_likes')
    order_comments_button = types.InlineKeyboardButton("Order Comments", callback_data='order_comments')
    inline_keyboard_markup.add(order_followers_button, order_likes_button, order_comments_button)

    await bot.send_message(user_id, text, reply_markup=inline_keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
