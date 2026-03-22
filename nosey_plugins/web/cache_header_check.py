"""Sample WebNosey plugin: cache control checks for dynamic pages."""

def run(context):
    findings = []
    fetch = context.get("fetch")
    target = context.get("target_url")
    if not fetch or not target:
        return findings

    resp = fetch(target)
    if not resp:
        return findings

    cache_control = resp.headers.get("Cache-Control", "")
    pragma = resp.headers.get("Pragma", "")
    if "no-store" not in cache_control.lower() and "no-cache" not in cache_control.lower() and "no-cache" not in pragma.lower():
        findings.append({
            "severity": "LOW",
            "title": "Potentially permissive cache directives",
            "url": target,
            "evidence": "No no-store/no-cache directive detected in response headers.",
            "recommendation": "Set cache directives appropriately for sensitive pages.",
        })
    return findings
