#!/usr/bin/env python3
"""Time Format Conversion

This module defines functions that convert time from Unix format to
Timestamp and vice versa.
"""
import pandas as pd


def ts_to_unix(ts):
    """
    Convert String of Time or pd.Timestamp to Unix.

    Parameters
    ----------
    ts : str/pd.Timestamp
        String of Time. e.g. "1970-01-01"

    Returns
    -------
    int
        Epoch (Unix) Time in Seconds

    """
    if isinstance(ts, str):
        ts = pd.Timestamp(ts)

    return (ts - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')


def unix_to_ts(tu):
    """
    Convert Unix to Pd.Timestamp.

    Parameters
    ----------
    tu : int/str
        Epoch (Unix) Time in Seconds. e.g. "1597795200"
        
    Returns
    -------
    pd.Timestamp
        Time.

    """
    if isinstance(tu, str):
        tu = int(tu)

    return pd.Timestamp(tu, unit='s')


def remove_tz(ts):
    """
    Remove Timezone components of a Time String.

    Parameters
    ----------
    ts : str
        String of Time with Timezone.

    Returns
    -------
    str
        String of Time without Timezone.

    """
    return ts.replace('T', ' ').replace('Z', '')


def date_to_str(ts):
    """
    Convert timestamps into strings with format '%Y-%m-%d %H:%M:%S'.

    Parameters
    ----------
    ts : pd.timestamp
        Timestamp.

    Returns
    -------
    str
        Strings with format '%Y-%m-%d %H:%M:%S'.

    """
    return ts.strftime('%Y-%m-%d %H:%M:%S')
