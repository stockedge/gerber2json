import attr

from enum import Enum, auto


class Polarity(Enum):
    CLEAR = auto()
    DARK = auto()


@attr.s
class Shape:
    polarity: Polarity = attr.ib(validator=attr.validators.instance_of(Polarity))


@attr.s
class CircleShape(Shape):
    pass


@attr.s
class StrokeShape(Shape):
    circle: CircleShape = attr.ib(validator=attr.validators.instance_of(CircleShape))


@attr.s
class RectangleShape(Shape):
    pass


@attr.s
class ObroundShape(Shape):
    pass


@attr.s
class PolygonShape(Shape):
    pass


@attr.s
class VectorLineShape(Shape):
    pass


@attr.s
class CenterLineShape(Shape):
    pass


@attr.s
class ThermalShape(Shape):
    pass


@attr.s
class ContourShape(Shape):
    contours: list[Shape] = attr.ib(validator=attr.validators.instance_of(list[Shape]), default=[])
