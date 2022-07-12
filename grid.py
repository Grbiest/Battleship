class Grid:
    row_labels = None
    col_labels = None
    grid_dict = None
    grid_dict_keys = None
    cell_display_dict = {"empty": " ",
                         "miss": "~",
                         "hitship": "#",
                         "hitnonship": "X",
                         "emptyship": "□",
                         "hiddenship": " ",
                         "selected": "+"}

    def __init__(self):
        # Variables used for grid creation
        alphabet_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.row_labels = alphabet_list[0:10]
        self.col_labels = list(range(1, 11))
        self.grid_dict = {}
        self.grid_dict_keys = []
        self.grid_title = ""
        self.hit_message = ""




        # Creating the empty grid dictionary
        for letter in self.row_labels:
            for number in self.col_labels:
                self.grid_dict_keys.append(letter + str(number))
        for key in self.grid_dict_keys:
            self.grid_dict[key] = "empty"

    def set_cell(self, cell_id, state = "empty"):
        self.grid_dict[cell_id] = state

    def check_faulty_xy(self, xy):
        if xy[0] not in range(len(self.row_labels)) or xy[1] not in range(len(self.col_labels)):
            return True
        else:
            return False
    def view_hidden_cells(self):
        grid_dict_copy = self.grid_dict.copy()
        grid_dict_reset = self.grid_dict.copy()
        for cell in grid_dict_copy.keys():
            if grid_dict_copy[cell] == "hiddenship":
                grid_dict_copy[cell] = "emptyship"
        self.grid_dict = grid_dict_copy
        print(self)
        self.grid_dict = grid_dict_reset

    def check_for_none(self, value):
        is_none = False
        for item in value:
            if item is None:
                is_none = True
        return is_none

    def get_xy_from_cell(self, cell_id):
        cell_row = cell_id[0]
        cell_col = cell_id[1:]
        try:
            x = self.row_labels.index(cell_row)
            y = self.col_labels.index(int(cell_col))
            return tuple((x, y))
        except (ValueError, TypeError):
            pass

    def grid_clear(self):
        for cell in self.grid_dict.keys():
            self.grid_dict[cell] = "empty"

    def get_cell_from_xy(self, xy):
        try:
            x = xy[0]
            y = xy[-1]
        except TypeError:
            x = None
            y = None
        if x in range(len(self.row_labels)):
            cell1 = self.row_labels[x]
        else:
            cell1 = ""
        if y in range(len(self.col_labels)):
            cell2 = self.col_labels[y]
        else:
            cell2 = ""
        return str(cell1) + str(cell2)

    def is_col_and_or_row(self, cell):
        cell_row = False
        cell_col = False
        for character in cell:
            if character.isalpha() == True:
                cell_row = True
            if character.isdigit() == True:
                cell_col = True
        if cell_row == True and cell_col == True:
            answer = "Both"
        elif cell_row == True and cell_col == False:
            answer = "Row only"
        elif cell_row == False and cell_col == True:
            answer = "Column only"
        else:
            answer = "Neither"
        return answer

    def hit_check(self, cell):
        if self.grid_dict[cell] == "empty":
            return False
        if self.grid_dict[cell] == "hiddenship" or self.grid_dict[cell] == "emptyship":
            return True





    def __repr__(self):
        # Declaring necessary dictionary and list for organizing and displaying
        grid_dict_display_dict = self.grid_dict.copy()
        grid_dict_display_list = []

        for grid_key in grid_dict_display_dict.keys():
            for cell_display_key in self.cell_display_dict.keys():
                if grid_dict_display_dict[grid_key] == cell_display_key:
                    grid_dict_display_dict[grid_key] = self.cell_display_dict[cell_display_key]

        # Creating the main rows, labeled
        grid_dict_display_values = list(grid_dict_display_dict.values()).copy()
        grid_dict_display_list_rows = []
        for label in self.row_labels:
            row = []
            row.append("\n")
            row.append(label)
            for label in self.col_labels:
                row.append("[" + grid_dict_display_values.pop(0) + "]")
            grid_dict_display_list_rows.append(row)
        for row in grid_dict_display_list_rows:
            for item in row:
                grid_dict_display_list.append(item)

        # Creating the row for the column labels
        col_labels_str_list = []
        for col_label in self.col_labels:
            col_labels_str_list.append(str(col_label))
        i = 1
        while i < len(col_labels_str_list):
            col_labels_str_list.insert(i, "  ")
            i += 2
        col_labels_str_list.insert(0, "  ")
        for i in range(len(col_labels_str_list)):
            if col_labels_str_list[i] == "10":
                col_labels_str_list.pop(i-1)
                col_labels_str_list.insert(i-1, " ")
        col_labels_str = "".join(col_labels_str_list)

        # Aligning column labels before grid rows
        grid_dict_display_list.insert(0, col_labels_str)

        # Inserting grid title
        grid_dict_display_list.insert(0, self.grid_title + "\n")

        # Inserting hit message

        grid_dict_display_list.append("\n" + self.hit_message)
        grid_str = "".join(grid_dict_display_list)
        return grid_str