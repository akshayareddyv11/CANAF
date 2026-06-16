import json
import yaml
from pathlib import Path

CONFIG_FILE = Path("compliance/reports/cat8000v_running_config.txt")
POLICY_FILE = Path("compliance/policies/cisco_ios.yml")
REPORT_FILE = Path("compliance/reports/compliance_report.json")


def load_config():
    return CONFIG_FILE.read_text()


def load_policies():
    with open(POLICY_FILE, "r") as file:
        return yaml.safe_load(file)


def check_compliance(config, policies):
    results = []

    for rule in policies["rules"]:
        status = "PASS"
        findings = []

        for required_item in rule.get("required", []):
            if required_item not in config:
                status = "FAIL"
                findings.append(f"Missing required config: {required_item}")

        for forbidden_item in rule.get("forbidden", []):
            if forbidden_item in config:
                status = "FAIL"
                findings.append(f"Forbidden config found: {forbidden_item}")

        results.append({
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "status": status,
            "findings": findings
        })

    return results


def main():
    config = load_config()
    policies = load_policies()

    results = check_compliance(config, policies)

    REPORT_FILE.write_text(json.dumps(results, indent=4))

    print("Compliance check complete.")
    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()