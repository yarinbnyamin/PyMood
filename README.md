# PyMood
An experimental prototype for the **"Safe Zone" game jam**, designed to test the potential of **vibe coding** in a game development context.  
Rather than starting from scratch, this project explores how **Pygame** and **ChatGPT** can be combined to rapidly prototype a mini-demo of the final concept — all without manually writing or modifying code line by line.

The sections below walk through the development process, with each *prompt* followed by a link to the corresponding *commit*.

Overall, the results were very satisfying — with minimal time wasted. After just seven iterations, I was happy with the outcome of the concept demo.

```
Note that the player moves with the arrow keys.
```


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
```
1. The game restarts when the timer runs out and the player survives — but I want it to continue from the current position, with a new goal and new enemies instead.
2. The player can't leave the Safe Zone after it's locked.
3. The player can unlock the Safe Zone.
4. Zombies should get knocked back (not stuck) when they touch the locked Safe Zone.
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/89f80cb57250bffdef99329590ec629ebf4cdef0)


# Iteration No. 5
```
1. Add a restart button after the player loses.
2. Add a scoring system.
3. Lock/unlock actions should require holding the button for 1 second. If the button is held longer, it won't have any additional effect until it's released and pressed again.
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/4aeaf33036980e035f8651a56f9cfa1fc4b3a4f3)


# Iteration No. 6
```
1. The zombies can still manage to harm the player while he is in the locked Safe Zone.
2. I need to have a random spot on the map with a green dot (Health Up).
3. I want a small indicator for the locking mechanism of the Safe Zone (maybe a small loading bar).
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood/tree/9acb4ee13991bff351566b771b14541200b3ed29)


# Iteration No. 7
```
1. The Safe Zone should not be visible unless the player is inside it.
2. Pressing ESC should pause the game and show options to Continue or Restart.
3. The game should get harder over time by adding more enemies. Use a linear difficulty curve, e.g., number of enemies = 5 + score * 2.
```

[Link to the commit](https://github.com/yarinbnyamin/PyMood)
