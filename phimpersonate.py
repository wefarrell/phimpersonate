from faker import Faker
from datetime import date

fake = Faker()
fake.first_name()


def parse_config_args(config_arg):
    return dict([parse_config_item(arg) for arg in config_arg.split(',')])


def parse_config_item(arg_str):
    [cols, faker_field] = arg_str.split(':')
    [start, end] = [int(col) for col in  cols.split('-')]
    return ((start, end), faker_field)


def replace_field(input, config, filler = ' '):
    [(_start, end)] = config
    if _start > end:
        raise ValueError
    [faker_type] = config.values()
    start = _start - 1
    length = end-start
    original = input[start:end]
    fake_value = generate_fake_value(faker_type, original)
    padding = filler * (length - len(fake_value))
    return input[:start] + fake_value[0:length] + padding + input[end:]


def generate_fake_value(faker_type, original):
    is_uppercase = original == original.upper()
    Faker.seed(original.lower())
    kwargs = {}
    if faker_type == 'date':
        kwargs = {
            'pattern': '%Y%m%d',
            'end_datetime': date(2000, 1, 1)
        }
    fake_value = getattr(fake, faker_type)(**kwargs)
    return fake_value.upper() if is_uppercase else fake_value


def replace_fields(line, configs):
    for (pos, field) in configs.items():
        line = replace_field(line, {pos: field})
    return line


def replace_fwf(file_path, config_args):
    configs = parse_config_args(config_args)
    file = open(file_path, 'r').readlines()
    last_line = file[-1]
    for index, line in enumerate(file):
        if index != 0 and line != last_line:
            line = replace_fields(line, configs)
        yield line.rstrip('\r\n')

