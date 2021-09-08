from abc import abstractmethod
from typing import TypeVar, Optional

import attr

from command_converter import CommandVisitor

from enum import Enum, auto


class Metric(Enum):
    MILLE = auto()
    INCH = auto()


T = TypeVar('T')


@attr.s
class Command:
    @abstractmethod
    def accept(self, visitor: 'CommandVisitor') -> T: pass


@attr.s
class D01Command(Command):
    x: int = attr.ib(validator=attr.validators.instance_of(int))
    y: int = attr.ib(validator=attr.validators.instance_of(int))
    i: int = attr.ib(validator=attr.validators.instance_of(int))
    j: int = attr.ib(validator=attr.validators.instance_of(int))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d01(self)


@attr.s
class D02Command(Command):
    x: Optional[int] = attr.ib()
    y: Optional[int] = attr.ib()

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d02(self)


@attr.s
class D03Command(Command):
    x: int = attr.ib(validator=attr.validators.instance_of(int))
    y: int = attr.ib(validator=attr.validators.instance_of(int))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_d03(self)


@attr.s
class DnnCommand(Command):
    x: int = attr.ib(validator=attr.validators.instance_of(int))
    y: int = attr.ib(validator=attr.validators.instance_of(int))

    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_dnn(self)


@attr.s
class SRCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_sr(self)


@attr.s
class G04Command(Command):
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


@attr.s
class ADCommand(Command):
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ad(self)


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
    def accept(self, visitor: 'CommandVisitor') -> T:
        return visitor.visit_ab(self)


@attr.s
class TFCommand(Command):
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
