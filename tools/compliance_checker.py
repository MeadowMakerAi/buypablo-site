#!/usr/bin/env python3
"""
Pablo Fresh Content Compliance Checker

Scans captions, hashtags, and content metadata against the social.compliance_rules
table in Supabase. Every piece of content runs through this before hitting the
Slack approval gate.

Usage:
    python compliance_checker.py --platform instagram --caption "Great vibes today" --hashtags "#nyc #flavor"
    python compliance_checker.py --platform instagram --caption-file caption.txt
    python compliance_checker.py --platform x --caption "New Pablo Fresh drop" --hashtags "#pablofresh"

Returns exit code 0 if compliant, 1 if violations found, 2 if warnings only.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone


# --- Rule Loading ---
# Rules can come from Supabase or local fallback

def load_rules_from_supabase():
    """Load compliance rules from Supabase. Requires SUPABASE_URL and SUPABASE_SERVICE_KEY env vars."""
    try:
        import httpx
    except ImportError:
        return None

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        return None

    try:
        resp = httpx.get(
            f"{url}/rest/v1/compliance_rules?active=eq.true&select=*",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Accept-Profile": "social",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def load_rules_local():
    """Hardcoded fallback rules — subset of what's in Supabase. Use when offline."""
    return {
        "banned_words": {
            "instagram": {
                "block": [
                    "cannabis", "marijuana", "weed", "thc", "cbd", "420", "pot",
                    "stoner", "blazed", "stoned", "lifted", "dank", "kush", "ganja",
                    "reefer", "mary jane", "dispensary", "budtender", "indica", "sativa",
                    "trichome", "nug", "preroll", "pre-roll", "blunt",
                    "buy now", "order now", "shop now", "in stock", "dm to order",
                    "dm for menu", "add to cart", "purchase", "delivery available",
                    "we deliver", "on sale", "discount", "promo code", "free shipping",
                    "milligram", "high potency", "get high", "intoxicating",
                    "psychoactive", "euphoria", "body high", "head high", "couch lock",
                ],
                "warn": [
                    "joint", "edible", "flower", "dab", "bud", "available now", "treats",
                ],
            },
        },
        "banned_hashtags": {
            "instagram": [
                "#cannabis", "#cannabiscommunity", "#cannabisculture", "#cannabistagram",
                "#cannabissociety", "#cannabisclub", "#cannabisconnoisseur",
                "#cannabisdaily", "#cannabislifestyle", "#cannabiscures", "#cannabisheals",
                "#marijuana", "#weed", "#weedporn", "#420", "#420life", "#420daily",
                "#thc", "#cbd", "#stoner", "#stonerlife", "#dispensary", "#pot",
                "#ganja", "#kush", "#prerolls", "#prerolled", "#concentrates",
                "#weededibles", "#delta8", "#mmj", "#mmjhealth", "#hemp", "#ouid",
                "#cannabiscup", "#medicalmarijuana",
            ],
        },
        "health_claims": [
            "cures", "heals", "relieves pain", "anti-inflammatory",
            "anxiety relief", "sleep aid",
        ],
    }


def parse_supabase_rules(raw_rules):
    """Convert Supabase rows into the structured format the checker uses."""
    parsed = {"banned_words": {}, "banned_hashtags": {}, "health_claims": []}

    for rule in raw_rules:
        rt = rule["rule_type"]
        platform = rule["platform"]
        value = rule["rule_value"]
        severity = rule["severity"]

        if rt == "banned_word":
            if platform not in parsed["banned_words"]:
                parsed["banned_words"][platform] = {"block": [], "warn": []}
            parsed["banned_words"][platform][severity].append(value)

        elif rt == "banned_hashtag":
            if platform not in parsed["banned_hashtags"]:
                parsed["banned_hashtags"][platform] = []
            parsed["banned_hashtags"][platform].append(value)

        elif rt == "banned_word" and rule.get("category") == "health_claim":
            parsed["health_claims"].append(value)

    return parsed


# --- Checking Logic ---

def check_caption(caption, platform, rules):
    """Check a caption against banned word rules. Returns list of violations."""
    violations = []
    caption_lower = caption.lower()

    # Get platform-specific rules + 'all' rules
    platforms_to_check = [platform, "all"]

    for p in platforms_to_check:
        word_rules = rules.get("banned_words", {}).get(p, {})

        for word in word_rules.get("block", []):
            # Word boundary matching for short words, substring for phrases
            if len(word.split()) > 1:
                # Multi-word phrase: substring match
                if word.lower() in caption_lower:
                    violations.append({
                        "type": "banned_word",
                        "severity": "BLOCK",
                        "value": word,
                        "platform": p,
                        "message": f'Caption contains blocked phrase: "{word}"',
                    })
            else:
                # Single word: word boundary match
                pattern = r'\b' + re.escape(word.lower()) + r'\b'
                if re.search(pattern, caption_lower):
                    violations.append({
                        "type": "banned_word",
                        "severity": "BLOCK",
                        "value": word,
                        "platform": p,
                        "message": f'Caption contains blocked word: "{word}"',
                    })

        for word in word_rules.get("warn", []):
            if len(word.split()) > 1:
                if word.lower() in caption_lower:
                    violations.append({
                        "type": "banned_word",
                        "severity": "WARN",
                        "value": word,
                        "platform": p,
                        "message": f'Caption contains flagged phrase: "{word}" — review context',
                    })
            else:
                pattern = r'\b' + re.escape(word.lower()) + r'\b'
                if re.search(pattern, caption_lower):
                    violations.append({
                        "type": "banned_word",
                        "severity": "WARN",
                        "value": word,
                        "platform": p,
                        "message": f'Caption contains flagged word: "{word}" — review context',
                    })

    # Health claims (all platforms)
    for claim in rules.get("health_claims", []):
        if claim.lower() in caption_lower:
            violations.append({
                "type": "health_claim",
                "severity": "BLOCK",
                "value": claim,
                "platform": "all",
                "message": f'Caption contains health claim: "{claim}" — prohibited by OCM and Meta',
            })

    return violations


def check_hashtags(hashtags, platform, rules):
    """Check hashtags against banned list. Returns list of violations."""
    violations = []

    banned = set()
    for p in [platform, "all"]:
        banned.update(h.lower() for h in rules.get("banned_hashtags", {}).get(p, []))

    for tag in hashtags:
        tag_clean = tag.strip().lower()
        if not tag_clean.startswith("#"):
            tag_clean = "#" + tag_clean

        if tag_clean in banned:
            violations.append({
                "type": "banned_hashtag",
                "severity": "BLOCK",
                "value": tag_clean,
                "platform": platform,
                "message": f'Hashtag {tag_clean} is banned/shadowban trigger on {platform}',
            })

        # Check for cannabis-adjacent patterns
        cannabis_patterns = [
            r'#.*cannabis', r'#.*weed', r'#.*marijuana', r'#.*420',
            r'#.*stoner', r'#.*kush', r'#.*ganja',
        ]
        for pattern in cannabis_patterns:
            if re.search(pattern, tag_clean) and tag_clean not in banned:
                violations.append({
                    "type": "banned_hashtag",
                    "severity": "WARN",
                    "value": tag_clean,
                    "platform": platform,
                    "message": f'Hashtag {tag_clean} contains cannabis-adjacent pattern — review',
                })

    return violations


def check_pricing(caption):
    """Check for pricing language in caption."""
    violations = []
    # Dollar amounts
    if re.search(r'\$\d+', caption):
        violations.append({
            "type": "pricing",
            "severity": "BLOCK",
            "value": re.findall(r'\$\d+[\.\d]*', caption),
            "platform": "instagram",
            "message": "Caption contains dollar amounts — prohibited on Instagram",
        })
    return violations


def check_potency(caption):
    """Check for THC/potency percentages."""
    violations = []
    if re.search(r'\d+\s*%\s*(thc|cbd|cannabinoid)', caption, re.IGNORECASE):
        violations.append({
            "type": "potency",
            "severity": "BLOCK",
            "value": re.findall(r'\d+\s*%\s*\w+', caption, re.IGNORECASE),
            "platform": "all",
            "message": "Caption contains potency percentages — prohibited",
        })
    if re.search(r'\d+\s*mg', caption, re.IGNORECASE):
        violations.append({
            "type": "potency",
            "severity": "BLOCK",
            "value": re.findall(r'\d+\s*mg', caption, re.IGNORECASE),
            "platform": "all",
            "message": "Caption contains milligram dosage — prohibited on Instagram",
        })
    return violations


def run_compliance_check(caption, hashtags, platform):
    """Run full compliance check. Returns structured result."""
    # Try Supabase first, fall back to local
    raw_rules = load_rules_from_supabase()
    if raw_rules:
        rules = parse_supabase_rules(raw_rules)
        source = "supabase"
    else:
        rules = load_rules_local()
        source = "local_fallback"

    all_violations = []
    all_violations.extend(check_caption(caption, platform, rules))
    all_violations.extend(check_hashtags(hashtags, platform, rules))
    all_violations.extend(check_pricing(caption))
    all_violations.extend(check_potency(caption))

    blocks = [v for v in all_violations if v["severity"] == "BLOCK"]
    warns = [v for v in all_violations if v["severity"] == "WARN"]

    if blocks:
        status = "FAIL"
        exit_code = 1
    elif warns:
        status = "WARN"
        exit_code = 2
    else:
        status = "PASS"
        exit_code = 0

    result = {
        "status": status,
        "platform": platform,
        "rules_source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "blocks": len(blocks),
        "warnings": len(warns),
        "violations": all_violations,
        "caption_preview": caption[:100] + "..." if len(caption) > 100 else caption,
        "hashtag_count": len(hashtags),
        "gate_question": (
            "If someone who knows nothing about cannabis saw this, "
            "would they just see a sick NYC lifestyle brand?"
        ),
    }

    return result, exit_code


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Pablo Fresh Content Compliance Checker"
    )
    parser.add_argument(
        "--platform", required=True, choices=["instagram", "x", "email"],
        help="Target platform"
    )
    parser.add_argument("--caption", help="Caption text to check")
    parser.add_argument("--caption-file", help="Read caption from file")
    parser.add_argument(
        "--hashtags", default="",
        help='Space or comma separated hashtags, e.g. "#nyc #flavor"'
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Get caption
    if args.caption_file:
        with open(args.caption_file) as f:
            caption = f.read().strip()
    elif args.caption:
        caption = args.caption
    else:
        print("Error: provide --caption or --caption-file", file=sys.stderr)
        sys.exit(1)

    # Parse hashtags
    hashtag_str = args.hashtags.replace(",", " ")
    hashtags = [h.strip() for h in hashtag_str.split() if h.strip()]

    # Run check
    result, exit_code = run_compliance_check(caption, hashtags, args.platform)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}")
        print(f"  PABLO FRESH COMPLIANCE CHECK — {result['status']}")
        print(f"{'='*60}")
        print(f"  Platform:  {args.platform}")
        print(f"  Rules:     {result['rules_source']}")
        print(f"  Blocks:    {result['blocks']}")
        print(f"  Warnings:  {result['warnings']}")
        print(f"{'='*60}")

        if result["violations"]:
            for v in result["violations"]:
                icon = "X" if v["severity"] == "BLOCK" else "!"
                print(f"  [{icon}] {v['message']}")
            print()

        if exit_code == 0:
            print("  PASS — Content is platform-compliant.")
            print(f'\n  Final gate: "{result["gate_question"]}"')
        elif exit_code == 2:
            print("  WARN — Review flagged items before posting.")
            print(f'\n  Final gate: "{result["gate_question"]}"')
        else:
            print("  FAIL — Content has blocking violations. Do not post.")

        print()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
