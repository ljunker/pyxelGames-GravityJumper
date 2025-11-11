import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Gravity Jumper")

        self.player_x = 72
        self.player_y = 20
        self.player_size = 10
        self.player_dy = 0
        self.gravity = 1
        self.is_alive = True

        self.start_screen = True

        self.floor = [(i * 60, pyxel.rndi(8, 104), True) for i in range(4)]

        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(0)
        if self.start_screen:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.start_screen = False
        else:
            self.update_player()

    def update_player(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            print("Space pressed")
            self.gravity = self.gravity * -1
        if self.player_y < pyxel.height - (self.player_size/2) or self.player_y <= self.player_size/2:
            self.player_dy = min(self.player_dy + 1, 4)
        else:
            self.player_dy = 0
        self.player_y += self.player_dy * self.gravity

    def draw(self):
        pyxel.cls(0)
        if self.start_screen:
            pyxel.text(55, 41, "Gravity Jumper", 10)
        else:
            pyxel.rect(self.player_x, self.player_y, self.player_size, self.player_size, 100)


App()