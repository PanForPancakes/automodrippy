# miscellaneous
import os, re, discord, glob, json, os, os.path, math, random, time, threading

# fuzzywuzzy search
from fuzzywuzzy import process as fuzz



DEFAULT = "not_found.mp3"



# basic json-"db" "manager" for storing data
class JsonDB:
    data: dict = None
    __last_data: dict = None
    __filename: str = None
    __autosave_interval: int = None

    def save(self, force = True):
        if self.data == self.__last_data and not force:
            return

        with open(self.__filename, "w") as file:
            self.__last_data = self.data
            json.dump(self.__last_data, file)
    
    def __save(self):
        self.save(force = False)
        threading.Timer(interval = self.__autosave_interval, function = self.__save)

    def __init__(self, filename, autosave_interval = 300):
        self.__filename = filename
        self.__autosave_interval = autosave_interval

        with open(self.__filename) as file:
            self.__last_data = json.load(file)
            self.data = self.__last_data

        if self.__autosave_interval != None:
            self.__save()

# very clever index search
def vcis(what: object, where: list, gate: int = 75):
    found, accuracy = fuzz.extract(what, where, limit = 1)[0]

    if accuracy < gate:
        return None
    else:
        return {
            "index": where.index(found),
            "accuracy": accuracy
        }

# car finder helper function
def find_car(query: str, gate = None):
    if gate:
        search_result = vcis(query, cars, gate)
    else:
        search_result = vcis(query, cars)

    if not search_result:
        return None
    
    index = search_result["index"]
    accuracy = search_result["accuracy"]

    return {
        "name": cars[index],
        "url": f"https://awesomecars.neocities.org/ver2/{index + 1}.mp4",
        "accuracy": accuracy
    }

# simple embed generator
def create_embed(title, description):
    return discord.Embed(title = title, description = description)

# number to ordinal function
def to_ordinal(number):
    last_digit = number % 10 in [1, 2, 3]
    suffix = ["st", "nd", "rd"][last_digit] if last_digit in [1, 2, 3] else "th"
    return f"{number}{suffix}"

# duplicate finder
def find_duplicates(where: list):
    seen = set()
    buffer = []

    for element in where:
        if element in seen:
            buffer.append(element)
        else:
            seen.add(element)

    return buffer



# load cars info
with open("cars.txt") as lines:
    cars = [line.strip().lower() for line in lines]

duplicates = find_duplicates(cars)
if len(duplicates) > 0:
    print("Duplicate cars are found!")

    reverse_cars = cars[::-1]
    cars_count = len(cars)

    for element in duplicates:
        where = cars_count - reverse_cars.index(element) - 1
        print(f"\"{cars[where]}\" at line {where + 1}")

    print("Note: currently only last duplicates are shown, if there is >2 cars with same name this screen wouldn't tell you all of them immediately.")
    print("Exiting.")

    exit(1)

# open databases
name_db = JsonDB("name_data.json")
user_db = JsonDB("user_data.json")
frequency_db = JsonDB("frequency_db.json")

# create instance of discord.Client
intents = discord.Intents.default()
intents.message_content = True

dripcarbot = discord.Client(intents = intents)

async def post_leaderboards(message: discord.Message):
    total_posted = 0
    for car in frequency_db.data.keys():
        total_posted += frequency_db.data[car]

#    filename = "frequency_data.json"
#    
#    create_json(filename)
#
#    with open(filename, "r") as file:
#        data = json.loads(file.read())
#        length = 0
#        files = len(glob.glob(VIDEO_DIRECTORY) + glob.glob(IMAGE_DIRECTORY))
#
#        for d in data:
#            length += data[d]
#    
#    filename = "user_data.json"
#    
#    create_json(filename)
#
#    with open(filename, "r") as file:
#        data = json.loads(file.read())
#        list = []
#        
#        for d in data:
#            with open("name_data.json", "r") as other_file:
#                other_data = json.loads(other_file.read())
#                list.append((other_data[d], len(data[d])))
#
#    list.sort(key=lambda tup: tup[1])
#    
#    if len(list) > 5:
#        list = list[-5:]
#
#    list.reverse()
#
    description = ""
#    index = 0
#
#    for l in list:
#        index += 1
#        max_format = "**" if l[1] == files else ""
#        separator = "🚗🚙" if index % 2 == 0 else "🚙🚗"
#        description += f"{index}. {separator[0]} **{l[0]}** with {max_format}{l[1]}/{files}{max_format} cars {separator[1]}\n\n"
#
    await message.reply(embed = create_embed(f"car of fame (posted {total_posted} cars in total)", description))

async def reply_to_query(message: discord.Message, query: str):
#    length = len(query)
#
#    filename = "name_data.json"
#    
#    create_json(filename)
#
#    with open(filename, "r") as file:
#        data = json.loads(file.read())
#        data[author.id] = author.name
#
#    os.remove(filename)
#
#    with open(filename, "w") as file:
#        json.dump(data, file, indent=4)
#
#    while len(query):
#        videos = glob.glob(VIDEO_DIRECTORY) + glob.glob(IMAGE_DIRECTORY) 
#        videos_length = len(videos)
#        matches = []
#
#        try:
#            regex = re.compile(query.lower())
#            matches = [ s for s in videos if regex.search(s.replace("E:/!!!/absolute elite memes/cars\\", "").replace(".mp4", "").replace(".png", "")) != None ]
#        except:
#            query = query[:-1]
#            continue
#
#        if len(matches) != 0:
#            video = random.choice(matches)
#            preview = video.replace("E:/!!!/absolute elite memes/cars\\", "").replace(".mp4", "").replace(".png", "")
#            title = ""
#
#            filename = "frequency_data.json"
#            
#            create_json(filename)
#
#            with open(filename, "r") as file:
#                data = json.loads(file.read())
#                id = str(preview)
#                times_format = "time"
#
#                if id not in data:
#                    data[id] = 0
#                    times_format = "EVER SEEN"
#
#                data[id] += 1
#                times_seen = data[id]
#
#            os.remove(filename)
#
#            with open(filename, "w") as file:
#                json.dump(data, file, indent=4)
#
#            filename = "user_data.json"
#
#            with open(filename, "r") as file:
#                data = json.loads(file.read())
#                description = f"already seen"
#                id = str(author.id)
#
#                if id not in data:
#                    data[id] = []
#
#                if preview not in data[id]:
#                    data[id].append(preview)
#                    description = f"**+1**"
#                    title = "NEW "
#                    
#                description += f" ({len(data[id])}/{videos_length})" if len(data[id]) < videos_length else " (**all cars obtained**)"
#            
#            os.remove(filename)
#
#            with open(filename, "w") as file:
#                json.dump(data, file, indent=4)
#                
#            return (
#                create_embed(
#                    f"{title}[{preview}] (found {len(matches)}, {to_ordinal(times_seen)} {times_format})",
#                    f"🚗 {math.floor(len(query) / length * 100)}% accuracy, {description} 🚙"
#                ),
#                discord.File(video)
#            )
#
#        query = query[:-1]

    result = find_car(query, 1)

    # reply accordingly if car found
    if result:
        name = result["name"]
        url = result["url"]
        accuracy = result["accuracy"]

        await message.reply(url)
        await message.channel.send(embed = create_embed(f"found {name}!", f"🚗 {accuracy}% accuracy 🚙"))
        return
    
    # ...or reply with error message
    await message.reply(embed = create_embed("no car found", "🚗 choot choot 🚙 (0% accuracy)"), file = discord.File(DEFAULT))

@dripcarbot.event
async def on_message(message: discord.Message):
    # ignore bot messages
    if message.author == dripcarbot.user:
        return
    
    # ignore messages from non-text channels
    if message.channel.type != discord.channel.ChannelType.text:
        return

    # --- nc group: ignore spaces in the beginning
    # --- nc group: bot prefixes
    # --- nc group: ignore spaces after bot prefix
    # 1st ct group: user query
    regex = r"(?: *)(?:🚗|🚙|:dripcar:)(?: *)(.*)"

    # parse user message
    match = re.search(regex, message.content)

    # ignore if regex doesn't match
    if not match:
        return
    
    # get data from query
    query = match.group(1)

    # send leaderboards if query is empty
    if query == "":
        await post_leaderboards(message)
        return
    
    # ...or else reply to query
    await reply_to_query(message, query)

@dripcarbot.event
async def on_ready():
    # TODO: random presences
    await dripcarbot.change_presence(activity = discord.Game("videos of drip cars"))

dripcarbot.run(os.getenv("DRIPCARBOT_TOKEN"))