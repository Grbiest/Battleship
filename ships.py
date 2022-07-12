import grid
class Ships:
    def __init__(self):
        self.grid = grid.Grid()
        self.ship_dict = {"Destroyer": 2, "Submarine": 3, "Cruiser": 3, "Battleship": 4, "Carrier": 5}
        self.ship_locations_dict = {}

        self.ship_abbr_dict_keys = []
        for ship in self.ship_dict.keys():
            self.ship_abbr_dict_keys.append(ship[:2])
        self.ship_abbr_dict = dict(zip(self.ship_abbr_dict_keys, list(self.ship_dict.values())))

    def get_abbr(self, full_ship_name):
        for abbr in self.ship_abbr_dict.keys():
            if full_ship_name[:2] == abbr:
                return abbr

    def ship_check(self, cell_id):
        for ship in self.ship_locations_dict:
            if cell_id in self.ship_locations_dict[ship]:
                return ship

    def ship_overlap_check(self, ship):
        other_ship_locations = []
        for key in list(self.ship_locations_dict.keys()):
            other_ship_locations.append(key)
        other_ship_locations.remove(ship)
        overlap_list = []
        for shipname in other_ship_locations:
            for cell in self.ship_locations_dict[shipname]:
                if cell in self.ship_locations_dict[ship]:
                    overlap_list.append(cell)
        if len(overlap_list) > 0:
            print(other_ship_locations)
            print(overlap_list)
            print(self.ship_locations_dict)
            return True
        return False



    def ship_wrap_around_check(self, ship):
        cell_rows = []
        cell_columns = []
        for cell_id in self.ship_locations_dict[ship]:
            cell_rows.append(cell_id[0])
            if len(cell_id) == 2:
                cell_columns.append(cell_id[-1])
            if len(cell_id) == 3:
                cell_columns.append(cell_id[-2:])
        if len(cell_columns) + len(cell_rows) < 2 * self.ship_dict[ship]:
            return True
        else:
            return False

    def ship_invalid_location_check(self, ship):
        if self.ship_overlap_check(ship) == True or self.ship_overlap_check(ship) == True:
            return True
        else:
            return False


    def get_full_ship_name(self, abbr):
        for full_name in self.ship_dict.keys():
            if abbr == full_name[:2]:
                return full_name




    def __repr__(self):
        ships_left_list = []
        for ship in self.ship_dict.keys():
            shipname = "".join("[" + self.get_abbr(ship) + "]" + ship[2:])
            ships_left_list.append(shipname)
        if len(ships_left_list) > 1:
            ships_left_str = ", ".join(ships_left_list[:-1]) + " and " + ships_left_list[-1]
        else:
            ships_left_str = str(ships_left_list[0])
        return "Your available ships are: {}.".format(ships_left_str)