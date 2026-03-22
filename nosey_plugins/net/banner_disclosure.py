"""Sample NetNosey plugin: banner disclosure heuristics."""

def run(context):
    findings = []
    banners = context.get("service_banners", {})
    for (host, port), banner in banners.items():
        lower = banner.lower()
        if "server:" in lower and "/" in lower:
            findings.append({
                "severity": "LOW",
                "title": "Verbose service banner disclosure",
                "host": host,
                "port": port,
                "evidence": f"Banner appears to include version details: {banner[:120]}",
                "recommendation": "Reduce service banner verbosity where feasible.",
            })
    return findings
