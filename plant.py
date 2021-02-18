import telegram
from telegram import ChatAction, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters,CallbackQueryHandler,PicklePersistence
from telegram.ext.dispatcher import run_async
import logging
import os
import requests
import base64

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update,context):
	name=update.message.chat.first_name
	update.message.reply_text("Hi! "+name+"\nWelcome to Plant Identifier Bot, Send a clear image of a plant and i will try to recognise the plant in it\nWant to support this bot? click /donate \nRate this bot by clicking --> /rate")

@run_async	
def rate(update,context):
    update.message.reply_text("To give ratings to this bot click here\nhttps://t.me/BotsArchive/1504")

@run_async    
def donate(update,context):
    update.message.reply_text("If you really liked ❤️ this bot and want to support it and help me to pay for the server expenses , you can donate to me any amount you wish because _every penny counts\.\.\._\nYour support can really help this bot to run *24x7*  \n*Payment Options* \n\n1\. [Paypal](https://paypal.me/yamit11) \n\n2\. UPI : `amity11@kotak` \n\n3\. [Debit/Credit cards/UPI](https://rzp.io/l/amity11)\nIf you want different payment option please contact @amit\_y11",parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
def encode_files(file_names):
    files_encoded = []
    for file_name in file_names:
        with open(file_name, "rb") as file:
            files_encoded.append(base64.b64encode(file.read()).decode("ascii"))
    return files_encoded
    
keyboard=[[InlineKeyboardButton("➕Add Image ➕", callback_data="add"), InlineKeyboardButton ("⚙️ Process ⚙️",callback_data="process")]]
reply_markup = InlineKeyboardMarkup(keyboard)

@run_async    
def identify (update,context):
	####################
	#Getting user info
    global chat_id
    chat_id=update.effective_chat.id
    #####################

    check=context.bot.get_chat_member("@botsbyamit",update.effective_chat)
    if check['status']=="member" or check['status']=="creator":
        try:
            images = context.user_data['images']
        except KeyError:
            images = context.user_data['images'] = []
        i=len(images)+1
        file="plant"+str(i)+".jpg"
        
        file_id = update.message.photo[-1].file_id
        try:
            fileid=context.user_data['fileid']
        except KeyError:
            fileid=context.user_data['fileid']=[]        
        fileid.insert(i-1,file_id)
        
        newFile=context.bot.get_file(file_id)
        newFile.download(file)
        images.insert(i-1,file)
        context.bot.send_message(chat_id=chat_id,text="Click Add image option to add another image of the plant or click process button to start processing with the sent image",reply_markup=reply_markup)
    else:
        update.message.reply_text("You need to be a member of @botsbyamit in order to use this bot.\n\nPlease join @botsbyamit and send your image again to continue.")

        
#############################
@run_async
def button(update,context):
    images=context.user_data['images']
    query=update.callback_query
    query.answer()
    if query.data=="process":
        try:
            query.edit_message_text("Processing .....")
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id ,action=telegram.ChatAction.TYPING)
            api_key = "Your Api key from Plant.id"
            image=encode_files(images)
            json_data = {"images": image,"modifiers": ["similar_images"],"plant_details": ["common_names", "url", "wiki_description", "taxonomy"]}
            response = requests.post("https://api.plant.id/v2/identify", json=json_data, headers={"Content-Type": "application/json","Api-Key": api_key}).json()
            data=response ['suggestions'][0]
            name=data['plant_name']
            probability=data['probability']
            data1=data['plant_details']
            scientific_name=data1['scientific_name']
            common=data1['common_names']
            try:
                common=", ".join(common)
            except:
                common="<i>None</i>"
            url=data1['url']
        
        
            message="<b>Plant Name : </b>"+name+"\n\n<b>Probability : </b>"+str(probability*100)+"\n\n<b>Scientific name : </b>"+scientific_name+"\n\n<b>Common Names : </b>"+common+"\n\n<b>Wikipedia Page : </b>"+url+"\n\n<i>powered by </i><a href='https://web.plant.id/plant-identification-api/'>Plant.id Api</a>\n\n"
            query.edit_message_text(message,parse_mode=telegram.ParseMode.HTML)
            images.clear()
        except Exception as e:
            query.edit_message_text("Limit for this week has been reached please check back again next week")
            images.clear()
    
    elif query.data=="add":
        query.edit_message_text(text="Send another image of the same plant")
    return images

@run_async
def clear(update,context):
	try:
		images=context.user_data['images']
	except KeyError:
		update.message.reply_text("You haven't sent any image of the plant yet")
	images.clear()
	update.message.reply_text("All images removed")

@run_async
def remove(update,context):
    try:
        images=context.user_data['images']
    except KeyError:
        update.message.reply_text("You haven't sent any image of the plant yet")
    if len(images)==0:
        update.message.reply_text("You haven't sent any image of the plant yet")
    else:
        images.pop()
        update.message.reply_text("Last image sent by you is been removed",reply_markup=reply_markup)
	
def getinfo(update,context):
	try:
		images=context.user_data['images']
	except KeyError:
		update.message.reply_text("You have not sent any images yet")
	info=len(images)
	update.message.reply_text("You have sent "+str(info)+" images")
	
	

persistence=PicklePersistence('plantdata')
def main():   
    token="Your Bot Token"
    updater = Updater(token,use_context=True, persistence=persistence)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('donate',donate))
    dp.add_handler(CommandHandler('rate',rate))
    dp.add_handler(MessageHandler(Filters.photo, identify))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler ('removeall',clear))
    dp.add_handler(CommandHandler ('removelast', remove))
    dp.add_handler(CommandHandler ("getinfo",getinfo))
    updater.start_polling()
    updater.idle()
 
	
if __name__=="__main__":
	main()
