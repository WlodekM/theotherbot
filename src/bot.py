class Commands:
    def help(cl, chat, user, args):
        post(cl, "Hi! I'm a work-in-progress meower bot created by @theotherhades (Find me in the meower discord)\nCurrently I'm featureless, but stay tuned 😉", chat = chat)

def post(cl, msg: str, chat = "home"):
    """
    Post to meower home, or a chat if specified
    """
    if chat == "home":
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_home", "val": msg}})
    else:
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_chat", "val": {"chatid": chat, "p": msg}}})