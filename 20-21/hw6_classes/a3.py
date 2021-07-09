class Money:
    def __init__(self, dollars: int, cents: int):
        self.total_cents = 100 * dollars + cents

    @property
    def dollars(self) -> int:
        return self.total_cents // 100

    @dollars.setter
    def dollars(self, value: int):
        if isinstance(value, int) is False:
            print("Error dollars")
        elif value < 0:
            print("Error dollars")
        else:
            self.total_cents = self.total_cents % 100 + 100 * value

    @property
    def cents(self) -> int:
        return self.total_cents % 100

    @cents.setter
    def cents(self, value: int):
        if isinstance(value, int) is False:
            print("Error cents")
        elif value < 0 or value > 99:
            print("Error cents")
        else:
            self.total_cents = (self.total_cents // 100) * 100 + value

    def __str__(self) -> str:
        return "Ваше состояние составляет %s долларов %s центов" \
               % (self.dollars, self.cents)
