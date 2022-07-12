import random
import ships
import grid

class Player:
    grid = None
    ships = None

    def __init__(self):
        self.grid = grid.Grid()
        self.ships = ships.Ships()
        self.grid.grid_title = None

    def define_other_grid(self, grid):
        self.other_grid = grid

    def select_cell(self, cell_id):
        self.grid.set_cell(cell_id, "selected")

    def place_boat_cell(self, cell_id):
        self.grid.set_cell(cell_id, "emptyship")

    def check_available_directions(self, xy):
        x = xy[0]
        y = xy[-1]
        available_directions = []
        if y != range(len(self.grid.col_labels))[-1]:
            available_directions.append("East")
        if y != range(len(self.grid.col_labels))[0]:
            available_directions.append("West")
        if x != range(len(self.grid.row_labels))[-1]:
            available_directions.append("South")
        if x != range(len(self.grid.row_labels))[0]:
            available_directions.append("North")
        for direction in available_directions:
            if direction == "East":
                if self.grid.grid_dict[self.grid.get_cell_from_xy((x, y + 1))] != "empty":
                    available_directions.remove(direction)
            if direction == "West":
                if self.grid.grid_dict[self.grid.get_cell_from_xy((x, y - 1))] != "empty":
                    available_directions.remove(direction)
            if direction == "South":
                if self.grid.grid_dict[self.grid.get_cell_from_xy((x + 1, y))] != "empty":
                    available_directions.remove(direction)
            if direction == "North":
                if self.grid.grid_dict[self.grid.get_cell_from_xy((x - 1, y))] != "empty":
                    available_directions.remove(direction)
        return available_directions

    def get_next_segment_xy(self, prev_segment_xy, direction):
        try:
            x = prev_segment_xy[0]
            y = prev_segment_xy[-1]
        except (ValueError, TypeError):
            x = None
            y = None
        try:
            if direction == "East":
                y += 1
            if direction == "West":
                y -= 1
            if direction == "South":
                x += 1
            if direction == "North":
                x -= 1
            return (x, y)
        except TypeError:
            pass


    def ghost_ship_spawn(self, ship, current_cell, direction):
        ghost_ship_list = []
        for ship_segment in range(self.ships.ship_dict[ship]):
            if self.grid.is_col_and_or_row(current_cell) == "Both":
                ghost_ship_list.append(current_cell)
                current_xy = self.grid.get_xy_from_cell(current_cell)
                current_xy = self.get_next_segment_xy(current_xy, direction)
                current_cell = self.grid.get_cell_from_xy(current_xy)
        return ghost_ship_list


    def check_possible_ship_directions_from_cell(self, ship, cell_id):

        ghost_ship_armada = {}
        directions_list = ["North", "South", "East", "West"]
        for direction in directions_list:
            ghost_ship_armada[direction] = self.ghost_ship_spawn(ship, cell_id, direction)
        #Length checker
        for ghost_ship in list(ghost_ship_armada.keys()):
            if len(ghost_ship_armada[ghost_ship]) < self.ships.ship_dict[ship]:
                ghost_ship_armada.pop(ghost_ship)
        #Collision detector
        for ghost_ship in list(ghost_ship_armada.keys()):
            for ship_segment in ghost_ship_armada[ghost_ship]:
                if self.grid.grid_dict[ship_segment] != "empty":
                    if ghost_ship in ghost_ship_armada:
                        ghost_ship_armada.pop(ghost_ship)
        possible_ship_directions = []
        for ship in ghost_ship_armada.keys():
            possible_ship_directions.append(ship)
        return possible_ship_directions

    def ship_place(self):
        while True:
            print(self.ships)
            shipabbr = None
            ship = self.ships.get_full_ship_name(shipabbr)
            if ship not in self.ships.ship_dict.keys():
                continue
            else:
                break

        while True:
            starting_cell_id = None
            ship_validity_check = self.check_possible_ship_directions_from_cell(ship, starting_cell_id)
            if starting_cell_id not in self.grid.grid_dict.keys() or len(ship_validity_check) == 0:
                continue
            else:
                self.select_cell(starting_cell_id)
                break

        while True:
            starting_xy = self.grid.get_xy_from_cell(starting_cell_id)
            direction = None
            if direction in ship_validity_check:
                cell_list = []
                current_xy = starting_xy
                for segment in range(self.ships.ship_dict[ship]):
                    current_cell_id = self.grid.get_cell_from_xy(current_xy)
                    self.select_cell(current_cell_id)
                    cell_list.append(self.grid.get_cell_from_xy(current_xy))
                    current_xy = self.get_next_segment_xy(current_xy, direction)

                self.ships.ship_locations_dict[ship] = cell_list
                break

            else:
                continue

        self.ships.ship_dict.pop(ship)
        return ship


    def armada_place(self):
        for ship in range(len(self.ships.ship_dict.keys())):
            self.ship_place()
        for cell in self.grid.grid_dict.keys():
            if self.grid.grid_dict[cell] == "selected":
                self.place_boat_cell(cell)

    def armada_health_check(self):
        ship_locations_copy = self.ships.ship_locations_dict.copy()
        for ship in self.ships.ship_locations_dict:
            for segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[segment] == "hitship" or self.grid.grid_dict[segment] == "hitnonship":
                    self.ships.ship_locations_dict[ship].remove(segment)
            if len(self.ships.ship_locations_dict[ship]) == 0:
                print("{} {} sunk {} {}.".format(None, None, None, ship))
                ship_locations_copy.pop(ship)
        self.ships.ship_locations_dict = ship_locations_copy

    def ship_down_detect(self):
        ship_down = True
        ship_intact = ["hiddenship", "emptyship"]
        for ship in self.ships.ship_locations_dict:
            for ship_segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[ship_segment] in ship_intact:
                    ship_down = False
            if ship_down:
                print("{player} {verb} sunk {player} {ship}.".format(None, None, None, ship))
                self.ships.ship_locations_dict.pop(ship)

    def shot_fire(self, other_player):
        other_grid = other_player.grid
        while True:
            target_cell = None
            if target_cell not in other_grid.grid_dict:
                continue
            if other_grid.grid_dict[target_cell] == "miss" or other_grid.grid_dict[target_cell] == "hitnonship":
                continue
            else:
                if other_grid.hit_check(target_cell) == True:
                    other_grid.hit_message = None
                    other_grid.grid_dict[target_cell] = "hitnonship"
                elif other_grid.hit_check(target_cell) == False:
                    other_grid.hit_message = None
                    other_grid.grid_dict[target_cell] = "miss"
                break

    def victory_detect(self, other_player):
        if len(other_player.ships.ship_locations_dict.keys()) == 0:
            print(other_player.ships.ship_locations_dict.keys())
            return True
        return False


class Human(Player):
    def __init__(self):
        super().__init__()
        self.grid.grid_title = "Your grid:"


    def place_boat_cell(self, cell_id):
        self.grid.set_cell(cell_id, "emptyship")

    def ship_place(self):
        while True:
            print(self.ships)
            shipabbr = input("What are the first two letters of the ship you would like to place?")
            ship = self.ships.get_full_ship_name(shipabbr)
            if ship not in self.ships.ship_dict.keys():
                print("Ship unavailable.")
                continue
            else:
                break

        while True:
            starting_cell_id = input("On which cell would you like to start?")
            ship_validity_check = self.check_possible_ship_directions_from_cell(ship, starting_cell_id)
            if starting_cell_id not in self.grid.grid_dict.keys() or len(ship_validity_check) == 0:
                print("Invalid cell. Try again.")
                continue
            else:
                self.select_cell(starting_cell_id)
                print(self.grid)
                break

        while True:
            starting_xy = self.grid.get_xy_from_cell(starting_cell_id)
            direction = input("Choose a direction to place it.\nAvailable directions:" +
                              ", ".join(ship_validity_check))
            if direction in ship_validity_check:
                cell_list = []
                current_xy = starting_xy
                for segment in range(self.ships.ship_dict[ship]):
                    current_cell_id = self.grid.get_cell_from_xy(current_xy)
                    self.select_cell(current_cell_id)
                    cell_list.append(self.grid.get_cell_from_xy(current_xy))
                    current_xy = self.get_next_segment_xy(current_xy, direction)

                self.ships.ship_locations_dict[ship] = cell_list
                break

            else:
                continue

        self.ships.ship_dict.pop(ship)
        return ship

    def auto_ship_place(self):
        while True:
            ship = random.choice(list(self.ships.ship_dict.keys()))
            if ship not in self.ships.ship_dict.keys():
                continue
            else:
                break

        while True:
            starting_cell_id = random.choice(list(self.grid.grid_dict.keys()))
            ship_validity_check = self.check_possible_ship_directions_from_cell(ship, starting_cell_id)
            if starting_cell_id not in self.grid.grid_dict.keys() or len(ship_validity_check) == 0:
                continue
            else:
                self.select_cell(starting_cell_id)
                break


        starting_xy = self.grid.get_xy_from_cell(starting_cell_id)
        direction = random.choice(ship_validity_check)
        cell_list = []
        current_xy = starting_xy
        for segment in range(self.ships.ship_dict[ship]):
            current_cell_id = self.grid.get_cell_from_xy(current_xy)
            self.select_cell(current_cell_id)
            cell_list.append(self.grid.get_cell_from_xy(current_xy))
            current_xy = self.get_next_segment_xy(current_xy, direction)

        self.ships.ship_locations_dict[ship] = cell_list




        self.ships.ship_dict.pop(ship)
        return ship

    def auto_armada_place(self):
        for ship in range(len(self.ships.ship_dict.keys())):
            self.auto_ship_place()
            for cell in self.grid.grid_dict.keys():
                if self.grid.grid_dict[cell] == "selected":
                    self.place_boat_cell(cell)
        print(self.ships.ship_locations_dict)
        print(self.grid)

    def armada_place(self):
        print(self.grid)
        for ship in range(len(self.ships.ship_dict.keys())):
            self.ship_place()
            for cell in self.grid.grid_dict.keys():
                if self.grid.grid_dict[cell] == "selected":
                    self.place_boat_cell(cell)
            print(self.ships.ship_locations_dict)
            print(self.grid)

    def armada_health_check(self):
        ship_locations_copy = self.ships.ship_locations_dict.copy()
        for ship in self.ships.ship_locations_dict:
            for segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[segment] == "hitship" or self.grid.grid_dict[segment] == "hitnonship":
                    self.ships.ship_locations_dict[ship].remove(segment)
            if len(self.ships.ship_locations_dict[ship]) == 0:
                print("{} {} sunk {} {}.".format("Your opponent", "has", "your", ship))
                ship_locations_copy.pop(ship)
            self.ships.ship_locations_dict = ship_locations_copy
    def ship_down_detect(self):
        ship_down = True
        ship_intact = ["hiddenship", "emptyship"]
        for ship in self.ships.ship_locations_dict:
            for ship_segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[ship_segment] in ship_intact:
                    ship_down = False
            if ship_down:
                print("{Player} {verb} sunk {player} {ship}.".format("You", "have", "your opponent's", ship))
                self.ships.ship_locations_dict.pop(ship)

    def shot_fire(self, other_player):
        other_grid = other_player.grid
        while True:
            target_cell = input("Take aim and fire!")
            if target_cell not in other_grid.grid_dict:
                print("Invalid cell. Choose another.")
                continue
            if other_grid.grid_dict[target_cell] == "miss" or other_grid.grid_dict[target_cell] == "hitnonship":
                print("You've already fired there!")
                continue
            else:
                if other_grid.hit_check(target_cell) == True:
                    other_grid.hit_message = "You hit your opponent's ship!"
                    other_grid.grid_dict[target_cell] = "hitnonship"
                elif other_grid.hit_check(target_cell) == False:
                    other_grid.hit_message = "You missed!"
                    other_grid.grid_dict[target_cell] = "miss"
                break


    def victory_detect(self, other_player):
        if len(other_player.ships.ship_locations_dict.keys()) == 0:
            print(other_player.ships.ship_locations_dict.keys())
            return True
        return False



class Opponent(Player):
    def __init__(self):
        super().__init__()
        self.ship_dict_copy = self.ships.ship_dict.copy()
        self.grid.grid_title = "Your opponent's grid:"

    def ship_place(self):
        while True:
            ship = random.choice(list(self.ship_dict_copy.keys()))
            if ship not in self.ship_dict_copy.keys():
                continue
            else:
                break

        while True:
            starting_cell_id = random.choice(list(self.grid.grid_dict.keys()))
            ship_validity_check = self.check_possible_ship_directions_from_cell(ship, starting_cell_id)
            if starting_cell_id not in self.grid.grid_dict.keys() or len(ship_validity_check) == 0:
                continue
            else:
                self.select_cell(starting_cell_id)
                break


        starting_xy = self.grid.get_xy_from_cell(starting_cell_id)
        direction = random.choice(ship_validity_check)
        cell_list = []
        current_xy = starting_xy
        for segment in range(self.ships.ship_dict[ship]):
            current_cell_id = self.grid.get_cell_from_xy(current_xy)
            self.select_cell(current_cell_id)
            cell_list.append(self.grid.get_cell_from_xy(current_xy))
            current_xy = self.get_next_segment_xy(current_xy, direction)

        self.ships.ship_locations_dict[ship] = cell_list




        self.ship_dict_copy.pop(ship)
        return ship

    def armada_place(self):

        for ship in range(len(self.ships.ship_dict.keys())):
            self.ship_place()
            for cell in self.grid.grid_dict.keys():
                if self.grid.grid_dict[cell] == "selected":
                    self.place_boat_cell(cell)
        print(self.grid)
        print(self.ships.ship_locations_dict)

    def armada_clear(self):
        self.grid.grid_clear()
        for ship in self.ships.ship_locations_dict.keys():
            self.ship_dict_copy[ship] = self.ships.ship_dict[ship]
        self.ships.ship_locations_dict = {}

    def armada_health_check(self):
        ship_locations_copy = self.ships.ship_locations_dict.copy()
        for ship in self.ships.ship_locations_dict:
            for segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[segment] == "hitship" or self.grid.grid_dict[segment] == "hitnonship":
                    self.ships.ship_locations_dict[ship].remove(segment)
            if len(self.ships.ship_locations_dict[ship]) == 0:
                print("{} {} sunk {} {}.".format("You", "have", "your opponent's", ship))
                ship_locations_copy.pop(ship)
            self.ships.ship_locations_dict = ship_locations_copy

    def ship_down_detect(self):
        ship_down = True
        ship_intact = ["hiddenship", "emptyship"]
        for ship in self.ships.ship_locations_dict:
            for ship_segment in self.ships.ship_locations_dict[ship]:
                if self.grid.grid_dict[ship_segment] in ship_intact:
                    ship_down = False
            if ship_down:
                print("{player} {verb} sunk {player} {ship}.".format("Your opponent", "has", "your", ship))
                self.ships.ship_locations_dict.pop(ship)

    def shot_fire(self, other_player):
        other_grid = other_player.grid
        while True:
            target_cell = random.choice(list(other_grid.grid_dict.keys()))
            if target_cell not in other_grid.grid_dict:
                continue
            if other_grid.grid_dict[target_cell] == "miss" or other_grid.grid_dict[target_cell] == "hitnonship":
                continue
            else:

                if other_grid.hit_check(target_cell) == True:
                    other_grid.hit_message = "Your opponent hit your ship!"
                    other_grid.grid_dict[target_cell] = "hitship"
                elif other_grid.hit_check(target_cell) == False:
                    other_grid.hit_message = "Your opponent missed!"
                    other_grid.grid_dict[target_cell] = "miss"
                break




    def victory_detect(self, other_player):
        if len(other_player.ships.ship_locations_dict.keys()) == 0:
            print(other_player.ships.ship_locations_dict.keys())
            return True
        return False