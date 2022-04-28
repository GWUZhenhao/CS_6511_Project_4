import time
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage
UNIT = 100
HEIGHT = 7
WIDTH = 7

class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Q Learning')
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.texts = []

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT)

        for c in range(0, WIDTH * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1)

        self.agent = canvas.create_image(50, 50, image=self.shapes[0])
        self.trap1 = canvas.create_image(350, 250, image=self.shapes[1])
        self.trap2 = canvas.create_image(150, 350, image=self.shapes[1])
        self.exit = canvas.create_image(350, 450, image=self.shapes[2])

        canvas.pack()

        return canvas

    def load_images(self):
        agent = PhotoImage(
            Image.open("r.png").resize((65, 65)))
        triangle = PhotoImage(
            Image.open("f.png").resize((65, 65)))
        exit = PhotoImage(
            Image.open("e.png").resize((65, 65)))

        return agent, triangle, exit

    def text_value(self, row, col, contents, action, font='Helvetica', size=10,
                   style='normal', anchor="nw"):

        if action == 0:
            origin_x, origin_y = 7, 42
        elif action == 1:
            origin_x, origin_y = 85, 42
        elif action == 2:
            origin_x, origin_y = 42, 5
        else:
            origin_x, origin_y = 42, 77

        x, y = origin_y + (UNIT * col), origin_x + (UNIT * row)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=contents,
                                       font=font, anchor=anchor)
        return self.texts.append(text)

    def print_value_all(self, q_table):
        for i in self.texts:
            self.canvas.delete(i)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                for action in range(0, 4):
                    state = [i, j]
                    if str(state) in q_table.keys():
                        temp = q_table[str(state)][action]
                        self.text_value(j, i, round(temp, 2), action)

    def coords_to_state(self, coords):
        x = int((coords[0] - 50) / 100)
        y = int((coords[1] - 50) / 100)
        return [x, y]

    def state_to_coords(self, state):
        x = int(state[0] * 100 + 50)
        y = int(state[1] * 100 + 50)
        return [x, y]

    def reset(self):
        self.update()
        time.sleep(0.5)
        x, y = self.canvas.coords(self.agent)
        self.canvas.move(self.agent, UNIT / 2 - x, UNIT / 2 - y)
        self.render()
        return self.coords_to_state(self.canvas.coords(self.agent))

    def step(self, action):
        state = self.canvas.coords(self.agent)
        base_action = np.array([0, 0])
        self.render()

        if action == 0:
            if state[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:
            if state[1] < (HEIGHT - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:
            if state[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 3:
            if state[0] < (WIDTH - 1) * UNIT:
                base_action[0] += UNIT

        self.canvas.move(self.agent, base_action[0], base_action[1])
        self.canvas.tag_raise(self.agent)
        next_state = self.canvas.coords(self.agent)

        if next_state == self.canvas.coords(self.exit):
            reward = 100
            done = True
        elif next_state in [self.canvas.coords(self.trap1),
                            self.canvas.coords(self.trap2)]:
            reward = -100
            done = False
        else:
            reward = 0
            done = False

        next_state = self.coords_to_state(next_state)
        return next_state, reward, done

    def render(self):
        time.sleep(0.03)
        self.update()
