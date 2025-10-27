import os
import time
import telebot
from dotenv import load_dotenv
from database import create_tables, add_order, get_menu_items, add_menu_item

load_dotenv()
BOT_TOKEN = os.getenv("7978577832:AAHAHagcPe5Rigx-6qlE2u339i8zUzMgSlg")
LOGS_GROUP_ID = os.getenv("-1003282574590")
OWNER_ID = 6954401932
USERNAME_OWNER = @kopi657

bot = telebot.TeleBot("7978577832:AAHAHagcPe5Rigx-6qlE2u339i8zUzMgSlg)
create_tables()

# Tambahkan menu default jika kosong
if len(get_menu_items()) == 0:
    add_menu_item("Userbot Plan Basic", 15000, "addprem", "Dana", "081219623569", "Lusiana Kurniawati")
    add_menu_item("Userbot Plan Pro", 25000, "addpro", "Qris", "", "", "https://files.catbox.moe/5clazs.jpg")

@bot.message_handler(commands=['start'])
def start(message):
    menu_items = get_menu_items()
    text = "Halo! Bot Auto Order siap.\n\nMenu Item:\n"
    for item in menu_items:
        text += f"{item[0]}. {item[1]} - Rp{item[2]}\n"
    text += "\nKetik nomor item untuk order."
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: m.text.isdigit())
def order_item(message):
    item_id = int(message.text)
    items = get_menu_items()
    selected = next((i for i in items if i[0]==item_id), None)
    if not selected:
        bot.reply_to(message, "Item tidak ditemukan, ketik /start untuk melihat menu.")
        return
    user_id = message.from_user.id
    _, name, price, access_type, payment_type, number, owner, link = selected

    # Payment info
    if payment_type.lower() == "dana":
        payment_info = f"Bayar via Dana:\nNomor: {number}\nA/n: {owner}"
    elif payment_type.lower() == "qris":
        payment_info = f"Bayar via QRIS:\nLink QR: {link}"
    else:
        payment_info = "Payment info tidak tersedia."

    access_granted = f"{access_type} granted by @GARFIELD28_Bot"
    add_order(user_id, name, price, access_granted, status="SUCCESS")

    bot.reply_to(message, f"Pesanan diterima!\nItem: {name}\nHarga: Rp{price}\nAkses: {access_granted}\n\n{payment_info}")

    if LOGS_GROUP_ID:
        bot.send_message(LOGS_GROUP_ID,
                         f"Order baru!\nUser: {message.from_user.username} ({user_id})\nItem: {name}\nHarga: {price}\nAkses: {access_granted}")

# Tambah menu via bot (admin only)
@bot.message_handler(commands=['addmenu'])
def add_menu(message):
    if message.from_user.username != "@kopi657" 
        bot.reply_to(message, "Kamu bukan admin!")
        return
    try:
        args = message.text[len("/addmenu "):].split("|")
        name = args[0].strip()
        price = int(args[1].strip())
        access_type = args[2].strip()
        payment_type = args[3].strip()
        number = args[4].strip() if len(args)>4 else ""
        owner = args[5].strip() if len(args)>5 else ""
        link = args[6].strip() if len(args)>6 else ""
        add_menu_item(name, price, access_type, payment_type, number, owner, link)
        bot.reply_to(message, f"Menu baru ditambahkan: {name}")
    except Exception as e:
        bot.reply_to(message, f"Gagal menambahkan menu: {e}")

@bot.message_handler(func=lambda m: True)
def default_reply(message):
    bot.reply_to(message, "Silakan pilih nomor item atau ketik /start untuk melihat menu.")

if __name__ == "__main__":
    print("Bot Auto Order berjalan...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
