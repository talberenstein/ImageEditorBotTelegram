import logging

# from warnings import filters
from telegram import ext
from telegram import ForceReply
from telegram.ext import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

import Constants

# updater = Updater(
#     "5199045475:AAHBcN0_bQKNqswNAFPN2U5CgTfhUDYViiM", use_context=True)

CONVERT, PHOTO, FORMAT_TO, BIO = range(4)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
	/convert - To convert the format of the image (jpg, svg, png)
	/resize - To resize image with pixels
	/compress - To compress the image""")
    return CONVERT




def youtube_url(update: Update, context: CallbackContext):
    update.message.reply_text("Youtube Link =>\
	https://www.youtube.com/")


def handleSendRequest(urlToConver):
    pass


def photo(update: Update, context: CallbackContext) -> int:
    print("insert photo")
    url = "https://image-processing4.p.rapidapi.com/imageconvert"
    querystring = {
        "imageUrl": "https://codingforum.site/img/logo.png", "outputType": "gif"}

    headers = {
        "X-RapidAPI-Host": "image-processing4.p.rapidapi.com",
        "X-RapidAPI-Key": Constants.API_KEY_SERVICE
    }
    photo_file = update.message.photo[-1].get_file()
    print(photo_file.file_path)
    # urlToConver = photo_file.file_path
    # handleSendRequest(urlToConver)
    update.message.reply_text(text="Please provide a type")
    return formatTo(update, context)
    querystring = {"imageUrl": photo_file.file_path, "outputType": "gif"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    print(response)

    update.message.reply_text(response.text)


def formatTo(update: Update, context: CallbackContext) -> int:
    print("FORMAT_TO -> formatTo")
    formatToConvert = update.message
    print(formatToConvert)


def convert(update: Update, context: CallbackContext):
    update.message.reply_text("""You selected /convert""")
    update.message.reply_text(text="Please provide a picture")
    return PHOTO


def geeks_url(update: Update, context: CallbackContext):
    update.message.reply_text(
        "GeeksforGeeks URL => https://www.geeksforgeeks.org/")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    print("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# updater.dispatcher.conv_handler(ConversationHandler(
# 	entry_points=[CommandHandler("start", start)],
# 	states={
# 		PHOTO: [MessageHandler(filters.PHOTO, photo)]
# 	}
# ))

def main() -> None:
    """Run the bot"""
    updater = Updater(
        "5199045475:AAHBcN0_bQKNqswNAFPN2U5CgTfhUDYViiM", use_context=True)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", convert)],
        states={
            # GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            CONVERT: [],
            PHOTO: [MessageHandler(Filters.photo, photo),
                    formatTo],
            # FORMAT_TO: [MessageHandler(Filters.text, formatTo), formatTo]
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()

# updater.dispatcher.add_handler(ConversationHandler(
#     entry_points=[CommandHandler("start", start)],
#     states={
#         TYPE: [MessageHandler(filters.PHOTO, photo), MessageHandler(filters.Regex("^(jpg|svg|gif)$"), type)],
#     }
# ))

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler('convert', convert))
# updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
# updater.dispatcher.add_handler(
#     MessageHandler(Filters.photo, photo))
# updater.dispatcher.add_handler(MessageHandler(
#     Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
