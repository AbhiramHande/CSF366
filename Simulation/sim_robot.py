import math
import numpy as np

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
        self.path = [[0.0, 0.0]]

    # Helper function to round all values up to 4 decimal digits
    def _round_values(self):
        self.position = [round(x, 4) for x in self.position]
        self.dir_facing = [round(x, 4) for x in self.dir_facing]
        self.dir_left = [round(x, 4) for x in self.dir_left]

    def set_speed(self, value):
        self.speed = value

    def _move(self, direction, time):
        dx = direction[0] * self.speed * time
        dy = direction[1] * self.speed * time
        self.position[0] += dx
        self.position[1] += dy
        self._round_values()
        self.path.append(list(self.position))

    def move_horizontal(self, time):
        self._move(self.dir_facing, time)

    def move_rhorizontal(self, time):
        self._move([-x for x in self.dir_facing], time)

    def move_vertical(self, time):
        self._move(self.dir_left, time)

    def move_rvertical(self, time):
        self._move([-x for x in self.dir_left], time)

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

    def rotate_clockwise(self, angle_deg):
        self._rotate(angle_deg)

    def rotate_anticlockwise(self, angle_deg):
        self._rotate(-angle_deg)

    def _get_nearest_wall_coord(self, direction, room_corners):
        def intersect(ray_origin, ray_dir, seg_start, seg_end):
            """
            Computes intersection point of ray (ray_origin + t * ray_dir)
            with segment (seg_start to seg_end), if it exists.

            Returns:
                Tuple (x, y) if intersection occurs, else None
            """
            EPSILON = 1e-8
            r = ray_dir
            s = [seg_end[0] - seg_start[0], seg_end[1] - seg_start[1]]
            r_cross_s = r[0] * s[1] - r[1] * s[0]

            if abs(r_cross_s) < EPSILON:
                return None  # Parallel lines

            qp = [seg_start[0] - ray_origin[0], seg_start[1] - ray_origin[1]]
            t = (qp[0] * s[1] - qp[1] * s[0]) / r_cross_s
            u = (qp[0] * r[1] - qp[1] * r[0]) / r_cross_s

            if t >= 0 and 0 <= u <= 1:
                intersection = (ray_origin[0] + t * r[0], ray_origin[1] + t * r[1])
                return intersection

            return None

        pos = self.position
        ray = direction
        min_dist = float('inf')
        closest_point = None

        n = len(room_corners)
        for i in range(0, len(room_corners) - 1):
            p1 = room_corners[i]
            p2 = room_corners[i + 1]
            if len(p1) != 2 or len(p2) != 2:
                print(f"Malformed segment: p1={p1}, p2={p2}")
                continue
            hit = intersect(pos, ray, p1, p2)
            if hit:
                dist = (hit[0] - pos[0]) ** 2 + (hit[1] - pos[1]) ** 2
                if dist < min_dist:
                    min_dist = dist
                    closest_point = hit

        return closest_point

    
    def get_forward_wall(self, room_corners):
        return self._get_nearest_wall_coord(self.dir_facing, room_corners)

    def get_side_wall(self, room_corners):
        return self._get_nearest_wall_coord(self.dir_left, room_corners)


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
