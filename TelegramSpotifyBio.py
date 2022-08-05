import asyncio, json, requests, time
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import FloodWaitError
from telethon.sync import TelegramClient

api_id = 1131570
api_hash = '35bf2560c857273cc2129bd23be78bd8'
session = 'Your Telethon Session'
lastfm = 'Your LastFM Username'

def spotify():
    global play, about
    base_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
    userName = lastfm
    apiKey = '460cda35be2fbf4f28e8ea7a38580730'
    r = requests.get(base_url+userName+'&api_key='+apiKey+'&format=json')
    data = json.loads(r.text)
    latest_track = data['recenttracks']['track'][0]
    try:
        if latest_track['@attr']['nowplaying'] == 'true':
            artist = latest_track['artist']['#text']
            song = latest_track['name']
            now_playing = f"🎶 {artist} - {song}"
            if len(now_playing) > 67:
                about = now_playing[0:67] + '...'
            else:
                about = now_playing
            print(time.asctime(), '-', about)
            play = True
    except Exception as e:
        print(time.asctime(), '-', f'Error: {e}')
        play = False
    return play, about

# Then we need a loop to work with
loop = asyncio.get_event_loop()
client = TelegramClient(session, api_id, api_hash, sequential_updates=True).start()

# We also need something to run
async def main():
    full = await client(GetFullUserRequest('me'))
    bio = full.about
    print(time.asctime(), '-', bio)
    while True:
        try:
            spotify()
            if play == True:
                await client(UpdateProfileRequest(about = about))
            else:
                await client(UpdateProfileRequest(about = bio))
            time.sleep(60)
        except FloodWaitError as e:
            to_wait = e.seconds
            time.sleep(int(to_wait))

# Then, we need to run the loop with a task
loop.run_until_complete(main())