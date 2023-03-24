from PIL import Image, ImageDraw
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GraphicsEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.edge_list = []
    
    def add_edge(self, start, end):
        self.edge_list.append((start, end))
    
    def draw_lines(self, color):
        for start, end in self.edge_list:
            self.draw.line((start.x, start.y, end.x, end.y), fill=color)
    
    def draw_circle(self, center, radius, color):
        x = 0
        y = radius
        d = 1 - radius
        self.draw_circle_points(center, x, y, color)
        while y > x:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            self.draw_circle_points(center, x, y, color)
    
    def draw_circle_points(self, center, x, y, color):
        self.set_pixel(center.x + x, center.y + y, color)
        self.set_pixel(center.x - x, center.y + y, color)
        self.set_pixel(center.x + x, center.y - y, color)
        self.set_pixel(center.x - x, center.y - y, color)
        self.set_pixel(center.x + y, center.y + x, color)
        self.set_pixel(center.x - y, center.y + x, color)
        self.set_pixel(center.x + y, center.y - x, color)
        self.set_pixel(center.x - y, center.y - x, color)
    
    def draw_bezier_curve(self, points, color):
        for t in range(0, 101):
            x, y = self.evaluate_bezier_curve(points, t / 100)
            self.set_pixel(int(round(x)), int(round(y)), color)
    
    def evaluate_bezier_curve(self, points, t):
        n = len(points) - 1
        x = 0
        y = 0
        for i in range(n + 1):
            coeff = math.comb(n, i) * pow(1 - t, n - i) * pow(t, i)
            x += coeff * points[i].x
            y += coeff * points[i].y
        return x, y
    
    def draw_hermite_curve(self, start, end, tangent1, tangent2, color):
        for t in range(0, 101):
            x, y = self.evaluate_hermite_curve(start, end, tangent1, tangent2, t / 100)
            self.set_pixel(int(round(x)), int(round(y)), color)
    
    def evaluate_hermite_curve(self, start, end, tangent1, tangent2, t):
        h1 = 2 * pow(t, 3) - 3 * pow(t, 2) + 1
        h2 = -2 * pow(t, 3) + 3 * pow(t, 2)
        h3 = pow(t, 3) - 2 * pow(t, 2) + t
        h4 = pow(t, 3) - pow(t, 2)
        x = h1 * start.x + h2 * end.x + h3 * tangent1.x + h4 * tangent2.x
        y = h1 * start.y + h2 * end.y + h3 * tangent1.y + h4 * tangent2.y
        return x, y
    
    def set_pixel(self, x, y, color):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.image.putpixel((x, y), color)
    
    def apply_transformation(self, transformation_matrix):
        for i in range(0, len(self.edge_list)):
            start = self.edge_list[i][0]
            end = self.edge_list[i][1]
            start_matrix = [start.x, start.y, 1]
            end_matrix = [end.x, end.y, 1]
            new_start = self.multiply_matrix(transformation_matrix, start_matrix)
            new_end = self.multiply_matrix(transformation_matrix, end_matrix)
            self.edge_list[i] = (Point(new_start[0], new_start[1]), Point(new_end[0], new_end[1]))
    
    def multiply_matrix(self, matrix1, matrix2):
        result = [0, 0, 0]
        for i in range(0, len(matrix1)):
            for j in range(0, len(matrix2[0])):
                for k in range(0, len(matrix2)):
                    result[i] += matrix1[i][k] * matrix2[k][j]
        return result
    
    def translate(self, dx, dy):
        self.apply_transformation([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
    
    def rotate(self, theta):
        radians = math.radians(theta)
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)
        self.apply_transformation([[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0], [0, 0, 1]])
    
    def dilate(self, scale):
        self.apply_transformation([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
    
    def save_image(self, filename):
        self.image.save(filename)
    
    def display_image(self):
        self.image.show()

    def draw_line(self, start, end, color):
        dx = end.x - start.x
        dy = end.y - start.y
        if dx == 0:
            self.draw_vertical_line(start.y, end.y, start.x, color)
        elif dy == 0:
            self.draw_horizontal_line(start.x, end.x, start.y, color)
        else:
            slope = dy / dx
            if abs(slope) <= 1:
                if dx > 0:
                    self.draw_low_slope_line(start, end, color)
                else:
                    self.draw_low_slope_line(end, start, color)
            else:
                if dy > 0:
                    self.draw_high_slope_line(start, end, color)
                else:
                    self.draw_high_slope_line(end, start, color)
    
    def draw_horizontal_line(self, x1, x2, y, color):
        for x in range(x1, x2 + 1):
            self.set_pixel(x, y, color)
    
    def draw_vertical_line(self, y1, y2, x, color):
        for y in range(y1, y2 + 1):
            self.set_pixel(x, y, color)
    
    def draw_low_slope_line(self, start, end, color):
        dx = end.x - start.x
        dy = end.y - start.y
        d = 2 * dy - dx
        y = start.y
        for x in range(start.x, end.x + 1):
            self.set_pixel(x, y, color)
            if d > 0:
                y += 1
                d -= 2 * dx
            d += 2 * dy
    
    def draw_high_slope_line(self, start, end, color):
        dx = end.x - start.x
        dy = end.y - start.y
        d = 2 * dx - dy
        x = start.x
        for y in range(start.y, end.y + 1):
            self.set_pixel(x, y, color)
            if d > 0:
                x += 1
                d -= 2 * dy
            d += 2 * dx

def test_graphics_engine():
    # initialize the graphics engine with a width and height
    engine = GraphicsEngine(500, 500)

    # draw a line from (100, 100) to (400, 400)
    engine.draw_line(Point(100, 100), Point(400, 400), (255, 0, 0))

    # draw a circle with center (250, 250) and radius 100
    engine.draw_circle(Point(250, 250), 100, (0, 255, 0))

    # draw a Bezier curve with control points (100, 100), (150, 400), (350, 100), and (400, 400)
    engine.draw_bezier_curve([Point(100, 100), Point(150, 400), Point(350, 100), Point(400, 400)], (0, 0, 255))

    # draw a Hermite curve with start point (100, 100), end point (400, 400), start tangent (150, 200), and end tangent (300, 300)
    engine.draw_hermite_curve(Point(100, 100), Point(400, 400), Point(150, 200), Point(300, 300), (255, 255, 0))

    # apply transformations to the edge list of points
    engine.translate(50, 50)
    engine.rotate(45)
    engine.dilate(0.5)

    # save and display the resulting image
    engine.save_image("test_image.png")
    engine.display_image()

test_graphics_engine()