from ..utils import SUDOKU, get_peers, flatten

class SudokuSolver(SUDOKU):
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        # peers
        super().__init__(matrix, rows, cols, stage)
        self.peers = get_peers(rows, cols)
        self.peers_ix_dict = self.get_peer_ixs()
        self.digits = list(range(1, len(rows)+1))
        # result
        from copy import deepcopy
        # should be an instance of SUDOKU
        self.solution = None

    def solve(self) -> None:
        """ Abstract method place holder for later solvers """
        pass

    def ix2rcix(self, ix):
        return ix//9, ix%9

    def get_peer_ixs(self, ):
        peer_ix = {}
        rc2ix = self.map_rc2ix
        for p in self.peers:
            peer_ix[rc2ix[p]] = [rc2ix[i] for i in self.peers[p]]
        return peer_ix

    def get_candidate_value_s(self, ix):
        """ Retrieve candidate values for a given index
        : param ix: int or list of int
        : return
        """
        if not isinstance(ix, int): # 1d ix
            srow = self.rows[ix[0]]
            scol = self.cols[ix[1]]
            ix = self.map_rc2ix[srow+scol]
        peer_vals = [self.value_1d[p] for p in self.peers_ix_dict[ix]]
        return set(self.digits) - set(peer_vals) - set([0])

    def get_candidate_value_d(self, matrix, ix):
        value_1d = flatten(matrix)
        peer_vals = [value_1d[p] for p in self.peers_ix_dict[ix]]
        return set(self.digits) - set(peer_vals) - set([0])

    def get_all_candidates_s(self, ):
        ixs = list(self.map_rc2ix.values())
        return dict(zip(ixs, [self.get_candidate_value_s(ix) for ix in ixs]))
