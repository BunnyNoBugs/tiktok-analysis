class GoodInt(int):
    def __new__(cls, number: int) -> int:
        if isinstance(number, int):
            number = round(number)
        if isinstance(number, float):
            number = round(number)
        if isinstance(number, str):
            number = round(float(number))

        return int.__new__(cls, number)
