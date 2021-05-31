import telegram
from telegram import ChatAction, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters,CallbackQueryHandler,PicklePersistence
from telegram.ext.dispatcher import run_async
import logging
import requests
import wikipedia
import os
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

##########################
api_key = os.environ.get("api_key")                      #Your api key from plantnet.org
bot_token= os.environ.get("bot_token")                   #Your bot token

@run_async
def start(update,context):
	name=update.message.chat.first_name
	update.message.reply_text("Hi! "+name+"\nWelcome to Plant Identifier Bot, Send a clear image of a plant and i will try to recognise the plant in it")
    
keyboard=[[InlineKeyboardButton("➕Add Image ➕", callback_data="add"), InlineKeyboardButton ("🔍 Identify 🔍",callback_data="process")]]
reply_markup = InlineKeyboardMarkup(keyboard)
keyboard1=[[InlineKeyboardButton("Flower",callback_data='flower'),InlineKeyboardButton("Leaf",callback_data='leaf'),InlineKeyboardButton("Fruit",callback_data='fruit'),InlineKeyboardButton("Bark",callback_data='bark')]]
reply_markup1=InlineKeyboardMarkup(keyboard1)

@run_async    
def identify (update,context):
    chat_id=update.effective_chat.id
    try:
        images = context.user_data['images']
    except KeyError:
        images = context.user_data['images'] = []
    try:
        organs = context.user_data['organs']
    except KeyError:
        organs = context.user_data['organs'] = []
    file_id = update.message.photo[-1].file_id
    try:
        fileid=context.user_data['fileid']
    except KeyError:
        fileid=context.user_data['fileid']=[]        
    fileid.append(file_id)
    
    imageinfo=context.bot.get_file(file_id)
    images.append(imageinfo['file_path'])
    context.bot.send_message(chat_id=chat_id,text="Select the part of the plant that your image represents",reply_markup=reply_markup1)
 
@run_async
def button(update,context):
    images=context.user_data['images']
    organs=context.user_data['organs']
    fileid=context.user_data['fileid']
    query=update.callback_query
    query.answer()
    if query.data =="flower" or query.data == 'leaf' or query.data =='fruit' or query.data == 'bark':
        organs.append(query.data)
        query.edit_message_text("Click Add image button to add another image of the plant or click Identify button to start Identifying plant with the sent image",reply_markup=reply_markup)
    if query.data=="process":
        try:
            query.edit_message_text("Identifying plant .....")
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id ,action=telegram.ChatAction.TYPING)
            params = {"api-key":api_key,"images":images,"organs":organs}
            r = requests.get("https://my-api.plantnet.org/v2/identify/all",params=params)
            if r.status_code == 200:
                response=r.json()
                name=response['results'][0]['species']['scientificNameWithoutAuthor']
                probability=response['results'][0]['score']
                scientific_name=response['results'][0]['species']['scientificName']
                common=', '.join(response["results"][0]['species']['commonNames'])
                try:
                    a=wikipedia.page(name)
                    url=a.url
                except Exception:
                    url="<i>Not Found</i>"
                message=f"<b>Plant Name : </b>{name}\n\n<b>Probability : </b>{probability*100}\n\n<b>Scientific name : </b>{scientific_name}\n\n<b>Common Names : </b>{common}\n\n<b>Wikipedia Page : </b>{url}"
                query.edit_message_text(message,parse_mode=telegram.ParseMode.HTML)
                fileid.clear()
                images.clear()
                organs.clear()
            else:
                query.edit_message_text("Something went wrong!")
                fileid.clear()
                images.clear()
                organs.clear()
        except Exception as e:
            print(e)
            query.edit_message_text("Something went wrong!")
            fileid.clear()
            images.clear()
            organs.clear()

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
    token=bot_token
    updater = Updater(token,use_context=True, persistence=persistence)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(MessageHandler(Filters.photo and Filters.private, identify))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler ('removeall',clear))
    dp.add_handler(CommandHandler ('removelast', remove))
    dp.add_handler(CommandHandler ("getinfo",getinfo))
    updater.start_polling(clean=True)
    print("Bot Started")
    updater.idle()
 
	
if __name__=="__main__":
	main()
