from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

import requests

from utils import *

config = read_json(config_path)["TELEGRAM_BOT"]

url = "http://127.0.0.1:3000"

storage = MemoryStorage()
bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher(bot, storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Devices'),
    KeyboardButton('Activity'),
    KeyboardButton('Add device'),
    KeyboardButton('Start notification'),
    KeyboardButton('Stop notification'),
)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(
        "Hi, I am Systems Monitoring Bot. I can help you with monitoring devices in your local network",
        reply_markup=kb
    )


async def get_all_devices(message: types.Message):
    devices = json.loads(requests.get(f"{url}/device").text)
    answer_str = ''
    for device in devices:
        inkb = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text=f'Resources', callback_data=f'resources_{device["id"]}'),
            InlineKeyboardButton(text=f'Plots', callback_data=f'plots_{device["id"]}'),
            InlineKeyboardButton(text=f'Delete', callback_data=f'delete_{device["id"]}'),
        )
        inkb.add(InlineKeyboardButton(text=f'{"Stop" if device["notification"] else "Start"} notifications',
                                      callback_data=f'notifications_'
                                                    f'{"stop" if device["notification"] else "start"}_{device["id"]}'))

        available_actions = json.loads(requests.get(f"{url}/action").text)
        action_kb = [
            InlineKeyboardButton(text=f'{action["action_name"]}',
                                 callback_data=f'action_{device["id"]}_{action["action_id"]}')
            for action in available_actions
        ]
        inkb.row(*action_kb)

        # TODO: implement scenario when device do not have activity
        device_activity = json.loads(requests.get(f'{url}/activity/{device["id"]}').text)
        answer_str += f'Status: {"🟢" if device_activity["is_online"] else "🔴"} \
                    Notifications: {"🔔" if device["notification"] else "🔕"} '

        answer_str += "\n\n" if device_activity["is_online"] else \
            f'\n\n\n⏳Last seen:   {convert_time_format(device_activity["last_time_online"])} \n\n\n'
        answer_str += f'🔌: {device["name"]}                        🌐: {device["ip"]} \n'

        response = requests.get(f'{url}/resources/{device["id"]}?limit=1').text
        if len(response) > 2:
            device_resources = json.loads(response)[0]
            answer_str += \
                f'\n==============💻SYSTEM INFORMATION💻==============\n' \
                f'System: {device_resources["system"]}\n' \
                f'CPU model: {device_resources["cpu_model"]}\n' \
                f'Video driver: {device_resources["video_driver_model"]}\n' \
                f'Boot time: {device_resources["boot_time"]}\n' \
                '==================================================='

        await message.answer(answer_str, reply_markup=inkb)
        answer_str = ''


async def get_all_activity(message: types.Message):
    all_activity = json.loads(requests.get(f"{url}/activity").text)
    answer_str = ""
    for activity in all_activity:
        status_indicator = "🔴" if not activity["is_online"] else "🟢"
        last_time_online = f'⏳: {convert_time_format(activity["last_time_online"])}' if not activity[
            "is_online"] else ''

        answer_str += f'{status_indicator}  ' \
                      f'🔌: {activity["device_name"].ljust(20)}' \
                      f'🌐: {activity["device_ip"].ljust(15)}' \
                      f'{last_time_online}\n'

    await message.answer(answer_str)


async def start_notifications(message: types.Message):
    configuration = read_json(config_path)
    configuration["TELEGRAM_BOT"]["NOTIFICATIONS"] = True
    configuration(config_path, configuration)

    await message.answer("🔔Notifications ON🔔")


async def stop_notifications(message: types.Message):
    configuration = read_json(config_path)
    configuration["TELEGRAM_BOT"]["NOTIFICATIONS"] = False
    write_json(config_path, configuration)

    await message.answer("🔕Notifications OFF🔕")


async def delete_device(callback: types.CallbackQuery):
    response = json.loads(requests.delete(f"{url}/device/{callback.data.split('_')[1]}").text)
    await callback.answer("Device was removed"
                          if response["status"] == 204 else
                          "Something went wrong", show_alert=True)
    await callback.answer()


async def update_device_notifications(callback: types.CallbackQuery):
    onOrOff = True if callback.data.split('_')[1] == 'start' else False
    device_id = callback.data.split('_')[2]
    response = json.loads(requests.put(f"{url}/device/{device_id}?notifications={onOrOff}").text)
    await callback.answer(f"Notifications {'enabled' if onOrOff else 'disabled'}"
                          if response["status"] == 204 else 'Something went wrong', show_alert=True)
    await callback.answer()


async def perform_action(callback: types.CallbackQuery):
    payload = {
        "device_id": callback.data.split('_')[1],
        "action_id": callback.data.split('_')[2]
    }
    requests.post(f"{url}/action", json=payload)


async def get_resources(callback: types.CallbackQuery):
    answer_str = ''
    response = requests.get(f"{url}/resources/{callback.data.split('_')[1]}?limit=1").text

    if len(response) < 2:
        await callback.answer("No information about this device")
        await callback.answer()
    else:
        device_resources = json.loads(response)[0]
        answer_str += f'🔌: {device_resources["device_name"]}\t\t🌐: {device_resources["device_ip"]}\n' \
                      f'\n==============⚡️CPU INFORMATION⚡️==============\n' \
                      f'CPU used: {device_resources["cpu_used"]}%\n' \
                      f'Physical cores: {device_resources["physical_cores"]}\n' \
                      f'Total cores: {device_resources["total_cores"]}\n' \
                      f'Cores used:\n{device_resources["cores_used"]}' \
                      f'\n==============💽RAM INFORMATION💽==============\n' \
                      f'Total RAM: {device_resources["total_ram"]}\n' \
                      f'{device_resources["used_free_ram"]}\n' \
                      f'\n==============💾DICKS INFORMATION💾==============\n' \
                      f'{format_drive_info(device_resources["disks"])}' \
                      f'\n==============🔋BATTERY INFORMATION🔋==============\n' \
                      f'Charge: {device_resources["charge"]}%\n' \
                      f'Time left: {device_resources["time_left"]}'
        await callback.message.reply(answer_str)
        await callback.answer()


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

    new_device = {
        "name": data[0],
        "ip": data[1],
        "notification": data[2]
    }
    requests.post(f"{url}/device", json=new_device)
    await message.reply('Everything is fine. Device was added', reply_markup=kb)
    await state.finish()


def reg_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(perform_action), lambda x: x.data and x.data.startswith('action_')
    dp.register_callback_query_handler(get_resources), lambda x: x.data and x.data.startswith('resources_')
    dp.register_callback_query_handler(update_device_notifications), lambda x: x.data and x.data.startswith(
        'notifications_')
    dp.register_callback_query_handler(delete_device), lambda x: x.data and x.data.startswith('delete_')
    dp.register_message_handler(get_all_devices, lambda message: 'Devices' in message.text)
    dp.register_message_handler(get_all_activity, lambda message: 'Activity' in message.text)
    dp.register_message_handler(start_notifications, lambda message: 'Start notification' in message.text)
    dp.register_message_handler(stop_notifications, lambda message: 'Stop notification' in message.text)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cm_start, lambda message: 'Add device' in message.text, state=None)
    dp.register_message_handler(load_name, state=FSMDevice.name)
    dp.register_message_handler(load_ip, state=FSMDevice.ip)
    dp.register_message_handler(load_notifications, state=FSMDevice.notifications)


if __name__ == "__main__":
    reg_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)
