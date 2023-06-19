import os.path
from test.utils import normalize_path
from unittest.mock import MagicMock

import pytest
from gen_edgerc import generate_edgerc


@pytest.fixture
def setup(request):
    request.param = {k: normalize_path(
        v) if k != 'section' else v for k, v in request.param.items()}

    if os.path.exists(request.param['target_path']):
        os.remove(request.param['target_path'])

    mock = MagicMock()
    mock.cred_file = request.param['input_configuration']
    mock.config_section = request.param['section']

    if 'preconfig' in request.param:
        with open(request.param['preconfig'], 'rb') as src, open(request.param['target_path'], 'wb') as dst:
            dst.write(src.read())

    yield mock, request.param

    if os.path.exists(request.param['target_path']):
        os.remove(request.param['target_path'])


@pytest.mark.parametrize(
    'setup',
    [
        {
            'expected_path': 'testfiles/expected_default',
            'target_path': 'testfiles/target_default',
            'input_configuration': 'testfiles/config_default',
            'section': 'default'
        },
        {
            'expected_path': 'testfiles/expected_secondary',
            'target_path': 'testfiles/target_secondary',
            'input_configuration': 'testfiles/config_secondary',
            'preconfig': 'testfiles/preconfig_secondary',
            'section': 'secondary'
        },
    ],
    indirect=True)
def test_generate_edgerc(setup):
    args_mock, params = setup

    generate_edgerc(args_mock, params['target_path'], False)

    with open(params['target_path']) as res, open(params['expected_path']) as expected:
        assert list(res) == list(expected)
