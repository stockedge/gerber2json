from typing import Any

from parsita import *
from parsita.util import constant

from raw_command import G36Command, G37Command, D02Command, M02Command, G01Command, G02Command, G03Command, G75Command, \
    DnnCommand, G04Command, AMVar, AMFloat, AMAdd, AMSub, AMMul, AMDiv, AMExpr, TFCommand, TFType, D01Command, \
    ABCommand, SRCommand, G74Command


def make_d02command(arg: list[list[str]]) -> D02Command:
    return D02Command(
        None if len(arg[0]) <= 0 else arg[0][0],
        None if len(arg[1]) <= 0 else arg[1][0])


def make_addsub_term(args: list[Any]) -> AMExpr:
    l = args[0]
    for i in range(len(args[1])):
        l = (AMAdd(l, args[1][i][1]) if args[1][i][0] == '+' else AMSub(l, args[1][i][1]))
    return l


def make_muldiv_factor(args: list[Any]) -> AMExpr:
    l = args[0]
    for i in range(len(args[1])):
        l = (AMMul(l, args[1][i][1]) if args[1][i][0] == 'x' else AMDiv(l, args[1][i][1]))
    return l


class Rs274xParsers(TextParsers):
    aperture_ident = reg(r'D[0-9]{2,}') > (lambda arg: int(arg[1:]))
    name = reg(r'[._a-zA-Z$][._a-zA-Z0-9]*')
    user_name = reg(r'[_a-zA-Z$][._a-zA-Z0-9]*')  # Cannot start with a dot
    string = reg(r'[^%*]*')  # All characters except * %
    field = reg(r'[^%*,]*')  # All characters except * % ,

    addsub_operator = reg(r'[+-]')
    muldiv_operator = reg(r'[x/]')
    unsigned_integer = reg(r'[0-9]+') > int
    positive_integer = reg(r'[0-9]*[1-9][0-9]*') > int
    integer = reg(r'[+-]?[0-9]+')
    unsigned_decimal = reg(r'((([0-9]+)(\.[0-9]*)?)|(\.[0-9]+))') > float
    decimal = reg(r'[+-]?((([0-9]+)(\.[0-9]*)?)|(\.[0-9]+))') > float
    term = fwd()
    expression = fwd()
    term_with_op = term & rep1(addsub_operator & term) > make_addsub_term
    expression.define(term_with_op |
                      term)
    macro_variable = lit('$') >> positive_integer > AMVar
    factor = lit('(') >> expression << lit(')') | \
             macro_variable | \
             (unsigned_decimal > AMFloat)
    factor_with_op = factor & rep1(muldiv_operator & factor) > make_muldiv_factor
    term.define(factor_with_op |
                factor)

    nxt_field = lit(',') >> field
    TF_atts = (lit('.Part') >> nxt_field > (lambda args: TFCommand(TFType.PART))) | \
              (lit('.FileFunction') >> rep(nxt_field) > (lambda args: TFCommand(TFType.FILE_FUNCTION))) | \
              lit('.FilePolarity') >> nxt_field | \
              lit('.SameCoordinates') >> opt(nxt_field) | \
              lit('.CreationDate') >> nxt_field | \
              lit('.GenerationSoftware') >> nxt_field & nxt_field & opt(nxt_field) | \
              lit('.ProjectId') >> nxt_field & nxt_field & nxt_field | \
              lit('.MD5') >> nxt_field | \
              user_name
    TF = lit('%TF') >> TF_atts << lit('*%')
    TA_atts = lit('.AperFunction') >> rep(nxt_field) | \
              lit('.DrillTolerance') >> nxt_field & nxt_field | \
              lit('.FlashText') >> rep(nxt_field) | \
              user_name & rep(nxt_field)
    TA = lit('%TA') >> TA_atts << lit('*%')
    TO_atts = lit('.N') >> nxt_field & rep(nxt_field) | \
              lit('.P') >> nxt_field & nxt_field & opt(nxt_field) | \
              lit('.C') >> nxt_field | \
              lit('.CRot') >> nxt_field | \
              lit('.CMfr') >> nxt_field | \
              lit('.CMPN') >> nxt_field | \
              lit('.CVal') >> nxt_field | \
              lit('.CMnt') >> nxt_field | \
              lit('.CFtp') >> nxt_field | \
              lit('.CPgN') >> nxt_field | \
              lit('.CPgD') >> nxt_field | \
              lit('.CHgt') >> nxt_field | \
              lit('.CLbN') >> nxt_field | \
              lit('.CLbD') >> nxt_field | \
              lit('.CSup') >> nxt_field & nxt_field & rep(nxt_field & nxt_field) | \
              user_name & rep(nxt_field)
    TO = lit('%TO') >> TO_atts << lit('*%')
    all_atts = TF_atts | TA_atts | TO_atts
    TD = lit('%TD') >> opt(all_atts) << lit('*%')

    G36 = lit('G36*') > constant(G36Command())
    G37 = lit('G37*') > constant(G37Command())
    coordinate_data1 = \
        (lit('X') >> integer) & \
        (opt(lit('Y') >> integer) > (lambda y: y[0] if len(y) > 0 else None)) & \
        (opt(lit('I') >> integer << lit('J') >> integer) > (lambda ij: ij[0] if len(ij) > 0 else [None, None]))
    coordinate_data2 = \
        (opt(lit('X') >> integer) > (lambda x: x[0] if len(x) > 0 else None)) & \
        (lit('Y') >> integer) & \
        (opt(lit('I') >> integer << lit('J') >> integer) > (lambda ij: ij[0] if len(ij) > 0 else [None, None]))
    coordinate_data = coordinate_data1 | coordinate_data2
    D01 = (coordinate_data << opt(lit('D01')) << lit('*')) > (lambda args: D01Command(args[0], args[1], args[2][0], args[2][1]))
    D02 = (coordinate_data << opt(lit('D02')) << lit('*')) > (lambda args: D02Command(args[0], args[1]))
    interpolation_state_command = fwd()
    contour = D02 & rep(D01 | interpolation_state_command) > (lambda args: [args[0]] + args[1:])
    region_statement = (G36 & rep1(contour) & G37) > (lambda args: [args[0]] + args[1] + [args[2]])
    AB_open = (lit('%AB') >> aperture_ident << lit('*%'))
    AB_close = lit('%AB*%')
    in_block_statement = fwd()
    AB_statement = (AB_open & rep(in_block_statement) << AB_close) > (lambda args: ABCommand(args[0], args[1]))
    SR_close = lit('%SR*%')
    SR_open = (lit('%SRX') >> positive_integer << lit('Y') >> positive_integer << lit('I') >> decimal << lit(
        'J') >> decimal << lit('*%')) > (lambda args: (args[0], args[1], args[2], args[3]))
    single_statement = fwd()
    in_block_statement.define(single_statement | region_statement | AB_statement)
    SR_statement = (SR_open & rep(in_block_statement) << SR_close) > (lambda args: SRCommand(args[0], args[1]))

    macro_name = name << lit('*')
    par = lit(',') >> expression
    primitive = lit('0') >> string << lit('*') | \
                lit('1') >> par & par & par & par & opt(par) << lit('*') | \
                lit('20') >> par & par & par & par & par & par & par << lit('*') | \
                lit('21') >> par & par & par & par & par & par << lit('*') | \
                lit('4') >> par & par & par & par & rep1(par & par) & par << lit('*') | \
                lit('5') >> par & par & par & par & par & par << lit('*') | \
                lit('7') >> par & par & par & par & par & par << lit('*')
    variable_definition = macro_variable << lit('=') >> expression << lit('*')
    in_macro_block = primitive | variable_definition
    macro_body = rep1(in_macro_block)
    AM = lit('%AM') >> macro_name & macro_body << lit('%')

    nxt_par = lit('X') >> decimal
    fst_par = lit(',') >> decimal
    template_call = (
            lit('C') >> fst_par & opt(nxt_par) |
            lit('R') >> fst_par & nxt_par & opt(nxt_par) |
            lit('O') >> fst_par & nxt_par & opt(nxt_par) |
            lit('P') >> fst_par & nxt_par & opt(nxt_par & opt(nxt_par)) |
            name & opt(fst_par & rep(nxt_par)))
    AD = lit('%AD') >> aperture_ident & template_call << lit('*%')
    LP = lit('%LP') >> (lit('C', 'D')) << lit('*%')
    LM = lit('%LM') >> (lit('N', 'XY', 'Y', 'X')) << lit('*%')
    LR = lit('%LR') >> decimal << lit('*%')
    LS = lit('%LS') >> decimal << lit('*%')
    Dnn = aperture_ident << lit('*') > DnnCommand
    G04 = lit('G04') >> string << lit('*') > G04Command
    M02 = lit('M02*') > constant(M02Command())
    G01 = lit('G01*') > constant(G01Command())
    G02 = lit('G02*') > constant(G02Command())
    G03 = lit('G03*') > constant(G03Command())
    GnnD01 = (lit('G') >> lit('01', '02', '03') &
              coordinate_data &
              opt(lit('D01*', 'D02*'))) > (lambda args: args)
    G75 = lit('G75*') > constant(G75Command())
    D03 = coordinate_data & opt(lit('D03')) << lit('*')
    coordinate_digits = reg(r'[1-6][56]')
    FS = (lit('%FS') >>
          lit('L', 'T') & lit('A', 'I') &
          lit('X') & coordinate_digits & lit('Y') & coordinate_digits << lit('*%'))
    MO = lit('%MO') >> lit('MM', 'IN') << lit('*%')

    AS = lit('%AS') >> lit('AXBY', 'AYBX') << lit('*%')
    IN = lit('%IN') >> name << lit('*%')
    IP = lit('%IP') >> lit('POS', 'NEG') << lit('*%')
    IR = lit('%IR') >> lit('0', '90', '180', '270') << lit('*%')
    LN = lit('%LN') >> name << lit('*%')
    MI = lit('%MI') >> opt('A' >> lit('0', '1')) & opt('B' >> lit('0', '1')) << lit('*%')
    OF = lit('%OF') >> opt(lit('A') >> decimal) & opt(lit('B') >> decimal) << lit('*%')
    SF = lit('%SF') >> opt(lit('A') >> decimal) & opt(lit('B') >> decimal) << lit('*%')
    G74 = lit('G74*') > constant(G74Command())

    attribute_command = TO | \
                        TD | \
                        TA | \
                        TF
    transformation_state_command = LP | \
                                   LM | \
                                   LR | \
                                   LS
    interpolation_state_command.define(GnnD01 |
                                       G01 |
                                       G02 |
                                       G03 |
                                       G75)
    operation = D01 | \
                D02 | \
                D03
    coordinate_command = FS | \
                         MO
    single_statement.define(operation |
                            interpolation_state_command |
                            Dnn |
                            G04 |
                            attribute_command |
                            AD |
                            AM |
                            coordinate_command |
                            transformation_state_command |
                            AS |
                            IN |
                            IP |
                            IR |
                            LN |
                            MI |
                            OF |
                            SF |
                            G74 |
                            M02)
    compound_statement = region_statement | \
                         SR_statement | \
                         AB_statement
    statement = single_statement | compound_statement
    statements = rep1(statement)


