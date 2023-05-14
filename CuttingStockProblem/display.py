import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk, LEFT, Frame, Scrollbar
from typing import List, Dict
import queue
import threading

from EP_approach import EP_Optimizer
from GA_approach import GA_Optimizer


class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Loading...")
        self.geometry("200x100")
        self.loading_label = tk.Label(self, text="Loading...")
        self.loading_label.pack(expand=True)


class Display(object):

    def __init__(self):
        self.window = tk.Tk()
        self.loading_screen = None
        self.SCREEN_W = self.window.winfo_screenwidth()
        self.SCREEN_H = self.window.winfo_screenheight()
        self.MAIN_STOCK_LEN_SCALED = self.SCREEN_W // 3
        self.INITIAL_STOCK_X = 50
        self.INITIAL_STOCK_Y = 50
        self.STOCK_H = 20
        self.STOCK_SPACE = 10
        self.DEFAULT_COLORS = ['#e0edcc', '#e6d9cc', '#d1eded', '#e5d1ed', '#cfb8b8', '#fafcd4', '#d3cfff', '#ffd1fd', '#bac2b8', '#e6cbb3',
                               '#c6afc7', '#ebeada', '#d4fae0', '#bfd4db', '#e6bee6', '#bdc7af', '#c7afb3', '#bdbedb', '#dbd1bd', '#b8cfd1',
                               '#d1b8c1', '#eddfec', '#c0b8d1', '#ededdf']
        self.window.geometry(f'{self.SCREEN_W}x{self.SCREEN_H}')
        self.window.config(bg='#fff')
        self.window.title('Cutting stock problem')
        self.var = tk.IntVar()
        self.requirements_canvas = self.create_canvas()
        self.result_canvas = self.create_canvas()
        self.requirements_canvas.grid(row=1, column=0, padx=5, pady=5)
        self.result_canvas.grid(row=1, column=2, padx=5, pady=5)
        self.optimizer = EP_Optimizer()
        self.chosen_file = None

    def scale(self, main_stock_len, stock_len):
        return int(self.MAIN_STOCK_LEN_SCALED * stock_len / main_stock_len)

    def select_file(self):
        file_types = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        self.chosen_file = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=file_types)
        self.reload()

    def reload(self):
        my_queue = queue.Queue()
        self.loading_screen = LoadingScreen(self.window)
        thread = threading.Thread(target=self.optimizer.optimize, args=(self.chosen_file, my_queue))
        thread.start()
        self.window.after(100, self.check_queue, my_queue)

    def check_queue(self, my_queue):
        if not my_queue.empty():
            stock_len, l_arr, d_arr, result = my_queue.get(block=False)
            self.display_content(stock_len, l_arr, d_arr, result)
            self.loading_screen.destroy()
        else:
            self.window.after(100, self.check_queue, my_queue)

    def display_prompt(self):
        frame = Frame(self.window, width=self.SCREEN_W, height=150)
        frame.grid(row=0, column=0, sticky='EW', columnspan=3, padx=10, pady=10)
        open_button = ttk.Button(
            frame,
            text='Open a File',
            command=self.select_file
        )
        open_button.pack(side=LEFT)
        option_ep = tk.Radiobutton(frame, text='Evolutionary programming', variable=self.var, value=1, command=self.selected_option_changed)
        option_ga = tk.Radiobutton(frame, text='Genetic algorithm', variable=self.var, value=2, command=self.selected_option_changed)
        option_ga.pack(side=tk.RIGHT)
        option_ep.pack(side=tk.RIGHT)
        option_ep.select()

    def selected_option_changed(self):
        if self.var.get() == 2:
            self.optimizer = GA_Optimizer()
        else:
            self.optimizer = EP_Optimizer()
        self.reload()

    def display_requirements(self, L, lengths, demand):
        N = len(lengths)
        colors = self.DEFAULT_COLORS[:N]
        if N > len(colors):
            diff = N - len(colors)
            for i in range(diff):
                colors.append('#%06x' % random.randint(0x999999, 0xFFFFFF))
        colors_dict = {lengths[i]: colors[i] for i in range(N)}

        canvas = self.create_canvas()
        canvas.grid(row=1, column=0, padx=5, pady=5)
        scroll = self.create_scrollbar(canvas)
        scroll.grid(row=1, column=1, sticky='NE', pady=5)

        canvas.create_text((70, 15), text='Requirements', font='Helvetica 14 bold')
        canvas.create_rectangle(
            self.INITIAL_STOCK_X, self.INITIAL_STOCK_Y,
            self.INITIAL_STOCK_X + self.MAIN_STOCK_LEN_SCALED, self.INITIAL_STOCK_Y + self.STOCK_H,
            outline='black',
            fill='#333')
        canvas.create_text((self.INITIAL_STOCK_X + 30, self.INITIAL_STOCK_Y + 10), text=str(L) + 'm', fill='#fff', font='Helvetica 10 bold')

        for i in range(N):
            canvas.create_rectangle(
                self.INITIAL_STOCK_X, self.INITIAL_STOCK_Y + (i + 1) * (self.STOCK_H + self.STOCK_SPACE),
                                      self.INITIAL_STOCK_X + self.scale(L, lengths[i]),
                                      self.INITIAL_STOCK_Y + (i + 1) * (self.STOCK_H + self.STOCK_SPACE) + self.STOCK_H,
                outline='black',
                fill=colors[i])
            canvas.create_text((self.INITIAL_STOCK_X + 30, self.INITIAL_STOCK_Y + (i + 1) * (self.STOCK_H + self.STOCK_SPACE) + 10),
                               text=str(lengths[i]) + 'm', font='Helvetica 10 bold')
            canvas.create_text((self.INITIAL_STOCK_X - 20, self.INITIAL_STOCK_Y + (i + 1) * (self.STOCK_H + self.STOCK_SPACE) + 10),
                               text=str(demand[i]) + ' x  ', font='Helvetica 12 bold')
        return colors_dict

    def display_result(self, patterns: List[List[int]], colors: Dict[int, str], L):
        patterns_str = []
        for pattern in patterns:
            pattern.sort(reverse=True)
            patterns_str.append(','.join([str(num) for num in pattern]))
        patterns_cnt = {}
        for pattern in patterns_str:
            if pattern not in patterns_cnt:
                patterns_cnt[pattern] = 0
            patterns_cnt[pattern] += 1

        canvas = self.create_canvas()
        canvas.grid(row=1, column=2, padx=5, pady=5)
        scroll = self.create_scrollbar(canvas)
        scroll.grid(row=1, column=3, sticky='NE', pady=5)

        canvas.create_text((35, 15), text='Result', font='Helvetica 14 bold')
        i = 0
        for pattern, cnt in patterns_cnt.items():
            canvas.create_text((self.INITIAL_STOCK_X - 20, self.INITIAL_STOCK_Y + i * (self.STOCK_H + self.STOCK_SPACE) + 10),
                               text=str(cnt) + ' x  ', font='Helvetica 12 bold')
            start_x = self.INITIAL_STOCK_X
            for j, num in enumerate(pattern.split(',')):
                num = int(num)
                current_stock_len = self.scale(L, num)
                canvas.create_rectangle(
                    start_x, self.INITIAL_STOCK_Y + i * (self.STOCK_H + self.STOCK_SPACE),
                             start_x + current_stock_len, self.INITIAL_STOCK_Y + i * (self.STOCK_H + self.STOCK_SPACE) + self.STOCK_H,
                    outline='black',
                    fill=colors[num]
                )
                canvas.create_text(
                    start_x + 30, self.INITIAL_STOCK_Y + i * (self.STOCK_H + self.STOCK_SPACE) + 10,
                    text=str(num) + 'm', font='Helvetica 10 bold'
                )
                start_x += current_stock_len
            i += 1

    def create_canvas(self):
        canvas = tk.Canvas(
            self.window,
            height=self.SCREEN_H - 100,
            width=self.SCREEN_W // 2 - 40,
            bg='white'
        )
        canvas.configure(scrollregion=canvas.bbox("all"))
        return canvas

    def create_scrollbar(self, canvas):
        scroll = Scrollbar(self.window, orient='vertical', command=canvas.yview)
        return scroll

    def display_content(self, stock_len, l_arr, d_arr, result):
        colors = self.display_requirements(stock_len, l_arr, d_arr)
        self.display_result(result, colors, stock_len)

    def display(self):
        self.display_prompt()
        self.window.mainloop()


if __name__ == '__main__':
    display = Display()
    display.display()
