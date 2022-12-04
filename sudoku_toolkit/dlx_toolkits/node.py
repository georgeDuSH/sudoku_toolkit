class Node:
    def __init__(self, column = None, row = None):
        if row is None:
            self.row = self
            self.rowCount = 0
        else:
            self.row = row
        self.column = column
        self.up = self
        self.down = self
        self.left = self
        self.right = self

