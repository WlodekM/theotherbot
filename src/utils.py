import json, os, src.bot as bot

def load_credentials():
    """
    Get bot's credentials
    """
    try:
        # When running locally
        with open("CREDENTIALS.json", "r") as f:
            return json.loads(f.read())
    
    except FileNotFoundError:
        # When deploying via railway
        return {
            "username": os.environ["CLIENT_USERNAME"],
            "password": os.environ["CLIENT_PASSWORD"]
        }

def get_prefix():
    """
    Get bot's command prefix
    """
    return "idk"

def get_commands():
    """
    Get bot's commands
    """
    return {
        "help": bot.Commands.help,
        "botinfo": bot.Commands.botinfo,
        "whois": bot.Commands.whois,
        "stats": bot.Commands.stats,
        "dice": bot.Commands.dice,
        "define": bot.Commands.define
    }