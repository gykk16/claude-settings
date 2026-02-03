#!/usr/bin/env python3
"""
mail_brief.py - Fetch Gmail and IMAP messages

Discovers Google accounts via gog CLI and IMAP accounts via config file,
classifies them as personal or work, then fetches email messages for the
specified time period. Outputs JSON with message summaries.
"""

import argparse
import datetime
import email
import email.header
import imaplib
import json
import os
import re
import subprocess
import sys
from email.utils import parsedate_to_datetime


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch Gmail messages for personal/work accounts"
    )

    # Account specification
    parser.add_argument(
        "--personal",
        type=str,
        metavar="EMAIL",
        help="Personal account email (optional, auto-discovers if not provided)"
    )
    parser.add_argument(
        "--work",
        type=str,
        metavar="EMAIL",
        help="Work account email (optional, auto-discovers if not provided)"
    )

    # Date range specification (mutually exclusive)
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--today",
        action="store_true",
        help="Fetch messages from today (default)"
    )
    date_group.add_argument(
        "--yesterday",
        action="store_true",
        help="Fetch messages from yesterday"
    )
    date_group.add_argument(
        "--this-week",
        action="store_true",
        help="Fetch messages from this week (Sunday to today)"
    )
    date_group.add_argument(
        "--last-week",
        action="store_true",
        help="Fetch messages from last week (Sunday to Saturday)"
    )
    date_group.add_argument(
        "--date",
        type=str,
        metavar="YYYY-MM-DD",
        help="Fetch messages from a specific date"
    )

    args = parser.parse_args()

    # Default to --today if no date option specified
    if not any([args.today, args.yesterday, args.this_week, args.last_week, args.date]):
        args.today = True

    return args


def discover_accounts():
    """
    Discover Google accounts using gog CLI.

    Returns:
        List of email addresses
    """
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        return [a["email"] for a in data.get("accounts", [])]

    except Exception:
        return []


def classify_account(email):
    """
    Classify an email account as personal or work.

    Personal domains: gmail.com, naver.com, daum.net, hanmail.net, yahoo.com,
                     hotmail.com, outlook.com, icloud.com, kakao.com, nate.com

    Args:
        email: Email address to classify

    Returns:
        "personal" or "work"
    """
    personal_domains = {
        "gmail.com",
        "naver.com",
        "daum.net",
        "hanmail.net",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
        "kakao.com",
        "nate.com"
    }

    domain = email.split("@")[-1].lower()
    return "personal" if domain in personal_domains else "work"


def load_imap_accounts():
    """
    Load IMAP accounts from config file.

    Returns:
        List of IMAP account dictionaries
    """
    config_path = os.path.expanduser("~/.claude/skills/mail-brief/accounts.json")

    if not os.path.exists(config_path):
        return []

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("imap_accounts", [])
    except Exception:
        return []


def connect_imap(account):
    """
    Connect to IMAP server and login.

    Args:
        account: IMAP account dictionary with server settings

    Returns:
        Connected IMAP4_SSL or IMAP4 object

    Raises:
        RuntimeError: If connection or authentication fails
    """
    try:
        if account.get("use_ssl", True):
            imap = imaplib.IMAP4_SSL(
                account["imap_server"],
                account.get("imap_port", 993)
            )
        else:
            imap = imaplib.IMAP4(
                account["imap_server"],
                account.get("imap_port", 143)
            )

        imap.login(account["username"], account["password"])
        return imap

    except Exception as e:
        raise RuntimeError(f"IMAP connection failed for {account['email']}: {e}")


def build_imap_search_criteria(args):
    """
    Build IMAP search criteria based on date arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        IMAP search criteria string
    """
    today = datetime.date.today()

    if args.today:
        date_str = today.strftime("%d-%b-%Y")
        return f'SINCE {date_str}'

    elif args.yesterday:
        yesterday = today - datetime.timedelta(days=1)
        date_str = yesterday.strftime("%d-%b-%Y")
        return f'ON {date_str}'

    elif args.this_week:
        days_since_sunday = (today.weekday() + 1) % 7
        sunday = today - datetime.timedelta(days=days_since_sunday)
        date_str = sunday.strftime("%d-%b-%Y")
        return f'SINCE {date_str}'

    elif args.last_week:
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - datetime.timedelta(days=days_since_sunday)
        last_sunday = this_sunday - datetime.timedelta(days=7)
        last_saturday = this_sunday - datetime.timedelta(days=1)
        since_str = last_sunday.strftime("%d-%b-%Y")
        before_str = this_sunday.strftime("%d-%b-%Y")
        return f'SINCE {since_str} BEFORE {before_str}'

    elif args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
            date_str = target_date.strftime("%d-%b-%Y")
            return f'ON {date_str}'
        except ValueError:
            raise ValueError(f"Invalid date format: {args.date}. Use YYYY-MM-DD")

    # Default to today
    date_str = today.strftime("%d-%b-%Y")
    return f'SINCE {date_str}'


def decode_header_value(header_value):
    """
    Decode email header value handling various encodings.

    Args:
        header_value: Raw header value string

    Returns:
        Decoded string
    """
    if not header_value:
        return ""

    decoded_parts = []
    for part, encoding in email.header.decode_header(header_value):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or "utf-8", errors="replace"))
        else:
            decoded_parts.append(part)

    return "".join(decoded_parts)


def fetch_imap_messages(account, search_criteria):
    """
    Fetch messages from IMAP server.

    Args:
        account: IMAP account dictionary
        search_criteria: IMAP search criteria string

    Returns:
        List of simplified message dictionaries

    Raises:
        RuntimeError: If IMAP operations fail
    """
    try:
        imap = connect_imap(account)
        imap.select("INBOX")

        # Search for messages
        status, message_ids = imap.search(None, search_criteria)
        if status != "OK":
            raise RuntimeError("IMAP search failed")

        message_id_list = message_ids[0].split()
        messages = []

        # Fetch messages (limit to 50 most recent)
        for msg_id in message_id_list[-50:]:
            status, msg_data = imap.fetch(msg_id, "(RFC822 FLAGS)")
            if status != "OK":
                continue

            # Parse message
            raw_email = msg_data[0][1]
            flags = msg_data[0][0].decode()
            msg = email.message_from_bytes(raw_email)

            # Extract fields
            subject = decode_header_value(msg.get("Subject", "(No subject)"))
            from_header = decode_header_value(msg.get("From", ""))
            date_header = msg.get("Date", "")

            # Parse date
            try:
                msg_date = parsedate_to_datetime(date_header)
                date_str = msg_date.isoformat()
            except:
                date_str = ""

            # Parse from
            from_name, from_email_addr = parse_from(from_header)

            # Check if unread
            is_unread = "\\Seen" not in flags

            messages.append({
                "date": date_str,
                "subject": subject,
                "from_name": from_name,
                "from_email": from_email_addr,
                "labels": [],
                "is_unread": is_unread,
                "account_type": account["type"]
            })

        imap.close()
        imap.logout()

        return messages

    except Exception as e:
        raise RuntimeError(f"IMAP fetch failed for {account['email']}: {e}")


def resolve_accounts(args):
    """
    Resolve which accounts to query based on args and config.

    Args:
        args: Parsed command-line arguments

    Returns:
        Tuple of (gmail_accounts, imap_accounts)
        - gmail_accounts: List of dicts with "email" and "type"
        - imap_accounts: List of IMAP account config dicts
    """
    gmail_accounts = []

    # If explicit Gmail accounts provided, use them
    if args.personal:
        gmail_accounts.append({"email": args.personal, "type": "personal"})
    if args.work:
        gmail_accounts.append({"email": args.work, "type": "work"})

    # If no explicit accounts, auto-discover Gmail accounts
    if not gmail_accounts:
        for email_addr in discover_accounts():
            gmail_accounts.append({"email": email_addr, "type": classify_account(email_addr)})

    # Load IMAP accounts from config
    imap_accounts = load_imap_accounts()

    return gmail_accounts, imap_accounts


def build_gmail_query(args):
    """
    Build Gmail search query based on date arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Gmail search query string
    """
    today = datetime.date.today()

    if args.today:
        return "newer_than:1d"

    elif args.yesterday:
        yesterday = today - datetime.timedelta(days=1)
        after = yesterday.strftime("%Y/%m/%d")
        before = today.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.this_week:
        # Sunday of current week to tomorrow
        days_since_sunday = (today.weekday() + 1) % 7  # Sun=0
        sunday = today - datetime.timedelta(days=days_since_sunday)
        tomorrow = today + datetime.timedelta(days=1)
        after = sunday.strftime("%Y/%m/%d")
        before = tomorrow.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.last_week:
        # Previous Sunday to this Sunday
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - datetime.timedelta(days=days_since_sunday)
        last_sunday = this_sunday - datetime.timedelta(days=7)
        after = last_sunday.strftime("%Y/%m/%d")
        before = this_sunday.strftime("%Y/%m/%d")
        return f"after:{after} before:{before}"

    elif args.date:
        # Specific date to next day
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
            next_day = target_date + datetime.timedelta(days=1)
            after = target_date.strftime("%Y/%m/%d")
            before = next_day.strftime("%Y/%m/%d")
            return f"after:{after} before:{before}"
        except ValueError:
            raise ValueError(f"Invalid date format: {args.date}. Use YYYY-MM-DD")

    # Default to today
    return "newer_than:1d"


def fetch_messages(account_email, query):
    """
    Fetch Gmail messages using gog CLI.

    Args:
        account_email: Email address of the account
        query: Gmail search query

    Returns:
        List of message dictionaries

    Raises:
        RuntimeError: If gog command fails
    """
    try:
        cmd = [
            "gog", "gmail", "messages", "search",
            query,
            "--json",
            "--max=50",
            f"--account={account_email}"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(f"gog gmail search failed: {result.stderr}")

        data = json.loads(result.stdout)
        return data.get("messages", [])

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"gog gmail search timed out after 30 seconds for {account_email}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse gog output for {account_email}: {e}")


def parse_from(raw):
    """
    Parse 'From' header into display name and email.

    Handles formats:
    - "Display Name <email@domain.com>"
    - "email@domain.com"

    Args:
        raw: Raw 'From' header value

    Returns:
        Tuple of (display_name, email)
    """
    raw = raw.strip()

    # Check for "Name <email>" format
    if "<" in raw and ">" in raw:
        name_part = raw[:raw.index("<")].strip()
        email_part = raw[raw.index("<") + 1:raw.index(">")].strip()
        return (name_part, email_part)

    # Bare email address
    return (raw, raw)


def simplify_message(msg, account_type):
    """
    Simplify message to essential fields.

    Args:
        msg: Raw message dictionary from gog
        account_type: "personal" or "work"

    Returns:
        Simplified message dictionary
    """
    # Parse from field
    from_raw = msg.get("from", "")
    from_name, from_email = parse_from(from_raw)

    # Filter labels and detect unread status
    labels = msg.get("labels", [])
    is_unread = "UNREAD" in labels
    filtered_labels = [label for label in labels if label != "UNREAD"]

    return {
        "date": msg.get("date", ""),
        "subject": msg.get("subject", "(No subject)"),
        "from_name": from_name,
        "from_email": from_email,
        "labels": filtered_labels,
        "is_unread": is_unread,
        "account_type": account_type
    }


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()

        # Resolve accounts
        gmail_accounts, imap_accounts = resolve_accounts(args)

        if not gmail_accounts and not imap_accounts:
            json.dump(
                {"error": "No accounts found. Use --personal/--work, configure gog auth, or add IMAP accounts to ~/.claude/skills/mail-brief/accounts.json"},
                sys.stdout,
                ensure_ascii=False,
                indent=2
            )
            sys.exit(1)

        # Build queries
        gmail_query = build_gmail_query(args)
        imap_criteria = build_imap_search_criteria(args)

        # Fetch messages from all accounts
        all_messages = []
        errors = []
        all_accounts_info = []

        # Fetch Gmail messages
        for account in gmail_accounts:
            all_accounts_info.append({"email": account["email"], "type": account["type"], "source": "gmail"})
            try:
                messages = fetch_messages(account["email"], gmail_query)
                all_messages.extend(
                    simplify_message(m, account["type"]) for m in messages
                )
            except Exception as e:
                errors.append({"email": account["email"], "error": str(e), "source": "gmail"})

        # Fetch IMAP messages
        for account in imap_accounts:
            all_accounts_info.append({"email": account["email"], "type": account["type"], "source": "imap"})
            try:
                messages = fetch_imap_messages(account, imap_criteria)
                all_messages.extend(messages)
            except Exception as e:
                errors.append({"email": account["email"], "error": str(e), "source": "imap"})

        # Output results
        output = {
            "accounts": all_accounts_info,
            "messages": all_messages,
        }
        if errors:
            output["errors"] = errors

        json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
        sys.exit(0)

    except Exception as e:
        # Top-level error handling
        error_output = {
            "error": str(e)
        }
        json.dump(error_output, sys.stdout, ensure_ascii=False, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
