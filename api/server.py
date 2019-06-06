#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import render_template
from flask import Response
from flask import abort
from flask import request as flask_request
from flask import jsonify
from config import api_configuration
from core.alert import write_to_api_console
from database import connector
from api.database_queries import top_ips_groupby
from api.database_queries import top_machine_names_groupby
from api.database_queries import top_ports_groupby
from api.database_queries import top_countries_groupby
from api.database_queries import sort_by_count
from api.database_queries import sort_by_count_and_id
from api.utility import msg_structure
from api.utility import all_mime_types
from api.utility import root_dir
from api.utility import fix_date
from api.utility import fix_limit
from api.utility import fix_skip
from api.utility import flask_null_array_response
from api.utility import aggregate_function

template_dir = os.path.join(
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "web"
    ),
    "static"
)
app = Flask(
    __name__,
    template_folder=template_dir
)
app.config.from_object(
    __name__
)


def get_file(filename):
    """
    open the requested file in HTTP requests

    Args:
        filename: path and the filename

    Returns:
        content of the file or abort(404)
    """
    try:
        src = os.path.join(root_dir(), filename)
        return open(src, 'rb').read()
    except IOError as _:
        abort(404)


def get_value_from_request(_key):
    """
    get a value from GET, POST or CCOKIES

    Args:
        _key: the value name to find

    Returns:
        the value content if found otherwise None
    """
    global flask_request
    try:
        key = flask_request.args[_key]
    except Exception as _:
        try:
            key = flask_request.form[_key]
        except Exception as _:
            try:
                key = flask_request.cookies[_key]
            except Exception as _:
                key = None
    if key:
        # todo: fix it later
        key = key.replace("\\\"", "\"").replace("\\\'", "\'")
    return key


def is_authorized():
    """
    check the validity of API key

    Returns:
        200 HTTP code if it's valid otherwise 401 error

    """
    global app
    if app.config["OWASP_HONEYPOT_CONFIG"]["api_access_key"] is not None \
            and app.config["OWASP_HONEYPOT_CONFIG"]["api_access_key"] != get_value_from_request("key"):
        abort(401, "invalid API key")
    return True


@app.errorhandler(400)
def error_400(error):
    """
    handle the 400 HTTP error

    Args:
        error: the flask error

    Returns:
        400 JSON error
    """
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 400


@app.errorhandler(401)
def error_401(error):
    """
    handle the 401 HTTP error

    Args:
        error: the flask error

    Returns:
        401 JSON error
    """
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 401


@app.errorhandler(403)
def error_403(error):
    """
    handle the 403 HTTP error

    Args:
        error: the flask error

    Returns:
        403 JSON error
    """
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 403


@app.errorhandler(404)
def error_404(error):
    """
    handle the 404 HTTP error

    Args:
        error: the flask error

    Returns:
        404 JSON error
    """
    del error
    return jsonify(
        msg_structure(status="error", msg="file/path not found!")
    ), 404


@app.before_request
def authorization_check():
    """
    check if IP filtering applied and API address is in whitelist also API Key is valid

    Returns:
        None or Abort(403) or Abort(401)
    """
    # IP Limitation
    if app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list"]:
        if flask_request.remote_addr not in app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list_ips"]:
            abort(403, "unauthorized IP")
    if not app.config["OWASP_HONEYPOT_CONFIG"]["api_access_without_key"]:
        is_authorized()
    return


@app.route("/", methods=["GET", "POST"])
def index():
    """
    index page for WebUI

    Returns:
        rendered HTML page
    """
    return render_template("index.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def get_static_files(path):
    """
    getting static files and return content mime types

    Args:
        path: path and filename

    Returns:
        file content and content type if file found otherwise abort(404)
    """
    static_types = all_mime_types()
    return Response(
        get_file(
            os.path.join(
                root_dir(), path
            )
        ),
        mimetype=static_types.get(
            os.path.splitext(path)[1],
            "text/html"
        )
    )


@app.route("/api/events/count-all-events", methods=["GET"])
def count_all_events():
    """
    Get total number of events

    Returns:
        JSON/Dict number of all events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    if date:
        try:
            return jsonify(
                {
                    "count_all_events_by_date":
                        connector.honeypot_events.count_documents(
                            {
                                "date": {
                                    "$gte": date[0],
                                    "$lte": date[1]
                                }
                            }
                        ) + connector.network_events.count_documents(
                            {
                                "date": {
                                    "$gte": date[0],
                                    "$lte": date[1]
                                }
                            }
                        ),
                    "date": date
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()
    else:
        try:
            return jsonify(
                {
                    "count_all_events": (
                            connector.honeypot_events.estimated_document_count() +
                            connector.network_events.estimated_document_count()
                    )
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()


@app.route("/api/events/count-honeypot-events", methods=["GET"])
def count_honeypot_events():
    """
    Get total number of honeypot events

    Returns:
        JSON/Dict number of honeypot events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    if date:
        try:
            return jsonify(
                {
                    "count_honeypot_events_by_date": connector.honeypot_events.count_documents(
                        {
                            "date": {
                                "$gte": date[0],
                                "$lte": date[1]
                            }
                        }
                    ),
                    "date": date
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()
    else:
        try:
            return jsonify(
                {
                    "count_honeypot_events": connector.honeypot_events.estimated_document_count()
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()


@app.route("/api/events/count-network-events", methods=["GET"])
def count_network_events():
    """
    Get total number of network events

    Returns:
        JSON/Dict number of network events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    if date:
        try:
            return jsonify(
                {
                    "count_network_events_by_date": connector.network_events.count_documents(
                        {
                            "date":
                                {
                                    "$gte": date[0],
                                    "$lte": date[1]
                                }
                        }
                    ),
                    "date": date
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()
    else:
        try:
            return jsonify(
                {
                    "count_network_events": connector.network_events.estimated_document_count()
                }
            ), 200
        except Exception as _:
            return flask_null_array_response()


@app.route("/api/events/honeypot-events-ips", methods=["GET"])
def top_ten_ips_in_honeypot_events():
    """
    get top ten repeated ips in honeypot events

    Returns:
        JSON/Dict top ten repeated ips in honeypot events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    country = get_value_from_request("country")
    top_ips_query = [
        top_ips_groupby,
        {
            "$skip": fix_skip(get_value_from_request("skip"))
        },
        {
            "$limit": fix_limit(get_value_from_request("limit"))
        }
    ]

    if country and date:
        match_by_country_and_date = {
            "$match": {
                "country": country,
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_ips_query.insert(0, match_by_country_and_date)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif country:
        match_by_country = {

            "$match": {
                "country": country
            }
        }
        top_ips_query.insert(0, match_by_country)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif date:
        match_by_date = {
            "$match": {
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_ips_query.insert(0, match_by_date)
        top_ips_query.insert(2, sort_by_count)

    else:
        top_ips_query.insert(1, sort_by_count)

    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_ips_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/network-events-ips", methods=["GET"])
def top_ten_ips_in_network_events():
    """
    get top ten repeated ips in network events

    Returns:
        JSON/Dict top ten repeated ips in network events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    country = get_value_from_request("country")
    top_ips_query = [
        top_ips_groupby,
        {
            "$skip": fix_skip(
                get_value_from_request("skip")
            )
        },
        {
            "$limit": fix_limit(
                get_value_from_request("limit")
            )
        }
    ]
    if country and date:
        match_by_country_and_date = {
            "$match": {
                "country": country,
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_ips_query.insert(0, match_by_country_and_date)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif country:
        match_by_country = {
            "$match": {
                "country": country
            }
        }
        top_ips_query.insert(0, match_by_country)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif date:
        match_by_date = {
            "$match": {
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_ips_query.insert(0, match_by_date)
        top_ips_query.insert(2, sort_by_count)

    else:
        top_ips_query.insert(1, sort_by_count)

    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_ips_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events-ports", methods=["GET"])
def top_ten_ports_in_honeypot_events():
    """
    get top ten repeated ports in honeypot events

    Returns:
        JSON/Dict top ten repeated ports in honeypot events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    country = get_value_from_request("country")
    top_ports_query = [
        top_ports_groupby,
        {
            "$skip": fix_skip(get_value_from_request("skip"))
        },
        {
            "$limit": fix_limit(get_value_from_request("limit"))
        }
    ]
    if country and date:
        match_by_country_and_date = {
            "$match":
                {
                    "country": country,
                    "date": {
                        "$gte": date[0],
                        "$lte": date[1]
                    }
                }
        }
        top_ports_query.insert(0, match_by_country_and_date)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif country:
        match_by_country = {
            "$match":
                {
                    "country": country,
                }
        }
        top_ports_query.insert(0, match_by_country)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif date:
        match_by_date = {
            "$match": {
                "date":
                    {
                        "$gte": date[0],
                        "$lte": date[1]
                    }
            }
        }
        top_ports_query.insert(0, match_by_date)
        top_ports_query.insert(2, sort_by_count)
    else:
        top_ports_query.insert(1, sort_by_count)
    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_ports_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/network-events-ports", methods=["GET"])
def top_ten_ports_in_network_events():
    """
    get top ten repeated ports in network events

    Returns:
        JSON/Dict top ten repeated ports in network events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    country = get_value_from_request("country")
    top_ports_query = [
        top_ports_groupby,
        {
            "$skip": fix_skip(get_value_from_request("skip"))
        },
        {
            "$limit": fix_limit(get_value_from_request("limit"))
        }
    ]
    if country and date:
        match_by_country_and_date = {
            "$match":
                {
                    "country": country,
                    "date": {
                        "$gte": date[0],
                        "$lte": date[1]
                    }
                }
        }
        top_ports_query.insert(0, match_by_country_and_date)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif country:
        match_by_country = {
            "$match":
                {
                    "country": country,
                }
        }
        top_ports_query.insert(0, match_by_country)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif date:
        match_by_date = {
            "$match": {
                "date":
                    {
                        "$gte": date[0],
                        "$lte": date[1]
                    }
            }
        }
        top_ports_query.insert(0, match_by_date)
        top_ports_query.insert(2, sort_by_count)
    else:
        top_ports_query.insert(1, sort_by_count)
    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_ports_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events", methods=["GET"])
def get_honeypot_events():
    """
    get honeypot events

    Returns:
        an array contain honeypot events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    if date:
        try:
            return jsonify(
                [
                    i for i in
                    connector.honeypot_events.find(
                        {
                            "date":
                                {
                                    "$gte": date[0],
                                    "$lte": date[1]
                                }
                        },
                        {
                            "_id": 0
                        }
                    ).skip(
                        fix_skip(
                            get_value_from_request("skip")
                        )
                    ).limit(
                        fix_limit(
                            get_value_from_request("limit")
                        )
                    )
                ]
            ), 200
        except Exception as _:
            return flask_null_array_response()
    else:
        try:
            return jsonify(
                [
                    i for i in
                    connector.honeypot_events.find(
                        {},
                        {
                            "_id": 0
                        }
                    ).skip(
                        fix_skip(
                            get_value_from_request("skip")
                        )
                    ).limit(
                        fix_limit(
                            get_value_from_request("limit")
                        )
                    )
                ]
            ), 200
        except Exception as _:
            return flask_null_array_response()


@app.route("/api/events/network-events", methods=["GET"])
def get_network_events():
    """
    get network events

    Returns:
        an array contain network events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    if date:
        try:
            return jsonify(
                [
                    i for i in
                    connector.network_events.find(
                        {
                            "date":
                                {
                                    "$gte": date[0],
                                    "$lte": date[1]
                                }
                        },
                        {
                            "_id": 0
                        }
                    ).skip(
                        fix_skip(
                            get_value_from_request("skip")
                        )
                    ).limit(
                        fix_limit(
                            get_value_from_request("limit")
                        )
                    )
                ]
            ), 200
        except Exception as _:
            return flask_null_array_response()
    else:
        try:
            return jsonify(
                [
                    i for i in
                    connector.network_events.find(
                        {},
                        {
                            "_id": 0
                        }
                    ).skip(
                        fix_skip(
                            get_value_from_request("skip")
                        )
                    ).limit(
                        fix_limit(
                            get_value_from_request("limit")
                        )
                    )
                ]
            ), 200
        except Exception as _:
            return flask_null_array_response()


@app.route("/api/events/honeypot-events-countries", methods=["GET"])
def top_ten_countries_in_honeypot_events():
    """
    get top ten repeated countries in honeypot events

    Returns:
        JSON/Dict top ten repeated countries honeypot in events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    top_countries_query = [
        top_countries_groupby,
        sort_by_count,
        {
            "$skip": fix_skip(
                get_value_from_request("skip")
            )
        },
        {
            "$limit": fix_limit(
                get_value_from_request("limit")
            )
        }
    ]
    if date:
        match_by_date_and_country = {
            "$match":
                {
                    "country": {
                        "$gt": "-"
                    },
                    "date":
                        {
                            "$gte": date[0],
                            "$lte": date[1]
                        }
                }
        }
        top_countries_query.insert(0, match_by_date_and_country)
    else:
        match_by_country = {
            "$match":
                {
                    "country": {
                        "$gt": "-"
                    }
                }
        }
        top_countries_query.insert(0, match_by_country)
    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_countries_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/network-events-countries", methods=["GET"])
def top_ten_countries_in_network_events():
    """
    get top ten repeated countries in network events

    Returns:
        JSON/Dict top ten repeated countries in network events
    """
    date = fix_date(
        get_value_from_request("date")
    )
    top_countries_query = [
        top_countries_groupby,
        sort_by_count,
        {
            "$skip": fix_skip(
                get_value_from_request("skip")
            )
        },
        {
            "$limit": fix_limit(
                get_value_from_request("limit")
            )
        }
    ]
    if date:
        match_by_date_and_country = {
            "$match":
                {
                    "country": {
                        "$gt": "-"
                    },
                    "date":
                        {
                            "$gte": date[0],
                            "$lte": date[1]
                        }
                }
        }
        top_countries_query.insert(0, match_by_date_and_country)
    else:
        match_by_country = {
            "$match":
                {
                    "country": {
                        "$gt": "-"
                    }
                }
        }
        top_countries_query.insert(0, match_by_country)
    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_countries_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/network-events-machinenames", methods=["GET"])
def top_network_machine_names():
    """
    get top network machine names in network events

    Returns:
        JSON/Dict top network machine names in network events
    """
    date = fix_date(
        get_value_from_request("date")
    )

    top_machinenames_query = [
        top_machine_names_groupby,
        sort_by_count_and_id,
        {
            "$skip": fix_skip(
                get_value_from_request("skip")
            )
        },
        {
            "$limit": fix_limit(
                get_value_from_request("limit")
            )
        }
    ]
    if date:
        match_by_date = {
            "$match": {
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_machinenames_query.insert(0, match_by_date)
    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_machinenames_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events-machinenames", methods=["GET"])
def top_honeypot_machine_names():
    """
    get top honeypot machine names in honeypot events

    Returns:
        JSON/Dict top honeypot machine names
    """
    date = fix_date(
        get_value_from_request("date")
    )
    top_machinenames_query = [
        top_machine_names_groupby,
        sort_by_count_and_id,
        {
            "$skip": fix_skip(
                get_value_from_request("skip")
            )
        },
        {
            "$limit": fix_limit(
                get_value_from_request("limit")
            )
        }
    ]
    if date:
        match_by_date = {
            "$match": {
                "date": {
                    "$gte": date[0],
                    "$lte": date[1]
                }
            }
        }
        top_machinenames_query.insert(0, match_by_date)
    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_machinenames_query
            )
        ), 200
    except Exception as _:
        return flask_null_array_response()


def start_api_server():
    """
    start API server

    Returns:
        True
    """
    # Starting the API
    my_api_configuration = api_configuration()
    write_to_api_console(
        " * API access key: {0}\n".format(
            my_api_configuration["api_access_key"] if not my_api_configuration["api_access_without_key"]
            else "NOT REQUIRED!"
        )
    )
    global app
    app.config["OWASP_HONEYPOT_CONFIG"] = {
        "api_access_key": my_api_configuration["api_access_key"],
        "api_client_white_list": my_api_configuration["api_client_white_list"]["enabled"],
        "api_client_white_list_ips": my_api_configuration["api_client_white_list"]["ips"],
        "api_access_log": my_api_configuration["api_access_log"]["enabled"],
        "api_access_log_filename": my_api_configuration["api_access_log"]["filename"],
        "api_access_without_key": my_api_configuration["api_access_without_key"],
        "language": "en"
    }
    app.run(
        host=my_api_configuration["api_host"],
        port=my_api_configuration["api_port"],
        debug=my_api_configuration["api_debug_mode"],
        threaded=True
    )
    return True
