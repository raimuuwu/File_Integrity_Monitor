import argparse
import sys
from core.baseline import create_baseline
from core.monitor import start_live_monitoring
from core.verifier import verify_integrity
from utils.logger import log_event


def main():
    parser = argparse.ArgumentParser(description="File Integrity Monitor")

    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        required=True,
        help="Target directory to scan/monitor",
    )
    parser.add_argument(
        "-db",
        "--database",
        type=str,
        default="baseline.json",
        help="Path to baseline database file (default: baseline.json)",
    )


    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-b",
        "--baseline",
        action="store_true",
        help="Create baseline snapshot of the directory",
    )
    mode_group.add_argument(
        "-v",
        "--verify",
        action="store_true",
        help="Verify directory integrity against baseline database",
    )
    mode_group.add_argument(
        "-m",
        "--monitor",
        action="store_true",
        help="Start real-time live monitoring",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.baseline:
        print(f"[*] Creating baseline snapshot for: {args.dir}")
        if create_baseline(args.dir, args.database):
            log_event("BASELINE_CREATED", args.dir)

    elif args.verify:
        print(f"[*] Verifying integrity for: {args.dir}")
        results = verify_integrity(args.dir, args.database)

        print("\n=== INTEGRITY CHECK REPORT ===")

        if results["modified"]:
            print(f"[!] MODIFIED FILES ({len(results['modified'])}):")
            for file_path in results["modified"]:
                print(f"    - {file_path}")
                log_event("MODIFIED", file_path)

        if results["created"]:
            print(f"[+] NEW/CREATED FILES ({len(results['created'])}):")
            for file_path in results["created"]:
                print(f"    - {file_path}")
                log_event("CREATED", file_path)

        if results["deleted"]:
            print(f"[-] DELETED FILES ({len(results['deleted'])}):")
            for file_path in results["deleted"]:
                print(f"    - {file_path}")
                log_event("DELETED", file_path)

        if (
            not results["modified"]
            and not results["created"]
            and not results["deleted"]
        ):
            print("[+] Integrity intact. No unauthorized changes detected.")

    elif args.monitor:
        start_live_monitoring(args.dir, args.database)


if __name__ == "__main__":
    main()