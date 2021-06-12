# <h1 align=center>Plant Identifier Bot 🌵</h1>

<p align=center><img src="images/plant.png" alt="logo" width="250px" height="250px"/></p>

<h3 align=center>A telegram bot for identifying plants</h3>



## About

You can send an image of a plant to this bot and it will respond quickly with the identified plant in the picture!

Start chat with this bot on [telegram](https://telegram.me/plantidentifybot)


## Screenshots
<img src="images/captures.png" alt="PlantIdentifier Bot"/>

--- 
## Requirements

* Bot token from [Bot Father](https://t.me/BotFather), If you don't know how to get bot token, read [this](https://core.telegram.org/bots#6-botfather)

* Plantnet.org api key, get your api key from [here](https://my.plantnet.org/)

---
## Installation 

#### You can fork the repo and deploy it on Heroku :)  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

OR

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
#### Run Your Bot using the following command :
```sh
$  python3 plant.py
```
