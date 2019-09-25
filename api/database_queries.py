#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is to be used to store all the queries which are being used for querying mongodb using pymongo.
Created this file because the queries are repeated over the URI's.
"""
from bson.son import SON

top_ips_groupby = {
    "$group":
        {
            "_id":
                {
                    "ip": "$ip",
                    "country": "$country"
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

top_ports_groupby = {
    "$group":
        {
            "_id":
                {
                    "port": "$port",
                    "country": "$country",
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
            "_id": "$country",
            "count":
                {
                    "$sum": 1
                }
        }
}

group_by_ip = {
    "$group":
        {
            "_id": {
                "ip": "$ip"
            },
            "count": {
                "$sum": 1
            }
        }
}

group_by_ip_and_username = {
    "$group":
        {
            "_id":
                {
                    "ip": "$ip",
                    "username": "$username"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}

group_by_ip_and_password = {
    "$group":
        {
            "_id":
                {
                    "ip": "$ip",
                    "password": "$password"
                },
            "count":
                {
                    "$sum": 1
                }
        }
}
