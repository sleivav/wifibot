import logging
#import requests

from telegram.ext import Updater, CommandHandler

token = 'token'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

clave = 'ingenieria.uchile'
validez = 'Desde el 01 de junio del 2017'


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def wifi(bot, update):
    reply = clave + '\n' + validez
    update.message.reply_text(reply)


#def actualizarClave():
#    req = requests.get('https://servicios.cec.uchile.cl/')


def main():
    updater = Updater(token)
    dp = updater.dispatcher
    # respuesta para comando /wifi
    dp.add_handler(CommandHandler("wifi", wifi))
    dp.add_error_handler(error)
    # iniciar el bot
    updater.start_polling()
    # dejar corriendo
    updater.idle()


if __name__ == '__main__':
    main()
