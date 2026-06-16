import json
import subprocess
import sys

REPORT_FILE = "compliance/reports/compliance_report.json"


def run_command(command, description):
    print(f"\n{description}...\n")

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nFailed: {description}")
        sys.exit(1)


def read_report():
    with open(REPORT_FILE, "r") as file:
        return json.load(file)


def deployment_allowed(report):
    for rule in report:
        if rule["status"] == "FAIL":
            return False

    return True


def print_failures(report):
    print("\nCompliance failed. Deployment blocked.\n")

    for rule in report:
        if rule["status"] == "FAIL":
            print(f"{rule['rule_id']} - {rule['rule_name']}")
            print(f"Severity: {rule['severity']}")

            for finding in rule["findings"]:
                print(f"Finding: {finding}")

            print()


def deploy():
    run_command(
        [
            "ansible-playbook",
            "-i",
            "ansible/inventory/hosts.yml",
            "ansible/playbooks/baseline.yml",
        ],
        "Deploying configuration with Ansible",
    )


def main():
    run_command(
        ["python3", "compliance/device_connection.py"],
        "Collecting latest running configuration",
    )

    run_command(
        ["python3", "compliance/checker.py"],
        "Running compliance checker",
    )

    report = read_report()

    if deployment_allowed(report):
        print("\nCompliance passed.")
        deploy()
    else:
        print_failures(report)


if __name__ == "__main__":
    main()