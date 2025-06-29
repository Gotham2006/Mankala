from Players import StrategyPlayer, AmazingPlayer
import random, statistics

class KalahGame(object):
    def __init__(self, n, m, player_turn):
        self.pits = n
        self.stones = m
        self.store = [0, 0]
        self.game_pits = [[m] * n for _ in range(2)]
        self.player_turn = player_turn

    def make_move(self, pit_number):
        player_turn = self.player_turn
        no_of_stones = self.game_pits[player_turn][pit_number - 1]
        self.game_pits[player_turn][pit_number - 1] = 0
        pit_number_in_stones = 0
        stones_in_opposite_pit = 0

        while no_of_stones > 0:
            while pit_number_in_stones + pit_number < self.pits and no_of_stones > 0:
                self.game_pits[player_turn][pit_number + pit_number_in_stones] += 1
                last_turn = pit_number + pit_number_in_stones
                pit_number_in_stones += 1
                no_of_stones -= 1
                stones_in_opposite_pit = 0

            if pit_number_in_stones + pit_number == self.pits:
                self.store[player_turn] += 1
                pit_number_in_stones += 1
                no_of_stones -= 1
                last_turn = -1

            while stones_in_opposite_pit < self.pits and no_of_stones > 0:
                last_turn = -2
                self.game_pits[1 - player_turn][stones_in_opposite_pit] += 1
                stones_in_opposite_pit += 1
                no_of_stones -= 1
                pit_number = 0
                pit_number_in_stones = 0

        if last_turn >= 0:
            if self.game_pits[player_turn][last_turn] == 1:
                self.store[player_turn] += self.game_pits[player_turn][last_turn] + self.game_pits[1 - player_turn][last_turn]
                self.game_pits[player_turn][last_turn] = 0
                self.game_pits[1 - player_turn][last_turn] = 0

        return last_turn == -1

    def single_player(self):
        with open("single_play.txt", "w") as f:
            turn = 1
            while not self.game_over():
                f.write(f"\nTURN {turn}:\n")
                f.write(self.draw_board())

                if self.player_turn == 1:
                    f.write("AmazingPlayer's turn.\n")
                    pit_number = AmazingPlayer().make_move(self)
                    f.write(f"AmazingPlayer chooses pit {pit_number}\n")
                else:
                    f.write("StrategyPlayer's turn.\n")
                    pit_number = StrategyPlayer().make_move(self)
                    f.write(f"StrategyPlayer chooses pit {pit_number}\n")

                before_store = self.store[:]
                before_pits = [row[:] for row in self.game_pits]

                extra_turn = self.make_move(pit_number)

                f.write("Resulting board:\n")
                f.write(self.draw_board())

                if self.store != before_store:
                    f.write(f"Store update: {before_store} -> {self.store}\n")

                if extra_turn:
                    f.write("Player gets an **extra turn**!\n")
                else:
                    self.player_turn = 1 - self.player_turn
                    turn += 1

            f.write("\n--- GAME OVER ---\n")
            f.write(self.draw_board())
            outcome = self.game_over()
            f.write(outcome['result'].capitalize() + " Player wins!\n")

    def draw_board(self):
        board = ""
        pits_top = self.game_pits[1]
        pits_bottom = self.game_pits[0]
        n = self.pits
        pit_width = 4

        board += "       " + "".join([f"{n - i:>{pit_width}}" for i in range(n)]) + "   <-- AmazingPlayer\n"
        board += "      +" + ("-" * pit_width * n) + "+\n"
        board += "      |" + "".join(f"{x:>{pit_width}}" for x in reversed(pits_top)) + " |\n"
        total_width = pit_width * n
        board += f"{self.store[1]:>3}  |" + " " * total_width + f"|  {self.store[0]:<3}\n"
        board += "      |" + "".join(f"{x:>{pit_width}}" for x in pits_bottom) + " |\n"
        board += "      +" + ("-" * pit_width * n) + "+\n"
        board += "       " + "".join([f"{i + 1:>{pit_width}}" for i in range(n)]) + "   <-- StrategyPlayer\n\n"

        return board

    def game_over(self):
        if all(pit == 0 for pit in self.game_pits[0]) or all(pit == 0 for pit in self.game_pits[1]):
            p0_score = self.store[0]
            p1_score = self.store[1]
            result = "tie"
            if p0_score > p1_score:
                result = "strategy"
            elif p1_score > p0_score:
                result = "amazing"
            return {
                "result": result,
                "strategy_score": p0_score,
                "amazing_score": p1_score
            }
        else:
            return False


def run_multiple_games():
    no_of_rounds = int(input("\nNumber of rounds: "))

    strategy_scores = []
    amazing_scores = []
    results = {"strategy": 0, "amazing": 0, "tie": 0}

    for i in range(1,no_of_rounds+1):
        print(f"\n--- Round {i} ---")
        player_turn = random.randint(0, 1)
        no_of_pits = int(input("Number of Pits (2–6): "))
        no_of_stones = int(input("Number of Stones (1–6): "))
        kalah = KalahGame(no_of_pits, no_of_stones, player_turn)
        result = kalah_play(kalah)

        results[result["result"]] += 1
        strategy_scores.append(result["strategy_score"])
        amazing_scores.append(result["amazing_score"])

    with open("multiple_play.txt", "w") as file:
        file.write("=== Kalah Game Statistics ===\n")
        file.write(f"Total Rounds Played: {no_of_rounds}\n\n")

        def write_stats(name, scores, wins):
            file.write(f"{name} Player:\n")
            file.write(f"  Wins: {wins} ({(wins / no_of_rounds) * 100:.1f}%)\n")
            file.write(f"  Average Score: {statistics.mean(scores):.2f}\n")
            file.write(f"  Median Score: {statistics.median(scores):.2f}\n")
            file.write(f"  Highest Score: {max(scores)}\n")
            file.write(f"  Lowest Score: {min(scores)}\n\n")

        write_stats("Strategy", strategy_scores, results["strategy"])
        write_stats("Amazing", amazing_scores, results["amazing"])
        file.write(f"Ties: {results['tie']} ({(results['tie'] / no_of_rounds) * 100:.1f}%)\n")



def kalah_play(kalah):
    strategy_player = StrategyPlayer()
    amazing_player = AmazingPlayer()
    while not kalah.game_over():
        if kalah.player_turn == 0:
            pit_number = strategy_player.make_move(kalah)
        else:
            pit_number = amazing_player.make_move(kalah)

        extra_turn = kalah.make_move(pit_number)
        if not extra_turn:
            kalah.player_turn = 1 - kalah.player_turn
    return kalah.game_over()

def main():
    # Single game
    no_of_pits = int(input("Number of Pits (2-6): "))
    no_of_stones = int(input("Number of Stones (1-6): "))
    kalah = KalahGame(no_of_pits, no_of_stones, 1)  # AmazingPlayer goes first
    kalah.single_player()

    #multiple_games
    run_multiple_games()

if __name__ == "__main__":
    main()

