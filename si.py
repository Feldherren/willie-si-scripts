import willie
import os

def configure(config):
    config.interactive_add("si", "pathOngoing", "Location of ongoing game folders?")
    config.interactive_add("si", "pathFinished", "Location of finished game folders?")

def setup(bot):
    if not bot.config.has_section('si'):
        bot.say('SI not configured, make sure pathOngoing and pathFinished are defined')
        return
    if not bot.config.si.pathongoing.endswith('\\'):
        bot.config.si.pathongoing = bot.config.si.pathongoing + '\\'
    if not bot.config.si.pathfinished.endswith('\\'):
        bot.config.si.pathfinished = bot.config.si.pathfinished + '\\'

@willie.module.commands('check')
def check(bot, trigger):
    if os.path.isdir(bot.config.si.pathongoing + trigger.group(2)):
        mainSave = ""
        turnFiles = {}
        ready = True
        for file in os.listdir(bot.config.si.pathongoing + trigger.group(2)):
            if file.endswith(".trn"):
                bot.say(file)
                turnFiles[file] = os.stat(bot.config.si.pathongoing + trigger.group(2) + "\\" + file).st_mtime
            elif file.endswith(".sav"):
                bot.say(file)
                mainSave = os.stat(bot.config.si.pathongoing + trigger.group(2) + "\\" + file).st_mtime
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
    for dir in os.walk(bot.config.si.pathongoing).next()[1]:
        bot.say(dir)
        
@willie.module.commands('finished')
def finished(bot, trigger):
    for dir in os.walk(bot.config.si.pathfinished).next()[1]:
        bot.say(dir)

@willie.module.commands('debug')
def debug(bot, trigger):
    bot.say("Ongoing games location:" + bot.config.si.pathongoing)
    bot.say("Finished games location:" + bot.config.si.pathfinished)