#! /usr/bin/env python

import random
import threading

ATTEMPTS: int = 500000
BONUS: int = 6
DICE: tuple[int, int] = (3, 6)


class Player:
    def __init__(self, name, ac) -> None:
        self.name = name
        self.ac = ac
        self.times_hit = 0
        self.lock = threading.Lock()

    def does_hit(self, roll) -> None:
        with self.lock:
            if roll >= self.ac:
                self.times_hit += 1


class Otto(Player):
    def __init__(self, name, ac, shield_slots) -> None:
        super().__init__(name, ac)
        self.shield_slots = shield_slots

    def shield(self) -> int:
        if self.shield_slots <= 0:
            return 0
        else:
            self.shield_slots -= 1
            return 5

    def does_hit(self, roll) -> None:
        with self.lock:
            if roll >= self.ac + self.shield():
                self.times_hit += 1


def gen_dice(tuple_in: tuple[int, int]) -> int:
    accumulator: int = 0
    dice_amount, dice_sides = tuple_in
    for _ in range(dice_amount):
        accumulator += random.randint(1, dice_sides)
    return accumulator


def simulate_battle(player, attempts, bonus, dice_to_roll) -> None:
    for _ in range(attempts):
        attack_roll: int = gen_dice(dice_to_roll)
        player.does_hit(attack_roll + bonus)


if __name__ == "__main__":
    monolith: Player = Player("Monolith", 19)
    basilius: Player = Player("Basilius", 16)
    wulfkar: Player = Player("Wulfkar", 16)
    eshan: Player = Player("Eshan", 16)
    otto: Player = Otto("Otto", 20, 3)
    ludwig: Player = Player("Ludwig", 17)
    players: list[Player] = [monolith, basilius, eshan, otto, ludwig, wulfkar]

    threads: list[threading.Thread] = []
    for player in players:
        thread: threading.Thread = threading.Thread(
            target=simulate_battle, args=(player, ATTEMPTS, BONUS, DICE)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_hits: int = sum(player.times_hit for player in players)

    print(
        f"[SPOILER] HAS A +{BONUS} TO HIT. AND IS ROLLING {DICE[0]}d{DICE[1]} - {ATTEMPTS} ATTEMPTS EACH."
    )
    print(
        "------------------------------------------------------------------------------------"
    )
    print(
        f"[SPOILER] hit the party at a rate of {total_hits / (ATTEMPTS * 6):.0%}, {total_hits} hits across {ATTEMPTS * 6} attempts"
    )
    for player in players:
        print(
            f"{player.name} was hit {player.times_hit} times for a rate of {player.times_hit / (ATTEMPTS):.0%} of the time."
        )
