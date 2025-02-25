# delete_products.py

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import main_db
from aiogram.types import InputMediaPhoto


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_all = types.InlineKeyboardButton('Выввести все товары:',
                                            callback_data='delete_all')
    button_one = types.InlineKeyboardButton("Вывести по одному",
                                            callback_data='delete_one')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как просмотреть товары:',
                         reply_markup=keyboard)

async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название товара - {product["name_product"]}\n'
            f'Размер товара - {product["size"]}\n'
            f'Категория - {product["category"]}\n'
            f'Артикул - {product["product_id"]}\n'
            f'Инфо - {product["info_product"]}\n'
            f'Цена - {product["price"]}')

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            delete_button = types.InlineKeyboardButton(
                'Удалить', callback_data=f"delete_{product['product_id']}")
            keyboard.add(delete_button)

            await call.message.answer_photo(photo=product["photo"],
                                            caption=caption,
                                            reply_markup=keyboard)
    else:
        await call.message.answer('Товаров нет!')


async def delete_product(call: types.CallbackQuery):
    text_all = call.data
    text = call.data.split('_')[0]
    product_id = call.data.split('_')[1]

    print(text_all)
    print(text)
    print(product_id)

    main_db.delete_products(product_id)

    new_caption = 'Товар удален!'

    photo_404 = open('media/images.png', 'rb')

    await call.message.edit_media(
        InputMediaPhoto(media=photo_404, caption=new_caption),
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['delete_products'])
    dp.register_callback_query_handler(send_all_products, Text(equals='delete_all'))
    dp.register_callback_query_handler(delete_product, Text(startswith='delete_'))