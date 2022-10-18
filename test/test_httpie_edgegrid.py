import os
from test.utils import normalize_path

import pytest
from httpie_edgegrid import EdgeGridPlugin
from requests import Request


class TestHttpieEdgegrid:
    _host = "https://xxxx-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.luna.akamaiapis.net/"

    @pytest.fixture
    def setUp(self, request):
        old_rc_path = os.getenv("RC_PATH")
        os.environ["RC_PATH"] = normalize_path('testfiles/sample_edgerc')

        yield

        if old_rc_path:
            os.environ["RC_PATH"] = old_rc_path
        else:
            os.unsetenv("RC_PATH")

    def _test_case(self, url, expected_url, entry):
        edge_grid_plugin = EdgeGridPlugin()
        auth = edge_grid_plugin.get_auth(username=entry, password='')
        r = Request(method="GET", url=url).prepare()
        p = auth.__call__(r)

        assert expected_url == str(p.url)

    def test_http_to_https_conversion(self, setUp):
        self._test_case("http://abc.com", "https://abc.com/", "default")

    def test_localhost(self):
        self._test_case("https://localhost/", self._host, "default")

    @pytest.mark.parametrize(
        'rc_path, exception_code',
        [
            ('testfiles/not_existing_edgerc', 1),
            ('test_httpie_edgegrid.py', 2),
            ('testfiles/sample_edgerc_duplicated_section', 2),
            ('testfiles/binary', 2),
        ]
    )
    def test_bad_rc(self, rc_path, exception_code, setUp):
        with pytest.raises(SystemExit) as e:
            os.environ['RC_PATH'] = normalize_path(rc_path)
            self._test_case("https://localhost/", self._host, "default")

        assert e.value.code == exception_code

    def test_bad_rc_entry(self, setUp):
        with pytest.raises(SystemExit) as e:
            self._test_case("https://localhost/", self._host, "not_default")

        assert e.value.code == 3
