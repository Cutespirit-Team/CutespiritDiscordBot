import discord
import typing
from discord.ext import commands
from ..utils import cog_slash_managed
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from asyncio import subprocess, wait_for, ensure_future
from shlex import quote

async def run_command(args: typing.Tuple[str]):
    p = await subprocess.create_subprocess_exec(*args,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await wait_for(ensure_future(p.communicate()), timeout=15)
    return (p.returncode, stdout, stderr)

# core、community、extra、archlinuxcn、blackarch
class SlashPacman(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(base='pacman', description='查尋 Arch 套件資訊',
        options=[create_option('package', '套件名稱',
            option_type=SlashCommandOptionType.STRING,
            required=True)])
    async def pkg_info(self, ctx, package: str):
        await ctx.defer()
        # await ctx.send('正在尋找該套件之資訊...請稍後...')
        args = ('pacman', '-Si', quote(package))
        
        try:
            _, stdout, _ = await run_command(args)
            await ctx.send(stdout.decode())
        except TimeoutError as e:
            await ctx.send('timeout whene fetch information.')
        except Exception as e:
            await ctx.send('not applicable on this platform')

    @cog_slash_managed(base='pacman', description='查尋 Arch 指令所屬套件',
        options=[create_option('package', '套件名稱',
            option_type=SlashCommandOptionType.STRING,
            required=True)])
    async def pkg_files(self, ctx, package: str):
        await ctx.defer()
        # await ctx.send('正在尋找該指令所屬的套件...請稍後...')
        args = ('pacman', '-F', quote(package))

        try:
            _, stdout, _ = await run_command(args)
            await ctx.send(stdout.decode())
        except TimeoutError as e:
            await ctx.send('timeout whene fetching information.')
        except Exception as e:
            await ctx.send('not applicable on this platform')
