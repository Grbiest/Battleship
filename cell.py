class Cell:
    current_val = None
    display_dict = {"empty": " ",
                    "miss": "~",
                    "hitship": "#",
                    "hitnonship": "X",
                    "emptyship": "□"}

    def __init__(self):
        self.current_val = "empty"

    def __repr__(self):
        display_symbol = self.display_dict[self.current_val]
        return "[" + display_symbol + "]"
