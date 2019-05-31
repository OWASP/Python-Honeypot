"""
This file is to be used to store all the queries which are being used for querying mongodb using pymongo.
Created this file because the queries are repeated over the URI's.
"""
from bson.son import SON

top_ips_groupby={
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

sort_by_count={"$sort": SON([("count", -1)])}

sort_by_count_and_id={"$sort":
                          SON(
                              [("count", -1),
                               ("_id", -1)]
                          )}
