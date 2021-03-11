import telegram
from telegram.ext import updater, Updater, CommandHandler, MessageHandler
import config
import requests
from readability import Document

sendFile = False

def sitegetter(bots, update, args):
    url = args[0]
    raw = args[1] == "true"

    response = requests.get(url)

    if not sendFile:
        doc = Document(response.text)
        if raw is False:
            print('summary')
            text = doc.summary()
        else:
            text = doc.content()

        line = text
        n = 4000
        output = [line[i:i + n] for i in range(0, len(line), n)]



        for a in output:
            bots.send_message(chat_id=update.message.chat_id, text=a)
    else:
        with open('output.html', 'w+') as out:
            out.write(response.text)
            bots.send_document(chat_id=update.message.chat_id, document=open('output.html', 'rb'))






updater = Updater(config.TOKEN,use_context=False)
bot = updater.bot
dp = updater.dispatcher


def start(bots, update):
    bots.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    bots.send_message(chat_id=update.message.chat_id, text=bots.get_me())



def main():

    # Start the Bot
    updater.start_polling()
    updater.idle()


def filetoggle(bot,update):
    global sendFile
    sendFile = not sendFile
    bot.send_message(chat_id=update.message.chat_id, text="{} File toggle ".format(sendFile))

def register_handlers():
    dp.add_handler( CommandHandler('start',start))
    dp.add_handler( CommandHandler('stack',stackSearch,pass_args=True))
    dp.add_handler( CommandHandler('site',sitegetter,pass_args=True))
    dp.add_handler( CommandHandler('file',filetoggle))

def stackSearch(bot, update,args):


    terms = args


    url = "https://stackoverflow.com/search?q="

    response = requests.get(url+"+".join(terms))

    if not sendFile:
        line = response.content
        n = 4000
        output = [line[i:i + n] for i in range(0, len(line), n)]

        for a in output:
            bot.send_message(chat_id=update.message.chat_id, text=a)
    else:
        with open('output.html', 'w+') as out:
            out.write(response.text)
            bot.send_document(chat_id=update.message.chat_id, document=open('output.html', 'rb'))



if __name__ == '__main__':
    register_handlers()
    main()
    # sitegetter("https://stgackoverflow.com/documentation/",True)
    # print(stackSearch("Python how to remove whitespace replace"))
    # print(sitegetter("https://stackoverflow.com/questions/47986068/how-to-remove-whitespace-at-specfic-position-index-of-python-string",True))