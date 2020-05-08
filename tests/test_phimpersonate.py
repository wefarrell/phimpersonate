from faker import Faker
from phimpersonate import parse_config_args, \
    parse_config_item, replace_field, replace_fwf
FWF_PATH = 'fixtures/sample_with_phi.txt'
from datetime import datetime, date

def fake_first_name(seed):
    Faker.seed(seed)
    faker = Faker()
    return faker.first_name() + ' ' * 100


def test_parse_config_args():
    config_str = '1-12:first_name,13-24:last_name'
    expected = {(1, 12): 'first_name', (13, 24): 'last_name'}
    assert parse_config_args(config_str) == expected


def test_parse_parse_config_item():
    str = '1-12:first_name'
    expected = ((1, 12), 'first_name')
    assert parse_config_item(str) == expected


def test_replace_field():
    input_start = 'a'
    input_to_replace = 'bcde'
    input_end = 'fghijklmnop'
    input = f'{input_start}{input_to_replace}{input_end}'
    config = {(2,5): 'first_name'}
    expected = input_start + fake_first_name(input_to_replace)[0:4] + input_end
    result = replace_field(input, config)
    assert result == expected

    # when the block to be replaced is longer than the fake value
    input_to_replace += ' ' * 10
    config = {(2, 5 + 10): 'first_name'}
    input = f'{input_start}{input_to_replace}{input_end}'
    expected = input_start + fake_first_name(input_to_replace)[0:4+10] + input_end
    result = replace_field(input, config)
    assert result == expected

    # date fields
    input_to_replace = '19551018'
    input = f'{input_start}{input_to_replace}{input_end}'
    config = {(2, 9): 'date'}
    replaced = replace_field(input, config)[len(input_start):len(input_to_replace)+1]
    assert replaced != input_to_replace
    assert isinstance(datetime.strptime(replaced, '%Y%m%d'), datetime)


def test_replace_fwf():
    config = '697-747:first_name,747-781:last_name,1057-1064:date'
    output = list(replace_fwf(FWF_PATH, config))
    input_file = open(FWF_PATH).read().split('\n')
    assert output[0] == input_file[0]
    assert 'JOE' not in output[1]
    assert 'SMITH' not in output[1]
    birth_date = output[1][1056:1064]
    assert birth_date != '19650814'
    print(birth_date)
    assert isinstance(datetime.strptime(birth_date, '%Y%m%d'), datetime)
    assert output[-1] == input_file[-1]
