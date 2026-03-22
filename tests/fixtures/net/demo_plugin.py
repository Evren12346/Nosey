def run(context):
    return [
        {
            "severity": "LOW",
            "title": "Plugin Hit",
            "host": "127.0.0.1",
            "port": 22,
            "evidence": "Fixture plugin executed successfully",
            "recommendation": "No action required for test fixture",
        }
    ]