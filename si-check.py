# Checks an on-going game and lists present files

import willie
import os

@willie.module.commands('check')

def check(bot, trigger):
    if os.path.isdir("G:\Tools\Google Drive\Solium Infernum\Ongoing Games\\" + trigger.group(2)):
        mainSave = ""
        turnFiles = {}
        ready = True
        for file in os.listdir("G:\Tools\Google Drive\Solium Infernum\Ongoing Games\\" + trigger.group(2)):
            if file.endswith(".trn"):
                bot.say(file)
                turnFiles[file] = os.stat("G:\Tools\Google Drive\Solium Infernum\Ongoing Games\\" + trigger.group(2) + "\\" + file).st_mtime
            elif file.endswith(".sav"):
                bot.say(file)
                mainSave = os.stat("G:\Tools\Google Drive\Solium Infernum\Ongoing Games\\" + trigger.group(2) + "\\" + file).st_mtime
        if len(turnFiles) > 0:
            for turn in turnFiles:
                if turnFiles[turn] <= mainSave:
                    ready = False
            if ready:
                bot.say("All turns present newer than main save file.")
            else:
                bot.say("Some or all turns present older than main save file.")
        else:
            bot.say("No turn files present.")
    else:
        bot.say("I can't find the ongoing game '" + trigger.group(2) + "'")