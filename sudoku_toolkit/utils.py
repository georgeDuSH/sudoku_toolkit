# basic sudoku class
# calculation in int type
class SUDOKU:
    """ Basic SUDOKU demonstration and retrieving tool
        [Prettify]
        - prettify printing via override __str__()
            >>> sdk = [[0,8,5,0,0,0,2,1,0],
                       [0,9,4,0,1,2,0,0,3],
                       [0,0,0,3,0,0,7,0,4],
                       [5,0,3,4,0,9,0,0,0],
                       [0,4,0,2,0,6,0,3,0],
                       [0,0,0,1,0,3,9,0,7],
                       [6,0,8,0,0,5,0,0,0],
                       [1,0,0,8,4,0,3,6,0],
                       [0,2,7,0,0,0,8,9,0]]
            >>> sdk = SUDOKU(sdk)
            >>> print(sdk)
                0 8 5 	 0 0 0 	 2 1 0
                0 9 4 	 0 1 2 	 0 0 3
                0 0 0 	 3 0 0 	 7 0 4

                5 0 3 	 4 0 9 	 0 0 0
                0 4 0 	 2 0 6 	 0 3 0
                0 0 0 	 1 0 3 	 9 0 7

                6 0 8 	 0 0 5 	 0 0 0
                1 0 0 	 8 4 0 	 3 6 0
                0 2 7 	 0 0 0 	 8 9 0

        [Easier Access]
        - element access: slicing via override __getitem__()
            >>> sdk[1]       # 8
            >>> sdk[0]       # 0
            >>> sdk[1,2]     # 3
            >>> sdk['A8']    # 1
            >>> sdk['C','4'] # 3

        Try to explore more!
    """
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        """ Basic class for SUDOKU.
            The class has some basic methods, e.g. peers for each cube
            to check, currently filled clues, mapping converting ix in matrix to 1d vector
        """
        # settings
        from copy import deepcopy
        self.sudoku_matrix = deepcopy(matrix)
        self.rows = rows
        self.cols = cols
        self.stage = stage
        self.cubes = comb(rows, cols) # all elements
        # values
        self.value_dict = self._smat_val_dict() # values in dict
        self.value_1d = list(self.value_dict.values()) # values in 1d vec
        # map(loc in matrix to 1d array): (i,j) -> (ix)
        self.map_rc2ix = self._rc2ix()

    def _smat_val_dict(self, ) -> dict:
        """ SUDOKU values in dictionary, including 0s
        """
        digits = list(range(1,1+len(self.rows)))
        vals = []
        for line in self.sudoku_matrix:
            for elem in line:
                if elem in digits:
                    vals.append(elem)
                else:
                    vals.append(0) # unknown digit
        return dict(zip(self.cubes, vals))

    def _rc2ix(self, ):
        """ Storing mapping indeces from cordinate in matrix to 1d array
        """
        elem_nums = len(self.cubes)
        return dict(zip(self.cubes, list(range(elem_nums))))

    def __getitem__(self, key):
        """ Retrieve value for matrix
            >>> m = [[0,8,5,0,0,0,2,1,0],
                     [0,9,4,0,1,2,0,0,3],
                     [0,0,0,3,0,0,7,0,4],
                     [5,0,3,4,0,9,0,0,0],
                     [0,4,0,2,0,6,0,3,0],
                     [0,0,0,1,0,3,9,0,7],
                     [6,0,8,0,0,5,0,0,0],
                     [1,0,0,8,4,0,3,6,0],
                     [0,2,7,0,0,0,8,9,0]]
            >>> sm = SUDOKU(m)
            >>> sm[1]       # 8
            >>> sm[0]       # 0
            >>> sm[1,2]     # 3
            >>> sm['A8']    # 1
            >>> sm['C','4'] # 3
        """
        if isinstance(key, int):
            return self.value_1d[key]
        elif isinstance(key[0], int) and isinstance(key[1], int):
            return self.sudoku_matrix[key[0]][key[1]]
        elif (isinstance(key[0], str) and isinstance(key[1], str)) or isinstance(key, str):
            return self.value_1d[self.map_rc2ix[key[0]+key[1]]]
        else:
            print('Invalid Index')

    def __str__(self, ):
        """ Prettify the printing result for SUDOKU matrix
        """
        sep_line = '\n'
        res = ''
        col_sep = ''
        row_sep = ''
        for i in range(self.stage-1):
            col_sep += self.cols[(i+1)*self.stage-1]
            row_sep += self.rows[(i+1)*self.stage-1]

        sudoku_val_dict = self.value_dict
        for r in self.rows:
            res += ' '.join(
                str(sudoku_val_dict[r+c]) + (' \t' if c in col_sep else '')
                for c in self.cols) + '\n'
            if r in row_sep:
                res += sep_line
        return res


def comb(a, b) -> list:
    return [s+t for s in a for t in b]


def get_peers(rows='ABCDEFGHI', cols='123456789'):
    all_elem = comb(rows, cols)
    row_units = [comb(r, cols) for r in rows]
    col_units = [comb(rows, c) for c in cols]
    square_units = [comb(r_sq, c_sq) for r_sq in [rows[:3], rows[3:6], rows[6:]] \
                    for c_sq in [cols[:3], cols[3:6], cols[6:]]]
    check_units = row_units+col_units+square_units
    # all units related to elem
    check_list = dict(
        (elem, [unit for unit in check_units if elem in unit]) for elem in all_elem)
    # all candidates that should be different from elem
    peer_list = dict(
        (elem, set(sum(check_list[elem], [])) - {elem}) for elem in all_elem)

    return peer_list

flatten = lambda l: [item for sublist in l for item in sublist]