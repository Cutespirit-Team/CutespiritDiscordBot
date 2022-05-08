import os
import configparser
import typing

'''
config sample
[bot]
token = MTa4MjS3ASI ....
owner = 196207520585351180

[command]
enable_slash = true
general_prefix = !

[slash]
all = <guild_id>
<class without 'Slash' prefix>.<method> = <guild_id>
example.ping = 866199579014987816

# 個別 guilds 設定
[guild_866199579014987816]

# 只響應指定頻道的訊息以逗號分隔, 如果為空響應所有頻道
responsible_channels = 866213047016882206,866977922929917972

'''

def to_ints(ids: typing.List[str]) -> typing.List[int]:
    return set(map(int, filter(str.isdigit, ids)))

def parse_bool(s: str):
    return s.lower() in ['on', '1', 'true']

class BotConfig:
    config_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, filename: str='config.ini'):
        self.filename = filename
        self.path = os.path.realpath(os.path.join(BotConfig.config_dir, filename))
        self.guilds = {}
        self.load()

    def save(self):
        with open(self.path, 'w') as configfile:
            self._config.write(configfile)

    def load(self):
        parser = configparser.ConfigParser()
        if os.path.exists(self.path):
            parser.read([self.path])
        else:
            BotConfig.create_default(parser, save_to=self.path)
        self._config = parser
        self._parse_guilds_section()
    
    def _parse_guilds_section(self):
        
        type_mapping = {
            'responsible_channels': {'type': list},
            '__default__': {'type': str}
        }

        sections = filter(lambda section: section.startswith('guild_'), self._config.sections())
        guilds = {}
        for section in sections:
            guild_id = section.split('_')[1]
            guilds.setdefault(guild_id, {})
            for key, value in self._config.items(section):
                t = type_mapping.get(key, type_mapping.get('__default__'))
                if t.get('type') == list:
                    value = to_ints(value.split(','))
                guilds[guild_id].setdefault(key, value)
        self.guilds = guilds
    
    @classmethod
    def create_default(cls, parser: configparser.ConfigParser, save_to=None):
        parser.read_dict({
            'bot': {
                'token': '',
                'owner': '',
            },
            'command': {
                'enable_slash': 'false',
                # 'enable_general': 'true',
                'general_prefix': '!',
            },
            'slash': {
                'all': ''
            }
        })

        if save_to:
            with open(save_to, 'w') as f:
                parser.write(f)

    def get_token(self):
        return self._config.get('bot', 'token', fallback='')

    def get_owner(self):
        return self._config.get('bot', 'owner', fallback='')

    def get_enable_slash(self):
        return parse_bool(self._config.get('command', 'enable_slash', fallback='false'))

    def get_enable_general(self):
        return parse_bool(self._config.get('command', 'enable_general', fallback='false'))

    def get_general_prefix(self):
        return self._config.get('command', 'general_prefix', fallback='!')
     
    def get_responsible_channels(self, guild: int) -> typing.List[int]:
        guild = self.guilds.get(str(guild), {})
        channel_ids = guild.get('responsible_channels', set())
        return channel_ids

    def get_slash_command_guilds_id(self, module: str, method: str) -> typing.List[int]:
        all_guilds_id = self._config.get('slash', 'all', fallback='').split(',')
        method_guilds_id = self._config.get('slash', f'{module}.{method}', fallback='').split(',')
        return to_ints(all_guilds_id + method_guilds_id)

def _generate_getter_function(section: str, option: str, _type: type):
    def getter_wrapper(self):
        value = self._config.get(section, option, fallback='')
        if _type == list:
            value = value.split(',')
        return value

    def getter_guild_wrapper(self, guild_id: str):
        value = self._config.get(guild_id, option, fallback='')
        if _type == list:
            value = value.split(',')
        return value

    return getter_guild_wrapper if section == 'guild' else getter_wrapper
    
'''
    {'name': 'responsible_channels', 'section': 'guild'}
    setattr(CTConfig, ...)
'''

# config = CTBotConfig('config.ini')
# print(config.get_slash_command_guilds_id('activity', 'change'))
