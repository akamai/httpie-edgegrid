import os
import unittest

from requests import Request

from httpie_edgegrid import EdgeGridPlugin

from test.utils import normalize_path


class HttpieEdgegridTest(unittest.TestCase):
    old_rc_path = ''
    _host = "https://xxxx-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.luna.akamaiapis.net/"

    def _test_case(self, url, expected_url, entry):
        edge_grid_plugin = EdgeGridPlugin()
        auth = edge_grid_plugin.get_auth(username=entry, password='')
        r = Request(method="GET", url=url).prepare()
        p = auth.__call__(r)
        self.assertEqual(expected_url, str(p.url))

    def setUp(self) -> None:
        self.old_rc_path = os.getenv("RC_PATH")
        os.environ["RC_PATH"] = normalize_path('testfiles/sample_edgerc')

    def tearDown(self) -> None:
        if self.old_rc_path:
            os.environ["RC_PATH"] = self.old_rc_path
        else:
            os.unsetenv("RC_PATH")

    def test_http_to_https_conversion(self):
        self._test_case("http://abc.com", "https://abc.com/", "default")

    def test_localhost(self):
        self._test_case("https://localhost/", self._host, "default")

    def test_bad_rc_path(self):
        with self.assertRaises(SystemExit) as err_msg:
            os.environ["RC_PATH"] = normalize_path('testfiles/not_existing_edgerc')
            self._test_case("https://localhost/", self._host, "default")
        self.assertEqual(1, err_msg.exception.code)

    def test_bad_rc_entry(self):
        with self.assertRaises(SystemExit) as err:
            self._test_case("https://localhost/", self._host, "not_default")
        self.assertEqual(1, err.exception.code)


if __name__ == '__main__':
    unittest.main()
