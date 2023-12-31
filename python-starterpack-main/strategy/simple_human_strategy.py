# This is a simple human strategy:
# 6 Marksman, 6 Medics, and 4 Traceurs
# Move as far away from the closest zombie as possible
# If there are any zombies in attack range, attack the closest
# If a Medic's ability is available, heal a human in range with the least health

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.ability_action_type import AbilityActionType
from game.character.action.attack_action import AttackAction
from game.character.action.attack_action_type import AttackActionType
from game.character.action.move_action import MoveAction
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position
from strategy.strategy import Strategy


class SimpleHumanStrategy(Strategy):
    def decide_character_classes(
            self,
            possible_classes: list[CharacterClassType],
            num_to_pick: int,
            max_per_same_class: int,
            ) -> dict[CharacterClassType, int]:
        # The maximum number of special classes we can choose is 16
        # Selecting 6 Marksmen, 6 Medics, and 4 Traceurs
        # The other 4 humans will be regular class
        choices = {
            CharacterClassType.MARKSMAN: 5,
            CharacterClassType.MEDIC: 5,
            CharacterClassType.TRACEUR: 4,
            CharacterClassType.DEMOLITIONIST: 2
        }
        return choices

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
        ) -> list[MoveAction]:
        
        choices = []

        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the human
            closest_zombie_pos = pos  # default position is zombie's pos
            closest_zombie_distance = 1234  # large number, map isn't big enough to reach this distance

            # Find the positions of all other humans
            other_human_positions = [c.position for c in game_state.characters.values() if not c.is_zombie and c.id != character_id]

            # Iterate through every zombie to find the closest one
            for c in game_state.characters.values():
                if not c.is_zombie:
                    continue  # Fellow humans are frens :D, ignore them

                distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y)  # calculate manhattan distance between human and zombie
                if distance < closest_zombie_distance:  # If distance is closer than current closest, replace it!
                    closest_zombie_pos = c.position
                    closest_zombie_distance = distance

            # Calculate moves to maximize distance from zombies and other humans
            move_distance = -1  # Distance between the move action's destination and the closest zombie
            move_choice = moves[0]  # The move action the human will be taking

            for m in moves:
                distance_to_zombie = abs(m.destination.x - closest_zombie_pos.x) + abs(m.destination.y - closest_zombie_pos.y)
                distance_to_other_humans = min([abs(m.destination.x - p.x) + abs(m.destination.y - p.y) for p in other_human_positions])

                if distance_to_zombie > move_distance and distance_to_other_humans > 1:
                    move_distance = distance_to_zombie
                    move_choice = m

            choices.append(move_choice)  # add the choice to the list

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

            # For this strategy, humans will attack any available target
            choices.extend(attacks)

        return choices

    # def decide_abilities(
    #         self, 
    #         possible_abilities: dict[str, list[AbilityAction]], 
    #         game_state: GameState
    #         ) -> list[AbilityAction]:
    #     choices = []

    #     for [character_id, abilities] in possible_abilities.items():
    #         if len(abilities) == 0:  # No choices? Next!
    #             continue

    #         # Since we only have medics, the choices must only be healing a nearby human
    #         human_target = abilities[0]  # the human that'll be healed
    #         least_health = 999  # The health of the human being targeted

    #         for a in abilities:
    #             health = game_state.characters[a.character_id_target].health  # Health of human in question

    #             if health < least_health:  # If they have less health, they are the new patient!
    #                 human_target = a
    #                 least_health = health

    #         if human_target:  # Give the human a cookie
    #             choices.append(human_target)
        
    #     return choices

    def decide_abilities(
            self, 
            possible_abilities: dict[str, list[AbilityAction]], 
            game_state: GameState
            ) -> list[AbilityAction]:
        choices = []

        for [character_id, abilities] in possible_abilities.items():
            if len(abilities) == 0:
                continue

            # Filter abilities to only consider healing actions (for medics)
            healing_abilities = [a for a in abilities if a.type == AbilityActionType.HEAL]

            if not healing_abilities:
                continue  # No healing abilities available for this character

            # Sort healing abilities by the health of the target character (ascending order)
            healing_abilities.sort(key=lambda a: game_state.characters[a.character_id_target].health)

            # Select the first (lowest health) healing ability and add it to choices
            choices.append(healing_abilities[0])

        return choices