# Nosey

Defensive security scanners for authorized assessments.

Nosey currently includes two command-line tools:

- `NetNosey`: network exposure scanner for hosts, hostnames, and CIDR ranges
- `WebNosey`: web exposure scanner for HTTP/HTTPS targets

These tools are intended for defensive validation, internal review, lab environments, and authorized security testing only.

## Legal And Safety Notice

Only scan systems, networks, and websites that you own or have explicit permission to assess.

Both scanners require an explicit authorization flag before they run:

- `--authorized`

## Repository Layout

- `NetNosey`: main network scanner
- `WebNosey`: main web scanner
- `nosey_plugins/net/`: optional NetNosey plugin checks
- `nosey_plugins/web/`: optional WebNosey plugin checks
- `tests/`: unit tests

## Features

### NetNosey

- Scans IPs, hostnames, and CIDR ranges
- Concurrent port scanning
- Service banner sampling
- Core risk heuristics for exposed services
- JSON report output
- HTML report output
- Plugin support for extra checks
- Configurable ports, workers, timeouts, and host caps

### WebNosey

- HTTPS and TLS checks
- Security header checks
- HTTP method checks
- Cookie flag checks
- Sensitive path discovery heuristics
- Error disclosure heuristics
- JSON report output
- HTML report output
- Plugin support for extra checks

## Requirements

- Python 3.10+
- `requests`

Repository dependency file:

```bash
python3 -m pip install -r requirements.txt
```

Install dependencies:

```bash
python3 -m pip install requests
```

## NetNosey Usage

Basic example:

```bash
python3 NetNosey 192.168.1.10 --authorized
```

Scan a CIDR with custom output files:

```bash
python3 NetNosey 192.168.1.0/24 \
	--authorized \
	--json-out net_report.json \
	--html-out net_report.html
```

Scan specific ports only:

```bash
python3 NetNosey example.internal \
	--authorized \
	--ports 22,80,443,8080
```

Scan a range of ports:

```bash
python3 NetNosey 10.0.0.15 \
	--authorized \
	--ports 1-1024
```

Useful flags:

- `--ports`: comma-separated ports or ranges, or `default`
- `--timeout`: socket timeout in seconds
- `--workers`: concurrent scan workers
- `--max-hosts`: cap for CIDR scans
- `--plugin-dir`: plugin directory override
- `--json-out`: write JSON report
- `--html-out`: write HTML report

## WebNosey Usage

Basic example:

```bash
python3 WebNosey https://example.com --authorized
```

Generate reports:

```bash
python3 WebNosey https://example.com \
	--authorized \
	--json-out web_report.json \
	--html-out web_report.html
```

Override timeout and plugin directory:

```bash
python3 WebNosey app.internal \
	--authorized \
	--timeout 8 \
	--plugin-dir nosey_plugins/web
```

Useful flags:

- `--timeout`: request and TLS timeout in seconds
- `--plugin-dir`: plugin directory override
- `--json-out`: write JSON report
- `--html-out`: write HTML report

## Reports

Both tools support:

- terminal summaries
- machine-readable JSON output
- browser-friendly HTML reports

JSON reports are useful for automation and dashboards.
HTML reports are useful for manual review and sharing findings internally.

## Plugins

Plugins let you add custom checks without modifying the core scanner.

### Net Plugin Contract

Place Python files in `nosey_plugins/net/`.

Each plugin should expose:

```python
def run(context):
		return [
				{
						"severity": "LOW",
						"title": "Example finding",
						"host": "127.0.0.1",
						"port": 22,
						"evidence": "Example evidence",
						"recommendation": "Example fix",
				}
		]
```

Net plugin context includes:

- `open_ports`
- `host_to_ports`
- `service_banners`

### Web Plugin Contract

Place Python files in `nosey_plugins/web/`.

Each plugin should expose:

```python
def run(context):
		return [
				{
						"severity": "LOW",
						"title": "Example finding",
						"url": "https://example.com",
						"evidence": "Example evidence",
						"recommendation": "Example fix",
				}
		]
```

Web plugin context includes:

- `target_url`
- `fetch`
- `latest_info`

## Tests

Run the test suite from the repository root:

```bash
python3 -m unittest -q tests/test_nosey.py
```

Current tests cover:

- port parsing
- URL normalization
- HTML report generation
- plugin loading

## Continuous Integration

GitHub Actions now runs the repository test workflow on pushes and pull requests.

The workflow currently:

- installs Python dependencies from `requirements.txt`
- runs `tests/test_nosey.py`
- performs CLI smoke checks for `NetNosey` and `WebNosey`

## Example Workflow

1. Run a scanner against an authorized target.
2. Save JSON and HTML reports.
3. Review findings in the terminal and browser report.
4. Add team-specific checks as plugins.
5. Re-run after remediation.

## Current Plugin Examples

- `nosey_plugins/net/banner_disclosure.py`
- `nosey_plugins/web/cache_header_check.py`

## Notes

- Findings are heuristic indicators, not guaranteed exploitation proof.
- Use these tools alongside patch verification, configuration review, logging review, and authenticated testing where appropriate.
