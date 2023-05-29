# miscellaneous
import os, re, discord, os, os.path, logging, random

# thefuzz search
from thefuzz import process as fuzz

# sillydbmanager improvised databases
from sillydbmanager import JsonDictionaryDB, CsvListDB

# car finder helper function
def find_car(query: str, gate: int = 75):
    hashplussearchname = dict()
    for car_hash in cars.keys():
        hashplussearchname[car_hash] = cars[car_hash][2]

    results = fuzz.extractBests(query, hashplussearchname, limit = 20, score_cutoff = gate)

    if len(results) == 0:
        return None

    _, accuracy, hash = random.choice(results)

    car = cars[hash]

    return {
        "url": car[0],
        "name": car[1],
        "accuracy": accuracy
    }

# simple embed generator
def create_embed(title, description):
    return discord.Embed(title = title, description = description)

# number to ordinal function
def to_ordinal(number):
    last_digit = number % 10
    suffix = ["st", "nd", "rd"][last_digit - 1] if last_digit in [1, 2, 3] else "th"
    return f"{number}{suffix}"

# load cars info
def load_cars():
    raw_cars_db = CsvListDB("cars.csv")
    for car_entry in raw_cars_db.data_list:
        # cars[file_hash] = [file_link, visible_name, search_name]
        cars[car_entry[0]] = [car_entry[1], car_entry[2], car_entry[3]]

cars = {}
load_cars()

# open databases
name_db = JsonDictionaryDB(".automodrippy/name_data.json")
user_db = JsonDictionaryDB(".automodrippy/user_data.json")
frequency_db = JsonDictionaryDB(".automodrippy/frequency_data.json")

# create instance of discord.Client
intents = discord.Intents().default()
intents.message_content = True

automodrippy = discord.Client(intents = intents)

async def post_leaderboards(message: discord.Message):
    total_posted = 0
    for car in frequency_db.data_dict.keys():
        total_posted += frequency_db.data_dict[car]

    people = []
    for name in user_db.data_dict.keys():
        if name not in name_db.data_dict.keys():
            people.append((f"<@{name}>", len(user_db.data_dict[name])))
        else:
            people.append((name_db.data_dict[name], len(user_db.data_dict[name])))

    people.sort(key = lambda element: element[1])
    
    if len(people) > 5:
        people = people[-5:]

    people.reverse()

    description = ""

    for index in range(len(people)):
        person = people[index]
        max_format = "**" if person[1] == len(cars) else ""
        separator = "🚗🚙" if index % 2 == 0 else "🚙🚗"
        description += f"{index + 1}. {separator[0]} **{person[0]}** with {max_format}{person[1]}/{len(cars)}{max_format} cars {separator[1]}\n"

    await message.reply(embed = create_embed(f"car of fame (posted {total_posted} cars in total)", description))

async def reply_to_query(message: discord.Message, query: str):
    # update display name of author
    name_db.data_dict[str(message.author.id)] = message.author.display_name
    name_db.save()

    # deletes car suffix, copypaste of some code above
    query = re.sub(r"(.+) +?car", "\\1", query, 1)
    
    result = None
    for gate in range(90, 50, -10):
        result = find_car(query, gate)

        if result:
            break

    # reply accordingly and save data if car was found
    if result:
        name = result["name"]
        url = result["url"]
        accuracy = result["accuracy"]

        times_format = "time"
        if name not in frequency_db.data_dict.keys():
            times_format = "EVER SEEN"
            frequency_db.data_dict[name] = 1
            times_seen = 1
        else:
            frequency_db.data_dict[name] += 1
            times_seen = frequency_db.data_dict[name]

        description = "already seen"
        title = ""
        if str(message.author.id) not in user_db.data_dict.keys():
            user_db.data_dict[str(message.author.id)] = []

        if name not in user_db.data_dict[str(message.author.id)]:
            description = "**+1**"
            title = "NEW "
            user_db.data_dict[str(message.author.id)].append(name)

        random_tlds = [".com", ".xxx", ".xyz", ".love", ".io", ".roblox", ".volvo", ".kia", ".mercedes", ".bmw", ".cars", ".dripcar"]
        random_links = ["download-more-cars", "i-love-my-car", "hot-cars-watch-for-free", "dripcar-my-beloved", "i-have-car-videos", "car-share", "my-drip-car", "free-cars-watch-online"]

        # GENERATED URLS BOTH MIGHT AND MIGHT NOT EXIST
        # CONTENT ON THESE PAGES IS NOT CONTROLLED SO FOR YOUR SAFETY DO NOT VISIT GENERATED URLS

        lol = random_links[random.randint(0, len(random_links) - 1)] + random_tlds[random.randint(0, len(random_tlds) - 1)]

        await message.reply(f"{lol}: {url}")
        await message.channel.send(embed = create_embed(f"{title}[{name}] ({to_ordinal(times_seen)} {times_format})", f"🚗 {accuracy}% accuracy, {description} 🚙"))

        # save data
        frequency_db.save()
        user_db.save()

        return
    
    # ...or reply with error message
    await message.reply(embed = create_embed("no car found", "🚗 choot choot 🚙 (0% accuracy)"))

@automodrippy.event
async def on_message(message: discord.Message):
    # ignore bot messages
    if message.author == automodrippy.user:
        return
    
    # ignore messages from non-text channels
    if message.channel.type != discord.channel.ChannelType.text:
        return

    # --- nc group: ignore spaces in the beginning
    # --- nc group: bot prefixes
    # --- nc group: ignore spaces after bot prefix
    # 1st ct group: user query
    prefixes = ["🚗", "🚙", ":DripCar:"]
    regex = rf"(?: *)(?:{'|'.join(prefixes)})(?: *)(.*)"

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

@automodrippy.event
async def on_ready():
    logging.info(f"Add bot via this link: https://discord.com/api/oauth2/authorize?client_id={automodrippy.user.id}&permissions=52224&scope=bot")
    await automodrippy.change_presence(activity = discord.Game("videos of drip cars"))

automodrippy.run(os.getenv("AUTOMODRIPPY_TOKEN"))