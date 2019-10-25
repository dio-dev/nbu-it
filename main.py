import ssl
from functions.main import *
from aiogram.dispatcher.webhook import get_new_configured_app, SendMessage
from aiohttp import web
from daemons import start_checker

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv("token")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # Domain name or IP addres which your bot is located.

WEBHOOK_PORT = 443  # Telegram Bot API allows only for usage next ports: 443, 80, 88 or 8443
WEBHOOK_URL_PATH = '/'  # Part of URL

# This options needed if you use self-signed SSL certificate
# Instructions: https://core.telegram.org/bots/self-signed
WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

# Web app settings:
#   Use LAN address to listen webhooks
#   User any available port in range from 1024 to 49151 if you're using proxy, or WEBHOOK_PORT if you're using direct webhook handling
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3001
BAD_CONTENT = ContentTypes.AUDIO


loop = asyncio.get_event_loop()
#loop.create_task(start_checker())
bot = Bot(TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def cancel(message: types.Message):
    # Get current state context
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    # If current user in any state - cancel it.
    if await state.get_state() is not None:
        await state.set_state(state=None)

        return SendMessage(message.chat.id, 'Current action is canceled.')
        # Otherwise do nothing


async def unknown(message: types.Message):
    """
    Handler for unknown messages.
    """
    return SendMessage(message.chat.id,
                       f"I don\'t know what to do with content type `{message.content_type()}`. Sorry :c")


async def on_startup(app):
    # Demonstrate one of the available methods for registering handlers
    # This command available only in main state (state=None)
    dp.register_message_handler(start,
                                commands=['start'],
                                state='*')

    dp.register_callback_query_handler(start,
                                       lambda c: c.data and c.data == "back",
                                       state="*")

    dp.register_message_handler(start,
                                lambda m: m.text == "Искать заново",
                                state="*")

    dp.register_callback_query_handler(get_name,
                                       lambda c: c.data,
                                       state=UserStates.select_type)

    dp.register_message_handler(get_location,
                                lambda m: m.text,
                                state=UserStates.select_name)

    dp.register_callback_query_handler(get_location,
                                lambda c: c.data,
                                state=UserStates.select_name)

    dp.register_message_handler(show_result, content_types=ContentTypes.LOCATION, state=UserStates.get_location)

    dp.register_callback_query_handler(send_location,
                                       lambda c: c.data,
                                       state=UserStates.show_result)

    webhook = await bot.get_webhook_info()

    # If URL is bad
    if webhook.url != WEBHOOK_URL:

        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))
        # If you want to use free certificate signed by LetsEncrypt you need to set only URL without sending certificate.


async def on_shutdown(app):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':

    # Get instance of :class:`aiohttp.web.Application` with configured router.
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)

    # Setup event handlers.
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    # Start web-application.
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)
    # Note:
    #   If you start your bot using nginx or Apache web server, SSL context is not required.
    #   Otherwise you need to set `ssl_context` parameter.