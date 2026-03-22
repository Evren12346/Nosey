import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path


def load_module(path):
    loader = importlib.machinery.SourceFileLoader(path.stem, str(path))
    spec = importlib.util.spec_from_loader(path.stem, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


class NoseyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = Path(__file__).resolve().parent.parent
        cls.base = base
        net_path = base / "NetNosey"
        if not net_path.exists():
            net_path = base / "netNosey.py"

        web_path = base / "WebNosey"
        if not web_path.exists():
            web_path = base / "webNosey.py"

        cls.net = load_module(net_path)
        cls.web = load_module(web_path)

    def test_parse_ports_mixed(self):
        ports = self.net.parse_ports("22,80,443,1000-1002")
        self.assertEqual(ports, [22, 80, 443, 1000, 1001, 1002])

    def test_parse_ports_default(self):
        ports = self.net.parse_ports("default")
        self.assertIn(22, ports)
        self.assertIn(443, ports)

    def test_normalize_url(self):
        self.assertEqual(self.web.normalize_url("example.com"), "https://example.com")
        self.assertEqual(self.web.normalize_url("http://example.com"), "http://example.com")

    def test_html_report_generation(self):
        finding = self.net.Finding(
            severity="HIGH",
            title="Test",
            host="127.0.0.1",
            port=22,
            evidence="demo",
            recommendation="fix",
        )
        html = self.net.render_html_report("127.0.0.1", [finding], {"HIGH": 1, "risk_score": 10})
        self.assertIn("NetNosey Defensive Scan Report", html)
        self.assertIn("127.0.0.1", html)
        self.assertIn("HIGH", html)

    def test_plugin_loading_net(self):
        scanner = self.net.NetworkScanner("127.0.0.1", [22], timeout=0.1, workers=4, max_hosts=1)
        scanner.open_ports = [("127.0.0.1", 22)]
        scanner.run_plugins(self.base / "tests" / "fixtures" / "net")
        self.assertTrue(any(f.title == "Plugin Hit" for f in scanner.findings))

    def test_plugin_loading_web(self):
        scanner = self.web.WebScanner("https://example.com", timeout=1.0)

        class FakeResponse:
            headers = {"Cache-Control": "public"}

        scanner.fetch = lambda *args, **kwargs: FakeResponse()
        scanner.run_plugins(self.base / "tests" / "fixtures" / "web")
        self.assertTrue(any(f.title == "Fixture Web Plugin Hit" for f in scanner.findings))


if __name__ == "__main__":
    unittest.main()
