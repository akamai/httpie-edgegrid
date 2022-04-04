import io
import os.path
import sys
import unittest

if sys.version_info[0] >= 3:
    # python3
    from unittest.mock import MagicMock
else:
    # python2.7
    from mock.mock import MagicMock

from gen_edgerc import generate_edgerc
from test.utils import normalize_path


def test_case(assert_func, target_path, input_configuration, expected_path, section):
    mock = MagicMock()
    mock.cred_file = input_configuration
    mock.config_section = section
    generate_edgerc(mock, target_path, False)

    expected = io.open(expected_path)
    target = io.open(target_path)
    assert_func(list(expected), list(target))

    target.close()
    expected.close()

    if os.path.exists(target_path):
        os.remove(target_path)


class MyTestCase(unittest.TestCase):
    def test_default(self):
        expected_path = normalize_path("testfiles/expected_default")
        target_path = normalize_path("testfiles/target_default")
        input_configuration = normalize_path("testfiles/config_default")

        if os.path.exists(target_path):
            os.remove(target_path)

        test_case(self.assertListEqual, target_path, input_configuration, expected_path, "default")

    def test_appending(self):
        expected_path = normalize_path("testfiles/expected_secondary")
        target_path = normalize_path("testfiles/target_secondary")
        input_configuration = normalize_path("testfiles/config_secondary")
        preconfig = normalize_path("testfiles/preconfig_secondary")

        if os.path.exists(target_path):
            os.remove(target_path)

        with open(preconfig, 'rb') as src, open(target_path, 'wb') as dst:
            dst.write(src.read())

        test_case(self.assertListEqual, target_path, input_configuration, expected_path, "secondary")


if __name__ == '__main__':
    unittest.main()
