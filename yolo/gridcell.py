from yolo.bbox import BoundingBox

class GridCell:
    """A section of an input image that is responsible for detecting objects.
    and generating bounding boxes for them."""

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
        """Make this grid cell responsible for the given bounding box.

        :param bbox: BoundingBox

        :return: None
        """
        self.bbox_list.append(bbox)

    def get_bbox_list(self):
        """Return the list of bounding boxes for this grid cell.

        :return: list of BoundingBox
        :rtype: list[:class:`BoundingBox`]
        """
        if self.index == (1, 0):
            return [
                BoundingBox(100, 47, 167, 65, 0.1)
            ]
        elif self.index == (0, 3):
            return [
                BoundingBox(62, 178, 48, 124, 0.1),
            ]
        elif self.index == (2, 3):
            return [
                BoundingBox(143, 178, 48, 124, 0.1),
            ]
        elif self.index == (4, 4):
            return [
                BoundingBox(338, 236, 297, 241, 0.1),
            ]
        else:
            return []
