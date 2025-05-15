import math

class Robot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Robot, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.position = [0.0, 0.0]
        self.speed = 5.0
        self.dir_facing = [1.0, 0.0]
        self.dir_left = [0.0, -1.0]

    # Helper function to round all values up to 4 decimal digits
    def _round_values(self):
        self.position[0] = round(self.position[0], 4)
        self.position[1] = round(self.position[1], 4)
        self.dir_facing[0] = round(self.dir_facing[0], 4)
        self.dir_facing[1] = round(self.dir_facing[1], 4)
        self.dir_left[0] = round(self.dir_left[0], 4)
        self.dir_left[1] = round(self.dir_left[1], 4)

    def set_speed(self, value):
        self.speed = value

    def move_horizontal(self, time):
        dx = self.dir_facing[0] * self.speed * time
        dy = self.dir_facing[1] * self.speed * time
        self.position[0] += dx
        self.position[1] += dy
        self._round_values()

    def move_rhorizontal(self, time):
        dx = -self.dir_facing[0] * self.speed * time
        dy = -self.dir_facing[1] * self.speed * time
        self.position[0] += dx
        self.position[1] += dy
        self._round_values()

    def move_vertical(self, time):
        dx = self.dir_left[0] * self.speed * time
        dy = self.dir_left[1] * self.speed * time
        self.position[0] += dx
        self.position[1] += dy
        self._round_values()

    def move_rvertical(self, time):
        dx = -self.dir_left[0] * self.speed * time
        dy = -self.dir_left[1] * self.speed * time
        self.position[0] += dx
        self.position[1] += dy
        self._round_values()

    def rotate_clockwise(self, angle_deg):
        self._rotate(angle_deg)

    def rotate_anticlockwise(self, angle_deg):
        self._rotate(-angle_deg)

    def _rotate(self, angle_deg):
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        def rotate_vector(v):
            x, y = v
            return [x * cos_a - y * sin_a, x * sin_a + y * cos_a]

        self.dir_facing = rotate_vector(self.dir_facing)
        self.dir_left = rotate_vector(self.dir_left)
        self._round_values()

# Singleton instance
robot = Robot()

# Example usage
if __name__ == "__main__":
    robot.set_speed(10)
    print("Initial Position:", robot.position)
    robot.move_horizontal(2)
    print("After move_horizontal (2s):", robot.position)
    
    robot.rotate_clockwise(90)
    robot.move_vertical(1)  # move left (up) for 1 second
    print("After rotate_anticlockwise (90 deg) and move_vertical (1s):", robot.position)
    print("Facing Dir:", robot.dir_facing)
    print("Left Dir:", robot.dir_left)
