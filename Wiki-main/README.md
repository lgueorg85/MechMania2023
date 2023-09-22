<div align="center">

<a href="https://mechmania.org"><img width="25%" src="https://github.com/MechMania-29/Website/blob/main/images/mm29_logo.png" alt="MechMania 29"></a>

### [website](https://mechmania.org) | [python-starterpack](https://github.com/MechMania-29/python-starterpack) | [java-starterpack](https://github.com/MechMania-29/java-starterpack) | [visualizer](https://github.com/MechMania-29/Visualizer) | [engine](https://github.com/MechMania-29/engine) | wiki

</div>

# Infection Wiki
Please be advised: There has been a large spike in recorded cases recently, reports indicate that the virus has mutated into something new and highly dangerous. Infected people are becoming zombies! Even more, the government has declared a state of emergency, and a quarantine zone has been established with us in it! If we survive long enough, we might find a way to escape.

---

## Contents
- [Overview and Objectives](#overview-and-objectives)
- [Humans and Zombies](#humans-and-zombies)
    - [Turn Order](#turn-order)
    - [Humans](#humans)
    - [Zombies](#zombies)
- [Obstacles](#obstacles)
- [Further Questions](#further-questions)
- [Disclaimer](#disclaimer)

# Overview and Objectives
Infection is a 1v1 Apocalyptic survival game where you hunt or be hunted. One player will control all the humans, trying to evade the zombies and survive for as long as possible. The other will control all the zombies, pursuing, attacking, and infecting the remaining humans. Stay alert, the horde cannot be stopped.

## Map
The landscape is a 100x100 square grid containing buildings, trees, rivers, and many obstacles. Some of these obstacles can be destroyed to create a new path. The coordinates of the top left is (0,0) while the bottom right is (99,99). Every game will have the same map.

<div align="center">
    
![mm29landscape](https://github.com/MechMania-29/Wiki/assets/60795673/b907d418-e454-4038-a56a-df3c349bc488)
> The landscape, humans spawn in the center while zombies near the top

</div>

## Endgame
The game ends after **200** turns, or after all humans have fallen. Humans earn more points the longer they survive, while zombies earn points the quicker they infect all humans.

## Scoring:
Human points = end_turn + (humans_alive * 5)

Zombie points = 200 - end_turn + (humans_infected * 5)

# Humans and Zombies
In a game, a bot will either control all of the zombies or all of the humans. Each side has unique stats and attributes to take advantage of. 
## Turn Order:
Zombies will have their turn first, then humans second. A single turn is made up of multiple phases for either the zombies or humans. Odd turns are the zombies, while even turns are for the humans. Multiple characters can stand in the same tile.

### Zombie phases:

#### 1. Movement
- Choose a location within range to move to immediately. If the location cannot be reached, the zombie will not move.
#### 2. Attack
- Choose any human or obstacle within range to attack, decreasing health or durability by **1** respectively.

### Human phases:
#### 1. Movement
- Choose a location within range to move to immediately. If the location cannot be reached, the human will not move.
#### 2. Attack
- Choose any zombie or obstacle within range to attack, stunning it or decreasing durability by **1** respectively.
#### 3. Ability
- Use any available active ability the human possesses.


## Humans:
The game begins with **20** humans. Each human can have a class that gives them special abilities and stats. If a zombie is within the range of a human, the human can shoot and stun it for **1** turn. Multiple attacks on a zombie in a single turn will not stack the number of turns it will remain stunned.
If a human loses all health, they will turn and become a zombie by the next zombie turn.

At the start of the game, **16** humans can have a chosen class, the rest will have the Normal class.

Up to **5** humans can have the same class.

Humans can attack either an obstacle or a single zombie. Attacking an obstacle removes **1** durability from it. Attacking a zombie will stun it.

- Health: How many hits a human can take before falling, **max 10 health**
- Speed: The distance a human can travel in a single turn
- Range: The distance a human can attack, Some obstacles can block the attack, however
- Cooldown: The number of turns a human must wait before they can attack again. This includes zombie turns.
- Passive Ability: Abilities that automatically occur
- Active Ability: Abilities that are actively used in the ability phase
  
All human distances are calculated with Manhattan Distance
- D<sub>Manhattan</sub> = |x<sub>2</sub> - x<sub>1</sub>| + |y<sub>2</sub> - y<sub>1</sub>|

|  Class  | Health | Move Speed |Attack Range|Attack cooldown|Ability|Description| |
|--------|--------|--------|-------|-------|-------|-------|-------|
|Normal|1|3|4|8|None|Talents truly shine when the world calls for it.|![mm29human](https://github.com/MechMania-29/Wiki/assets/60795673/2bf9a84c-38be-4ca5-9ac7-f68485fd068a)|
|Marksman|1|3|6|6|None|Hunting scopes are more effective when used properly, like when it isn’t on a sword.|![mm29marksman](https://github.com/MechMania-29/Wiki/assets/60795673/1aaa389e-5ab7-47cb-9bcd-0bcaa2e3bd00)|
|Traceur|1|4|2|4|(Passive) Can move on top of barricades|Isn’t parkour the greatest skill to have in a post-apocalyptic world?| ![mm29traceur](https://github.com/MechMania-29/Wiki/assets/60795673/fbb8cb64-04bd-402b-a9e8-fb0b5f1958ba)|
|Medic|2|3|3|6|(Active) Give another human within attack range +1 health. Cooldown **6** turns|The place to save lives is in the field, not an office.| ![mm29medic](https://github.com/MechMania-29/Wiki/assets/60795673/cde8ce26-8810-44cb-9738-54c559d077c4)|
|Builder|1|3|4|6|(Active) Place a barricade within attack range, cannot place on top of a human, zombie, or debris. Cooldown **6** turns|You can quickly make a barricade with some duct tape, wood, string, and a barricade.|![mm29builder](https://github.com/MechMania-29/Wiki/assets/60795673/41e937f3-9ccf-45b5-9b8d-19a5b6fba767)|
|Demolitionist|1|3|2|6|(Passive) Attacks on obstacles will destroy it (except rivers, too many piranhas)|A good demolitionist is one that’s still here.| ![mm29demo](https://github.com/MechMania-29/Wiki/assets/60795673/ec3a633b-3d0c-4d10-af93-d0b84fa2d2d7)|


## Zombies
The game begins with **6** zombies. When a human falls, they will become a zombie and join the ever growing horde.
Zombies have no attack cooldown, but still can only attack once per turn.
When a zombie is attacked, they will not die, but instead be stunned for **1** turn. While a zombie is stunned, no actions can be performed by that zombie.

Zombie Attack Range uses Chebyshev distance, while Speed uses Manhattan.
- D<sub>Chebyshev</sub> = max( |x<sub>2</sub> - x<sub>1</sub>|, |y<sub>2</sub> - y<sub>1</sub>| )

| Class | Move Speed | Attack Range | Description | |
|------|------|------|------|------|
|Zombie|5|1| Braaainsss...|![mm29zombie](https://github.com/MechMania-29/Wiki/assets/60795673/db7810b5-e7c0-414f-873a-af7ee85af87a)|


# Obstacles
Throughout the landscape there will be different types of obstacles that cannot be passed. They must be destroyed or another path must be taken to bypass objects. When any obstacle is destroyed, its debris is left behind, allowing humans and zombies to pass, but preventing building new obstacles on top. All obstacles block zombie attacks (due to their range), but some do not block human attacks. 

| Type | Durability| Blocks human attacks? | Description | |
|------|------|------|------|------|
|Wall|3|Y|Luckily it’s actually just drywall, unfortunately it’s just drywall.| ![mm29wall](https://github.com/MechMania-29/Wiki/assets/60795673/de82d2d7-7e78-48f7-b22d-2bab5b3fcbde)|
|Barricade|1|N|Something is written next to it... DON’T DEAD OPEN INSIDE…?|![mm29barricade](https://github.com/MechMania-29/Wiki/assets/60795673/b0c21d88-856e-4443-80e7-db3d58debd37)|
|Tree|2|Y|A nice oak tree, don’t punch it.|![mm29tree](https://github.com/MechMania-29/Wiki/assets/60795673/b49ed5ea-ff1b-4021-a947-281a3c6c0195)|
|Water|Infinity|N| Zombie Piranhas. | ![mm29river](https://github.com/MechMania-29/Wiki/assets/60795673/fe0cc3e8-838c-4b87-95e2-049ef69499a5)|

# Further questions
If you need something clarified, don't hesitate to ask! You can contact staff in the [MechMania 29 Discord Server](https://discord.gg/Fz2zEM4nGf) through the #ask-a-question-here channel. We'll be providing help throughout the commpetition!

# Disclaimer
In an unlikely event, we may make adjustments to the game in the interest of keeping the game fair, balanced, and diverse in gameplay. 
