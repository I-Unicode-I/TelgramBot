""" Import lib for able to use Bot"""
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Import logging for able create logger
import logging

# Import our lib which we will need
from alpha_vantage.timeseries import TimeSeries
from AddCompany_state import AddCompany

# Import lib for functioning of the bot
import config  # consist of Bot TOKEN and API stocks
from UserInfo import Info, User  # consist of func and class for work with db

"""
Begin setting logging:
logging.basicConfig() - set level for logging our code
logging.getLogger() - creating new logger
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Name button for our button(command) in telegram
button_stock = 'Stock'

# Definition bot with method from aiogram lib and
# assign it the value of our token
bot = Bot(token=config.TOKEN)
# Create storage for collect data about company which user enter
storage = MemoryStorage()
# Definition dispatcher with our bot with storage
dp = Dispatcher(bot=bot, storage=storage)

# Create str variable for keep answer with stock price
STOCK = ""


# Func for 'start' command in telegram
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """
        inserting users to db with user id
        Creating message greeting person and about bot;
        Next, sending this message.
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user which sended message.
    """
    user = User(id=message.from_user.id,
                full_name=message.from_user.full_name,
                user_name=message.from_user.mention,
                company=None,
                reminder_action=None)

    try:
        Info.insert_info_user(user)
    finally:

        hello = "Hello!\nI'm StockBot, and I can help you monitor popular companies and their market prices!"
        helps = "My command:\n" \
                "Stock price your follow companies -- /stock\n" \
                "Help, list of commands(this command) -- /help\n" \
                "List of your selected companies -- /mycompany\n" \
                "List of all companies -- /companies"

        await message.answer(text=hello)
        await message.answer(text=helps)


# Func for 'help' command in telegram
@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    """
        Creating message greeting person and about bot;
        Next, sending this message.
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user which sended message.
    """
    helps = "My command:\n" \
            "Stock price your follow companies -- /stock\n" \
            "Help, list of commands(this command) -- /help\n" \
            "List of your companies -- /mycompany\n" \
            "List of all companies -- /companies"

    await message.answer(text=helps)


def stock_function(message: types.Message):
    """
        Create dict for collect stock price;
        Collect stock price in variable ts from Alpha_vantage API;
        Choose company market name from the list;
        Add info about company in dict;
        Create text about all companies stock price;
        return text consist of info about companies;
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about Tesla stock price now.
    """
    users = Info().get_all_users()
    user_companies = []
    for u in users:
        if u.id == str(message.from_user.id):
            user_companies = u.company
    ts = TimeSeries(key=config.API_STOCK, output_format='pandas')
    stock_keys = [k for k in user_companies]
    stock_values = []
    for k in stock_keys:
        stock, _ = ts.get_intraday(symbol=k, interval='1min')
        stock_values.append(str(stock['4. close'][0]))

    stock_companies = dict(zip(stock_keys, stock_values))

    global STOCK
    STOCK = "Shares cost in:\n>>" + \
            "\n>>".join([k + ": " + v + " $" for k, v in stock_companies.items()])


# Func for 'stock' command in telegram
@dp.message_handler(commands=['stock'])
async def button_stock_handler(message: types.Message):
    """
        Call function "stock_function"
        take text from "stock_function"
        Sending message with this text;
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about Tesla stock price now.
    """
    stock_function(message)
    global STOCK
    await message.answer(text=STOCK)


# Func for 'user' command in telegram
@dp.message_handler(commands=['user'])
async def button_user_handler(message: types.Message):
    """
        Collection info about users from DB which consisting of users;
        Creating text for answer with info about users;
        Sending a message consisting of user info;
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about user which are in the db.
    """
    users = Info().get_all_users()
    answer_message = "User info:\n| " + \
                     "\n| ".join([u.full_name + " ("+", ".join(u.company)+")" for u in users])
    await message.reply(
        text=answer_message,
        reply_markup=types.reply_keyboard.ReplyKeyboardRemove(),
        reply=False
    )


# Func for 'company' command in telegram
@dp.message_handler(commands=['companies'])
async def button_companies_handler(message: types.Message):
    """
        Collecting info about all companies which are in list;
        Create list consist of all companies;
        Creating text for answer with info about companies;
        Sending a message consisting of all companies.
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about companies which are in list.
    """
    all_companies = Info().get_all_companies()
    await message.answer(
        text="\n Market name ~~ Company name\n | \t" +
             "\n | \t".join([c.market_name + "\t~~\t".center(20) + c.company_name for c in all_companies])
    )


# Func for 'company' command in telegram
@dp.message_handler(commands=['mycompany'])
async def button_company_handler(message: types.Message):
    """
        Collecting info about user company which he has;
        Create list consist of user company;
        Creating text for answer with info about users;
        Sending a message consisting of company which user has.
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about companies which is user has.
    """
    users = Info().get_all_users()
    user_companies = []
    for u in users:
        if u.id == str(message.from_user.id):
            user_companies = u.company
    answer_message = "Your companies:\n | " + "\n | ".join(user_companies)
    await message.reply(
        text=answer_message,
        reply_markup=types.reply_keyboard.ReplyKeyboardRemove(),
        reply=False
    )


# Func for 'addcompany' command in telegram
@dp.message_handler(commands=['addcompany'], state=None)
async def button_addcompany_handler(message: types.Message):
    """
        Collection info which user enter;
        update info about user in db, column company;
        Sending a message consisting of about what all his company added.
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, about what all his company added.
    """
    all_companies = Info().get_all_companies()
    await message.reply(
        text="Choose company which you need: "
             "\n Market name ~~ Company name\n | \t" +
             "\n | \t".join([c.market_name + "\t~~\t".center(20) + c.company_name for c in all_companies]),
        reply_markup=types.reply_keyboard.ReplyKeyboardRemove(),
        reply=False
    )
    await message.answer(text="Please enter >market name< company:")
    await AddCompany.Q1.set()


# This function for function command 'addcompany'
@dp.message_handler(state=AddCompany.Q1)
async def companies(message: types.Message, state: FSMContext):
    """
        Take answer which enter user;
        Collect answer in current state
    :param message: aiogram message which get message id and etc.
    :param state: aiogram state which has user
    :return: data from answer user
    """
    user_companies = message.text
    column = 'company'

    Info.update_info_user(column, user_companies, message.from_user.id)

    await message.answer("Thank you!\n Your companies are added in your list!")

    await state.finish()


# Func for answering message from telegram
@dp.message_handler(content_types=types.ContentType.TEXT)
async def message_handler(message: types.Message):
    """
        Collecting message which user sended;
        Creating Keyboard with buttons;
        replies to message;
    :param message: aiogram message which get message id and etc.
    :return: message to telegram user, and keyboard with our button
             the names of which we have previously identified
    """
    text = message.text

    reply_markup = types.reply_keyboard.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.reply_keyboard.KeyboardButton(text=button_stock),
            ],
        ],
        resize_keyboard=True
    )

    if text and isinstance(text, str):
        await message.answer(text='Hello ' + message.from_user.full_name, reply_markup=reply_markup)

    if text == button_stock:
        stock_function(message)
        global STOCK
        await message.answer(text=STOCK)


# Run our bot with executor.start_polling() - method for run form aiogram lib
if __name__ == '__main__':
    executor.start_polling(dp)
