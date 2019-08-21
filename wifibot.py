import datetime
import logging
import re

import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

token = 'token'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

claves = ''
ultimaActualizacion = datetime.datetime.min


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def wifi(bot, update):
    if diferenciaMeses() >= 1:
        actualizarClaves()
    update.message.reply_text(claves)


def force(bot, update):
    actualizarClaves()
    update.message.reply_text("Las contraseñas se actualizaron correctamente")


def diferenciaMeses():
    global ultimaActualizacion
    now = datetime.datetime.now()
    return (now.year - ultimaActualizacion.year) * 12 + now.month - ultimaActualizacion.month


def actualizarClaves():
    global claves
    global ultimaActualizacion
    payload = {'usuario': 'usuarioCEC',
               'contrasena': 'contraCECnia'}
    # login al cec
    r = requests.post('https://servicios.cec.uchile.cl/index.php', data=payload)
    # obtener pagina con datos de invitado
    data = requests.get('https://servicios.cec.uchile.cl/wifiInvitados_sistemaAntiguo.php', cookies=r.cookies)
    # crear parser
    soup = BeautifulSoup(data.text, 'html.parser')
    # obtener tabla con los datos clave - validez
    table = soup.find_all('table')[1].find_all('td')
    # eliminar titulos
    table[0:2] = []
    claves2 = ''
    for element in table:
        # regex para obtener los datos
        regex = re.compile("(?<=')[^']+(?=')")
        claves2 += regex.findall(str(element.renderContents()))[0] + '\n'
    # actualizar fecha de la ultima actualizacion
    if claves2 != claves:
        claves = claves2
        ultimaActualizacion = datetime.datetime.now()
    return claves


def main():
    updater = Updater(token)
    dp = updater.dispatcher
    # respuesta para comando /wifi
    dp.add_handler(CommandHandler("wifi", wifi))
    dp.add_handler(CommandHandler("force", force))
    dp.add_error_handler(error)
    # iniciar el bot
    updater.start_polling()
    # dejar corriendo
    updater.idle()


if __name__ == '__main__':
    main()
