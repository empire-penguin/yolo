class BoundingBox:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.w = 0.0
        self.h = 0.0
        self.c = 0.0

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

    def intersects(self, other: "BoundingBox"):
        """returns True if this bounding box intersects another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            bool: True if this bounding box intersects another bounding box
        """
        return (
            self.get_top_left()[0] < other.get_bottom_right()[0]
            and self.get_top_left()[1] < other.get_bottom_right()[1]
            and self.get_bottom_right()[0] > other.get_top_left()[0]
            and self.get_bottom_right()[1] > other.get_top_left()[1]
        )

    def get_area(self):
        return self.w * self.h

    def union_area(self, other: "BoundingBox"):
        """returns the union of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            BoundingBox: the union of this bounding box and another bounding box
        """
        area = 0.0
        if self.intersects(other):
            top_left = (
                min(self.get_top_left()[0], other.get_top_left()[0]),
                min(self.get_top_left()[1], other.get_top_left()[1]),
            )
            bottom_right = (
                max(self.get_bottom_right()[0], other.get_bottom_right()[0]),
                max(self.get_bottom_right()[1], other.get_bottom_right()[1]),
            )
            area = (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[1])
        else:
            area = self.get_area() + other.get_area()

    def intrsect_area(self, other: "BoundingBox"):
        """returns the intersection of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            BoundingBox: the intersection of this bounding box and another bounding box
        """
        area = 0.0
        if self.intersects(other):
            top_left = (
                max(self.get_top_left()[0], other.get_top_left()[0]),
                max(self.get_top_left()[1], other.get_top_left()[1]),
            )
            bottom_right = (
                min(self.get_bottom_right()[0], other.get_bottom_right()[0]),
                min(self.get_bottom_right()[1], other.get_bottom_right()[1]),
            )
            area = (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[1])
        return area

    def iou(self, other: "BoundingBox"):
        """returns the intersection over union of this bounding box and another bounding box

        Args:
            other (BoundingBox): another bounding box

        Returns:
            float: the intersection over union of this bounding box and another bounding box
        """
        return self.intrsect_area(other) / self.union_area(other)
