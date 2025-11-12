import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Gravity Jumper")

        self.start_screen = True
        self.reset_game()

        self.score = 0

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player_x = 30
        self.player_y = 20
        self.player_size = 10
        self.player_dy = 0
        self.gravity = 1
        self.is_alive = True

        self.game_over = False

        self.obstacles = [
            (
                pyxel.width + i * 50,
                pyxel.rndi(0, pyxel.height - 20),
                pyxel.rndi(self.player_size + 4, self.player_size + 16),
                False,
                2,  # Startgeschwindigkeit
                0
            )
            for i in range(3)
        ]

        self.score = 0

    def update(self):
        pyxel.cls(0)
        if self.start_screen:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.start_screen = False
        elif self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            if pyxel.btn(pyxel.KEY_Q):
                pyxel.quit()
        else:
            self.update_player()
            self.update_obstacles()
            if not self.is_alive:
                self.game_over = True

    def update_player(self):
        if not self.is_alive:
            return
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.gravity *= -1

        max_speed = 4

        self.player_dy = max(-max_speed, min(self.player_dy + self.gravity, max_speed))

        self.player_y += self.player_dy

        top = 0
        bottom = pyxel.height - self.player_size
        if self.player_y < top:
            self.player_y = top
            self.player_dy = 0
        elif self.player_y > bottom:
            self.player_y = bottom
            self.player_dy = 0

        if self.is_alive:
            px, py, ps = self.player_x, self.player_y, self.player_size
            for ox, oy, os, _, _, _ in self.obstacles:
                if px < ox + os and px + ps > ox and py < oy + os and py + ps > oy:
                    self.is_alive = False
                    break

    def update_obstacles(self):
        if not self.is_alive:
            return
        # Hindernisse sind Quadrate größer als der Spieler, bewegen sich von rechts nach links
        base_speed = 1.5
        difficulty = 0.05 * self.score
        var_range = min(difficulty, 3.5)
        y_spawn_speed = 0.05 * self.score
        min_size = self.player_size + 4
        max_size = self.player_size + 8

        new_obstacles = []
        for x, y, size, passed, speed, yspeed in self.obstacles:
            current_speed = speed + difficulty
            x -= current_speed
            y += yspeed

            if not passed and x + size < self.player_x:
                self.score += 1
                passed = True

            # Nur behalten, wenn noch im Bildschirm
            if x + size > 0:
                new_obstacles.append((x, y, size, passed, speed, yspeed))
            else:
                # Wieder rechts neu spawnen
                ny = pyxel.rndi(0, pyxel.height - max_size)
                ny_speed = pyxel.rndf(0, y_spawn_speed)
                if ny > pyxel.height//2:
                    ny_speed *= -1
                nsize = pyxel.rndi(min_size, max_size)
                nspeed = base_speed + pyxel.rndf(0, var_range)
                new_obstacles.append((pyxel.width + pyxel.rndi(0, 30), ny, nsize, False, nspeed, ny_speed))

        # Spawning-Ausdünnung: wenn zu wenige, füge neue rechts hinzu
        while len(new_obstacles) < 3:
            ny = pyxel.rndi(0, pyxel.height - max_size)
            ny_speed = pyxel.rndf(0, y_spawn_speed)
            if ny > pyxel.height // 2:
                ny_speed *= -1
            nsize = pyxel.rndi(min_size, max_size)
            nspeed = base_speed + pyxel.rndf(0, var_range)
            new_obstacles.append((pyxel.width + pyxel.rndi(0, 60), ny, nsize, False, nspeed, ny_speed))

        self.obstacles = new_obstacles

        # Optionale einfache Kollision
        px, py, ps = self.player_x, self.player_y, self.player_size
        for ox, oy, os, _, _, _ in self.obstacles:
            if px < ox + os and px + ps > ox and py < oy + os and py + ps > oy:
                self.is_alive = False

    def draw(self):
        pyxel.cls(0)
        if self.start_screen:
            self.draw_centered_text(41, "Gravity Jumper", 10)
            self.draw_centered_text(60, "ENTER to start", 7)
        elif self.game_over:
            self.draw_centered_text(41, "Game Over", 8)
            self.draw_centered_text(60, f"Score: {self.score}", 8)
            self.draw_centered_text(80, "[R]estart  [Q]uit", 8)
        else:

            pyxel.rect(self.player_x, self.player_y, self.player_size, self.player_size, 11)
            for x, y, size, _, _, _ in self.obstacles:
                pyxel.rect(x, y, size, size, 9)
            pyxel.text(4, 4, f"Score: {self.score}", 7)

    def draw_centered_text(self, y: int, text: str, color: int):
        w = len(text)*4
        x = (pyxel.width - w)//2
        pyxel.text(x, y, text, color)


App()