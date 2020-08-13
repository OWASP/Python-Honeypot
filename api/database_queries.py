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

top_ip_dests_groupby = {
    "$group":
        {
            "_id":
                {
                    "ip_dest": "$ip_dest",
                    "country_ip_dest": "$country_ip_dest"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}

sort_by_count = {
    "$sort": SON(
        [
            ("count", -1)
        ]
    )
}

sort_by_count_and_id = {
    "$sort":
        SON(
            [
                ("count", -1),
                ("_id", -1)
            ]
        )
}

top_port_dests_groupby = {
    "$group":
        {
            "_id":
                {
                    "port_dest": "$port_dest",
                    "country_ip_dest": "$country_ip_dest",
                },
            "count":
                {
                    "$sum": 1
                }
        }
}

top_machine_names_groupby = {
    "$group":
        {
            "_id":
                {
                    "machine_name": "$machine_name"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}

top_countries_groupby = {
    "$group":
        {
            "_id": "$country_ip_dest",
            "count":
                {
                    "$sum": 1
                }
        }
}

group_by_ip_dest = {
    "$group":
        {
            "_id": {
                "ip_dest": "$ip_dest"
            },
            "count": {
                "$sum": 1
            }
        }
}

group_by_ip_dest_and_username = {
    "$group":
        {
            "_id":
                {
                    "ip_dest": "$ip_dest",
                    "username": "$username",
                    "module_name": "$module_name"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}

group_by_ip_dest_and_password = {
    "$group":
        {
            "_id":
                {
                    "ip_dest": "$ip_dest",
                    "password": "$password",
                    "module_name": "$module_name"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}


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
