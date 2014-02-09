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
        allPresent = True
        ready = True
        players = {}
        if os.path.exists(bot.config.si.pathongoing + trigger.group(2) + "\\Players.txt"):
            tempfile = open(bot.config.si.pathongoing + trigger.group(2) + "\\Players.txt")
            for line in tempfile:
                sline = line.split(":")
                if sline[0] is "Player":
                    players[sline[1]+ ".trn"] = False
                    print sline[1]+ ".trn"
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
                else:
                    players[turn] = True
            for p in players:
                if players[p] is not True:
                    allPresent = False
            if ready and allPresent:
                bot.say("All turns present and newer than main save file.")
            else:
                bot.say("Turns not present or older than main save file:")
                for p in players:
                    bot.say(p)
        else:
            bot.say("No turn files present.")
            bot.say("Waiting for:")
            for p in players:
                bot.say(p)
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

@willie.module.commands('monitor')
def monitor(bot, trigger):
    bot.say("Monitoring function not yet implemented.")