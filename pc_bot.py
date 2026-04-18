from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import pyautogui
import cv2

# 你的 Bot Token
TOKEN = "  "

# 你的 Telegram ID
AUTHORIZED_ID = ""


keyboard = [
    ["🌐 Edge", "🎮 Steam"],
    ["📸 截屏", "📷 摄像头"],
    ["🔒 锁屏"],
    ["🔄 重启", "⛔ 关机"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def is_authorized(update):
    return update.effective_user.id == AUTHORIZED_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_authorized(update):
        await update.message.reply_text("❌ 未授权用户")
        return

    await update.message.reply_text(
        "🖥 PC 控制台",
        reply_markup=markup
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_authorized(update):
        await update.message.reply_text("❌ 未授权用户")
        return

    text = update.message.text


    # 打开 Edge
    if text == "🌐 Edge":

        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

        if os.path.exists(edge_path):
            os.startfile(edge_path)
            await update.message.reply_text("Edge 已打开")
        else:
            await update.message.reply_text("❌ Edge 路径错误")


    # 打开 Steam（需要你改路径）
    elif text == "🎮 Steam":

        steam_path = r"C:\Program Files (x86)\Steam\steam.exe"

        if os.path.exists(steam_path):
            os.startfile(steam_path)
            await update.message.reply_text("Steam 已启动")
        else:
            await update.message.reply_text("❌ Steam 路径错误")


    # 截屏并发送
    elif text == "📸 截屏":

        try:
            img = pyautogui.screenshot()
            img.save("screen.png")

            with open("screen.png", "rb") as photo:
                await update.message.reply_photo(photo=photo)

        except Exception as e:
            await update.message.reply_text(f"截屏失败: {e}")


    # 摄像头拍照并发送
    elif text == "📷 摄像头":

        try:
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()

            if ret:
                cv2.imwrite("cam.jpg", frame)
                cam.release()

                with open("cam.jpg", "rb") as photo:
                    await update.message.reply_photo(photo=photo)
            else:
                await update.message.reply_text("❌ 摄像头无法访问")

        except Exception as e:
            await update.message.reply_text(f"摄像头错误: {e}")


    # 锁屏
    elif text == "🔒 锁屏":
        os.system("rundll32.exe user32.dll,LockWorkStation")


    # 重启
    elif text == "🔄 重启":
        os.system("shutdown /r /t 0")


    # 关机
    elif text == "⛔ 关机":
        os.system("shutdown /s /t 0")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("机器人已启动...")

app.run_polling()