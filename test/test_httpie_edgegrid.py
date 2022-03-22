import unittest

from requests import Request

from httpie_edgegrid import EdgeGridPlugin

from test.utils import normalize_path


def test_case(url, expected):
    edge_grid_plugin = EdgeGridPlugin()
    edge_grid_plugin.edgerc_location = normalize_path('testfiles/sample_edgerc')
    auth = edge_grid_plugin.get_auth("default", '')
    r = Request(method="GET", url=url).prepare()
    p = auth.__call__(r)
    assert expected == str(p.url)


class HttpieEdgegridTest(unittest.TestCase):
    def test_http_to_https_conversion(self):
        test_case("http://abc.com", "https://abc.com/")

    def test_localhost(self):
        test_case("https://localhost/",
                  "https://xxxx-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.luna.akamaiapis.net/")


if __name__ == '__main__':
    unittest.main()
