def run(context):
    target = context.get("target_url", "https://example.com")
    return [
        {
            "severity": "LOW",
            "title": "Fixture Web Plugin Hit",
            "url": target,
            "evidence": "Web fixture plugin executed successfully",
            "recommendation": "No action required for test fixture",
        }
    ]