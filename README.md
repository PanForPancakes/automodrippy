# automodrippy

currently WIP  
*expect the unexpected*

## Usage

The bot uses the syntax 🚗 (`:red_car:`) or 🚙 (`:blue_car:`) or :trollface: (`:DripCar:`) at the start of a message.
Anything after prefix is treated as query.

- If query is empty, leaderboards are shown displaying the top 5 people with the most amount of seen media.

- Otherwise query is treated as a search query and is being searched with fuzzy search.

## Privacy

This Discord bot will process every message internally, messages aren't logged but some data is still collected.

Data that is saved/collected:
- User ID with displayed nickname
- Hashes of files that were found by user

## Setup (Docker / Podman)

1. Download or clone the repository, then `cd` into that folder:

```sh
git clone https://github.com/PanForPancakes/automodrippy.git
cd automodrippy
```

2. Run the convenience script to automatically deploy container, it will guide you through installation:

```sh
./deploy-container.sh
```

## "But I'm searching for Setup (Windows)"

Sorry, my mini-server runs linux with podman and because of that I didn't bother making scripts/detailed guides.

But if you okay with keeping some python file running you can probably do something like this (don't forget to replace `<token>` with your bot token):

```sh
git clone https://github.com/PanForPancakes/automodrippy.git
cd automodrippy
mkdir automodrippy_data
set AUTOMODRIPPY_TOKEN=<token>
python automodrippy.py
```

This snippet assumes that you have git installed and in your PATH, but you can always just extract latest source code and `cd` into its directory.