# take command as '.ongoing'
# checks G:\Tools\Google Drive\Solium Infernum\Ongoing Games and gets folder names
# make it take path from configuration, eventually

import willie
import os

@willie.module.commands('ongoing')

def ongoing(bot, trigger):
    for dir in os.walk('G:\Tools\Google Drive\Solium Infernum\Ongoing Games').next()[1]:
        bot.say(dir)