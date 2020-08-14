#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is to be used to store all the queries which are being used
for querying mongodb using pymongo.

Created this file because the queries are repeated over the URI's.
"""
from bson.son import SON
from api.utility import (fix_date,
                         fix_limit,
                         fix_skip)

sort_by_count = {
    "$sort": SON(
        [
            ("count", -1)
        ]
    )
}

group_by_elements = {
    "ip": {
        "$group":
            {
                "_id": {
                    "ip_dest": "$ip_dest"
                },
                "count": {
                    "$sum": 1
                }
            }
    },
    "country": {
        "$group":
            {
                "_id": "$country_ip_dest",
                "count": {
                    "$sum": 1
                }
            }
    },
    "port": {
        "$group":
            {
                "_id": "$port_dest",
                "count": {
                    "$sum": 1
                }
            }
    },
    "module_name": {
        "$group":
            {
                "_id": "$module_name",
                "count": {
                    "$sum": 1
                }
            }
    },
    "username": {
        "$group":
            {
                "_id": "$username",
                "count": {
                    "$sum": 1
                }
            }
    },
    "password": {
        "$group":
            {
                "_id": "$password",
                "count": {
                    "$sum": 1
                }
            }
    },
    "machine_name": {
        "$group":
            {
                "_id": "$machine_name",
                "count": {
                    "$sum": 1
                }
            }
    }
}

event_types = [
    "all",
    "honeypot",
    "network",
    "credential",
    "file"
]


def filter_by_date(date):
    date = fix_date(date)
    return {
        "date": {
            "$gte": date[0],
            "$lte": date[1]
        }
    }


def filter_by_skip(skip):
    return {
        "$skip": fix_skip(skip)
    }


def filter_by_limit(limit):
    return {
        "$limit": fix_limit(limit)
    }


def filter_by_country_ip_dest(country):
    return {
        "country_ip_dest": country
    }


def filter_by_module_name(module_name):
    return {
        'module_name': module_name
    }


# todo: not used?
def filter_by_exclude_unknown_country():
    return {
        "country_ip_dest": {
            "$gt": "-"
        }
    }


def filter_by_match(match_query):
    return {
        "$match": match_query
    }
