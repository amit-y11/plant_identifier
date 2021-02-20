# Plant Identifier Bot 🌵
<img src="plant.png" alt="logo" width="250px" height="250px"/>

A telegram bot for identifying plants:

You can send a screenshot of a plant to this bot and it will respond quickly with the identified plant in the picture! 

---
# Usage
* Click [here](https://t.me/plantIdentifyBot) to open the chat with the bot in the Telegram app
* Join this [Telegram channel](https://t.me/botsbyamit) in order to use this bot
---

# Captures
<img src="captures.png" alt="PlantIdentifier Bot"/>

--- 

# Installation : 
* Clone this repository using
```sh
$ git clone https://github.com/amit-y11/plant_identifier
```
* Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
* Get your bot token from [Bot Father](https://t.me/BotFather), If you dont't know how to get bot token read [this](https://core.telegram.org/bots#6-botfather)

* Get your plant.id api key from [here](https://web.plant.id/api-access-request/)

* Edit line 80 and paste your plant.id api key
```sh
80        api_key = "Your Api key from Plant.id"
```
* Edit line 141 and paste your Bot token
```sh
141       token="Your Bot Token"
```
#### Run Your Bot using following command :
```sh
$  python3 plant.py
```
