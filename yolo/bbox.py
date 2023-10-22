import math


class BoundingBox:
    """Bounding box around an object in an image"""

    def __init__(self, x, y, w, h, c):
        """Constructor for a bounding box

        :param x: x coordinate of center of bounding box
        :type x: float

        :param y: y coordinate of center of bounding box
        :type y: float

        :param w: width of bounding box
        :type w: float

        :param h: height of bounding box
        :type h: float

        :param c: confidence of bounding box (will be represented by boldness)
        :type c: float

        :returns: instance of the BoundingBox class
        :rtype: :class:`BoundingBox`
        """
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
        """
        :returns: top left corner of the bounding box
        :rtype: tuple (float, float)
        """
        return (self.x - self.w / 2, self.y - self.h / 2)

    def get_bottom_right(self):
        """
        :returns: bottom right corner of the bounding box
        :rtype: tuple (float, float)
        """
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_center(self):
        """
        :returns: center of the bounding box
        :rtype: tuple (float, float)
        """
        return (self.x, self.y)

    def get_width(self):
        """
        :returns: width of the bounding box
        :rtype: float
        """
        return self.w

    def get_height(self):
        """
        :returns: height of the bounding box
        :rtype: float
        """
        return self.h

    def get_confidence(self):
        """
        :returns: confidence of the bounding box
        :rtype: float
        """
        return self.c

    def get_area(self):
        """
        :returns: area of the bounding box
        :rtype: float
        """
        return self.w * self.h

    def get_xmin(self):
        """
        :returns: x coordinate of top left corner of the bounding box
        :rtype: float
        """
        return self.get_top_left()[0]

    def get_ymin(self):
        """
        :returns: y coordinate of top left corner of the bounding box
        :rtype: float
        """
        return self.get_top_left()[1]

    def get_xmax(self):
        """
        :returns: x coordinate of bottom right corner of the bounding box
        :rtype: float
        """
        return self.get_bottom_right()[0]

    def get_ymax(self):
        """
        :returns: y coordinate of bottom right corner of the bounding box
        :rtype: float
        """
        return self.get_bottom_right()[1]

    def intersects(self, other: "BoundingBox"):
        """Tests if this bounding box intersects another bounding box

        :returns: True if this bounding box intersects another bounding box
        :rtype: bool
        """
        return (
            self.get_xmin() <= other.get_xmax()
            and self.get_xmax() >= other.get_xmin()
            and self.get_ymin() <= other.get_ymax()
            and self.get_ymax() >= other.get_ymin()
        )

    def contains(self, x, y):
        """Tests if this bounding box contains a given (x,y) point

        :returns: True if this bounding box contains a point
        :rtype: bool
        """
        return (
            self.get_top_left()[0] < x
            and self.get_top_left()[1] < y
            and self.get_bottom_right()[0] > x
            and self.get_bottom_right()[1] > y
        )

    def on_edge(self, x, y, delta):
        """Tests if a given (x,y) point is on the edge of this bounding box

        :returns: True if a given (x,y) point is on the edge of this bounding box
        :rtype: bool
        """
        inclsv_bb = BoundingBox(self.x, self.y, self.w + delta, self.h + delta, self.c)
        exclsv_bb = BoundingBox(self.x, self.y, self.w - delta, self.h - delta, self.c)
        return inclsv_bb.contains(x, y) and not exclsv_bb.contains(x, y)

    def union_area(self, other: "BoundingBox"):
        """Performs the union of this bounding box and another bounding box
        and returns the area of the union

        :returns: the union of this bounding box and another bounding box
        :rtype: float
        """
        if self.intersects(other):
            return self.get_area() + other.get_area() - self.int_area(other)
        else:
            return self.get_area() + other.get_area()

    def int_area(self, other: "BoundingBox"):
        """Performs the intersection of this bounding box and another bounding box
        and returns the area of the intersection

        :returns: the intersection of this bounding box and another bounding box
        :rtype: float
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
        """Calculates the intersection over union of this bounding box and another bounding box

        :returns: intersection over union of this bounding box and another bounding box
        :rtype: float
        """
        return self.int_area(other) / self.union_area(other)
