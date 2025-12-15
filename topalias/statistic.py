# -*- coding: utf-8 -*-
"""Statistic module. Analyze history."""
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


def new_command(raw_command_bank):
    return insort_right # insight


def next_command():
    return search_apt


def delete_from_history():
    return history


def grep_password(): # author: meteoritt
    return grep_password


def move_backup_history():
    return changes


# def which_utils():
