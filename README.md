# Plant Identifier Bot 🌵

### Show some :heart: and :star: the repo

<img src="plant.png" alt="logo" width="250px" height="250px"/>

A telegram bot for identifying plants:

You can send a screenshot of a plant to this bot and it will respond quickly with the identified plant in the picture! 

---
## Screenshots
<img src="captures.png" alt="PlantIdentifier Bot"/>

--- 
## Requirements

* Bot token from [Bot Father](https://t.me/BotFather), If you dont't know how to get bot token read [this](https://core.telegram.org/bots#6-botfather)

* Plantnet.org api key, get your api key from [here](https://my.plantnet.org/)

#### You can fork the repo and deploy it on Heroku :)  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---
## Installation 
* Clone this repository using
```sh
$ git clone https://github.com/amit-y11/plant_identifier
```
* Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
* Edit line 15 and paste your plantnet.org api key
```sh
15        api_key = "Your Api key from Plant.id"
```
* Edit line 16 and paste your Bot token
```sh
16       token="Your Bot Token"
```
#### Run Your Bot using following command :
```sh
$  python3 plant.py
```
