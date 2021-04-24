from random import randint
import os
import pyglet as pg
import numpy as np
import tkinter as tk
from tkinter import messagebox as mb
import queue as qu


def game(m, n, mines):
    class Map:
        test_map = 0
        catalog = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        game = True

        def __init__(self, m, n, mines):
            self.n = n  # 10
            self.m = m  # 10
            if mines > m * n:
                self.mines = m * n
            else:
                self.mines = mines
            print(self.mines)

        def generator(self):
            self.time = 0
            self.smail = img['smail']
            self.count = self.mines
            self.arr = [[0 for j in range(self.m + 2)] for i in range(self.n + 2)]
            self.cell = 20
            if self.mines < self.n * self.m // 2:
                for i in range(self.mines):
                    x, y = randint(1, self.m), randint(1, self.n)
                    while self.arr[y][x] == -1:
                        x, y = randint(1, self.m), randint(1, self.n)
                    self.arr[y][x] = -1
            else:
                for i in range(1, self.n + 1):
                    for j in range(1, self.m + 1):
                        self.arr[i][j] = -1
                for i in range(self.n * self.m - self.mines):
                    x, y = randint(1, self.m), randint(1, self.n)
                    while self.arr[y][x] == 0:
                        x, y = randint(1, self.m), randint(1, self.n)
                    self.arr[y][x] = 0

            for i in range(1, self.n + 1):
                for j in range(1, self.m + 1):
                    if self.arr[i][j] != -1:
                        count = 0
                        for x, y in self.catalog:
                            if self.arr[i + x][j + y] == -1: count += 1
                        self.arr[i][j] = count

            self.arr = np.array([[self.arr[i][j] for j in range(1, self.m + 1)] for i in range(1, self.n + 1)])
            self.secrit = np.array([[self.test_map for j in range(self.m)] for i in range(self.n)])
            print(self.arr)

        def dead(self, x, y):
            self.smail = img['smail_dead']
            self.secrit[(self.arr != -1) == (self.secrit == -1)] = -2  # Miss Flag
            self.secrit[(self.secrit != -1) == (self.arr == -1)] = 1
            self.secrit[y][x] = -3  # Mines dead
            self.game = False
            mb.showinfo('Lose', 'You loose ( ´･･)ﾉ(._.`)')

        def win(self):
            if sum(self.arr[self.secrit == 1] != -1) == self.n * self.m - self.mines:
                self.smail = img['smail_win']
                self.game = False
                mb.showinfo('WIN', 'You win (～￣▽￣)～')

    pg.resource.path = ['./resources']
    pg.resource.reindex()

    img_list = list(os.walk('./resources'))[0][2]
    print(img_list)
    img = {i[:-4]: pg.resource.image(i) for i in img_list}

    map = Map(m, n, mines)
    map.generator()

    window = pg.window.Window(width=m * map.cell, height=n * map.cell + 40)

    # event_logger = pg.window.event.WindowEventLogger()  # Показывает все зарегестрированые события
    # window.push_handlers(event_logger)

    def time(dt):
        if map.time < 999:
            map.time += 1
    pg.clock.schedule_interval(time, 1)

    @window.event
    def on_draw():
        window.clear()
        pg.sprite.Sprite(img['line'], y=map.n * map.cell, x=-1980 + window.width).draw()
        pg.sprite.Sprite(map.smail, y=map.n * map.cell, x=window.width // 2 - 35 // 2).draw()
        pg.text.Label(str(map.count), y=window.height - 33, x=3, font_size=25, font_name='Calibri').draw()
        pg.text.Label(str(map.time), y=window.height - 33, x=window.width-50, font_size=25, font_name='Calibri').draw()

        if map.game:
            map.win()
        for i in range(map.n):
            for j in range(map.m):
                if map.secrit[i][j] == 0:
                    pg.sprite.Sprite(img['cell'], x=j * map.cell, y=i * map.cell).draw()
                elif map.secrit[i][j] == -1:
                    pg.sprite.Sprite(img['flag'], x=j * map.cell, y=i * map.cell).draw()
                elif map.secrit[i][j] == -2:
                    pg.sprite.Sprite(img['flag_miss'], x=j * map.cell, y=i * map.cell).draw()
                elif map.secrit[i][j] == -3:
                    pg.sprite.Sprite(img['mines_dead'], x=j * map.cell, y=i * map.cell).draw()
                else:
                    if map.arr[i][j] == -1:
                        pg.sprite.Sprite(img['mines'], x=j * map.cell, y=i * map.cell).draw()
                    elif map.arr[i][j] == 0:
                        pg.sprite.Sprite(img['empty'], x=j * map.cell, y=i * map.cell).draw()
                    else:
                        pg.sprite.Sprite(img[str(map.arr[i][j])], x=j * map.cell, y=i * map.cell).draw()

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == 1 and map.n * map.cell < y and map.n * map.cell + 40 > y \
                and map.m * map.cell // 2 - 17 < x and map.m * map.cell // 2 + 18 > x:
            map.generator()
            map.game = True
        elif map.game:
            if y // map.cell < n:
                if button == 1 and map.secrit[y // map.cell][x // map.cell] == 0:
                    map.secrit[y // map.cell][x // map.cell] = 1
                    if map.arr[y // map.cell][x // map.cell] == -1:
                        map.dead(x // map.cell, y // map.cell)
                    if map.arr[y // map.cell][x // map.cell] == 0:
                        catalog = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
                        q = qu.Queue()
                        q.put([x // map.cell, y // map.cell])
                        while not q.empty():
                            x, y = q.get()
                            for i in catalog:
                                if y + i[0] < n and x + i[1] < m and y + i[0] >= 0 and x + i[1] >= 0:
                                    if map.arr[y + i[0], x + i[1]] == 0 and map.secrit[y + i[0], x + i[1]] == 0:
                                        q.put([x + i[1], y + i[0]])
                                    map.secrit[y + i[0], x + i[1]] = 1
            if button == 4:
                if map.secrit[y // map.cell][x // map.cell] == 0:
                    map.secrit[y // map.cell][x // map.cell] = -1
                    map.count -= 1
                elif map.secrit[y // map.cell][x // map.cell] == -1:
                    map.secrit[y // map.cell][x // map.cell] = 0
                    map.count += 1

    pg.app.run()


def game_e():
    game(8, 8, 10)


def game_m():
    game(16, 16, 40)


def game_h():
    game(30, 16, 99)


def game_me():
    global nastoychivost
    try:
        m, n, mines = int(entry_m.get()), int(entry_n.get()), int(entry_mines.get())
        if m < 0 and n < 0:
            mb.showerror('Error', 'Entered too small values!\n Try again (✿◡‿◡)')
        elif m > 68 or n > 33:
            if not nastoychivost:
                mb.showerror('Error', 'Entered too large values <(＿　＿)>')
                nastoychivost = True
            else:
                mb.showerror('Error', 'Entered too large values ￣へ￣')
        else:
            game(m, n, mines)
    except:
        mb.showerror('Error', 'I entered non-natural numbers!')


def game_l():
    game(10, 10, 99)


nastoychivost = False
win = tk.Tk()
tk.Label(text='Hey, Minesweeper!').grid(row=0, columnspan=4)
tk.Label(text='Choose a difficulty level').grid(row=1, columnspan=4)

tk.Button(win, text='Easy', width=10, command=game_e).grid(row=2, column=0)
tk.Button(win, text='Normal', width=10, command=game_m).grid(row=2, column=1)
tk.Button(win, text='Hard', width=10, command=game_h).grid(row=2, column=2)
tk.Button(win, text='Pure luck', width=10, command=game_l).grid(row=2, column=3)

tk.Button(win, text='Customisable', width=10, command=game_me).grid(row=3, column=3, rowspan=2)

tk.Label(text='length').grid(row=3, column=0)
tk.Label(text='width').grid(row=3, column=1)
tk.Label(text='number of mines').grid(row=3, column=2)

entry_m = tk.Entry(win, width=10, font='callibri 10')
entry_m.grid(row=4, column=0)
entry_n = tk.Entry(win, width=10, font='callibri 10')
entry_n.grid(row=4, column=1)
entry_mines = tk.Entry(win, width=10, font='callibri 10')
entry_mines.grid(row=4, column=2)

win.mainloop()
