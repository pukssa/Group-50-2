from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import buttons
from db import main_db

# Состояния для формы добавления товара
class StoreFSM(StatesGroup):
    name_product = State()
    size = State()
    price = State()
    category = State()
    info_product = State()
    products_id = State()
    collection = State()
    photo = State()
    submit = State()

# Список товаров, для переключения по ним
products = []
current_product_index = 0

async def start_fsm_store(message: types.Message):
    await message.answer('Введите название товара:', reply_markup=buttons.cancel)
    await StoreFSM.name_product.set()

async def name_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите размер:')

async def size_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите цену товара:')

async def price_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите категорию товара:')

async def category_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите информацию о продукте:')

async def info_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите коллекцию товара:')

async def collection_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await StoreFSM.next()
    await message.answer('Введите артикул для товара: ')

async def product_id_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['products_id'] = message.text

    await StoreFSM.next()
    await message.answer("Отправьте фото товара:")

async def photo_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await StoreFSM.next()
    await message.answer('Верные ли данные?', reply_markup=buttons.submit)
    await message.answer_photo(photo=data['photo'],
                           caption=f'Название товара - {data["name_product"]}\n'
                                   f'Размер товара - {data["size_product"]}\n'
                                   f'Категория - {data["category_product"]}\n'
                                   f'Коллекция - {data["collection"]}\n'
                                   f'Артикул - {data["products_id"]}\n'
                                   f'Инфо - {data["info_product"]}\n'
                                   f'Цена - {data["price_product"]}')

async def submit_load(message: types.Message, state: FSMContext):
    if message.text == 'да':
        async with state.proxy() as data:
            # Запись в таблицу store
            await main_db.sql_insert_store(
                name_product=data['name_product'],
                size=data['size_product'],
                price=data['price_product'],
                product_id=data['products_id'],
                photo=data['photo']
            )

            # Запись в таблицу detail
            await main_db.sql_insert_detail(
                product_id=data['products_id'],
                info_product=data['info_product'],
                category=data['category_product']
            )

            # Запись в таблицу collection_products
            await main_db.sql_insert_collection(
                productid=data['products_id'],
                collection=data['collection']
            )

            await message.answer('Ваши данные в базе!', reply_markup=buttons.remove_keyboard)
            await state.finish()

            # Добавление товара в список
            products.append(data)  # Сохраняем в список

            # Показываем первый товар
            await show_next_product(message)


# Создание кнопки "далее" для переключения между товарами
async def show_next_product(message: types.Message):
    global current_product_index

    if current_product_index < len(products):
        product = products[current_product_index]
        current_product_index += 1

        # Кнопка "далее"
        next_button = InlineKeyboardButton(text="Далее", callback_data="next_product")
        keyboard = InlineKeyboardMarkup().add(next_button)

        await message.answer_photo(photo=product['photo'],
                                   caption=f'Название товара - {product["name_product"]}\n'
                                           f'Размер товара - {product["size_product"]}\n'
                                           f'Категория - {product["category_product"]}\n'
                                           f'Коллекция - {product["collection"]}\n'
                                           f'Артикул - {product["products_id"]}\n'
                                           f'Инфо - {product["info_product"]}\n'
                                           f'Цена - {product["price_product"]}',
                                   reply_markup=keyboard)
    else:
        await message.answer("Это был последний товар.", reply_markup=buttons.remove_keyboard)

# Обработка нажатия на кнопку "Далее"
async def next_product(callback_query: types.CallbackQuery):
    global current_product_index
    message = callback_query.message
    await show_next_product(message)

# Регистрация хендлеров
def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(start_fsm_store, commands=['store'])
    dp.register_message_handler(name_load, state=StoreFSM.name_product)
    dp.register_message_handler(size_load, state=StoreFSM.size)
    dp.register_message_handler(price_load, state=StoreFSM.price)
    dp.register_message_handler(category_load, state=StoreFSM.category)
    dp.register_message_handler(info_load, state=StoreFSM.info_product)
    dp.register_message_handler(collection_load, state=StoreFSM.collection)
    dp.register_message_handler(product_id_load, state=StoreFSM.products_id)
    dp.register_message_handler(photo_load, state=StoreFSM.photo, content_types=['photo'])
    dp.register_message_handler(submit_load, state=StoreFSM.submit)

    dp.register_callback_query_handler(next_product, text="next_product")