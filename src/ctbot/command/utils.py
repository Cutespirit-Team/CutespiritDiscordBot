import inspect
import importlib
import logging
import typing
import discord
import json
import sys
from ..ctbot import config
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice, create_option
from os.path import dirname, basename
from pathlib import Path

logger = logging.getLogger('ctbot')

def regist_slash_command(bot):
    modules = [p.name for p in Path(f'{dirname(__file__)}/slash/').glob('*.py') if p.is_file() and not p.name.endswith('__init__.py')]
    for m in modules:
        module = inspect.getmodulename(m)
        slash = importlib.import_module(f'.{module}', 'ctbot.command.slash')
        klasses = inspect.getmembers(slash, lambda x: inspect.isclass(x))
        for name, kless in klasses:
            #print(module , name.lower())
            if name.startswith('Slash') and module == name.lower()[5:]:
                logger.info(f'Registing Module {name}')
                bot.add_cog(kless(bot))

def reload_module(bot):
	modules = [p.name for p in Path(f'{dirname(__file__)}/slash/').glob('*.py') if p.is_file() and not p.name.endswith('__init__.py')]
	for m in modules:
		module_name = 'ctbot.command.slash.' + inspect.getmodulename(m)
		module = sys.modules[module_name]
		importlib.reload(module)
		klasses = inspect.getmembers(module, lambda x: inspect.isclass(x))
		for name, kless in klasses:
			#print(module , name.lower())
			if name.startswith('Slash') and inspect.getmodulename(m) == name.lower()[5:]:
				logger.info(f'Re-Registing Module {name}')
				bot.remove_cog(name)
				bot.add_cog(kless(bot))
	logger.info(f'All Modules has reloaded!')
			# print('reload ok' + inspect.getmodulename(m), name, kless)

def cog_slash_managed(*args, **kwargs):
	'''
	base=None,
	subcommand_group=None,
	name=None,
	description: str = None,
	base_description: str = None,
	base_desc: str = None,
	base_default_permission: bool = True,
	base_permissions: typing.Dict[int, list] = None,
	subcommand_group_description: str = None,
	sub_group_desc: str = None,
	guild_ids: typing.List[int] = None,
	options: typing.List[dict] = None,
	connector: dict = None,
	'''
	def wrapper(cmd):
		klass, method = cmd.__qualname__.split('.')
		guild_ids = []
		try:
			guild_configs = open('config/guild.json', mode='r', encoding='utf-8')
			guild_configs = json.load(guild_configs)
			if guild_configs['specific_guild'] == 'yes':
				guild_ids = set(config.get_slash_command_guilds_id(klass[5:], method))
				logger.debug(f'wrap slash {klass[5:]}.{method} for {set(guild_ids)}')
				kwargs.setdefault('guild_ids', guild_ids)

		except FileNotFoundError:
			filename = 'config/guild.json'
			content = {
				'specific_guild' : 'yes'
				}
			f = open(filename, 'w')
			json.dump(content, f, indent=4)
			f.close()

		if 'base' in kwargs.keys():
			obj = cog_ext.cog_subcommand(**kwargs)(cmd)
		else:
			obj = cog_ext.cog_slash(**kwargs)(cmd)

		return obj
	return wrapper

def gen_list_of_option_choices(options: typing.List[str]):
    choices = []
    for opt in options:
        choices.append(create_choice(f'--{opt}', opt))
    return choices

def gen_list_of_choices(options: typing.List[str]):
    choices = []
    for opt in options:
        choices.append(create_choice(opt, opt))
    return choices