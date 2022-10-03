import requests, json

class Commands:
    def help(cl, chat, user, args):
        post(cl, "Hi! I'm a work-in-progress meower bot created by @theotherhades (Find me in the meower discord)\nCurrently I'm featureless, but stay tuned 😉", chat = chat)

    def whois(cl, chat, user, args):
        target_user = args[0]
        userinfo = json.loads(requests.get(f"https://api.meower.org/users/{target_user}").text)

        if "created" in userinfo.keys():
            response = f"-- {target_user.upper()} --\nUsername: {userinfo['_id']}\nIs banned: {'yes' if userinfo['banned'] == True else 'no'}\nCreated (for now): {userinfo['created']}"
        else:
            response = f"-- {target_user.upper()} --\nUsername: {userinfo['_id']}\nIs banned: {'yes' if userinfo['banned'] == True else 'no'}"

        post(cl, response, chat = chat)

def post(cl, msg: str, chat = "home"):
    """
    Post to meower home, or a chat if specified
    """
    if chat == "home":
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_home", "val": msg}})
    else:
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "post_chat", "val": {"chatid": chat, "p": msg}}})