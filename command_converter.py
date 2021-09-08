from primitive_shape import Shape
from raw_command import *

T = TypeVar('T')


class CommandVisitor:
    @abstractmethod
    def visit_g04(self, command: 'G04Command') -> T: pass

    @abstractmethod
    def visit_mo(self, command: 'MOCommand') -> T: pass

    @abstractmethod
    def visit_fs(self, command: 'FSCommand') -> T: pass

    @abstractmethod
    def visit_ad(self, command: 'ADCommand') -> T: pass

    @abstractmethod
    def visit_am(self, command: 'AMCommand') -> T: pass

    @abstractmethod
    def visit_dnn(self, command: 'DnnCommand') -> T: pass

    @abstractmethod
    def visit_d01(self, command: 'D01Command') -> T: pass

    @abstractmethod
    def visit_d02(self, command: 'D02Command') -> T: pass

    @abstractmethod
    def visit_d03(self, command: 'D03Command') -> T: pass

    @abstractmethod
    def visit_g01(self, command: 'G01Command') -> T: pass

    @abstractmethod
    def visit_g02(self, command: 'G02Command') -> T: pass

    @abstractmethod
    def visit_g03(self, command: 'G03Command') -> T: pass

    @abstractmethod
    def visit_g75(self, command: 'G75Command') -> T: pass

    @abstractmethod
    def visit_lp(self, command: 'LPCommand') -> T: pass

    @abstractmethod
    def visit_lm(self, command: 'LMCommand') -> T: pass

    @abstractmethod
    def visit_lr(self, command: 'LRCommand') -> T: pass

    @abstractmethod
    def visit_ls(self, command: 'LSCommand') -> T: pass

    @abstractmethod
    def visit_g36(self, command: 'G36Command') -> T: pass

    @abstractmethod
    def visit_g37(self, command: 'G37Command') -> T: pass

    @abstractmethod
    def visit_ab(self, command: 'ABCommand') -> T: pass

    @abstractmethod
    def visit_sr(self, command: 'SRCommand') -> T: pass

    @abstractmethod
    def visit_tf(self, command: 'TFCommand') -> T: pass

    @abstractmethod
    def visit_ta(self, command: 'TACommand') -> T: pass

    @abstractmethod
    def visit_to(self, command: 'TOCommand') -> T: pass

    @abstractmethod
    def visit_td(self, command: 'TDCommand') -> T: pass

    @abstractmethod
    def visit_m02(self, command: 'M02Command') -> T: pass

    @abstractmethod
    def visit_g74(self, command: 'G74Command') -> T:
        pass


@attr.s
class CommandConverter(CommandVisitor):
    metric: 'Metric' = attr.ib()
    aperture_dictionary: dict[int, 'ADCommand'] = attr.ib(validator=attr.validators.instance_of(dict[int, 'ADCommand']))
    aperture_macro_definition: dict[str, 'AMCommand'] = attr.ib(
        validator=attr.validators.instance_of(dict[int, 'AMCommand']))

    def visit_g04(self, command: 'G04Command') -> Shape:
        pass

    def visit_mo(self, command: 'MOCommand') -> Shape:
        pass

    def visit_fs(self, command: 'FSCommand') -> Shape:
        pass

    def visit_ad(self, command: 'ADCommand') -> Shape:
        pass

    def visit_am(self, command: 'AMCommand') -> Shape:
        pass

    def visit_dnn(self, command: 'DnnCommand') -> Shape:
        pass

    def visit_d01(self, command: 'D01Command') -> Shape:
        pass

    def visit_d02(self, command: 'D02Command') -> Shape:
        pass

    def visit_d03(self, command: 'D03Command') -> Shape:
        pass

    def visit_g01(self, command: 'G01Command') -> Shape:
        pass

    def visit_g02(self, command: 'G02Command') -> Shape:
        pass

    def visit_g03(self, command: 'G03Command') -> Shape:
        pass

    def visit_g75(self, command: 'G75Command') -> Shape:
        pass

    def visit_lp(self, command: 'LPCommand') -> Shape:
        pass

    def visit_lm(self, command: 'LMCommand') -> Shape:
        pass

    def visit_lr(self, command: 'LRCommand') -> Shape:
        pass

    def visit_ls(self, command: 'LSCommand') -> Shape:
        pass

    def visit_g36(self, command: 'G36Command') -> Shape:
        pass

    def visit_g37(self, command: 'G37Command') -> Shape:
        pass

    def visit_ab(self, command: 'ABCommand') -> Shape:
        pass

    def visit_sr(self, command: 'SRCommand') -> Shape:
        pass

    def visit_tf(self, command: 'TFCommand') -> Shape:
        pass

    def visit_ta(self, command: 'TACommand') -> Shape:
        pass

    def visit_to(self, command: 'TOCommand') -> Shape:
        pass

    def visit_td(self, command: 'TDCommand') -> Shape:
        pass

    def visit_m02(self, command: 'M02Command') -> Shape:
        pass

    def visit_g74(self, command: 'G74Command') -> T:
        pass
