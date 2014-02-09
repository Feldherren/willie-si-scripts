willie-si-scripts
=================

Python script for Solium Infernum, for use with the willie IRC bot.

Clearly unfinished.

To use, drop in the modules directory of your willie IRC bot. Requires running config to set the locations of the folders storing ongoing and finished games.
Type .ongoing for a list of ongoing games, .finished for a list of finished games, and .check [ongoing game] to check files currently present in an ongoing game's directory, and if all turn files present are newer than the save file.