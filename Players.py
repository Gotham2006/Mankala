"This contains the two classes."

class StrategyPlayer(object):
    def make_move(self, kalah):
        player_index = 0  # StrategyPlayer is always player 0
        pits = kalah.game_pits[0]
        num_pits = kalah.pits

        # Try to find a move that ends in the store (i.e., exact stones to reach store)
        for i in range(num_pits):
            stones = pits[i]
            distance_to_store = num_pits - i  # Since pit 1 is farthest, pit i is num_pits - i from store
            if stones == distance_to_store:
                return i + 1  # pit number = index + 1

        # Pick the pit closest to the store that has stones in it
        for i in range(num_pits - 1, -1, -1):
            if pits[i] > 0:
                return i + 1
        return None

class AmazingPlayer(object):

    def make_move(self,kalah):
        """Focus on extra turns"""
        player_index = 1
        pits = kalah.game_pits[1]
        opp_pits = kalah.game_pits[0]
        num_pits = kalah.pits

        #Extra turn
        for i in range(num_pits):
            stones = pits[i]
            distance_to_store = num_pits - i  # Since pit 1 is farthest, pit i is num_pits - i from store
            if stones > 0:
                if stones == distance_to_store:
                    return i + 1  # pit number = index + 1

        # Finds empty pits
        empty_pits = []
        for j in range(num_pits):
            if pits[j] == 0:
                empty_pits.append(j)

        # Finds empty pits that can be sown in
        empty_sowable_pits = []
        for i in range(num_pits):
            stones = pits[i]
            if stones > 0:
                if stones - i in empty_pits:
                    empty_sowable_pits.append(i)
        if empty_sowable_pits != []:
            max_returnable_stones_index = 0
            max_returnable_stones = 0
            for i in empty_sowable_pits:
                if opp_pits[i]+pits[i] > max_returnable_stones:
                    max_returnable_stones_index = i
                    max_returnable_stones = opp_pits[i]+pits[i]
            return max_returnable_stones_index + 1

        empty_opp_pits = []
        for j in range(num_pits):
            if opp_pits[j] == 0:
                empty_opp_pits.append(j)

        # Pick the pit closest to the store that has stones in it
        for i in range(num_pits - 1, -1, -1):
            if pits[i] > 0:
                return i + 1

        return None





