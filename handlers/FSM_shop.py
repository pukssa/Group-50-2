from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
class Store(StatesGroup):
    product_name = State()  # Название товара
    size = State()          # Размер
    category = State()      # Категория
    price = State()         # Стоимость
    photo = State()         # Фото товара
    submit = State()        # Подтверждение данных
# Стадия 1: Название товара
async def start_add_product(message: types.Message):
    await Store.product_name.set()
    await message.answer('Введите название товара:')
# Обработчик для названия товара
async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await Store.next()
    await message.answer('Выберите размер товара:', reply_markup=buttons.size_keyboard)
# Стадия 2: Размер товара (кнопки с размерами)
async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await Store.next()
    await message.answer('Выберите категорию товара:', reply_markup=buttons.category_keyboard)
# Стадия 3: Категория товара
async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await Store.next()
    await message.answer('Введите стоимость товара:')
# Стадия 4: Стоимость товара
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await Store.next()
    await message.answer('Отправьте фотографию товара:', reply_markup=buttons.remove_keyboard)
# Стадия 5: Фото товара
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id  # Получаем id последней фотографии
    await Store.next()
    await message.answer('Правильные ли данные?', reply_markup=buttons.confirmation_keyboard)
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название товара: {data["product_name"]}\n'
                                       f'Размер: {data["size"]}\n'
                                       f'Категория: {data["category"]}\n'
                                       f'Стоимость: {data["price"]}\n',
                               reply_markup=buttons.confirmation_keyboard)
# Стадия подтверждения данных
async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            # Записываем данные в базу (например)
            product_name = data["product_name"]
            size = data["size"]
            category = data["category"]
            price = data["price"]
            photo = data["photo"]
            # Тут можно записать данные в БД или передать их на сервер
        await message.answer('Ваш товар добавлен в базу!', reply_markup=buttons.remove_keyboard)
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Хорошо, отменено!', reply_markup=buttons.remove_keyboard)
        await state.finish()
    else:
        await message.answer('Выберите да или нет', reply_markup=buttons.confirmation_keyboard)
# Отмена FSM
async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.remove_keyboard)
def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_add_product, commands='add_product')
    dp.register_message_handler(load_product_name, state=Store.product_name)