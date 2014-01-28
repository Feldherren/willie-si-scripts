# Monitors specified ongoing game for updates to files
# Alerts people in IRC when files update
# Checks initial files
# Takes game directory as parameter
# Gets player names from .trn files

import willie

@willie.module.commands('monitor')

def monitor(bot, trigger):
    