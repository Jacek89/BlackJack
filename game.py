from cards import Card
from player import HumanPlayer, Dealer, Player
import time


class BlackJack:
    def __init__(self, name_player: str, name_dealer: str):
        self.name_player = name_player
        self.name_dealer = name_dealer
        self.winner = None
        self.p2 = HumanPlayer(self.name_player)
        self.p1 = Dealer(self.name_dealer)

    def start(self):
        Card.creating(4)
        Card.shuffle_deck()
        for i in range(2):
            self.p1.hit(False)
            self.p2.hit(False)
        self.p1.print_first_card()
        self.p2.print_hand()

    def end_round(self):
        if self.p2.has_split:
            del Player.players[1]
            self.p2.name = self.p2.name[:-8]
        for player in Player.players:
            player.hand.clear()
            player.has_passed = False
            player.aces = 0
            player.has_split = False

    def result(self):
        player_points = self.p2.count_points()
        dealer_points = self.p1.count_points()
        if self.p2.has_split:
            if self.p2.count_points() < Player.players[1].count_points() <= 21:
                player_points = Player.players[1].count_points()
        print(f"Player points: {player_points}")
        print(f"Dealer points: {dealer_points}")
        time.sleep(0.8)
        #  Tie
        if dealer_points == player_points or player_points > 21 and dealer_points > 21:
            print("IT'S A TIE!")
            return 0
        #  BlackJack
        elif player_points == 21:
            print("You won with BLACKJACK!!")
            return 2
        #  Win
        elif dealer_points < player_points < 21 or player_points <= 21 and dealer_points > 21:
            print("You won!")
            return 1.5
        #  Lose
        else:
            print("You lose!")
            return -2

    @staticmethod
    def print_new_round(x):
        k = len(str(x))
        print("=" * 108 + "\n" + "=" * (54 - (k + 9) // 2) + f"  GAME {x}  " + "=" * (
                    99 - (54 - (k + 9) // 2) - k) + "\n" + "=" * 108 + "\n")
        time.sleep(0.8)

    def main(self):
        self.start()
        i = 0
        while i < len(Player.players):
            while not Player.players[i].has_passed:
                time.sleep(0.8)
                Player.players[i].move()
            i += 1


def play():
    timer = time.time() + 60 * 15
    points = 0
    name = input("Enter Your name here: ")
    game = BlackJack(name, "Dealer")
    game_number = 1
    while time.time() < timer:
        game.print_new_round(game_number)
        game.main()
        points += game.result()
        game.end_round()
        game_number += 1
        print(f"\nYour points: {points}\n")
        time.sleep(3.5)
    print(f"\n\n\nYOUR SCORE IS: {points}")


if __name__ == "__main__":
    play()
