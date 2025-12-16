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


def grep_password(command_bank):  # author: meteoritt
    """Search for sensitive data or password patterns in command history

    Args:
        command_bank: List of commands from history

    Returns:
        List of tuples (command, pattern_matched) containing sensitive commands
    """
    sensitive_patterns = [
        # Password patterns
        (r'password\s*[=:]\s*\S+', 'password assignment'),
        (r'passwd\s*[=:]\s*\S+', 'passwd assignment'),
        (r'pwd\s*[=:]\s*\S+', 'pwd assignment'),
        (r'--password\s+[\'"\S]+', 'password flag'),
        (r'--passwd\s+[\'"\S]+', 'passwd flag'),
        (r'-p\s+[\'"\S]+', 'password short flag'),
        (r'pass\s*[=:]\s*\S+', 'pass assignment'),

        # API keys and tokens
        (r'api[_-]?key\s*[=:]\s*[\'"\S]+', 'API key'),
        (r'apikey\s*[=:]\s*[\'"\S]+', 'API key'),
        (r'access[_-]?token\s*[=:]\s*[\'"\S]+', 'access token'),
        (r'secret[_-]?key\s*[=:]\s*[\'"\S]+', 'secret key'),
        (r'auth[_-]?token\s*[=:]\s*[\'"\S]+', 'auth token'),
        (r'bearer\s+[\'"\S]+', 'bearer token'),

        # Database connections
        (r'mysql\s+.*-p[\'"\S]+', 'MySQL password'),
        (r'psql\s+.*password[\'"\S]+', 'PostgreSQL password'),
        (r'mongodb://\S+@', 'MongoDB connection'),
        (r'postgres://\S+@', 'PostgreSQL connection'),
        (r'mysql://\S+@', 'MySQL connection'),

        # SSH and keys
        (r'ssh\s+-i\s+[\'"\S]+\.(pem|key|ppk)', 'SSH key file'),
        (r'sshpass\s+-p\s+[\'"\S]+', 'sshpass password'),

        # AWS and cloud credentials
        (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*[\'"\S]+', 'AWS secret key'),
        (r'aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*[\'"\S]+', 'AWS access key'),
        (r'AWS_SECRET_ACCESS_KEY\s*[=:]\s*[\'"\S]+', 'AWS secret env'),
        (r'AWS_ACCESS_KEY_ID\s*[=:]\s*[\'"\S]+', 'AWS access env'),

        # Environment variables with sensitive data
        (r'export\s+\w*PASS\w*\s*[=:]\s*[\'"\S]+', 'password export'),
        (r'export\s+\w*SECRET\w*\s*[=:]\s*[\'"\S]+', 'secret export'),
        (r'export\s+\w*KEY\w*\s*[=:]\s*[\'"\S]+', 'key export'),
        (r'export\s+\w*TOKEN\w*\s*[=:]\s*[\'"\S]+', 'token export'),

        # Git credentials
        (r'git\s+config\s+.*password', 'git password config'),
        (r'git\s+push\s+.*[\'"\S]+@[\'"\S]+', 'git push with credentials'),

        # Docker and container secrets
        (r'docker\s+login\s+.*-p\s+[\'"\S]+', 'docker login password'),
        (r'--password\s+[\'"\S]+.*docker', 'docker password'),
    ]

    sensitive_commands = []
    for command in command_bank:
        if not command or len(command.strip()) == 0:
            continue

        command_lower = command.lower()
        for pattern, pattern_name in sensitive_patterns:
            if re.search(pattern, command_lower, re.IGNORECASE):
                # Mask sensitive parts for display - mask values after =, :, or flags
                masked_command = re.sub(
                    r'(password|passwd|pwd|pass|key|token|secret)\s*[=:]\s*[\'"]?([^\'"\s]{3,})[\'"]?',
                    r'\1=****',
                    command,
                    flags=re.IGNORECASE
                )
                # Also mask flag values like -p value or --password value
                masked_command = re.sub(
                    r'(-[pP]|--password|--passwd)\s+[\'"]?([^\'"\s]{3,})[\'"]?',
                    r'\1 ****',
                    masked_command,
                    flags=re.IGNORECASE
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
