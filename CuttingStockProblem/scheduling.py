from typing import List

MACHINE_SIZE_CHANGED_COST = 50
STOCK_SWITCHED_COST = 10


class Stock(object):

    def __init__(self, stock: List[int], i, L):
        self.stock = sorted(stock, reverse=True)
        self.id = i
        self.iterations_of_cut = {}
        self.is_fully_used = (sum(self.stock) == L)

    def cut(self, i):
        length = self.stock.pop(0)
        self.iterations_of_cut[i] = length

    def __len__(self):
        return len(self.stock)

    def __getitem__(self, item):
        return self.stock[item]

    def __str__(self):
        return str(self.stock)


def schedule(result, L):
    for i, stock in enumerate(result):
        result[i] = Stock(stock, i, L)
    queue: List[Stock] = [result[0]]

    for i in range(1, len(result)):
        queue = insert_stock(queue, result[i])

    cut_cnt = 0
    stocks_removed = []
    while len(queue) > 0:
        stock_for_cutting = queue[0]
        length_cutting = stock_for_cutting.stock[0]
        while len(stock_for_cutting) > 1 and stock_for_cutting[0] == length_cutting:
            stock_for_cutting.cut(cut_cnt)
            cut_cnt += 1
        if len(stock_for_cutting) == 1 and stock_for_cutting[0] == length_cutting and not stock_for_cutting.is_fully_used:
            stock_for_cutting.cut(cut_cnt)
            cut_cnt += 1
            stocks_removed.append(stock_for_cutting)
            queue.pop(0)
        elif len(stock_for_cutting) == 1 and stock_for_cutting.is_fully_used:
            stocks_removed.append(stock_for_cutting)
            queue.pop(0)
        else:
            queue.pop(0)
            queue = insert_stock(queue, stock_for_cutting)
    return stocks_removed, cut_cnt


def insert_stock(queue: List[Stock], stock: Stock):
    i = 0
    stock_arr = stock.stock
    while i < len(queue):
        current_stock = queue[i]
        current_stock_arr = queue[i].stock
        if stock_arr[0] < current_stock_arr[0]:
            i += 1
        elif stock_arr[0] > current_stock_arr[0]:
            return queue[:i] + [stock] + queue[i:]
        else:
            if stock.is_fully_used and all_same_before_last(stock_arr):
                return queue[:i] + [stock] + queue[i:]
            elif stock_arr >= current_stock_arr and not (current_stock.is_fully_used and all_same_before_last(current_stock_arr)):
                return queue[:i] + [stock] + queue[i:]
            else:
                i += 1
    return queue + [stock]


def all_same_before_last(stock_arr: List[int]):
    return stock_arr[:-1].count(stock_arr[0]) == len(stock_arr[:-1])


def display(scheduled: List[Stock], cut_cnt):
    cuts_arr = [None] * cut_cnt
    for stock in scheduled:
        for i in stock.iterations_of_cut:
            cuts_arr[i] = (stock.id, stock.iterations_of_cut[i])
    for c in cuts_arr:
        print(c)


if __name__ == '__main__':
    l = 25
    arr = [[10, 4, 7, 4], [7, 7, 6, 5], [4, 4, 10, 7], [7, 7, 7, 4], [10, 10, 4], [7, 6, 6, 4]]
    res, cuts = schedule(arr, l)
    display(res, cuts)
