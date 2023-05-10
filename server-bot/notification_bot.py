import asyncio
import threading
import time
from datetime import datetime
from threading import Thread
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from db_scripts import *
from config_utils import *

config = read_json(config_path)["TELEGRAM_BOT"]

storage = MemoryStorage()
bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher(bot, storage=storage)


kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
                            KeyboardButton('Devices'),
                            KeyboardButton('Activity'),
                            KeyboardButton('Resources'),
                            KeyboardButton('Start notification'),
                            KeyboardButton('Stop notification'),
                            KeyboardButton('Add device'),
                            )


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(
        "Hi, I am Systems Monitoring Bot. I can help you with monitoring devices in your local network", reply_markup=kb)

async def get_all_devices(message: types.Message):
    devices = ''
    for device in select_all_devices():
        devices += f"🔌: {device[1]}\t🌐: {device[2]}\t"
        if device[3]:
            devices += "🔔\n"
        else:
            devices += "🔕\n"
    await message.answer(devices)


async def get_all_activity(message: types.Message):
    activity = ''
    formate = "%Y-%m-%d %H:%M:%S"
    for active in select_all_activity():
        activity += f"{'🟢' if active[2] else '🔴'}  " \
                    f"🔌: {active[0]}\t\t" \
                    f"🌐: {active[1]}\t\t" \
                    f"{'⏳: ' + str(active[3].strftime(formate)) if not active[2] else ''}\n"

    await message.answer(activity)

async def start_notifications(message: types.Message):
    tmp = read_json(config_path)
    tmp["TELEGRAM_BOT"]["NOTIFICATIONS"] = True
    write_json(config_path, tmp)

    await message.answer("🔔Notifications ON🔔")


async def stop_notifications(message: types.Message):
    tmp = read_json(config_path)
    tmp["TELEGRAM_BOT"]["NOTIFICATIONS"] = False
    write_json(config_path, tmp)
    await message.answer("🔕Notifications OFF🔕")


async def get_resources(message: types.Message):
    msg = ''
    for id in select_ids():
        information = select_all_resources(id[0])
        if not information:
            continue
        msg += f"🔌: {information[0][0]}\t\t🌐: {information[0][1]}\n" \
               f"\n==============💻SYSTEM INFORMATION💻==============\n" \
               f"System: {information[0][2]}\n" \
               f"Video driver: {information[0][3]}\n" \
               f"CPU model: {information[0][4]}\n" \
               f"Boot time: {information[0][14]}\n" \
               f"\n==============⚡️CPU INFORMATION⚡️==============\n" \
               f"CPU used: {information[0][5]}%\n" \
               f"Physical cores: {information[0][6]}\n" \
               f"Total cores: {information[0][7]}\n" \
               f"Cores used:\n{information[0][8]}\n" \
               f"\n==============💽RAM INFORMATION💽==============\n" \
               f"Total RAM: {information[0][9]}\n" \
               f"{information[0][10]}\n" \
               f"\n==============💾DICKS INFORMATION💾==============\n" \
               f"{information[0][11]}" \
               f"\n==============🔋BATTERY INFORMATION🔋==============\n" \
               f"Charge: {information[0][12]}%\n" \
               f"Time left: {information[0][13]}"
        await message.answer(msg)


class FSMDevice(StatesGroup):
    name = State()
    ip = State()
    notifications = State()


async def cm_start(message: types.Message):
    await FSMDevice.name.set()
    await message.reply('Enter device name')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Ok')
    await state.finish()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[0] = message.text
    await FSMDevice.next()
    await message.reply('Now enter device\'s ip')


async def load_ip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[1] = message.text
    await FSMDevice.next()
    await message.reply('Do you want to have notifications when device become offline?',
                        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                            KeyboardButton('Yes'),
                            KeyboardButton('Not')
                        ))


async def load_notifications(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[2] = message.text == "Yes"
    insert_device(data[0], data[1], data[2])
    await message.reply('Everything is fine. Device was added', reply_markup=kb)
    await state.finish()


dp.register_message_handler(get_all_devices, lambda message: 'Devices' in message.text)
dp.register_message_handler(get_all_activity, lambda message: 'Activity' in message.text)
dp.register_message_handler(start_notifications, lambda message: 'Start notification' in message.text)
dp.register_message_handler(stop_notifications, lambda message: 'Stop notification' in message.text)
dp.register_message_handler(get_resources, lambda message: 'Resources' in message.text)
dp.register_message_handler(cancel_handler, state="*", commands='cancel')
dp.register_message_handler(cm_start, lambda message: 'Add device' in message.text, state=None)
dp.register_message_handler(load_name, state=FSMDevice.name)
dp.register_message_handler(load_ip, state=FSMDevice.ip)
dp.register_message_handler(load_notifications, state=FSMDevice.notifications)

#executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    start_db()
    executor.start_polling(dp, skip_updates=True)
