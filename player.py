import time

from cards import Card


class Player:
    players = []

    def __init__(self, name, hand=[]):
        self.hand = hand
        self.name = name
        self.aces = 0
        self.has_passed = False
        self.has_split = False
        Player.players.append(self)

    def hit(self, print_cards=True):
        self.hand.append(Card.deck[0])
        if Card.deck[0].rank == "Ace":
            self.aces += 1
        if print_cards:
            print(f"You drew: {str(Card.deck[0])}")
            self.print_hand()
        del Card.deck[0]

    def stand(self):
        self.has_passed = True
        print("\n")

    def split(self):
        self.has_split = True
        HumanPlayer(f"{self.name}'s second", [self.hand[1]])
        self.hand = [self.hand[0]]
        self.name = f"{self.name}'s first"
        if self.hand[0].rank == "Ace":
            Player.players[1].aces = 1
            Player.players[2].aces = 1
        Player.players[1], Player.players[2] = Player.players[2], Player.players[1]

    def count_points(self):
        points = sum(c.points for c in self.hand)
        aces = self.aces
        while aces > 0:
            if points > 21:
                points -= 10
                aces -= 1
            else:
                return points
        return points

    def __possible_points__(self):  # do ogarnięcia
        points = sum(c.points for c in self.hand if c.rank != "Ace") + int(self.aces)
        return " [" + str(points) + ("/" + str(points+10) if self.aces >0 and points+10 <= 21 else "") + "]"

    def print_hand(self):
        print(f"{self.name}'s hand: " + ", ".join(str(card) for card in self.hand) + self.__possible_points__())

    def check_points(self):
        if self.count_points() > 21:
            self.stand()
            print(f"BUSTED!!!, You have {self.count_points()} points, passed 21\n")
        elif self.count_points() == 21:
            self.stand()
            print("BLACKJACK!!!\n")

    def move(self):
        pass

    def __repr__(self):
        return self.name


class Dealer(Player):
    def __init__(self, name, hand=[]):
        super().__init__(name, hand)

    def move(self):
        if len(self.hand) == 2:
            self.print_hand()
            time.sleep(0.4)
        if self.count_points() < 17:
            self.hit(False)
            time.sleep(0.4)
            self.print_hand()
        else:
            self.stand()

    def print_first_card(self):
        print(f"{self.name}'s hand: {str(self.hand[0])}, Covered Card "
              f"[{'1/11' if self.hand[0].rank == 'Ace' else self.hand[0].points}]\n")


class HumanPlayer(Player):
    move_dict = {"H": "Hit[H]", "S": "Stand[S]", "P": "Split[P]"}

    def __init__(self, name, hand=[]):
        super().__init__(name, hand)

    def move(self):
        self.check_points()
        if len(self.hand) == 1:
            self.print_hand()
        if not self.has_passed:
            move = input(f"Your move: " + ", ".join(self.move_dict[m] for m in self.__possible_moves__()))
            if move.upper() in self.__possible_moves__():
                if move in "Hh":
                    self.hit()
                if move in "Ss":
                    self.stand()
                if move in "Pp":
                    self.split()
            else:
                print("Wrong Move. Try Again")
                self.move()

    def __possible_moves__(self):
        if len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank and not Player.players[0].has_split:
            return "HSP"
        else:
            return "HS"
