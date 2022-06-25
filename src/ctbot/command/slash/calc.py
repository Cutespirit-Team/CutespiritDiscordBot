import discord
import math
import ast
import operator
from discord.ext import commands
from ..utils import cog_slash_managed, gen_list_of_choices
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

# TODO: Fix slash command error
# TODO: Fix expr has x y z error

class exprCalc(ast.NodeVisitor):

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return _OP_MAP[type(node.op)](left, right)

    def visit_Num(self, node):
        return node.n

    def visit_Expr(self, node):
        return self.visit(node.value)

    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])

def expression(expr: str):
    return Calc.evaluate(expr)

def linearEqSo(a: str, b: str, c: str):
    a = float(a)
    b = float(b)
    c = float(c)
    expr = b**2 - 4*a*c
    if expr > 0:
        x1=((-b + math.sqrt(expr)) / (2*a))
        x2=((-b - math.sqrt(expr)) / (2*a))
        return '有兩根實數解/兩根 x1={}, x2={}'.format(x1, x2)
    elif expr < 0:
        return '無實數根之解/無根'
    else:
        return '重根'

def bmi(weigh: str, heigh: str):
    weigh = float(weigh)
    heigh = float(heigh)
    assert(heigh > 0)
    bmi = weigh / (heigh / 100)**2
    text = ''
    
    if bmi >= 35:
        text = '過重'
    elif bmi >= 30:
        text = '中度肥胖'
    elif bmi >= 27:
        text = '輕度肥胖'
    elif bmi >= 24:
        text = '過重'
    elif bmi >= 18.5:
        text = '正常範圍'
    else:
        text = '體重過輕'

    return (bmi, text)
        
func_dict = {
    'sqrt': {'argc': 1, 'func': math.sqrt},
    'pow': {'argc': 2, 'func': math.pow},
    'factorial': {'argc': 1, 'func': math.factorial},
    'fabs': {'argc': 1, 'func': math.fabs},
    'sin': {'argc': 1, 'func': math.sin},
    'cos': {'argc': 1, 'func': math.cos},
    'tan': {'argc': 1, 'func': math.tan},
    'degrees': {'argc': 1, 'func': math.degrees},
    'radians': {'argc': 1, 'func': math.radians},
    'bmi': {'argc': 2, 'func': bmi},
    'linearEqSo': {'argc': 3, 'func': linearEqSo},
    'add': {'argc': 2, 'func': lambda x, y: x + y},
    'sub': {'argc': 2, 'func': lambda x, y: x - y},
    'mult': {'argc': 2, 'func': lambda x, y: x * y},
    'div': {'argc': 2, 'func': lambda x, y: x / y},
    'expr': {'argc': 1, 'func': expression},
}

_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.floordiv,
    ast.Invert: operator.neg,
}

class SlashCalc(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='calc',
        options=[create_option('func', '函式',
        option_type=SlashCommandOptionType.STRING,
        required=True,
        choices=gen_list_of_choices(func_dict.keys())),
        create_option('x', 'x / 公斤',
        option_type=SlashCommandOptionType.STRING,
        required=False),
        create_option('y', 'y / 公分',
        option_type=SlashCommandOptionType.STRING,
        required=False),
        create_option('z', 'z',
        option_type=SlashCommandOptionType.STRING,
        required=False)])
    async def calc(self, ctx, func: str, x: float=None, y: float=None, z: float=None):
        # args = []
        # if func not in func_dict.keys():
        #     args = func.split(' ')
        #     if args[0] not in func_dict.keys():
        #         await ctx.send(f'{func} 函式不可用')
        #     else:
        #         args = args[1:]
        # else:
        #     args = [x, y, z]
        args = [x, y, z]
        argc = func_dict.get(func)['argc']
        func = func_dict.get(func)['func']
        for i in range(argc):
            if args[i] == None:
                await ctx.send(f'參數個數不正確 必要 {argc}, 傳入 {i}')
                return
        
        try:
            await ctx.send(str(func(*args[:argc])))
        except ZeroDivisionError as e:
            await ctx.send('參數無效')