import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7354008760:AAFAkP7mCjePndhg-qd8tq1KftC2muwy-zQ'
GROUP_CHAT_ID = 'https://t.me/+com6IJZZYRRjZWNl'  # Replace with your actual group chat ID

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bot started. Use /send to broadcast a message.')

def get_group_members():
    """Get the list of members in the group."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMembers?chat_id={GROUP_CHAT_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_message_to_members(update: Update, context: CallbackContext) -> None:
    """Send a message to all members of the group."""
    message = ' '.join(context.args)
    if not message:
        update.message.reply_text('Please provide a message to send.')
        return

    members = get_group_members()
    if members and 'result' in members:
        for member in members['result']:
            user_id = member['user']['id']
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={message}"
            requests.get(url)
        update.message.reply_text('Message sent to all members.')
    else:
        update.message.reply_text('Failed to retrieve group members.')

def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send", send_message_to_members))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
