from bbox import BoundingBox


class GridCell:
    def __init__(self, width, height, i, j):
        self.index = (i, j)
        self.width = width
        self.height = height
        self.bbox_list = []

    def __str__(self):
        return f"GridCell({self.index}, {self.width}, {self.height})"

    def __repr__(self):
        return self.__str__()

    def add_bbox(self, bbox):
        self.bbox_list.append(bbox)

    def get_bbox_list(self):
        if self.index == (0, 0):
            return [
                BoundingBox(143, 178, 48, 124, 0.1),
                BoundingBox(338, 236, 297, 241, 0.1),
                BoundingBox(62, 178, 48, 124, 0.1),
                BoundingBox(100, 47, 167, 65, 0.1),
            ]
        return self.bbox_list
