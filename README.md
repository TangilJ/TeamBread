# Team Bread
Team Bread is a custom Rocket League bot team that plays Dropshot offline. The [RLBot framework](https://github.com/RLBot/RLBotPythonExample) is required to run this bot. Note that the RLBot framework only works on Windows.

# Running Team Bread

1. Download or clone the [RLBotPythonExample](https://github.com/RLBot/RLBotPythonExample) repository.
1. Follow the instructions in RLBotPythonExample to make sure everything works properly with RLBot.
1. Place the TeamBread folder found in this repository in the RLBotPythonExample repository's folder. The folder should look like [this](https://i.imgur.com/ydvKPL5.png).
1. Configure the match so that Team Bread plays. You can do this in one of two ways:
   1. Select the configurations in the RLBot GUI.
      1. Do this by double clicking `run-gui.bat` in the RLBotPythonExample folder.
      1. Click the [plus button](https://i.imgur.com/PYEbnkG.png) in the Blue and Orange sections to add however many bots you want per team.
      1. Click each bot and click the [Load button](https://i.imgur.com/2mIOvU3.png). Select the `fresh.cfg`, `stale.cfg`, or `mouldy.cfg` configurations in the TeamBread folder.
      1. Click [save at the top and then click the Run button](https://i.imgur.com/3IQZIhL.png) to start the match.
   1. Alternatively, change `rlbot.cfg` manually. This is only recommended if you know what you're doing.
      1. Change the `num_participants` in the `[Match Configuration]` section to how many players you want to have. This number includes how many bots and how many humans are playing.
      1. Change the `participant_config` lines in `rlbot.cfg` (from the RLBotPythonExample folder) so that they have paths to `Bread/fresh.cfg`, `Bread/stale.cfg`, `Bread/moudly.cfg`, or all of them (they're all the same bot with different names so it doesn't matter).
         It should look something like this:
         ```
         participant_config_0 = Bread/fresh.cfg
         participant_config_1 = Bread/fresh.cfg
         participant_config_2 = Bread/stale.cfg
         participant_config_3 = Bread/fresh.cfg
         participant_config_4 = Bread/fresh.cfg
         participant_config_5 = Bread/fresh.cfg
         ```
      1. Run the `run.bat` file to start the match.
