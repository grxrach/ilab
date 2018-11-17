"""
iLAB Demo Bot
"""

TOKEN = "556507843:AAHyeGc8p0rp1mTKpmCtO_MZaaw5ZUmuYHU"
URL = "https://api.telegram.org/bot556507843:AAHyeGc8p0rp1mTKpmCtO_MZaaw5ZUmuYHU/"

#Telegram imports
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import time
import requests
from datetime import datetime, date, timedelta

#Google Sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

#Google Sheets API authentication
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/rachelganrx/DDG_Chatbot/cred4.json", scope)
client = gspread.authorize(creds)

#Specifying sheet in Google Sheet
sh = client.open("Divorce_Docs")
# sheet1 = client.open("Divorce_Docs").sheet1
sheet1 = sh.worksheet("Sheet3")


# Enable logging for Telegram
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Specifying range (Telegram)
START_MENU, CATEGORY, GOTDIVDOCS, DIVWHICHDOC, DIVCHECKDATE, GOTPFNAME, GOTPFNRIC, MOA_INTIME, MOA_OUTOFTIME,\
GOTDFNAME, GOTDFNRIC, CONTEST_DIV_CHOICE, BANKRUPT_CHOICE, GOT_ADDRESS, CUSTODY_CHOICE, CUSTODY_CONTEST_CHOICE,\
ACCESS_CONTEST_CHOICE, CHILD_MAINT_CHOICE, CHILD_MAINT_DECISION, PROPERTY_QUERY, ASSETS_QUERY, ASSETS_EXP_CHOICE,\
ASSETS_DECISION, WIFE_MAINT_EXP_CHOICE, WIFE_MAINT_DECISION, COSTS_QUERY, COSTS_DECISION, H_OR_W, DFWIFE_MAINT_DECISION, \
GOT_DF_ADDRESS, GOT_DF_HP, MOA_COMPLETED, OTHER_OPTIONS = range(33)


# Telegram Bot Functions
def start(bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    
    #Getting user details
    user = update.message.from_user
    
    #Reply keyboard
    reply_keyboard= [   ['Divorce'], 
                        ['Custody of children'], 
                        ['Maintenance'],
                        ['Probate / Letters of Admin'], 
                        ['Mental Capacity Act / Deputyship'], 
                        ['Personal injury'],
                        ['Monetary claim'],
                        ['Other']                       ] 
                       
    update.message.reply_text("Hi %s! Welcome to iLAB." % user.first_name)
    time.sleep(1)
    update.message.reply_text("I'm here to give you legal information, and also help you figure out if LAB can assist for your type of problem.")
    time.sleep(1)
    update.message.reply_text("I'll be asking you a bunch of questions that will help me understand how best to help you.")
    time.sleep(1)
    update.message.reply_text("Okay! Let's get started.")
    time.sleep(1)
    update.message.reply_text("Which of the following categories does your problem fall into?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)) 
    return CATEGORY

def start_menu (bot, update):
    reply_keyboard= [   ['Divorce'], 
                        ['Custody of children'], 
                        ['Maintenance'],
                        ['Probate / Letters of Admin'], 
                        ['Mental Capacity Act / Deputyship'], 
                        ['Personal injury'],
                        ['Monetary claim'],
                        ['Other']                       ] 
    update.message.reply_text("Please select the matter that you need assistance with.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CATEGORY

def tobedefined (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    update.message.reply_text("Oops, this part is still under construction!")
    time.sleep(1)
    update.message.reply_text("Type 'back' to return to start menu.")
    return START_MENU


def divorce_start (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    # Reply to user
    reply_keyboard =    [   ['Yes'],
                            ['No'],
                            ['Not sure']  ]
    update.message.reply_text("Got it, you need help with a divorce matter.")
    time.sleep(1)
    update.message.reply_text("Have you received Court documents yet?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return GOTDIVDOCS 

def div_which_doc (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    reply_keyboard =    [   ['A'],
                            ['B'],
                            ['C'],
                            ['None of the above']  ]
    update.message.reply_text("Okay, you've received Court documents.")
    time.sleep(1)
    update.message.reply_text("Which of the following looks most like the document you received?")
    time.sleep(1)
    update.message.reply_text("Picture A: Picture of divorce Writ")
    time.sleep(1)
    update.message.reply_text("Picture B: Picture of a judgment")
    time.sleep(1)
    update.message.reply_text("Picture C: Picture of Registrar's Notice")
    time.sleep(1)
    update.message.reply_text("If what you got doesn't look like any of the above documents, please select 'None of the above'", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return DIVWHICHDOC

def gotwrit (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    update.message.reply_text("Mmm ok, you received a divorce Writ.")
    time.sleep(1)
    update.message.reply_text("When did you receive this?")
    time.sleep(1)
    update.message.reply_text("Please key in the exact date you received the Writ in the following format: DD/MM/YYYY")
    return DIVCHECKDATE

def div_check_date (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input
    text = update.message.text.strip()
    #Store user input in dictionary user_data
    user_data["date writ received"] = text
    #Validate time from date received
    str_date = text.split("/")
    int_date = [int(x) for x in str_date]
    date_received = date(int_date[2], int_date[1], int_date[0])
    todays_date = date(datetime.now().year, datetime.now().month, datetime.now().day)
    delta = (todays_date - date_received).days
    moa_deadline_raw = str(date_received + timedelta(days=8))
    moa_deadline_strip = datetime.strptime(moa_deadline_raw, '%Y-%m-%d')
    moa_deadline = moa_deadline_strip.strftime('%d %b %Y')
    user_data["moa deadline"] = moa_deadline
    #Segregate response based on whether in time or out of time
    if delta <=8: 
        reply_keyboard =    [   ['Yes'],
                                ['No']          ]
        update.message.reply_text("Okay, you received the Writ %d days ago." % delta)
        time.sleep(1)
        update.message.reply_text("That's good, because you need to submit your Memorandum of Appearance to Court within 8 days of receiving the Writ.")
        time.sleep(1)
        update.message.reply_text("In your case, it means that you need to submit this by {}.".format(moa_deadline))
        time.sleep(1)
        update.message.reply_text("Do you need help filling in the Memorandum of Appearance? I can help you generate one.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return MOA_INTIME
    else:
        reply_keyboard =    [   ['Option 1'],
                                ['Option 2']          ]
        update.message.reply_text("I see that you received the Writ %d days ago." % delta)
        time.sleep(1)
        update.message.reply_text("You actually need to fill up and submit the Memorandum of Appearance (MOA) within 8 days of receiving the Writ.")
        time.sleep(1)
        update.message.reply_text("In your case, you should have submitted this by {}.".format(moa_deadline))
        time.sleep(1)
        update.message.reply_text("You have two options:")
        time.sleep(1)
        update.message.reply_text("(1) You can do it yourself, i.e. ask the Plaintiff/Plaintiff's lawyer for permission to file the MOA out of time.")
        time.sleep(1)
        update.message.reply_text("(2) You can come down to the Bureau for advice.")
        time.sleep(1)
        update.message.reply_text("Which option do you prefer?", 
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return MOA_OUTOFTIME

#FILLING THE MOA

def moa_getpfname (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    update.message.reply_text("Sure, I'll help you with filling up the MOA.")
    time.sleep(1)
    update.message.reply_text("I'll be asking you some questions that will help me generate the MOA for you.")
    time.sleep(1)
    update.message.reply_text("First question: Look at the Writ. What's the Plaintiff's name as written there?")
    return GOTPFNAME

def fillpfname (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input
    text = update.message.text
    text_upper = text.upper()
    #Store user input
    user_data["pf name"] = text.title()
    #Update excel
    sheet1.update_acell("C5", text_upper)
    #Reply user
    update.message.reply_text("Got it.")
    time.sleep(1)
    update.message.reply_text("Next, I need {}'s NRIC number.".format(user_data["pf name"]))
    return GOTPFNRIC

def fillpfnric (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input
    text = update.message.text.upper()
    #Update excel
    sheet1.update_acell("D6", text)
    #Reply user
    update.message.reply_text("Thanks for that. Now I need your name as stated on the divorce Writ.")
    return GOTDFNAME

def filldfname (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input
    text = update.message.text.upper()
    text_dict = text.title()
    #Save to dictionary
    user_data["df name"] = text_dict
    #Update excel
    sheet1.update_acell("C10", text)
    #Reply user
    update.message.reply_text("Got it.")
    time.sleep(1)
    update.message.reply_text("Next, I need your NRIC number.")
    return GOTDFNRIC

def filldfnric (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input
    text = update.message.text.upper()
    #Save to dict
    user_data["df nric"] = text
    #Update excel
    sheet1.update_acell("D11", text)
    #Reply user
    reply_keyboard =    [       ["I wish to contest"],
                                ["I don't want to contest"]          ]
    update.message.reply_text("OK. We've settled the basic stuff.")
    time.sleep(1)
    update.message.reply_text("Read through the Statement of Particulars (SOP) now. This should be the second document attached behind the Writ.")
    time.sleep(1)
    update.message.reply_text("The SOP contains the facts that your spouse is relying on to get a divorce from you.")
    time.sleep(1)
    update.message.reply_text("Is there anything that you think is not true in the SOP?")
    time.sleep(1)
    update.message.reply_text("If you agree with everything that's written on the Statement of Particulars, then there's no need to contest the divorce.")
    time.sleep(1)
    update.message.reply_text("This would reduce the amount of time your divorce takes.")
    time.sleep(1)
    update.message.reply_text("However, if there are things that are not true, and wish to tell the Court what these are, then you should contest the divorce.")
    time.sleep(1)
    update.message.reply_text("If you're not sure, you should contest the divorce first to preserve your position.")
    time.sleep(1)
    update.message.reply_text("You can always attempt an amicable settlement later, after the MOA is filed.")
    time.sleep(1)
    update.message.reply_text("Now, please tell me if you wish to contest the divorce.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CONTEST_DIV_CHOICE

def contest_div (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Update excel
    sheet1.update_acell("B16", "I am the Defendant and I intend to defend the action.")
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Got it, you want to contest the divorce.")
    time.sleep(1)
    update.message.reply_text("Now please tell me if you're currently a bankrupt.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BANKRUPT_CHOICE

def not_bankrupt (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Update excel
    sheet1.update_acell("B17", "I am not a bankrupt.")
    #Reply user
    update.message.reply_text("Thanks, noted that you're not a bankrupt.")
    time.sleep(1)
    update.message.reply_text("Now I need to know WHERE you received the divorce Writ.")
    time.sleep(1)
    update.message.reply_text("Please type the exact address, complete with postal code.")
    return GOT_ADDRESS

def fill_address_date (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user input on address at which Writ received
    text = update.message.text.title()
    #Update excel
    sheet1.update_acell("B18", "I received the Writ of Summons and Statement of Claim on {} at {}.".format(user_data["date writ received"], text))
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Got it. Now look at paragraph in the MOA that lists what your spouse is asking for.")
    time.sleep(1)
    update.message.reply_text("This is usually paragraph 2 or 3 of the MOA.")
    time.sleep(1)
    update.message.reply_text("Is your spouse making a claim for custody, care and control of the children?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CUSTODY_CHOICE
    
def custody_choice_yes (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Let me explain a little about custody, care and control.")
    time.sleep(1)
    update.message.reply_text("Care and control is about who the child lives with on a day to day basis.")
    time.sleep(1)
    update.message.reply_text("The parent with care and control also makes day-to-day decisions for the child, e.g. what food the child eats, what time the child sleeps, etc.")
    time.sleep(1)
    update.message.reply_text("In the majority of cases, one parent gets care and control, although shared care and control orders are becoming more common.")
    time.sleep(1)
    update.message.reply_text("Custody, on the other hand, is about making major decisions for the child.")
    time.sleep(1)
    update.message.reply_text("The 3 common things that fall under 'custody' are decisions on religion, health, and education.")
    time.sleep(1)
    update.message.reply_text("The Courts usually order joint custody unless there are very exceptional circumstances, e.g. severe emotional, sexual or physical abuse.")
    time.sleep(1)
    update.message.reply_text("This also means that in most cases, non-emergency decisions on religion, health and education must be made jointly by both parents.")
    time.sleep(1)
    update.message.reply_text("So, do you wish to be heard on the issue of custody, care and control?")
    time.sleep(1)
    update.message.reply_text("If you're not sure, or if your spouse has not made any proposal, it's best to state that you wish to be heard for now.")
    time.sleep(1)
    update.message.reply_text("This is to preserve your rights for now. You can always change your mind later.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CUSTODY_CONTEST_CHOICE

def custody_contest_yes (bot, update):
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("C24", "Custody, care and control of the child/children of the marriage.")
    #Reply user
    update.message.reply_text("Got it, you wish to be heard on the issue of custody, care and control.")
    time.sleep(1)
    update.message.reply_text("Now, I need to know your position on access. Let me explain a little about access.")
    time.sleep(1)
    update.message.reply_text("The parent who doesn't live with the child has a right to spend time with the child.")
    time.sleep(1)
    update.message.reply_text("This time is called access.")
    time.sleep(1)
    update.message.reply_text("Do you wish to be heard on the issue of access? If you disagree with the access your spouse is proposing, then you should say you want to be heard.")
    time.sleep(1)
    update.message.reply_text("If you're not sure, or if your spouse did not make a proposal, it's best to state that you wish to be heard.")
    time.sleep(1)
    update.message.reply_text("This is to preserve your rights for now. You can always change your mind later.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ACCESS_CONTEST_CHOICE

def access_contest_yes (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("C26", "Access to the child/children of the marriage.")
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("OK, moving on now to maintenance for the children.")
    time.sleep(1)
    update.message.reply_text("Do you agree with what your spouse has proposed for maintenance of children?")
    time.sleep(1)
    update.message.reply_text("If you don't agree with the proposal, you should indicate that wish to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("It's possible that she hasn't proposed anything in the divorce papers yet. That means she's reserving her position.")
    time.sleep(1)
    update.message.reply_text("If she's reserving her position, you should also indicate that you wish to be heard on this issue, because you don't know what he/she will ask for.")
    time.sleep(1)
    update.message.reply_text("If you agree with what your spouse has proposed, then there's no need to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("Do you need an explanation of how child maintenance is calculated before you decide whether you wish to be heard on this issue?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHILD_MAINT_CHOICE

def child_maint_exp_no (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes, I wish to be heard"],
                                ["No, I do not wish to be heard"]          ]
    update.message.reply_text("OK. Please tell me if you wish to be heard on the issue of child maintenance.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHILD_MAINT_DECISION
    

def child_maint_heard (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("B28", "(c)")
    sheet1.update_acell("C28", "Maintenance for the child/children of the marriage.")
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Next, let's talk about division of assets.")
    time.sleep(1)
    update.message.reply_text("Do you and your spouse own real property, i.e. houses, in your sole or joint names?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PROPERTY_QUERY
    
def property_none (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Noted, you and your spouse don't own any real property.")
    time.sleep(1)
    update.message.reply_text("Next question: Do you and your spouse own other assets? e.g. CPF monies, bank account monies, etc.", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ASSETS_QUERY

def assets_yes (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]          ]
    update.message.reply_text("Noted, you and your spouse own assets.")
    time.sleep(1)
    update.message.reply_text("These need to be divided, regardless of whether they are held in your sole or joint names.")
    time.sleep(1)
    update.message.reply_text("If you disagree with what your spouse is proposing, you should indicate that you wish to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("Otherwise, if you agree with your spouse's proposals, you can indicate that you don't need to be heard.")
    time.sleep(1)
    update.message.reply_text("Do you need an explanation of how assets are divided before deciding whether you wish to be heard on this issue?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ASSETS_EXP_CHOICE

def assets_exp_no (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("OK. Do you wish to be heard on the issue of division of assets?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))   
    return ASSETS_DECISION

def assets_heard (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("B30", "(d)")
    sheet1.update_acell("C30", "Division of assets other than the matrimonial home.")
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("Next issue - wife maintenance.")
    time.sleep(1)
    update.message.reply_text("Look at what your spouse has proposed for wife maintenance.")
    time.sleep(1)
    update.message.reply_text("If you don't agree with it, you should say that you want to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("If you agree, then you can choose not to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("Do you need an explanation of how wife maintenance is calculated before making a decision on whether you wish to be heard?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))   
    return WIFE_MAINT_EXP_CHOICE

def wife_maint_exp_no (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("OK. Do you wish to be heard on the issue of wife maintenance?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return WIFE_MAINT_DECISION

def wife_maint_heard (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("B32", "(e)")
    sheet1.update_acell("C32", "Maintenance for the wife.")
    #Reply user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("Is there a prayer for costs in the MOA?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return COSTS_QUERY

def costs_asked (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("This technically means that your spouse is asking you to pay costs to her for this divorce.")
    time.sleep(1)
    update.message.reply_text("Don't be alarmed, though. It's just a standard prayer.")
    time.sleep(1)
    update.message.reply_text("Most divorce documents will include a prayer for costs.")
    time.sleep(1)
    update.message.reply_text("However, it's only in very rare cases that a spouse is expected to foot the other party's full legal fees.")
    time.sleep(1)
    update.message.reply_text("For now, I would say that it's best to indicate that you wish to be heard on this issue.")
    time.sleep(1)
    update.message.reply_text("That's the usual thing to do.")
    time.sleep(1)
    update.message.reply_text("Are you okay with that?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return COSTS_DECISION

def costs_heard (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("B34", "(f)")
    sheet1.update_acell("C34", "Costs.")
    #Reply to user 
    reply_keyboard =    [       ["Husband"],
                                ["Wife"]    ]
    update.message.reply_text("Moving on. Are you the husband or the wife?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return H_OR_W
    
def df_is_wife (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("A36", "3.")
    sheet1.update_acell("B36", "I am a wife Defendant.")
    #Reply to user 
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("Do you wish to make a claim in wife maintenance for yourself?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return DFWIFE_MAINT_DECISION

def dfwife_maint_claim (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Write to excel
    sheet1.update_acell("B37", "I wish to make a claim for maintenance for myself.")
    #Reply user
    update.message.reply_text("Noted. Now on to some administrative stuff.")
    time.sleep(1)
    update.message.reply_text("Which address would you like the Court to send its notifications to?")
    time.sleep(1)
    update.message.reply_text("The Court will mainly communicate with you by letter, so it's important that you put a valid address.")
    time.sleep(1)
    update.message.reply_text("It's best if you actually stay at that address. It doesn't matter if it's not the address on your NRIC.")
    time.sleep(1)
    update.message.reply_text("Please type in your full address now, including your postal code.")
    return GOT_DF_ADDRESS

def fill_df_address (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user data
    text = update.message.text.title()
    #Write to excel
    sheet1.update_acell("A39", "4.")
    sheet1.update_acell("B39", "The address to which communications to me should be sent is:")
    sheet1.update_acell("B40", text)
    #Reply user
    update.message.reply_text("Great! You're almost done. Just a few more questions.")
    time.sleep(1)
    update.message.reply_text("What's your handphone number? The Court may need to call you, so it's important you give a valid number.")
    time.sleep(1)
    update.message.reply_text("Please type in your handphone number now.")
    return GOT_DF_HP

def fill_df_hp (bot, update, user_data):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Get user data
    text = update.message.text.strip()
    #Write to excel
    sheet1.update_acell("A42", "5.")
    sheet1.update_acell("B42", "My other contact particulars are:")
    sheet1.update_acell("B43", "Handphone number: %s" % text)
    sheet1.update_acell("A46", "Signed:")
    sheet1.update_acell("A47", "Name: %s" % user_data["df name"])
    sheet1.update_acell("A48", "ID No.: %s" % user_data["df nric"])
    today = datetime.today().strftime('%d %b %Y')
    sheet1.update_acell("A49", "Date: {}".format(today))
    #Reply user
    update.message.reply_text("Thanks! Writing the information you've given me into your MOA now.")
    time.sleep(1)
    update.message.reply_text("OK, done! What's your email address? I'll share the file with you so you can print it.")
    return MOA_COMPLETED

def share_moa (bot, update, user_data):
    #Get user update and send email
    text = update.message.text
    sh.share(text, perm_type='user', role='writer')
    #Final instructions to user
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("I've shared the document with you. Please check your email for the link.")
    time.sleep(1)
    update.message.reply_text("What you need to do now is to print out the document and sign at the bottom.")
    time.sleep(1)
    update.message.reply_text("Then, go to the CrimsonLogic Service Bureau at Chinatown Point to file it by {}.".format(user_data["moa deadline"]))
    time.sleep(1)
    update.message.reply_text("The Service Bureau is located on #19-01/02.")
    time.sleep(1)
    update.message.reply_text("I'm giving you the Google Maps link to Chinatown Point.")
    time.sleep(1)
    update.message.reply_text("https://goo.gl/maps/76jqRhCZgEN2")
    time.sleep(1)
    update.message.reply_text("After you've filed it, please go to our e-services portal at this link: https://www.mlaw.gov.sg/eservices/labesvc/ if you want LAB to give you a lawyer for your divorce.")
    time.sleep(1)
    update.message.reply_text("Click on 'Register New Case'. You will need to upload the receipt CrimsonLogic gives you for filing the document, so please register your case after you've filed the MOA!")
    time.sleep(1)
    update.message.reply_text("If you don't need an LAB lawyer, then there's no need to log in to the portal.")
    time.sleep(1)
    update.message.reply_text("Do note that LAB can only help you if you qualify for legal aid.")
    time.sleep(1)
    update.message.reply_text("Is there anything else you need help with?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return START_MENU

    



# REGISTER FOR LAB

def registerforlab (bot, update):
    #Logger
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    #Reply to user
    update.message.reply_text("Okay, please register online to see our Duty Officer for advice.")
    time.sleep(1)
    update.message.reply_text("Here's the link for registration: https://www.mlaw.gov.sg/eservices/labesvc/")
    time.sleep(1)
    update.message.reply_text("Thanks for using iLAB!")
    return DIVWHICHDOC ##LOOP BACk

# OTHER TRACK

def other_start (bot, update):
    reply_keyboard= [   ['Criminal matter'], 
                        ['Defamation'], 
                        ['Small Claims Tribunal'],
                        ['Maintenance of parents'], 
                        ['Other']                       ] 
    update.message.reply_text("Does your case fall in any of these categories?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return OTHER_OPTIONS

def crim_matter (bot, update):
    reply_keyboard =    [       ["Yes"],
                                ["No"]    ]
    update.message.reply_text("Hmm, LAB doesn't handle criminal cases. LAB only handles civil cases.")
    time.sleep(1)
    update.message.reply_text("This is specified in the Legal Aid and Advice Act.")
    time.sleep(1)
    update.message.reply_text("You may wish to try the Criminal Legal Aid Scheme (CLAS) instead.")
    time.sleep(1)
    update.message.reply_text("Here's the link to CLAS' website: http://probono.lawsociety.org.sg/Pages/Criminal-Legal-Aid-Scheme.aspx")
    time.sleep(1)
    update.message.reply_text("Is there anything else I can help you with?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return START_MENU

#GENERAL STUFF

def cancel(bot, update):
    update.message.reply_text("Thanks for using LegalBot! Have a good day.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            START_MENU: [   RegexHandler('^(Yes)$', start_menu),
                            RegexHandler('^(No)$', tobedefined)           ],
            
            CATEGORY: [ RegexHandler('^(Divorce)$', divorce_start),
                        RegexHandler('^(Other)$', other_start),
                        RegexHandler('^(Custody of Children)$', tobedefined),
                        RegexHandler('^(Maintenance)$', tobedefined),
                        RegexHandler('^(Probate / Letters of Admin)$', tobedefined), 
                        RegexHandler('^(Mental Capacity Act / Deputyship)$', tobedefined),
                        RegexHandler('^(Personal injury)$', tobedefined),
                        RegexHandler('^(Monetary claim)$', tobedefined)   ],
            
            GOTDIVDOCS: [   RegexHandler('^(Yes)$', div_which_doc),
                            RegexHandler('^(No)$', tobedefined),
                            RegexHandler('^(Not sure)$', tobedefined )     ],
            
            DIVWHICHDOC: [      RegexHandler('^(A)$', gotwrit),
                                RegexHandler('^(Yes)$', gotwrit),
                                RegexHandler('^(B)$', tobedefined),
                                RegexHandler('^(C)$', tobedefined ),
                                RegexHandler('^(None of the above)$', tobedefined )     ],
            
            DIVCHECKDATE: [MessageHandler(Filters.text, div_check_date, pass_user_data=True)],

            MOA_INTIME: [   RegexHandler('^(Yes)$', moa_getpfname),
                            RegexHandler('^(No)$', tobedefined)           ],
            
            MOA_OUTOFTIME: [    RegexHandler('^(Option 1)$', tobedefined),
                                RegexHandler('^(Option 2)$', registerforlab)    ],
                        
            GOTPFNAME: [MessageHandler(Filters.text, fillpfname, pass_user_data=True)],

            GOTPFNRIC: [MessageHandler(Filters.text, fillpfnric, pass_user_data=True)],

            GOTDFNAME: [MessageHandler(Filters.text, filldfname, pass_user_data=True)],

            GOTDFNRIC: [MessageHandler(Filters.text, filldfnric, pass_user_data=True)],

            CONTEST_DIV_CHOICE: [   RegexHandler("^(I wish to contest)$", contest_div),
                                    RegexHandler("^(I don't want to contest)$", tobedefined)    ],
            
            BANKRUPT_CHOICE: [      RegexHandler("^(Yes)$", tobedefined),
                                    RegexHandler("^(No)$", not_bankrupt)    ],
                            
            GOT_ADDRESS: [MessageHandler(Filters.text, fill_address_date, pass_user_data=True)],

            CUSTODY_CHOICE: [      RegexHandler("^(Yes)$", custody_choice_yes),
                                    RegexHandler("^(No)$", tobedefined)    ],

            CUSTODY_CONTEST_CHOICE: [   RegexHandler("^(Yes)$", custody_contest_yes),
                                        RegexHandler("^(No)$", tobedefined)    ],
            
            ACCESS_CONTEST_CHOICE: [    RegexHandler("^(Yes)$", access_contest_yes),
                                        RegexHandler("^(No)$", tobedefined)    ],
            
            CHILD_MAINT_CHOICE: [   RegexHandler("^(Yes)$", tobedefined),
                                    RegexHandler("^(No)$", child_maint_exp_no)    ],

            CHILD_MAINT_DECISION: [     RegexHandler("^(Yes, I wish to be heard)$", child_maint_heard),
                                        RegexHandler("^(No, I do not wish to be heard)$", tobedefined)    ],
            
            PROPERTY_QUERY: [   RegexHandler("^(Yes)$", tobedefined),
                                RegexHandler("^(No)$", property_none)    ],
            
            ASSETS_QUERY: [     RegexHandler("^(Yes)$", assets_yes),
                                RegexHandler("^(No)$", tobedefined)    ],
            
            ASSETS_EXP_CHOICE: [    RegexHandler("^(Yes)$", tobedefined),
                                    RegexHandler("^(No)$", assets_exp_no)    ],
            
            ASSETS_DECISION: [  RegexHandler("^(Yes)$", assets_heard),
                                RegexHandler("^(No)$", tobedefined)    ],
            
            WIFE_MAINT_EXP_CHOICE: [    RegexHandler("^(Yes)$", tobedefined),
                                        RegexHandler("^(No)$", wife_maint_exp_no)    ],
            
            WIFE_MAINT_DECISION: [      RegexHandler("^(Yes)$", wife_maint_heard),
                                        RegexHandler("^(No)$", tobedefined)    ],
        
            COSTS_QUERY: [  RegexHandler("^(Yes)$", costs_asked),
                            RegexHandler("^(No)$", tobedefined)    ],

            COSTS_DECISION: [       RegexHandler("^(Yes)$", costs_heard),
                                    RegexHandler("^(No)$", tobedefined)    ],
            
            H_OR_W: [       RegexHandler("^(Husband)$", tobedefined),
                            RegexHandler("^(Wife)$", df_is_wife)    ],
        
            DFWIFE_MAINT_DECISION: [    RegexHandler("^(Yes)$", dfwife_maint_claim),
                                        RegexHandler("^(No)$", tobedefined)    ],
            
            GOT_DF_ADDRESS: [MessageHandler(Filters.text, fill_df_address, pass_user_data=True)],

            GOT_DF_HP: [MessageHandler(Filters.text, fill_df_hp, pass_user_data=True)],

            MOA_COMPLETED: [MessageHandler(Filters.text, share_moa, pass_user_data=True)],

            OTHER_OPTIONS: [        RegexHandler("^(Criminal matter)$", crim_matter),
                                    RegexHandler("^(Defamation)$", tobedefined),
                                    RegexHandler("^(Small Claims Tribunal)$", tobedefined),
                                    RegexHandler("^(Maintenance of parents)$", tobedefined),
                                    RegexHandler("^(Other)$", tobedefined),   ]


        },

        fallbacks=  [   CommandHandler('cancel', cancel),   
                        CommandHandler('gotwrit', gotwrit),
                        CommandHandler('custody', fill_address_date),
                        CommandHandler('childmaint', access_contest_yes),
                        CommandHandler('property', child_maint_heard),
                        CommandHandler('assets', property_none),
                        CommandHandler('wifemaint', assets_heard),
                        CommandHandler('costs', wife_maint_heard),
                        CommandHandler('hw', costs_heard),      
                        CommandHandler('filldfpartics', dfwife_maint_claim)               ]
    )


    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
