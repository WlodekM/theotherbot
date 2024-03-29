import requests
import json
import time
import src.bot as bot
import src.utils as utils
from cloudlink import CloudLink
from threading import Thread

class Bot:
    def on_connect():
        print("yourmother is online (check at https://svelte.meower.org)")

        # Pinger
        def pinger():
            while True:
                time.sleep(15)
                cl.sendPacket({"cmd": "ping", "val": ""})

        cl_pinger = Thread(target = pinger)
        cl_pinger.daemon = True
        cl_pinger.start()

        # Setup stuff
        cl.sendPacket({
            "cmd": "direct",
            "val": {
                "cmd": "ip",
                "val": requests.get("https://api.meower.org/ip").text
            }
        })
        cl.sendPacket({"cmd": "direct", "val": {"cmd": "type", "val": "py"}})
        cl.sendPacket({"cmd": "direct", "val": "meower", "listener": "trust"})

    def on_packet(packet):
        packet = json.loads(packet)
        if ("listener" in packet) and (packet["listener"] == "trust"):
            credentials = utils.load_credentials()
            cl.sendPacket({
                "cmd": "direct",
                "val": {
                    "cmd": "authpswd",
                    "val": {
                        "username": credentials["username"],
                        "pswd": credentials["password"]
                    }
                },
                "listener": "auth"
            })
        
        elif ("mode" in packet["val"]) and (packet["val"]["mode"] == "auth"):
            print("yourmother is online (check at https://svelte.meower.org)")

        elif "post_origin" in packet["val"]:
            packet = packet["val"]
            # packet_lower = packet["p"].lower()

            if packet["u"] == "Discord":
                packet["p"] = packet["p"].replace(f"{packet['p'].split(':')[0]}: ", "")
                packet["u"] = packet["p"].split(":")[0]

            if packet["p"].startswith(utils.get_prefix() + " "):
                cmd = packet["p"].split()[1]
                cmds = utils.get_commands()

                if cmd in cmds:
                    args = list()

                    for i in packet["p"].replace(f"{utils.get_prefix()} {cmd} ", "").split():
                        args.append(i)
                    
                    cmds[cmd](cl, packet["post_origin"], packet["u"], args)
                    
                    # Keep track of how many commands and whois commands have been used
                    analytics = list()
                    for i in json.loads(requests.get("https://api.meower.org/users/yourmother").text)["quote"].split(";"):
                        analytics.append(int(i))
                    
                    new_analytics = list()
                    new_analytics.append(str(analytics[0] + 1))
                    if cmd == "whois": new_analytics.append(str(analytics[1] + 1))
                    
                    if len(new_analytics) == 2:
                        new_quote = f"{new_analytics[0]};{new_analytics[1]}"
                    else:
                        new_quote = f"{new_analytics[0]};{analytics[1]}"

                    cl.sendPacket({"cmd": "direct", "val": {
                        "cmd": "update_config",
                        "val": {
                            "unread_inbox": True,
                            "theme": "blue",
                            "mode": False,
                            "bgm": True,
                            "bgm_song": 2,
                            "layout": "new",
                            "pfp_data": 6,
                            "quote": new_quote,
                            "sfx": True,
                        }
                    }})
                
                else:
                    print(f"Unknown command: {packet['p']}")

    def on_error(error):
        print(f"Ignoring error:\n\n{error}")

    def on_close():
        print("Yourmother was disconnected 💀\nAttempting to reconnect...")
        cl.state = 0
        cl.client(ip = "wss://server.meower.org/")

if __name__ == "__main__":
    cl = CloudLink(debug = True)
    
    cl.callback("on_connect", Bot.on_connect)
    cl.callback("on_packet", Bot.on_packet)
    cl.callback("on_error", Bot.on_error)
    cl.callback("on_close", Bot.on_close)

    cl.client(ip = "wss://server.meower.org/")