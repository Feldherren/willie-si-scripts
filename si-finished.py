# take command as '.finished'
# checks G:\Tools\Google Drive\Solium Infernum\Finished Games and gets folder names
# make it take path from configuration, eventually

import willie
import os

@willie.module.commands('finished')

def finished(bot, trigger):
    for dir in os.walk('G:\Tools\Google Drive\Solium Infernum\Finished Games').next()[1]:
        bot.say(dir)