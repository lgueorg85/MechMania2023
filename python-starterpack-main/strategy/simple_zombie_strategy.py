# Current zombie strategy:
# 1. Split the map into 4 quadrants
# 2. Determine the quadrant with the most humans
# 3. Split zombies into groups based on how many humans are in each quadrant

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.game_state import GameState
from game.character.action.attack_action_type import AttackActionType
from strategy.strategy import Strategy


class SimpleZombieStrategy(Strategy):

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> list[MoveAction]:
        
        choices = []

        if(game_state.turn < 1000):
            for [character_id, moves] in possible_moves.items():
                if len(moves) == 0:
                    continue
                
                pos = game_state.characters[character_id].position  # position of the zombie
                closest_human_pos = pos  # default position is zombie's pos
                closest_human_distance = 1984  # large number, map isn't big enough to reach this distance

                # Only move zombies
                for c in game_state.characters.values():
                    if c.is_zombie:
                        continue  # Fellow zombies are frens :D, ignore them

                    distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y) # calculate manhattan distance between human and zombie
                    if distance < closest_human_distance:  # If distance is closer than current closest, replace it!
                        closest_human_pos = c.position
                        closest_human_distance = distance

                    # Move as close to the human as possible
                    move_distance = 1337  # Distance between the move action's destination and the closest human
                    move_choice = moves[0]  # The move action the zombie will be taking
                    for m in moves:
                        distance = abs(m.destination.x - closest_human_pos.x) + abs(m.destination.y - closest_human_pos.y)  # calculate manhattan distance

                    # If distance is closer, that's our new choice!
                        if distance < move_distance:  
                            move_distance = distance
                            move_choice = m
                
                choices.append(move_choice)
        else:       
            # Calculate quadrants that humans are in
            human_counts = {1: 0, 2: 0, 3: 0, 4: 0}

            # Num zombies
            num_zombies = 0

            # Calculate the counts of zombies and humans in each quadrant.
            for c in game_state.characters.values():
                if c.is_zombie:
                    num_zombies += 1
                else:
                    if c.position.x < 50:
                        if c.position.y < 50:
                            human_counts[1] += 1
                        else:
                            human_counts[3] += 1
                    else:
                        if c.position.y < 50:
                            human_counts[2] += 1
                        else:
                            human_counts[4] += 1
                    
            # Calculate zombie to human ratio
            ratio = sum(human_counts.values()) // num_zombies

            # Already attack human

            # Prioritize top 2 quadrants since we want to shut off half of the map
            for [character_id, moves] in possible_moves.items():
                
                if(len(moves) == 0):                                # no moves, don't do anything
                    continue

                choice_len = len(choices)

                pos = game_state.characters[character_id].position  # position of the zombie

                move_choice = moves[0]


                min_distance = 2000
                

                if human_counts[1] > 1:
                    for c in game_state.characters.values():
                        if len(choices) > choice_len:
                            break

                        if c.is_zombie:
                            continue

                        for m in moves:
                            distance = abs(c.position.x - m.destination.x) + abs(c.position.y - m.destination.y) # calculate manhattan distance between human and zombie

                            if max(abs(c.position.x - m.destination.x), abs(c.position.y - m.destination.y)) <= 1:
                                choices.append(m)
                                break

                            quadrant = 0
                            if c.position.x < 50:
                                if c.position.y < 50:
                                    quadrant = 1
                                else:
                                    quadrant = 3
                            else:
                                if c.position.y < 50:
                                    quadrant = 2
                                else:
                                    quadrant = 4
                            if quadrant == 1 and distance < min_distance:
                                move_choice = m
                                character_attacking = c

                    
                    human_counts[1] -= ratio
                    if len(choices) > choice_len:
                        break
                        
                    choices.append(move_choice)
                    
                                    

                elif human_counts[2] > 1:
                    for c in game_state.characters.values():
                        if len(choices) > choice_len:
                            break

                        if c.is_zombie:
                            continue

                        for m in moves:
                            distance = abs(c.position.x - m.destination.x) + abs(c.position.y - m.destination.y) # calculate manhattan distance between human and zombie

                            if max(abs(c.position.x - m.destination.x), abs(c.position.y - m.destination.y)) <= 1:
                                choices.append(m)
                                break

                            quadrant = 0
                            if c.position.x < 50:
                                if c.position.y < 50:
                                    quadrant = 1
                                else:
                                    quadrant = 3
                            else:
                                if c.position.y < 50:
                                    quadrant = 2
                                else:
                                    quadrant = 4
                            if quadrant == 2 and distance < min_distance:
                                move_choice = m
                        
                        
                    human_counts[2] -= ratio
                    if len(choices) > choice_len:
                        break
                        
                    choices.append(move_choice)
                    
                # Water moment
                elif human_counts[3] > 1:
                    for c in game_state.characters.values():
                        if len(choices) > choice_len:
                            break

                        if c.is_zombie:
                            continue

                        if (((c.position.x < 35 ) and (c.position.y > 75))):
                            # Travel to midpoint in the water area (28 ,78)
                            for m in moves:
                                distance = abs(28 - m.destination.x) + abs(78 - m.destination.y)
                                if distance < min_distance:
                                    min_distance = distance
                                    move_choice = m
                        else: 
                            for m in moves:
                                distance = abs(c.position.x - m.destination.x) + abs(c.position.y - m.destination.y)
                                
                                if max(abs(c.position.x - m.destination.x), abs(c.position.y - m.destination.y)) <= 1:
                                    choices.append(m)
                                    break

                                quadrant = 0
                                if c.position.x < 50:
                                    if c.position.y < 50:
                                        quadrant = 1
                                    else:
                                        quadrant = 3
                                else:
                                    if c.position.y < 50:
                                        quadrant = 2
                                    else:
                                        quadrant = 4
                                if quadrant == 3 and distance < min_distance:
                                        move_choice = m
                                        character_attacking = c
                
                    human_counts[3] -= ratio
                    if len(choices) > choice_len:
                        break
                        
                    choices.append(move_choice)


                elif human_counts[4] > 1:
                    for c in game_state.characters.values():
                        if len(choices) > choice_len:
                            break

                        if c.is_zombie:
                            continue

                        for m in moves:
                            distance = abs(c.position.x - m.destination.x) + abs(c.position.y - m.destination.y) # calculate manhattan distance between human and zombie

                            if max(abs(c.position.x - m.destination.x), abs(c.position.y - m.destination.y)) <= 1:
                                choices.append(m)
                                break

                            quadrant = 0
                            if c.position.x < 50:
                                if c.position.y < 50:
                                    quadrant = 1
                                else:
                                    quadrant = 3
                            else:
                                if c.position.y < 50:
                                    quadrant = 2
                                else:
                                    quadrant = 4
                            if quadrant == 4 and distance < min_distance:
                                move_choice = m
                                character_attacking = c
                        
                    human_counts[4] -= ratio
                    if len(choices) > choice_len:
                        break
                        
                    choices.append(move_choice)
                
                else:
                    for c in game_state.characters.values():
                        if c.is_zombie:
                            continue  # Fellow zombies are frens :D, ignore them
                        
                        closest_human_distance = 2000
                        distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y) # calculate manhattan distance between human and zombie
                        if distance < closest_human_distance:  # If distance is closer than current closest, replace it!
                            closest_human_pos = c.position
                            closest_human_distance = distance

                    # Move as close to the human as possible
                    move_distance = 1337  # Distance between the move action's destination and the closest human
                    move_choice = moves[0]  # The move action the zombie will be taking
                    for m in moves:
                        distance = abs(m.destination.x - closest_human_pos.x) + abs(m.destination.y - closest_human_pos.y)  # calculate manhattan distance

                        # If distance is closer, that's our new choice!
                        if distance < move_distance:  
                            move_distance = distance
                            move_choice = m

                    choices.append(move_choice)
        
        return choices

    def decide_attacks(
            self, 
            possible_attacks: dict[str, list[AttackAction]], 
            game_state: GameState
            ) -> list[AttackAction]:
        
        choices = []

        for [character_id, attacks] in possible_attacks.items():
            if len(attacks) == 0:  # No choices... Next!
                continue

            choice_len = len(choices)

            terrain = []

            # Gather list of humans in range
            for a in attacks:
                if len(choices) > choice_len:
                    break
                
                if a.type is AttackActionType.CHARACTER:
                    choices.append(a)
                    break
                elif a.type is AttackActionType.TERRAIN:
                    terrain.append(a)
                    
            if len(choices) > choice_len:
                continue

            if terrain:
                choices.append(terrain[0])
                    
        return choices
    






