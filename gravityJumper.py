import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60, title="Gravity Jumper")

        self.start_screen = True
        self.reset_game()

        self.score = 0

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player_x = 30
        self.player_y = 20
        self.player_size = 10
        self.player_dy = 0
        self.gravity = 1.0
        self.is_alive = True

        self.game_over = False

        self.obstacles = [
            (
                pyxel.width + i * 50,
                pyxel.rndi(0, pyxel.height - 20),
                pyxel.rndi(self.player_size + 4, self.player_size + 16),
                False,
                1,
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

        max_speed = 2

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
        base_speed = .75
        difficulty = 0.025 * self.score
        var_range = min(difficulty, 3.5)
        y_spawn_speed = 0.025 * self.score
        seek_strength = max(0.000003 * self.score, 0.0)
        max_y_speed = 0.03 + 0.01 * self.score
        min_size = self.player_size + 4
        max_size = self.player_size + 8

        new_obstacles = []
        for x, y, size, passed, speed, yspeed in self.obstacles:
            current_speed = speed + difficulty + pyxel.rndf(-var_range, var_range)*0.5
            current_speed = max(0.4, current_speed)
            x -= current_speed

            dy_to_player = self.player_y - y
            yspeed += max(-seek_strength, min(seek_strength, dy_to_player * 0.01))
            if yspeed > max_y_speed:
                yspeed = max_y_speed
            elif yspeed < -max_y_speed:
                yspeed = -max_y_speed
            y += yspeed

            if not passed and x + size < self.player_x:
                self.score += 1
                passed = True

            if y < 0:
                y = 0
                yspeed *= -0.6
            elif y + size > pyxel.height:
                y = pyxel.height - size
                yspeed *= -0.6

            if x + size > 0:
                new_obstacles.append((x, y, size, passed, speed, yspeed))
            else:
                ny = pyxel.rndi(0, pyxel.height - max_size)
                nsize = pyxel.rndi(min_size, max_size)
                nbase = base_speed + 0.02 * self.score + pyxel.rndf(0.0, var_range)
                dir_to_player = 1 if ny < self.player_y else -1
                nys = dir_to_player * (0.2 + 0.01 * self.score) + pyxel.rndf(-0.1, 0.1)
                new_obstacles.append((pyxel.width + pyxel.rndi(0, 30), ny, nsize, False, nbase, nys))

        while len(new_obstacles) < 3:
            ny = pyxel.rndi(0, pyxel.height - max_size)
            nsize = pyxel.rndi(min_size, max_size)
            nbase = base_speed + 0.02 * self.score + pyxel.rndf(0.0, var_range)
            dir_to_player = 1 if ny < self.player_y else -1
            nys = dir_to_player * (0.2 + 0.01 * self.score) + pyxel.rndf(-0.1, 0.1)
            new_obstacles.append((pyxel.width + pyxel.rndi(0, 30), ny, nsize, False, nbase, nys))

        self.obstacles = new_obstacles

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