from collections import Counter


class Tree:
    # в ините говорили можно не делать тайпинги
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right


def huffman(node: 'node', left: bool = True, binString: str = '') -> dict:
    # лево - нолик, право - единичка. Бинарная строка "накапливает" кодировку
    if type(node) is not str:
        d = {}
        # рекурсивная функция - сначала разбирается левая ветвь
        d.update(huffman(node.left, True, binString + '0'))
        # рекурсивная функция - разбирается правая ветвь
        d.update(huffman(node.right, False, binString + '1'))
        return d
    return {node: binString}  # тут букве присваивается накопленная кодировка


def preparation(string: str) -> 'nodes':
    # расчет частоты
    freq = Counter(string)
    # сортируем по частоте
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = freq

    while len(nodes) > 1:
        (key1, f1) = nodes[-1]
        (key2, f2) = nodes[-2]
        nodes.pop(-1)
        nodes.pop(-1)  # убираем два последних элемента
        node = Tree(key1, key2)  # key1 - самое маленькое и получается левым
        nodes.append((node, f1 + f2))  # добавляем кортеж узла и его частоты
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes


def huffmanCode(dictionary: dict, text: str) -> str:
    for coded_letter in dictionary:
        for letter in text:
            if letter == coded_letter:
                text = text.replace(letter, dictionary[letter])
    return text


def huffmanDecode(dictionary: dict, text: str) -> str:
    res = ""
    while text:
        for k in dictionary.values():
            if text.startswith(k):
                for letter, code in dictionary.items():
                    if code == k:
                        res += letter
                text = text[len(k):]
    return res


# примеры
print('Пример 1:')
nodes1 = preparation('ASDAAAA')
dictionary1 = huffman(nodes1[0][0])  # передаю экземпляр класса Tree

print(dictionary1)
coded1 = huffmanCode(dictionary1, 'ASDAAAA')
print(coded1)
print(huffmanDecode(dictionary1, coded1))

####
print("####")
print('Пример 2:')
####
nodes2 = preparation('мама раму')
dictionary2 = huffman(nodes2[0][0])  # передаю экземпляр класса Tree

print(dictionary2)
coded2 = huffmanCode(dictionary2, 'мама раму')
print(coded2)
print(huffmanDecode(dictionary2, coded2))

####
print("####")
print('Пример 3:\n Нельзя кодировать из одного символа,'
      ' поэтому я считаю нормальным, что алгоритм не срабатывает')
####
nodes3 = preparation('v')
dictionary3 = huffman(nodes3[0][0])  # передаю экземпляр класса Tree

print(dictionary3)
coded3 = huffmanCode(dictionary3, 'v')
print(coded3)
print(huffmanDecode(dictionary3, coded3))
