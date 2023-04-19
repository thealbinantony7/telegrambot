from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Load the links and numbers from a file or a database
links = {
    1: 'https://example.com/1',
    2: 'https://example.com/2',
    3: 'https://example.com/3'
}

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a number to get a link.")

# Define the message handler
def message(update, context):
    try:
        # Try to convert the message to an integer
        number = int(update.message.text)
        
        # Get the link corresponding to the number
        link = links[number]
        
        # Send the link to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=link)
    except (ValueError, KeyError):
        # Handle invalid messages
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please send a number.")

# Define the admin command handler
def admin(update, context):
    # Check if the user is an admin
    if update.message.from_user.username == 'admin_username':
        try:
            # Get the number and link from the message
            parts = update.message.text.split()
            number = int(parts[1])
            link = parts[2]
            
            # Add the link to the dictionary
            links[number] = link
            
            # Confirm the addition
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Link {link} added for number {number}.")
        except (ValueError, IndexError):
            # Handle invalid messages
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please send a number and a link.")
    else:
        # Handle unauthorized access
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthorized access.")

# Define the main function
def main():
    # Create the Updater and pass the bot token
    updater = Updater("BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, message))
    dp.add_handler(CommandHandler("admin", admin))

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
