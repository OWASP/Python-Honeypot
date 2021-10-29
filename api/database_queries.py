#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is to be used to store all the queries which are being used
for querying elasticsearch using elasticsearch client.

Created this file because the queries are repeated over the URI's.
"""
from api.utility import fix_date

sort_by_count = {
    "$sort": (
        [
            ("count", -1)
        ]
    )
}


def filter_by_element(filter_by, element_value):
    return {
        "query": {
            "multi_match": {
                "query": element_value,
                "fields": ['*']
            }
        }
    } if filter_by and element_value else {
        "query": {}
    }


group_by_elements = [
    "ip_dest",
    "ip_src",
    "country_ip_src",
    "country_ip_dest",
    "port_dest",
    "port_src",
    "protocol",
    "module_name",
    "machine_name",
    "username",
    "password",
    "is_directory",
    "split_timeout"
]

event_types = {
    "all": "*",
    "honeypot": 'honeypot_events',
    "network": 'network_events',
    "credential": 'credential_events',
    "file": 'file_change_events',
    "data": 'data_events',
    "pcap": 'ohp_file_archive'
}


def filter_by_date(date):
    date = fix_date(date)
    return {
        "query": {
            "range":
                {
                    "date": {
                        "gte": date[0],
                        "lte": date[1]
                    }
                }
        }
    } if date else {
        "query": {}
    }


def filter_by_fields(query, fields):
    return {
        'query': {
            'simple_query_string': {
                'query': query,
                'fields': fields
            }
        }
    }


def filter_by_module_name(module_name):
    return {
        "match": {
            "module_name": module_name
        }
    }


def filter_by_regex(field, regex):
    return {
        "regexp": {
            field: regex
        }
    }
