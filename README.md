# PyMood
An experimental prototype for the "Safe Zone" game jam, aimed at testing the capabilities of vibe coding in a game setting. Instead of starting from scratch, this project explores how Pygame and ChatGPT can be used to rapidly prototype a mini-demo of the final project—without manually altering the code itself.

The following sections will explore the iterations in this process, with prompts followed by links to the associated commits in the code.


# Iteration No. 1
```
I want to participate in a game jam and I only have 4 hours.
Give me a game idea and a suggestion for how I can build it.

JamMamad is a game jam — a marathon of game creation where participants build a game around a common theme.
This time, the theme is already known:
Safe Zone
What is your safe zone? A place? An idea? A feeling? And how can it become a game?
```
```
Can u make a simple demo in Pygame?
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/7632b919faf94e2e216b0a4c3365b6d815fb121e)


# Iteration No. 2
```
Let’s add:
1. A dash option
2. Restrict the player from going out of bounds
3. A time limit to reach the Safe Zone
 3.1. If the player is not in the Safe Zone when time runs out, show "Game Over"
 3.2. If the player reaches the Safe Zone in time, generate a new Safe Zone location
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/df5ed6d76208313c082c2adb549abe09dece3aaa)


# Iteration No. 3
```
Generate some ideas to improve the game.
```
ChatGPT (short version): Add patrolling enemies or vision-based hazards for challenge. Introduce power-ups like Signal Boosters, Time Extenders, and Shields. Increase difficulty over rounds with shorter timers and weaker signals. Enhance visuals with dash trails, low-time screen effects, and ambient audio. Add flashback snippets for story depth, score tracking, pause menus, and cooldown indicators. Try co-op or versus modes as stretch goals.
```
Maybe a zombie theme?
Red dots chase the player.
When the player reaches the Safe Zone, they need to lock the door by activating a yellow circle.
Once the timer runs out, all the red dots are eliminated.
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/d5bfc013c0572b8390e9b89f187a85e5469b3dd4)


# Iteration No. 4
```
Add a health bar. If I touch a red dot, I take damage (the red dot also gets a small knockback).  
If I am in the safe zone and the door is locked, zombies can still come in.
```
```
Don't allow the zombies to get into the locked Safe Zone.
Encapsulate the code in a main() function and use clearer, well-defined utility functions.
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood)
