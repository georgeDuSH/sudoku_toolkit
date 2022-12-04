from .node import Node
import random

class DLX:
    def __init__(self):
        self.head = Node(None, 0)
        self.row_constraint = lambda itemIndex, value: 81 + (itemIndex // 9) * 9 + value
        self.col_constraint = lambda itemIndex, value: 162 + (itemIndex % 9) * 9 + value
        self.box_constraint = lambda itemIndex, value: 243 + (itemIndex // 27) * 27 + (itemIndex % 9) // 3 * 9 + value
        self.cols = []
        self.coverIndex = []
        self.alterNumsFlow = []

    def create_matrix(self, sudokuArr):
        head = self.head
        self.cols = [head]

        for i in range(324):
            current = Node(i+1, None)
            current.right = head
            current.left = head.left
            head.left.right = current
            head.left = current
            self.cols.append(current)

        for row in range(len(sudokuArr)):
            for col in range(9):
                cellID = row * 9 + col
                if sudokuArr[row][col] == 0:
                    for j in range(9):
                        self.create_node_links(cellID, j + 1)
                else:
                    self.create_node_links(cellID, sudokuArr[row][col])
                    self.coverIndex.append(cellID)

    def create_node_links(self, index, value):
        # Node(col, row)
        cellNode = Node(self.cols[index + 1], index * 9 + value)
        rowNode = Node(self.cols[self.row_constraint(index, value)], index * 9 + value)
        colNode = Node(self.cols[self.col_constraint(index, value)], index * 9 + value)
        areaNode = Node(self.cols[self.box_constraint(index, value)], index * 9 + value)

        cellNode.right, cellNode.left = rowNode, areaNode
        rowNode.right, rowNode.left = colNode, cellNode
        colNode.right, colNode.left = areaNode, rowNode
        areaNode.right, areaNode.left = cellNode, colNode

        for i in [cellNode, rowNode, colNode, areaNode]:
            i.column.rowCount += 1
            i.down = i.column
            i.up = i.column.up
            i.column.up.down = i
            i.column.up = i

    def cover(self, column):
        column.right.left = column.left
        column.left.right = column.right
        currentColNode = column.down

        while currentColNode != column:
            currentRowNode = currentColNode.right
            while currentRowNode != currentColNode:
                currentRowNode.down.up = currentRowNode.up
                currentRowNode.up.down = currentRowNode.down
                currentRowNode.column.rowCount -= 1
                currentRowNode = currentRowNode.right
            currentColNode = currentColNode.down

    def uncover(self, column):
        currentColNode = column.up

        while currentColNode != column:
            currentRowNode = currentColNode.left
            while currentRowNode != currentColNode:
                currentRowNode.down.up = currentRowNode
                currentRowNode.up.down = currentRowNode
                currentRowNode.column.rowCount += 1
                currentRowNode = currentRowNode.left
            currentColNode = currentColNode.up
        column.right.left = column
        column.left.right = column

    def search(self, solution = []):
        if self.head == self.head.right:
            return (solution, True)

        leastCol = None
        currentColNode = self.head.right
        s = 99999

        while currentColNode != self.head:
            if currentColNode.rowCount < s:
                leastCol = currentColNode
                s = currentColNode.rowCount
            currentColNode = currentColNode.right
        self.cover(leastCol)

        curNodeDown = leastCol.down
        while curNodeDown != leastCol:
            solution.append(curNodeDown)
            curNodeLat = curNodeDown.right
            while curNodeLat != curNodeDown:
                self.cover(curNodeLat.column)
                curNodeLat = curNodeLat.right
            solution, found = self.search(solution)
            if found:
                return (solution, True)
            curNodeDown = solution.pop()
            leastCol = curNodeDown.column
            curNodeLat = curNodeDown.left
            while curNodeLat != curNodeDown:
                self.uncover(curNodeLat.column)
                curNodeLat = curNodeLat.left
            curNodeDown = curNodeDown.down

        self.uncover(leastCol)
        return (solution, False)

    def search_sol_num(self, solution = [], solNum = 0):
        if self.head == self.head.right:
            return (solution, True, solNum)

        leastCol = None
        currentColNode = self.head.right
        s = 99999

        while currentColNode != self.head:
            if currentColNode.rowCount < s:
                leastCol = currentColNode
                s = currentColNode.rowCount
            currentColNode = currentColNode.right
        self.cover(leastCol)

        curNodeDown = leastCol.down
        while curNodeDown != leastCol:
            solution.append(curNodeDown)
            curNodeLat = curNodeDown.right
            while curNodeLat != curNodeDown:
                self.cover(curNodeLat.column)
                curNodeLat = curNodeLat.right
            solution, found, solNum= self.search_sol_num(solution, solNum)
            if found:
                solNum += 1
            curNodeDown = solution.pop()
            leastCol = curNodeDown.column
            curNodeLat = curNodeDown.left
            while curNodeLat != curNodeDown:
                self.uncover(curNodeLat.column)
                curNodeLat = curNodeLat.left
            curNodeDown = curNodeDown.down

        self.uncover(leastCol)
        return (solution, False, solNum)

    def search_if_multi_sol(self, solution = [], solNum = 0):
        if self.head == self.head.right:
            return (solution, 1, solNum)

        leastCol = None
        currentColNode = self.head.right
        s = 99999

        while currentColNode != self.head:
            if currentColNode.rowCount < s:
                leastCol = currentColNode
                s = currentColNode.rowCount
            currentColNode = currentColNode.right
        self.cover(leastCol)

        curNodeDown = leastCol.down
        while curNodeDown != leastCol:
            solution.append(curNodeDown)
            curNodeLat = curNodeDown.right
            while curNodeLat != curNodeDown:
                self.cover(curNodeLat.column)
                curNodeLat = curNodeLat.right
            solution, found, solNum= self.search_if_multi_sol(solution, solNum)
            if found == 1:
                solNum += 1
            elif found == 2:
                return (solution, 2, solNum)
            if solNum > 1:
                return (solution, 2, solNum)
            curNodeDown = solution.pop()
            leastCol = curNodeDown.column
            curNodeLat = curNodeDown.left
            while curNodeLat != curNodeDown:
                self.uncover(curNodeLat.column)
                curNodeLat = curNodeLat.left
            curNodeDown = curNodeDown.down

        self.uncover(leastCol)
        return (solution, 0, solNum)

    def cover_index(self):
        for index in self.coverIndex:
            self.cover(self.cols[index + 1])
            curNodeDown = self.cols[index + 1].down
            while curNodeDown != self.cols[index + 1]:
                curNodeLat = curNodeDown.right
                while curNodeLat != curNodeDown:
                    self.cover(curNodeLat.column)
                    curNodeLat = curNodeLat.right
                curNodeDown = curNodeDown.down

    def calculate_alter_nums(self):
        alterNumsList = []
        for i in range(81):
            if self.cols[i + 1].left.right == self.cols[i + 1]:
                currentColNode = self.cols[i + 1]
                alterNumsList.append([i + 1, currentColNode.rowCount])
        return alterNumsList

    def search_alter_nums(self, solution = []):
        if self.head == self.head.right:
            self.alterNumsFlow.pop()
            return (solution, True)

        leastCol = None
        s = 99999
        min_row = []

        for i in range(81):
            if self.cols[i + 1].left.right == self.cols[i + 1]:
                currentColNode = self.cols[i + 1]
                #
                if currentColNode.rowCount < s:
                    min_row.clear()
                    min_row.append(i)
                    s = currentColNode.rowCount
                elif currentColNode.rowCount == s:
                    min_row.append(i)
        leastCol = self.cols[random.choice(min_row) + 1]
                # if currentColNode.rowCount < s:
                #     leastCol = currentColNode
                #     s = currentColNode.rowCount
        self.cover(leastCol)

        curNodeDown = leastCol.down
        while curNodeDown != leastCol:
            solution.append(curNodeDown)
            curNodeLat = curNodeDown.right
            while curNodeLat != curNodeDown:
                self.cover(curNodeLat.column)
                curNodeLat = curNodeLat.right
            self.alterNumsFlow.append(self.calculate_alter_nums())
            solution, found = self.search_alter_nums(solution)
            if found:
                return (solution, True)
            self.alterNumsFlow.pop()
            curNodeDown = solution.pop()
            leastCol = curNodeDown.column
            curNodeLat = curNodeDown.left
            while curNodeLat != curNodeDown:
                self.uncover(curNodeLat.column)
                curNodeLat = curNodeLat.left
            curNodeDown = curNodeDown.down

        self.uncover(leastCol)
        return (solution, False)

    def alter_nums_flow(self):
        self.cover_index()
        self.alterNumsFlow.append(self.calculate_alter_nums())
        self.search_alter_nums()
        return self.alterNumsFlow

