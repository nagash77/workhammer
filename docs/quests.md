# Quests

Quests are the tasks that players can complete.  They give rewards to the player's
experience, class ranks, items for use, etc.  They are meant to be the major action
in this application.

## Permissions

Quests can only be defined and applied by DMs (Admins).  Players can view the quests
that they have performed (and other players have performed), but they cannot file
that they have completed any.

## Tables

There will be two tables for quests, one that defines each quest, the description,
name, rewards, etc.  Another that defines each quest that is completed and who has
completed it (this will be a general many-to-many table).
