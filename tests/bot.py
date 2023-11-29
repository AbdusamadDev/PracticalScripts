import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType
import xlrd

API_TOKEN = '6195275934:AAEngBypgfNw3SwcV9uV_jdatZtMvojF9cs'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def read_and_print_xls(file_path):
    workbook = xlrd.open_workbook(file_path).sheets()[0]
    # for sheet in workbook.sheets():
    #     print(f"Sheet Name: {sheet.name}\n")
    lst = []
    for row_idx in range(workbook.nrows):
        lst.append(workbook.row_values(row_idx))

    return lst


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def handle_docs(message: types.Message):
    if message.document.mime_type in ["application/vnd.ms-excel",
                                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        await message.reply("Received an Excel file. Processing...")
        file_info = await message.document.download()
        file_path = file_info.name  # Get the file path
        response = read_and_print_xls(file_path)
        for r in response:
            await message.answer(str(r))
    else:
        await message.reply("Please send an Excel file.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    