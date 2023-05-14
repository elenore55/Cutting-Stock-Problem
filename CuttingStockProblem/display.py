import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk, LEFT, Frame
from typing import List, Dict

from EP_approach import optimize

window = tk.Tk()
SCREEN_W = window.winfo_screenwidth()
SCREEN_H = window.winfo_screenheight()
MAIN_STOCK_LEN_SCALED = SCREEN_W // 3
INITIAL_STOCK_X = 50
INITIAL_STOCK_Y = 50
STOCK_H = 20
STOCK_SPACE = 10

window.geometry(f'{SCREEN_W}x{SCREEN_H}')
window.config(bg='#fff')
window.title('Cutting stock problem')

frame1 = Frame(window, width=100, height=150)
frame1.grid(row=0, column=0, sticky='NW', padx=10, pady=10)


def scale(main_stock_len, stock_len, main_stock_len_scaled):
    return int(main_stock_len_scaled * stock_len / main_stock_len)


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    stock_len, l_arr, d_arr, result = optimize(filename)
    display_everything(stock_len, l_arr, d_arr, result)


def display_everything(stock_len, l_arr, d_arr, result):
    colors = display_requirements(stock_len, l_arr, d_arr)
    display_result(result, colors, stock_len)
    window.mainloop()


def display_requirements(L, lengths, demand):
    N = len(lengths)
    colors = ['#%06x' % random.randint(0x999999, 0xFFFFFF) for _ in range(N)]
    colors_dict = {lengths[i]: colors[i] for i in range(N)}

    canvas = tk.Canvas(
        window,
        height=SCREEN_H - 100,
        width=SCREEN_W // 2 - 10,
        bg='white'
    )

    canvas.grid(row=1, column=0, padx=10, pady=5)

    canvas.create_text((70, 15), text='Requirements', font='Helvetica 14 bold')
    canvas.create_rectangle(
        INITIAL_STOCK_X, INITIAL_STOCK_Y,
        INITIAL_STOCK_X + MAIN_STOCK_LEN_SCALED, INITIAL_STOCK_Y + STOCK_H,
        outline='black',
        fill='#333')
    canvas.create_text((INITIAL_STOCK_X + 20, INITIAL_STOCK_Y + 10), text=str(L) + 'm', fill='#fff', font='Helvetica 10 bold')

    for i in range(N):
        canvas.create_rectangle(
            INITIAL_STOCK_X, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE),
            INITIAL_STOCK_X + scale(L, lengths[i], MAIN_STOCK_LEN_SCALED),
            INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + STOCK_H,
            outline='black',
            fill=colors[i])
        canvas.create_text((INITIAL_STOCK_X + 20, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + 10),
                           text=str(lengths[i]) + 'm', font='Helvetica 10 bold')
        canvas.create_text((INITIAL_STOCK_X - 20, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + 10),
                           text=str(demand[i]) + ' x  ', font='Helvetica 12 bold')
    return colors_dict


def display_result(patterns: List[List[int]], colors: Dict[int, str], L):
    patterns_str = []
    for pattern in patterns:
        pattern.sort(reverse=True)
        patterns_str.append(','.join([str(num) for num in pattern]))
    patterns_cnt = {}
    for pattern in patterns_str:
        if pattern not in patterns_cnt:
            patterns_cnt[pattern] = 0
        patterns_cnt[pattern] += 1

    canvas = tk.Canvas(
        window,
        height=SCREEN_H - 100,
        width=SCREEN_W // 2 - 10,
        bg='white'
    )

    canvas.grid(row=1, column=2, padx=10, pady=5)

    canvas.create_text((35, 15), text='Result', font='Helvetica 14 bold')
    i = 0
    for pattern, cnt in patterns_cnt.items():
        canvas.create_text((INITIAL_STOCK_X - 20, INITIAL_STOCK_Y + i * (STOCK_H + STOCK_SPACE) + 10),
                           text=str(cnt) + ' x  ', font='Helvetica 12 bold')

        start_x = INITIAL_STOCK_X
        for j, num in enumerate(pattern.split(',')):
            num = int(num)
            current_stock_len = scale(L, num, MAIN_STOCK_LEN_SCALED)
            canvas.create_rectangle(
                start_x, INITIAL_STOCK_Y + i * (STOCK_H + STOCK_SPACE),
                start_x + current_stock_len,
                INITIAL_STOCK_Y + i * (STOCK_H + STOCK_SPACE) + STOCK_H,
                outline='black',
                fill=colors[num]
            )
            start_x += current_stock_len
        i += 1


def display_prompt():
    open_button = ttk.Button(
        frame1,
        text='Open a File',
        command=select_file
    )
    open_button.pack(side=LEFT)
    window.mainloop()


if __name__ == '__main__':
    display_prompt()
