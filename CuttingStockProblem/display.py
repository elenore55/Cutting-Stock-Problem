import tkinter as tk
import random

BIG_LEN_SCALED = 500


def scale(big_len, small_len):
    # 400 : big = x : small
    return int(BIG_LEN_SCALED * small_len / big_len)


window = tk.Tk()
window.geometry('1000x600')
window.config(bg='#fff')

req_label = tk.Label(text='Requirements')
req_label.pack()

big_length = 25
len_arr = [10, 7, 6, 4]
demand_arr = [21, 25, 30, 55]
colors = ['#%06x' % random.randint(0x999999, 0xFFFFFF) for _ in range(len(len_arr))]

canvas = tk.Canvas(
    window,
    height=400,
    width=1000,
    bg='#fff'
)

canvas.pack()

canvas.create_rectangle(
    50, 30, 50 + BIG_LEN_SCALED, 50,
    outline='black',
    fill='#333')
canvas.create_text((70, 40), text=str(big_length) + 'm', fill='#fff', font='Helvetica 10 bold')

for i in range(len(len_arr)):
    canvas.create_rectangle(
        50, 30 * (i + 2) + 20, 50 + scale(big_length, len_arr[i]), 30 * (i + 2) + 40,
        outline='black',
        fill=colors[i])
    canvas.create_text((70, 30 * (i + 2) + 30), text=str(len_arr[i]) + 'm', font='Helvetica 10 bold')
    canvas.create_text((30, 30 * (i + 2) + 30), text=str(demand_arr[i]) + ' x  ', font='Helvetica 12 bold')

window.mainloop()
