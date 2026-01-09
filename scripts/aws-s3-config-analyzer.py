import json
import argparse
import os

def analyze_s3_config(file_path):
    """
    Analyzes a single S3 bucket configuration JSON file for security and operational issues.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"bucket_name": os.path.basename(file_path), "error": "Invalid JSON format."}
    except FileNotFoundError:
        return {"bucket_name": os.path.basename(file_path), "error": "File not found."}


    bucket_name = data.get("bucket_name", "N/A")
    findings = []

    # --- Security Checks ---
    security = data.get("security", {})

    # 1. Public Access Block
    pub_access_block = security.get("public_access_block", {}).get("security_analysis", {})
    if not pub_access_block.get("all_public_access_blocked", False):
        findings.append({
            "check": "Public Access Block",
            "severity": "CRITICAL",
            "message": "Public Access Block is not fully enabled. This significantly increases the risk of data exposure.",
            "details": pub_access_block
        })

    # 2. Encryption
    encryption = security.get("encryption", {}).get("analysis", {})
    if not encryption.get("is_encrypted", False):
        findings.append({
            "check": "Default Encryption",
            "severity": "HIGH",
            "message": "Default server-side encryption is not enabled. Data at rest is not automatically encrypted.",
        })

    # 3. Access Logging
    logging_analysis = security.get("logging", {}).get("analysis", {})
    if not logging_analysis.get("is_enabled", False):
        findings.append({
            "check": "Server Access Logging",
            "severity": "MEDIUM",
            "message": "Server access logging is not enabled. There is no audit trail for requests made to the bucket.",
        })
        
    # 4. ACL Public Access
    acl_analysis = security.get("acl", {}).get("security_analysis", {})
    if acl_analysis.get("has_public_access", False):
        findings.append({
            "check": "ACL Public Access",
            "severity": "CRITICAL",
            "message": "The bucket ACL grants public access. This is a direct data exposure risk.",
            "details": {"public_grants": acl_analysis.get("public_grants")}
        })

    # 5. CORS Wildcard Origin
    cors_analysis = security.get("cors", {}).get("analysis", {})
    if cors_analysis.get("has_wildcard_origin", False):
        findings.append({
            "check": "CORS Policy",
            "severity": "MEDIUM",
            "message": "CORS configuration allows wildcard ('*') origin. This could allow malicious websites to make requests to your bucket.",
            "details": {"allowed_origins": cors_analysis.get("allowed_origins")}
        })


    # --- Operational Checks ---
    operational = data.get("operational", {})

    # 6. Versioning
    versioning = operational.get("versioning", {}).get("analysis", {})
    if not versioning.get("is_enabled", False):
        findings.append({
            "check": "Object Versioning",
            "severity": "MEDIUM",
            "message": "Object versioning is not enabled. This can lead to data loss from accidental overwrites or deletions.",
        })

    # 7. MFA Delete
    if versioning.get("is_enabled", False) and not versioning.get("mfa_delete_enabled", False):
        findings.append({
            "check": "MFA Delete",
            "severity": "HIGH",
            "message": "MFA Delete is not enabled. A compromised account could permanently delete objects without multi-factor authentication.",
        })
        
    return {
        "bucket_name": bucket_name,
        "region": data.get("region", "N/A"),
        "findings": findings
    }

def print_report(analysis_result):
    """Prints a formatted report of the analysis findings."""
    print("-" * 60)
    print(f"Analysis Report for Bucket: {analysis_result['bucket_name']} (Region: {analysis_result['region']})")
    print("-" * 60)

    if analysis_result.get("error"):
        print(f"  [ERROR] {analysis_result['error']}")
        print("-" * 60)
        return

    findings = analysis_result.get("findings", [])
    if not findings:
        print("  [INFO] No issues found. The bucket configuration appears secure.")
    else:
        # Sort findings by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(findings, key=lambda x: severity_order.get(x['severity'], 99))
        
        for finding in sorted_findings:
            print(f"  [{finding['severity']}] {finding['check']}")
            print(f"    - {finding['message']}")
            if "details" in finding:
                 print(f"    - Details: {json.dumps(finding['details'], indent=2).replace('{', '').replace('}', '').replace('"', '')}")


    print("-" * 60)
    print("\n")


def main():
    """Main function to parse arguments and run the analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze AWS S3 bucket configuration JSON exports for common misconfigurations.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="Path to a single JSON file or a directory containing JSON files."
    )
    args = parser.parse_args()

    if os.path.isfile(args.path):
        result = analyze_s3_config(args.path)
        print_report(result)
    elif os.path.isdir(args.path):
        print(f"Scanning directory: {args.path}\n")
        for filename in sorted(os.listdir(args.path)):
            if filename.endswith(".json"):
                file_path = os.path.join(args.path, filename)
                result = analyze_s3_config(file_path)
                print_report(result)
    else:
        print(f"[ERROR] The path '{args.path}' is not a valid file or directory.")

if __name__ == "__main__":
    main()
