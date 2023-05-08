import requests
import json
import time

##### SETUP #####
    # https://dev.twitch.tv/
    
client_id = ""
client_secret = ""
channel_name = "" # ex. -> channel_name = "kaanflix" 
discord_webhook_url = ""

url = "https://id.twitch.tv/oauth2/token"
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}
response = requests.post(url, params=params)
data = json.loads(response.text)
oauth_token = data["access_token"]

url = "https://api.twitch.tv/helix/streams"
headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {oauth_token}"
}
params = {
    "user_login": channel_name
}

previous_stream_id = ""

#####  WEBHOOK & MESSAGES  #####
while True:
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)
    
    if len(data["data"]) > 0:
        if data["data"][0]["id"] != previous_stream_id:
            previous_stream_id = data["data"][0]["id"]
            channel_api_url = f"https://api.twitch.tv/helix/users?login={channel_name}"
            response = requests.get(channel_api_url, headers=headers)
            channel_data = json.loads(response.content)

            message = {
                "username": "Twitch Notification Tool", # optional and changeable
                "avatar_url": "https://i.pinimg.com/564x/3f/44/3a/3f443ad4508b8a45106c9ac08f11798d.jpg", # optional and changeable
                "embeds": [   # optional and changeable but be careful 
                    {
                        "author": {
                            "name": channel_name,
                            "url": f"https://www.twitch.tv/{channel_name}",
                            "icon_url": channel_data["data"][0]["profile_image_url"]
                        },
                        "title": f"{channel_name} is now live streaming!", 
                        "url": f"https://www.twitch.tv/{channel_name}",
                        "thumbnail": {
                            "url": channel_data["data"][0]["profile_image_url"]
                        },
                        "color": 6570404,
                        "description": data["data"][0]["title"],
                        "fields": [
                            {
                                "name": "Category",
                                "value": data["data"][0]["game_name"],
                                "inline": True
                            }
                        ]
                    }
                ]
            }
            requests.post(discord_webhook_url, json=message)

    else: 
        if previous_stream_id != "":
            previous_stream_id = ""
            message = {
                "username": "Twitch Notification Tool",
                "avatar_url": "https://i.pinimg.com/564x/53/89/b3/5389b33208ada20b074a9c5b6723f662.jpg",
                "embeds": [
                    {
                        "author": {
                            "name": channel_name,
                            "url": f"https://www.twitch.tv/{channel_name}",
                            "icon_url": channel_data["data"][0]["profile_image_url"]
                        },
                        "title": f"{channel_name} has stopped streaming!",
                        "thumbnail": {
                            "url": channel_data["data"][0]["profile_image_url"]
                        },
                        "color": 15158332
                    }
                ]
            }
            requests.post(discord_webhook_url, json=message)
            print(f"{channel_name} has stopped streaming.")
        print(f"{channel_name} is not streaming now.")
    time.sleep(10)