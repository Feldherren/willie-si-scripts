import willie
import os

pathOngoing = "G:\Tools\Google Drive\Solium Infernum\Ongoing Games\\"
pathFinished = "G:\Tools\Google Drive\Solium Infernum\Finished Games\\"

@willie.module.commands('check')
def check(bot, trigger):
    if os.path.isdir(pathOngoing + trigger.group(2)):
        mainSave = ""
        turnFiles = {}
        ready = True
        for file in os.listdir(pathOngoing + trigger.group(2)):
            if file.endswith(".trn"):
                bot.say(file)
                turnFiles[file] = os.stat(pathOngoing + trigger.group(2) + "\\" + file).st_mtime
            elif file.endswith(".sav"):
                bot.say(file)
                mainSave = os.stat(pathOngoing + trigger.group(2) + "\\" + file).st_mtime
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

@willie.module.commands('ongoing')
def ongoing(bot, trigger):
    for dir in os.walk(pathOngoing).next()[1]:
        bot.say(dir)
        
@willie.module.commands('finished')
def finished(bot, trigger):
    for dir in os.walk(pathFinished).next()[1]:
        bot.say(dir)