import math


class Clock:
    def __init__(self):
        self.last = 0
        self.round1 = 0
        self.hour = 0
        self.minutes = 0
        self.direction = 1
        self.reverse = 0
        self.angle = 0

        self.dot_pos = (250, 163)

    def calculate_angle(self, x, y):
        """Return angle based on cursor """
        if y <= 250 and x >= 250:
            a = 250 - y
            b = x - 250
            if a == 0:
                self.angle = 90
            else:
                tangens = b / a
                self.angle = math.degrees(math.atan(tangens))
        elif y >= 250 and x >= 250:
            a = y - 250
            b = x - 250

            if b == 0:
                self.angle = 180
            else:
                tangens = a / b
                self.angle = math.degrees(math.atan(tangens)) + 90
        elif y >= 250 and x <= 250 and self.round1 != 0:
            a = y - 250
            b = 250 - x

            if a == 0:
                self.angle = 270
            else:
                tangens = b / a
                self.angle = math.degrees(math.atan(tangens)) + 180
        elif y <= 250 and x <= 250 and self.round1 != 0:
            a = 250 - y
            b = 250 - x

            if a == 0:
                self.angle = 0
            else:
                tangens = a / b
                self.angle = math.degrees(math.atan(tangens)) + 270

        return int(self.angle)

    def clock_time(self):
        """returns time based on angle"""
        if self.last > self.angle:
            self.direction = 0
            self.round1 = 1
            if self.last - self.angle > 200:
                self.hour += 1
        elif self.last < self.angle:
            self.direction = 1

        if self.direction:
            if self.angle > 90 and self.round1 == 0:
                self.round1 = 1
        else:
            if self.angle > 300 and self.reverse == 0 and self.hour > 0:
                self.reverse = 1
                self.hour -= 1
            elif self.reverse == 1 and self.angle < 180 and self.hour > 0:
                self.reverse = 0
            elif self.hour == 0 and self.angle < 90:
                self.round1 = 0
        self.last = self.angle

        prompt_hour = str(self.hour)
        self.minutes = int(self.angle / 6)
        prompt_minutes = str(self.minutes)
        if self.hour < 10:
            prompt_hour = "0"+prompt_hour
        if self.minutes < 10:
            prompt_minutes = "0"+prompt_minutes
        return f"{prompt_hour}:{prompt_minutes}:00"

    def dot_validation(self):
        y = int(math.cos(math.radians(self.angle))*87)
        x = int(math.sin(math.radians(self.angle))*87)

        self.dot_pos = (250 + x, 250 - y)