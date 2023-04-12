# ChatGPT-Telegram-Bot
OpenAI library based python telegram bot. 

Language: Ukrainian

<span style="color:yellow">Before using the bot, you need to install **python** and several libraries.
You also need to put tokens to the config and your username telegram to main file (details below)</span>

To host the bot, you need any device with a command line (for Windows, it's cmd, for Android, it's termux). Then install python (pkg install python), libraries (pip install nameOfLibrary). After you have configured the bot, you need to change the directory (cd /path/) to the folder where the bot files are located (! CONFIG and MAIN MUST BE IN THE SAME FOLDER!), and then run the bot (python main.py).
To turn off the bot you need to close python's console (Windows) or press Ctrl+C in command line (Windows and Android). Also if you right configured the bot you can type /kill in a telegram chat.

**Necessary python libraries:**
- openai
- aiogram

**Configuration:**
- Put OpenAI API key into '' in config.py
- Put telegram bot token into '' in config.py
- Put your username into '' in main.py (line 86)