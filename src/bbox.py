import math


class BoundingBox:
    def __init__(self, x, y, w, h, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c

    def __str__(self):
        return f"({self.x}, {self.y}, {self.w}, {self.h}, {self.c})"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.w}, {self.h}, {self.c})"

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.w == other.w
            and self.h == other.h
            and self.c == other.c
        )

    def get_top_left(self):
        return (self.x - self.w / 2, self.y - self.h / 2)

    def get_bottom_right(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_center(self):
        return (self.x, self.y)

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def get_confidence(self):
        return self.c

    def get_xmin(self):
        return self.get_top_left()[0]

    def get_ymin(self):
        return self.get_top_left()[1]

    def get_xmax(self):
        return self.get_bottom_right()[0]

    def get_ymax(self):
        return self.get_bottom_right()[1]

    def intersects(self, other: "BoundingBox"):
        """returns True if this bounding box intersects another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            bool: True if this bounding box intersects another bounding box
        """
        return (
            self.get_xmin() <= other.get_xmax()
            and self.get_xmax() >= other.get_xmin()
            and self.get_ymin() <= other.get_ymax()
            and self.get_ymax() >= other.get_ymin()
        )

    def contains(self, x, y):
        """returns True if this bounding box contains a point

        Args:
            x (float): x coordinate of point
            y (float): y coordinate of point

        Returns:
            bool: True if this bounding box contains a point
        """
        return (
            self.get_top_left()[0] < x
            and self.get_top_left()[1] < y
            and self.get_bottom_right()[0] > x
            and self.get_bottom_right()[1] > y
        )

    def on_edge(self, x, y, delta):
        """returns True if these pairs of x, y coordinates are on the edge of this bounding box

        Args:
            x (float): x coordinate of point
            y (float): y coordinate of point

        Returns:
            bool: True if this bounding box contains a point
        """
        inclsv_bb = BoundingBox(self.x, self.y, self.w + delta, self.h + delta, self.c)
        exclsv_bb = BoundingBox(self.x, self.y, self.w - delta, self.h - delta, self.c)
        return inclsv_bb.contains(x, y) and not exclsv_bb.contains(x, y)

    def get_area(self):
        return self.w * self.h

    def union_area(self, other: "BoundingBox"):
        """returns the union of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            BoundingBox: the union of this bounding box and another bounding box
        """
        if self.intersects(other):
            return self.get_area() + other.get_area() - self.int_area(other)
        else:
            return self.get_area() + other.get_area()

    def int_area(self, other: "BoundingBox"):
        """returns the intersection of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            BoundingBox: the intersection of this bounding box and another bounding box
        """
        if self.intersects(other):
            top_left = (
                max(self.get_top_left()[0], other.get_top_left()[0]),
                max(self.get_top_left()[1], other.get_top_left()[1]),
            )
            bottom_right = (
                min(self.get_bottom_right()[0], other.get_bottom_right()[0]),
                min(self.get_bottom_right()[1], other.get_bottom_right()[1]),
            )
            return (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[1])
        else:
            return 0.0

    def iou(self, other: "BoundingBox"):
        """returns the intersection over union of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            float: the intersection over union of this bounding box and another bounding box
        """
        return self.int_area(other) / self.union_area(other)
