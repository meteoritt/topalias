# -*- coding: utf-8 -*-
"""Statistic module. Analyze history."""
import re
from bisect import insort_right
from collections import defaultdict


def top_command(command, limit) -> list:  # type: ignore
    """List top executed command from history"""
    counts = defaultdict(int)  # type: ignore
    for x in command:
        counts[x] += 1
    return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:limit]


def most_used_utils(raw_command_bank, limit=5, aliases=None) -> list:  # type: ignore
    """Return first utility from command usage statistic"""
    utility_bank = []
    if aliases is None:
        aliases = []
    for command in raw_command_bank:
        utility = command.split()[0]
        if aliases:
            if utility in aliases:
                utility_bank.append(utility)
        else:
            utility_bank.append(utility)

    utility_rank = top_command(utility_bank, limit)
    return utility_rank  # noqa: WPS331


def search_apt():
    """Search for apt-related commands in history"""
    pass


def grep_history():
    """Grep history for patterns"""
    pass


def history():
    """History operations"""
    pass


def changes():
    """Track changes in history"""
    pass


def new_command(raw_command_bank):
    """Return insort_right function for inserting commands in sorted order"""
    return insort_right


def next_command():
    """Return search_apt function"""
    return search_apt


def delete_from_history():
    """Return history function"""
    return history


_SENSITIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Password patterns
    (re.compile(r'password\s*[=:]\s*\S+', re.IGNORECASE), 'password assignment'),
    (re.compile(r'passwd\s*[=:]\s*\S+', re.IGNORECASE), 'passwd assignment'),
    (re.compile(r'pwd\s*[=:]\s*\S+', re.IGNORECASE), 'pwd assignment'),
    (re.compile(r'--password\s+[\'"\S]+', re.IGNORECASE), 'password flag'),
    (re.compile(r'--passwd\s+[\'"\S]+', re.IGNORECASE), 'passwd flag'),
    (re.compile(r'-p\s+[\'"\S]+', re.IGNORECASE), 'password short flag'),
    (re.compile(r'pass\s*[=:]\s*\S+', re.IGNORECASE), 'pass assignment'),

    # API keys and tokens
    (re.compile(r'api[_-]?key\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'API key'),
    (re.compile(r'apikey\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'API key'),
    (re.compile(r'access[_-]?token\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'access token'),
    (re.compile(r'secret[_-]?key\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'secret key'),
    (re.compile(r'auth[_-]?token\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'auth token'),
    (re.compile(r'bearer\s+[\'"\S]+', re.IGNORECASE), 'bearer token'),

    # Database connections
    (re.compile(r'mysql\s+.*-p[\'"\S]+', re.IGNORECASE), 'MySQL password'),
    (re.compile(r'psql\s+.*password[\'"\S]+', re.IGNORECASE), 'PostgreSQL password'),
    (re.compile(r'mongodb://\S+@', re.IGNORECASE), 'MongoDB connection'),
    (re.compile(r'postgres://\S+@', re.IGNORECASE), 'PostgreSQL connection'),
    (re.compile(r'mysql://\S+@', re.IGNORECASE), 'MySQL connection'),

    # SSH and keys
    (re.compile(r'ssh\s+-i\s+[\'"\S]+\.(pem|key|ppk)', re.IGNORECASE), 'SSH key file'),
    (re.compile(r'sshpass\s+-p\s+[\'"\S]+', re.IGNORECASE), 'sshpass password'),

    # AWS and cloud credentials
    (re.compile(r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'AWS secret key'),
    (re.compile(r'aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'AWS access key'),
    (re.compile(r'AWS_SECRET_ACCESS_KEY\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'AWS secret env'),
    (re.compile(r'AWS_ACCESS_KEY_ID\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'AWS access env'),

    # Environment variables with sensitive data
    (re.compile(r'export\s+\w*PASS\w*\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'password export'),
    (re.compile(r'export\s+\w*SECRET\w*\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'secret export'),
    (re.compile(r'export\s+\w*KEY\w*\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'key export'),
    (re.compile(r'export\s+\w*TOKEN\w*\s*[=:]\s*[\'"\S]+', re.IGNORECASE), 'token export'),

    # Git credentials
    (re.compile(r'git\s+config\s+.*password', re.IGNORECASE), 'git password config'),
    (re.compile(r'git\s+push\s+.*[\'"\S]+@[\'"\S]+', re.IGNORECASE), 'git push with credentials'),

    # Docker and container secrets
    (re.compile(r'docker\s+login\s+.*-p\s+[\'"\S]+', re.IGNORECASE), 'docker login password'),
    (re.compile(r'--password\s+[\'"\S]+.*docker', re.IGNORECASE), 'docker password'),
)


def grep_password(command_bank):  # author: meteoritt
    """Search for sensitive data or password patterns in command history

    Args:
        command_bank: List of commands from history

    Returns:
        List of tuples (command, pattern_matched) containing sensitive commands
    """
    sensitive_commands: list[tuple[str, str]] = []
    for command in command_bank:
        if not command or len(command.strip()) == 0:
            continue

        for pattern, pattern_name in _SENSITIVE_PATTERNS:
            if pattern.search(command):
                # Mask sensitive parts for display - mask values after =, :, or flags
                masked_command = re.sub(
                    r'(password|passwd|pwd|pass|key|token|secret)\s*[=:]\s*[\'"]?([^\'"\s]{3,})[\'"]?',
                    r'\1=****',
                    command,
                    flags=re.IGNORECASE,
                )
                # Also mask flag values like -p value or --password value
                masked_command = re.sub(
                    r'(-[pP]|--password|--passwd)\s+[\'"]?([^\'"\s]{3,})[\'"]?',
                    r'\1 ****',
                    masked_command,
                    flags=re.IGNORECASE,
                )
                sensitive_commands.append((masked_command, pattern_name))
                break  # Only match once per command

    return sensitive_commands


def move_backup_history():
    """Return changes function"""
    return changes


def which_utils():
    """Find which utilities are available"""
    pass
