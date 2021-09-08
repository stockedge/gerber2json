import unittest

from raw_command import D02Command
from rs274x_parser import Rs274xParsers


class TestRs274xParsers(unittest.TestCase):

    def test_aperture_ident(self) -> None:
        Rs274xParsers.aperture_ident.parse('D01').or_die()
        Rs274xParsers.aperture_ident.parse('D11').or_die()
        Rs274xParsers.aperture_ident.parse('D99').or_die()

    def test_name(self) -> None:
        Rs274xParsers.name.parse('hoge').or_die()
        Rs274xParsers.name.parse('FUGA').or_die()
        Rs274xParsers.name.parse('Foo123').or_die()

    def test_user_name(self) -> None:
        Rs274xParsers.user_name.parse('isseimori').or_die()

    def test_string(self) -> None:
        Rs274xParsers.string.parse('qwertyuiopasdfghjkl').or_die()

    def test_field(self) -> None:
        Rs274xParsers.field.parse('qwertyuiopasdfghjkl').or_die()

    def test_addsub_operator(self) -> None:
        Rs274xParsers.addsub_operator.parse('+').or_die()
        Rs274xParsers.addsub_operator.parse('-').or_die()

    def test_muldiv_operator(self) -> None:
        Rs274xParsers.muldiv_operator.parse('x').or_die()
        Rs274xParsers.muldiv_operator.parse('/').or_die()

    def test_unsigned_integer(self) -> None:
        Rs274xParsers.unsigned_integer.parse('012').or_die()

    def test_positive_integer(self) -> None:
        Rs274xParsers.positive_integer.parse('1').or_die()

    def test_integer(self) -> None:
        Rs274xParsers.integer.parse('0').or_die()
        Rs274xParsers.integer.parse('+1').or_die()
        Rs274xParsers.integer.parse('-1').or_die()

    def test_unsigned_decimal(self) -> None:
        pass

    def test_decimal(self) -> None:
        pass

    def test_expression(self) -> None:
        Rs274xParsers.expression.parse('1+1').or_die()

    def test_macro_variable(self) -> None:
        pass

    def test_factor(self) -> None:
        pass

    def test_term(self) -> None:
        pass

    def test_nxt_field(self) -> None:
        pass

    def test_TF_atts(self) -> None:
        pass

    def test_TF(self) -> None:
        Rs274xParsers.TF.parse('%TF.FilePolarity,Negative*%').or_die()
        Rs274xParsers.TF.parse('%TF.Part,Array*%').or_die()
        Rs274xParsers.TF.parse('%TF.FileFunction,Copper,L1,Top*%').or_die()
        Rs274xParsers.TF.parse('%TF.MD5,6ab9e892830469cdff7e3e346331d404*%').or_die()

    def test_TA_atts(self) -> None:
        pass

    def test_TA(self) -> None:
        Rs274xParsers.TA.parse('%TA.AperFunction,ComponentPad*%').or_die()
        Rs274xParsers.TA.parse('%TAMyApertureAttributeWithValue,value*%').or_die()
        Rs274xParsers.TA.parse('%TAMyApertureAttributeWithoutValue*%').or_die()

    def test_TO_atts(self) -> None:
        pass

    def test_TO(self) -> None:
        Rs274xParsers.TO.parse('%TO.C,R6*%').or_die()

    def test_all_atts(self) -> None:
        pass

    def test_TD(self) -> None:
        pass

    def test_G36(self) -> None:
        Rs274xParsers.G36.parse('G36*').or_die()

    def test_G37(self) -> None:
        Rs274xParsers.G37.parse('G37*').or_die()

    def test_D01(self) -> None:
        Rs274xParsers.D01.parse('X250000Y155000D01*').or_die()
        Rs274xParsers.D01.parse('X200Y200I50J50D01*').or_die()

    def test_D02(self) -> None:
        assert Rs274xParsers.D02.parse('X2152000Y1215000D02*').or_die() == D02Command(2152000, 1215000)

    def test_contour(self) -> None:
        Rs274xParsers.contour.parse('''X200Y300000D02*
                                        G01*
                                        X700000D01*
                                        Y100000D01*
                                        X1100000Y500000D01*
                                        X700000Y900000D01*
                                        Y700000D01*
                                        X200000D01*
                                        Y300000D01*''').or_die()

    def test_region_statement(self) -> None:
        pass

    def test_AB_open(self) -> None:
        Rs274xParsers.AB_open.parse('%ABD12*%').or_die()

    def test_AB_close(self) -> None:
        Rs274xParsers.AB_close.parse('%AB*%').or_die()

    def test_AB_statement(self) -> None:
        pass

    def test_SR_close(self) -> None:
        Rs274xParsers.SR_close.parse('%SR*%').or_die()

    def test_SR_open(self) -> None:
        Rs274xParsers.SR_open.parse('%SRX3Y2I5.0J4.0*%').or_die()

    def test_in_block_statement(self) -> None:
        pass

    def test_SR_statement(self) -> None:
        pass

    def test_macro_name(self) -> None:
        pass

    def test_par(self) -> None:
        pass

    def test_primitive(self) -> None:
        pass

    def test_variable_definition(self) -> None:
        pass

    def test_in_macro_block(self) -> None:
        pass

    def test_macro_body(self) -> None:
        pass

    def test_AM(self) -> None:
        Rs274xParsers.AM.parse('%AMTriangle_30*4,1,3,1,-1,1,1,2,1,1,-1,30*%')
        Rs274xParsers.AM.parse('''%AMBox*
                                    0 Rectangle with rounded corners, with rotation*
                                    0 The origin of the aperture is its center*
                                    0 $1 X-size*
                                    0 $2 Y-size*
                                    0 $3 Rounding radius*
                                    0 $4 Rotation angle, in degrees counterclockwise*
                                    0 Add two overlapping rectangle primitives as box body*
                                    21,1,$1,$2-$3-$3,0,0,$4*
                                    21,1,$2-$3-$3,$2,0,0,$4*
                                    0 Add four circle primitives for the rounded corners*
                                    $5=$1/2*
                                    $6=$2/2*
                                    $7=2X$3*
                                    1,1,$7,$5-$3,$6-$3,$4*
                                    1,1,$7,-$5+$3,$6-$3,$4*
                                    1,1,$7,-$5+$3,-$6+$3,$4*
                                    1,1,$7,$5-$3,-$6+$3,$4*%''')
        Rs274xParsers.AM.parse('%AMCircle*1,1,1.5,0,0,0*%')
        Rs274xParsers.AM.parse('%AMLine*20,1,0.9,0,0.45,12,0.45,0*%')
        Rs274xParsers.AM.parse('%AMRECTANGLE*21,1,6.8,1.2,3.4,0.6,30*%')
        Rs274xParsers.AM.parse('%AMPolygon*5,1,8,0,0,8,0*%')
        Rs274xParsers.AM.parse('%AMRect*21,1,$1,$2-2*$3,-$4,-$5+$2,0*%')
        Rs274xParsers.AM.parse('%AMTEST1*1,1,$1,$2,$3*$4=$1x0.75*$5=($2+100)x1.75*1,0,$4,$5,$3*%')
        Rs274xParsers.AM.parse('%AMTEST2*$4=$1x0.75*$5=100+$3*1,1,$1,$2,$3*1,0,$4,$2,$5*$6=$4x0.5*1,0,$6,$2,$5*%')

    def test_nxt_par(self) -> None:
        pass

    def test_fst_par(self) -> None:
        pass

    def test_template_call(self) -> None:
        pass

    def test_AD(self) -> None:
        Rs274xParsers.AD.parse('%ADD10C,.025*%').or_die()
        Rs274xParsers.AD.parse('%ADD10C,0.5X0.25*%').or_die()
        Rs274xParsers.AD.parse('%ADD22R,0.044X0.025*%').or_die()
        Rs274xParsers.AD.parse('%ADD22R,.050X.050X.027*%').or_die()
        Rs274xParsers.AD.parse('%ADD57O,.030X.040X.015*%').or_die()
        Rs274xParsers.AD.parse('%ADD22O,0.046X0.026X0.019*%').or_die()
        Rs274xParsers.AD.parse('%ADD30P,.016X6*%').or_die()
        Rs274xParsers.AD.parse('%ADD17P,.040X6X0.0X0.019*%').or_die()
        Rs274xParsers.AD.parse('%ADD15CIRC*%').or_die()

    def test_LP(self) -> None:
        Rs274xParsers.LP.parse('%LPD*%').or_die()
        Rs274xParsers.LP.parse('%LPC*%').or_die()

    def test_LM(self) -> None:
        Rs274xParsers.LM.parse('%LMX*%').or_die()
        Rs274xParsers.LM.parse('%LMN*%').or_die()

    def test_LR(self) -> None:
        Rs274xParsers.LR.parse('%LR90.0*%').or_die()
        Rs274xParsers.LR.parse('%LR0.0*%').or_die()
        Rs274xParsers.LR.parse('%LR-90*%').or_die()

    def test_LS(self) -> None:
        Rs274xParsers.LS.parse('%LS1.5*%').or_die()

    def test_Dnn(self) -> None:
        Rs274xParsers.Dnn.parse('D10*')

    def test_G04(self) -> None:
        Rs274xParsers.G04.parse('G04 This is a comment*').or_die()
        Rs274xParsers.G04.parse('G04 The space characters as well as ‘,’ and ‘;’ are allowed here.*').or_die()

    def test_M02(self) -> None:
        Rs274xParsers.M02.parse('M02*').or_die()

    def test_G01(self) -> None:
        Rs274xParsers.G01.parse('G01*').or_die()

    def test_G02(self) -> None:
        Rs274xParsers.G02.parse('G02*').or_die()

    def test_G03(self) -> None:
        Rs274xParsers.G03.parse('G03*').or_die()

    def test_G75(self) -> None:
        Rs274xParsers.G75.parse('G75*').or_die()

    def test_D03(self) -> None:
        Rs274xParsers.D03.parse('X1215000Y2152000D03*').or_die()

    def test_coordinate_digits(self) -> None:
        pass

    def test_FS(self) -> None:
        Rs274xParsers.FS.parse('%FSLAX36Y36*%').or_die()

    def test_MO(self) -> None:
        Rs274xParsers.MO.parse('%MOMM*%').or_die()
        Rs274xParsers.MO.parse('%MOIN*%').or_die()

    def test_attribute_command(self) -> None:
        pass

    def test_transformation_state_command(self) -> None:
        pass

    def test_interpolation_state_command(self) -> None:
        pass

    def test_operation(self) -> None:
        pass

    def test_coordinate_command(self) -> None:
        pass

    def test_single_statement(self) -> None:
        pass

    def test_compound_statement(self) -> None:
        pass

    def test_statement(self) -> None:
        pass
