from abc import abstractmethod
from typing import TypeVar, Optional

import attr
import re

from command_converter import CommandVisitor

from enum import Enum, auto


class Metric(Enum):
    MILLE = auto()
    INCH = auto()


T = TypeVar('T')

int_re = re.compile(r"\d+")


def int_str_validator(self, attr_x, s: Optional[str]):
    if isinstance(s, str) and int_re.fullmatch(s) is None:
        raise ValueError('整数ではありません')


@attr.s
class Command:
    @abstractmethod
    def accept(self, visitor: 'CommandVisitor') -> T: pass


@attr.s
class D01Command(Command):
    x: Optional[str] = attr.ib(validator=int_str_validator)
    y: Optional[str] = attr.ib(validator=int_str_validator)
    i: Optional[str] = attr.ib(validator=int_str_validator)
    j: Optional[str] = attr.ib(validator=int_str_validator)

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d01(self)


@attr.s
class D02Command(Command):
    x: Optional[str] = attr.ib(validator=int_str_validator)
    y: Optional[str] = attr.ib(validator=int_str_validator)

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d02(self)


@attr.s
class D03Command(Command):
    x: Optional[str] = attr.ib(validator=int_str_validator)
    y: Optional[str] = attr.ib(validator=int_str_validator)

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d03(self)


@attr.s
class DnnCommand(Command):
    nn: int = attr.ib(validator=attr.validators.instance_of(int))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_dnn(self)


@attr.s
class SRCommand(Command):
    x: int = attr.ib()
    y: int = attr.ib()
    i: int = attr.ib()
    j: int = attr.ib()
    block: list[Command] = attr.ib()

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_sr(self)


@attr.s
class G04Command(Command):
    comment: str = attr.ib(validator=attr.validators.instance_of(str))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g04(self)


@attr.s
class MOCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_mo(self)


@attr.s
class FSCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_fs(self)


class Aperture: pass


@attr.s
class CircleAperure(Aperture):
    param1: float = attr.ib(validator=attr.validators.instance_of(float))
    param2: Optional[float] = attr.ib()


@attr.s
class RectangleAperture(Aperture):
    param1: float = attr.ib(validator=attr.validators.instance_of(float))
    param2: float = attr.ib(validator=attr.validators.instance_of(float))
    param3: Optional[float] = attr.ib()


@attr.s
class PolygonAperture(Aperture):
    param1: float = attr.ib(validator=attr.validators.instance_of(float))
    param2: float = attr.ib(validator=attr.validators.instance_of(float))
    param3: Optional[float] = attr.ib()
    param4: Optional[float] = attr.ib()


@attr.s
class ObroundAperture(Aperture):
    param1: float = attr.ib(validator=attr.validators.instance_of(float))
    param2: float = attr.ib(validator=attr.validators.instance_of(float))
    param3: Optional[float] = attr.ib()


@attr.s
class MacroAperture(Aperture):
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    params: list[float] = attr.ib()


@attr.s
class ADCommand(Command):
    aperture: Aperture = attr.ib(validator=attr.validators.instance_of(Aperture))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ad(self)


class AMExpr: pass


@attr.s
class AMVar(AMExpr):
    var: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s
class AMFloat(AMExpr):
    val: float = attr.ib(validator=attr.validators.instance_of(float))


@attr.s
class AMAdd(AMExpr):
    r: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))
    l: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))


@attr.s
class AMSub(AMExpr):
    r: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))
    l: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))


@attr.s
class AMMul(AMExpr):
    r: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))
    l: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))


@attr.s
class AMDiv(AMExpr):
    r: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))
    l: AMExpr = attr.ib(validator=attr.validators.instance_of(AMExpr))


@attr.s
class AMCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_am(self)


@attr.s
class G01Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g01(self)


@attr.s
class G02Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g02(self)


@attr.s
class G03Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g03(self)


@attr.s
class G75Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g75(self)


@attr.s
class LPCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_lp(self)


@attr.s
class LMCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_lm(self)


@attr.s
class LRCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_lr(self)


@attr.s
class LSCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ls(self)


@attr.s
class G36Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g36(self)


@attr.s
class G37Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g37(self)


@attr.s
class ABCommand(Command):
    n: int = attr.ib()
    block: list[Command] = attr.ib()

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ab(self)


class TFType(Enum):
    PART = auto()
    FILE_FUNCTION = auto()
    FILE_POLARITY = auto()
    SAME_COORDINATES = auto()
    CREATION_DATE = auto()
    GENERATION_SOFTWARE = auto()
    PROJECT_ID = auto()
    MD5 = auto()


@attr.s
class TFCommand(Command):
    tf_type: TFType = attr.ib(attr.validators.instance_of(TFType))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_tf(self)


@attr.s
class TACommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ta(self)


@attr.s
class TOCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_to(self)


@attr.s
class TDCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_td(self)


@attr.s
class M02Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_m02(self)

@attr.s
class G74Command(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_g74(self)
