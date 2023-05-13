import tkinter as tk
import random

window = tk.Tk()

SCREEN_W = window.winfo_screenwidth()
SCREEN_H = window.winfo_screenheight()
MAIN_STOCK_LEN_SCALED = SCREEN_W // 2
INITIAL_STOCK_X = 50
INITIAL_STOCK_Y = 50
STOCK_H = 20
STOCK_SPACE = 10


def scale(main_stock_len, stock_len):
    return int(MAIN_STOCK_LEN_SCALED * stock_len / main_stock_len)


window.geometry(f'{SCREEN_W}x{SCREEN_H}')
window.config(bg='#fff')
window.title('Cutting stock problem')

big_length = 25
len_arr = [10, 7, 6, 4]
demand_arr = [21, 25, 30, 55]
colors = ['#%06x' % random.randint(0x999999, 0xFFFFFF) for _ in range(len(len_arr))]

canvas = tk.Canvas(
    window,
    height=(STOCK_H + STOCK_SPACE) * len(len_arr) + 85,
    width=SCREEN_W - 20,
    bg='#fff'
)

canvas.pack()

canvas.create_text((70, 15), text='Requirements', font='Helvetica 14 bold')
canvas.create_rectangle(
    INITIAL_STOCK_X, INITIAL_STOCK_Y,
    INITIAL_STOCK_X + MAIN_STOCK_LEN_SCALED, INITIAL_STOCK_Y + STOCK_H,
    outline='black',
    fill='#333')
canvas.create_text((INITIAL_STOCK_X + 20, INITIAL_STOCK_Y + 10), text=str(big_length) + 'm', fill='#fff', font='Helvetica 10 bold')

for i in range(len(len_arr)):
    canvas.create_rectangle(
        INITIAL_STOCK_X, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE),
        INITIAL_STOCK_X + scale(big_length, len_arr[i]), INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + STOCK_H,
        outline='black',
        fill=colors[i])
    canvas.create_text((INITIAL_STOCK_X + 20, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + 10),
                       text=str(len_arr[i]) + 'm', font='Helvetica 10 bold')
    canvas.create_text((INITIAL_STOCK_X - 20, INITIAL_STOCK_Y + (i + 1) * (STOCK_H + STOCK_SPACE) + 10),
                       text=str(demand_arr[i]) + ' x  ', font='Helvetica 12 bold')

window.mainloop()
