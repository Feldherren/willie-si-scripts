import willie
import os
import willie.module

# scheduler = None
# monitorjob = None

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
    # scheduler = willie.bot.Willie.JobScheduler(bot)
    # monitorjob = willie.bot.Willie.Job(30, monitoring)
    # scheduler.add_job(monitorjob)

@willie.module.commands('check')
def check(bot, trigger):
    if os.path.isdir(bot.config.si.pathongoing + trigger.group(2)):
        mainSave = ""
        host = ""
        turnFiles = {}
        # set these to false initially
        # players{Emp, Moo}; for(p in players){ walk filesystem to check for turn }
        allPresent = True
        ready = True
        players = {}
        if os.path.exists(bot.config.si.pathongoing + trigger.group(2) + "\\Players.txt"):
            tempfile = open(bot.config.si.pathongoing + trigger.group(2) + "\\Players.txt")
            for line in tempfile:
                line = line.strip().split(":")
                if line[0] == "Player":
                    players[line[1]] = False
                else:
                    host = line[1]
        for file in os.listdir(bot.config.si.pathongoing + trigger.group(2)):
            if file.endswith(".trn"):
                #bot.say(file)
                turnFiles[file] = os.stat(bot.config.si.pathongoing + trigger.group(2) + "\\" + file).st_mtime
            elif file.endswith(".sav"):
                #bot.say(file)
                mainSave = os.stat(bot.config.si.pathongoing + trigger.group(2) + "\\" + file).st_mtime
        if len(turnFiles) > 0:
            for turn in turnFiles:
                if turnFiles[turn] <= mainSave:
                    ready = False
                else:
                    players[turn.strip(".trn")] = True
            for p in players:
                if players[p] is False:
                    allPresent = False
            if ready and allPresent:
                bot.say("All turns present and newer than main save file.")
                bot.say(host + " can process the turn file now!")
            else:
                bot.say("Turns not present or older than main save file:")
                for p in players:
                    if players[p] is False:
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

# dict of dicts for keeping file modified times
# dict contains game-name linked to dict of files + time modified
monitored = {}
        
@willie.module.commands('monitor')
def monitor(bot, trigger):
    # if game exists and is not being monitored, add to list of monitored games
    if os.path.isdir(bot.config.si.pathongoing + trigger.group(2)):
        if trigger.group(2) in monitored:
            bot.say(trigger.group(2) + " is already being monitored.")
        else:
            monitored[trigger.group(2)] = False
            bot.say(trigger.group(2) + " added to monitored games.")
    else:
        bot.say("I can't find the ongoing game " + trigger.group(2))
    # if game is first game monitored, create job

@willie.module.commands('unmonitor')
def unmonitor(bot, trigger):
    # if game is last game monitored, remove job
    if trigger.group(2) in monitored:
        del monitored[trigger.group(2)]
        bot.say(trigger.group(2) + " removed from monitored games.")
    else:
        bot.say(trigger.group(2) + " is not being monitored.")

# set this to something more sensible when done testing
@willie.module.interval(5)
def monitoring(bot):
    # monitorjob.next()
    print "Running monitoring"
    for game in monitored:
        # compare time-modified of files in dict with time-modified of files in game folder
        for file in os.listdir(bot.config.si.pathongoing + game):
            if file in monitored[game]:
                if os.stat(bot.config.si.pathongoing + game + "\\" + file).st_mtime > monitored[game][file]:
                    bot.say(file + " updated!")
            monitored[game][file] = os.stat(bot.config.si.pathongoing + game + "\\" + file).st_mtime