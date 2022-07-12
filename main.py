import random
import ships
import grid
import players
import turns


# 1.  Player placing round
# 2.  Opponent placing round
# 3.  Game turns
#  3a.Player firing turn
#  3b.Opponent placing turn
#  3c.Resolution

def main():
    # Placing rounds
    human = players.Human()
    opponent = players.Opponent()
    choice = input("Which one will you test first: 1. opponent or 2. human?"
                   "\n Or 3. would you like to just run opponent 10 times?"
                   "\n Or 4. would you like to auto create human grid first?")
    if choice == "2":
        human.armada_place()
        opponent.armada_place()
    elif choice == "1":
        opponent.armada_place()
        human.armada_place()
    elif choice == "3":
        for i in range(10):
            opponent.armada_place()
            opponent.armada_clear()
    elif choice == "4":
        human.auto_armada_place()
        opponent.armada_place()

    while True:
        human.shot_fire(opponent)
        opponent.shot_fire(human)
        print(opponent.grid)
        print(human.grid)
        opponent.armada_health_check()
        print("Your ships:", human.ships.ship_locations_dict)
        human.armada_health_check()
        print("Your opponent's ships:", opponent.ships.ship_locations_dict)

        human_victory = human.victory_detect(opponent)
        opponent_victory = opponent.victory_detect(human)
        if human_victory == False and opponent_victory == False:
            continue
        elif opponent_victory:
            print("You lost!")
            break
        elif human_victory:
            print("You won!")
            break

    # Player placing round:
    # 1.  Select a position to start
    # 2.  Select a direction to place ship
    # 3.  Place ship segment on cell
    #  3a.Repeat in direction until all ship segments are gone
    #  3b.Repeat ship placement until all ships are placed


if __name__ == '__main__':
    main()
