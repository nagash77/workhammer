# ITRPG

So the idea for this application came from my boss (@nagash77).  He proposed having
an RPG like system for IT employees, where they would gain experience for doing
various things and level up based on these.  These docs will (hopefully) outline
and explain the goals of the project and document the various parts of the
functionality.

## Table of Contents
1. [Login](login.md)
1. [Players](players.md)
1. [Quests](quests.md)
1. [Usage](usage.md)

## Terminology
* **Player**: The 'game' unit, this is the alter ego that plays the game, their are
the hero for a certain person.  The player will go on quests (see below), accumulate
experience, and level up.
* **User**: The credential based login attached to a real person.  This is a
detachment from the player only in that there are going to be people who will
participate in the game without having a player character such as DMs (see below).
* **Dungeon Master (DM)**: These are users that will not have a player but are instead
in charge of managing the game itself.  They will award quests, items, manage the
available quests, handle tweaking the class system, etc.
* **Quest**: This is a real world task or accomplishment that has attached rewards,
such as experience, items, currency, etc.  These will be determined and outlined by
the DMs and performed by the players.
* **Items**: Some perk boosting rewards for quests, they will be able to modify the
rewards from other quests when equipped.
* **Class**: This will be attached to skill areas in the real world, things that
pertain to various specialities and will affect the rewards from quests.
