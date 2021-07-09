class Coin:
    wallet = 0

    def __init__(self, value: int):
        self.value = value
        if not isinstance(self.value, int):
            self.value = 0
        if self.value < 0:
            self.value = 0
        else:
            Coin.wallet += self.value

    @staticmethod
    def total_sum() -> int:
        return Coin.wallet

    def __del__(self):
        Coin.wallet -= self.value
