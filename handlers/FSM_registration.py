# FSM_registration.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import main_db
import buttons


class FSM_reg(StatesGroup):
    fullname = State()
    age = State()
    gender = State()
    date_age = State()
    email = State()
    photo = State()
    submit = State()


async def start_fsm_reg(message: types.Message):
    await FSM_reg.fullname.set()
    await message.answer('Введите своё фио: ', reply_markup=buttons.cancel_fsm)


async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text

    await FSM_reg.next()
    await message.answer('Отправь свой возраст')


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await FSM_reg.next()
    await message.answer('Укажите пол')



async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text


    await FSM_reg.next()
    await message.answer('Укажите дату рождения:')


async def load_date_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_age'] = message.text


    await FSM_reg.next()
    await message.answer('Укажите свою почту')


async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text


    await FSM_reg.next()
    await message.answer('Отправьте свою фотографию')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id


    await FSM_reg.next()
    await message.answer('Верные ли данные')
    await message.answer_photo(photo=data['photo'],
                               caption=f'ФИО - {data["fullname"]}\n'
                                       f'Возраст - {data["age"]}\n'
                                       f'Пол - {data["gender"]}\n'
                                       f'Дата рождения - {data["date_age"]}\n'
                                       f'Почта - {data["email"]}\n', reply_markup=buttons.submit)

async def submit(message: types.Message, state: FSMContext):
    if message.text == 'да':
        async with state.proxy() as data:

            await main_db.sql_insert_registered(
                fullname=data['fullname'],
                age=data['age'],
                gender=data['gender'],
                date_age=data['date_age'],
                email=data['email'],
                photo=data['photo']
            )

            await message.answer('Ваши данные в базе', reply_markup=buttons.start)

        await state.finish()

    elif message.text == 'нет':
        await message.answer('Хорошо, отменено!', reply_markup=buttons.start)
        await state.finish()

    else:
        await message.answer('Выберите да или нет')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.start)


def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm_reg, commands=['registration'])
    dp.register_message_handler(load_fullname, state=FSM_reg.fullname)
    dp.register_message_handler(load_age, state=FSM_reg.age)

    dp.register_message_handler(load_gender, state=FSM_reg.gender)
    dp.register_message_handler(load_date_age, state=FSM_reg.date_age)
    dp.register_message_handler(load_email, state=FSM_reg.email)
    dp.register_message_handler(load_photo, state=FSM_reg.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_reg.submit)