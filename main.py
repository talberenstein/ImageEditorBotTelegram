
from telegram.ext import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
import requests
from telegram import ReplyKeyboardRemove, Update

import json

import Constants

CONVERT, PHOTO, FORMAT_TO, HANDLE_CONVERT = range(4)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
	/convert - To convert the format of the image (jpg, svg, png)
	/resize - To resize image with pixels
	/compress - To compress the image""")
    return CONVERT


def handleSendRequest(urlToConver):
    pass


def photo(update: Update, context: CallbackContext) -> int:
    print("insert photo")
    photo_file = update.message.photo[-1].get_file()
    context.user_data["picture"] = photo_file.file_path
    #print(photo_file.file_path)
    # urlToConver = photo_file.file_path
    # handleSendRequest(urlToConver)
    update.message.reply_text(text="Please provide a type")
    return FORMAT_TO
    #return formatTo(photo_file.file_path ,update, context)
    #update.message.reply_text(response.text)


def formatTo(update: Update, context: CallbackContext) -> int:
    #print("formatTo: ", photoUrl)
    formatToConvert = update.message.text
    picture = context.user_data["picture"]
    print(formatToConvert)
    print(picture)
    url = "https://image-processing4.p.rapidapi.com/imageconvert"

    headers = {
        "X-RapidAPI-Host": "image-processing4.p.rapidapi.com",
        "X-RapidAPI-Key": Constants.API_KEY_SERVICE
    }
    querystring = {"imageUrl": picture, "outputType": formatToConvert}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    print(response.text)
    result = json.loads(response.text)
    update.message.reply_text(result["outPutUrl"])
    return ConversationHandler.END

def handleConvert(queryString, update: Update, context: CallbackContext) -> int:
    print("handleConvert")

def convert(update: Update, context: CallbackContext):
    update.message.reply_text("""You selected /convert""")
    update.message.reply_text(text="Please provide a picture")
    return PHOTO


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


def main() -> None:
    """Run the bot"""
    updater = Updater(
        Constants.TELEGRAM_KEY_SERVICE, use_context=True)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", convert)],
        states={
            # GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            CONVERT: [],
            PHOTO: [MessageHandler(Filters.photo, photo),
                    MessageHandler(Filters.regex("^(svg|jpg|png)$"), formatTo)],
            FORMAT_TO: [MessageHandler(Filters.text, formatTo), handleConvert],
            #HANDLE_CONVERT: [handleConvert]
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
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

#     Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
