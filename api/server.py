#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask, Response, abort, jsonify, render_template
from flask import request as flask_request

from api.database_queries import (group_by_ip_dest,
                                  group_by_ip_dest_and_password,
                                  group_by_ip_dest_and_username, sort_by_count,
                                  sort_by_count_and_id, top_countries_groupby,
                                  top_ip_dests_groupby,
                                  top_machine_names_groupby,
                                  top_port_dests_groupby,
                                  filter_by_date,
                                  filter_by_skip,
                                  filter_by_limit,
                                  filter_by_country_ip_dest,
                                  filter_by_module_name,
                                  filter_by_exclude_unknown_country,
                                  filter_by_match)
from api.utility import (aggregate_function, all_mime_types, fix_date,
                         fix_limit, fix_skip, flask_null_array_response,
                         msg_structure, root_dir)
from config import api_configuration
from core.alert import write_to_api_console
from core.get_modules import load_all_modules
from database import connector

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
    except IOError:
        abort(404)


def get_value_from_request(_key):
    """
    get a value from GET, POST or CCOKIES

    Args:
        _key: the value name to find

    Returns:
        the value content if found otherwise None
    """
    try:
        value = flask_request.args[_key]
    except Exception:
        try:
            value = flask_request.form[_key]
        except Exception:
            try:
                value = flask_request.cookies[_key]
            except Exception:
                value = None
    if value:
        # todo: fix it later
        value = value.replace("\\\"", "\"").replace("\\\'", "\'")
    return value


def is_authorized():
    """
    check the validity of API key

    Returns:
        200 HTTP code if it's valid otherwise 401 error

    """
    api_access_key = app.config["OWASP_HONEYPOT_CONFIG"]["api_access_key"]

    key_from_request = get_value_from_request("key")

    if api_access_key is not None and api_access_key != key_from_request:
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
    check if IP filtering applied and API address is in whitelist also
    API Key is valid

    Returns:
        None or Abort(403) or Abort(401)
    """
    # IP Limitation
    white_list_enabled = app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list"]
    white_list_ips = app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list_ips"]
    api_access_without_key = app.config["OWASP_HONEYPOT_CONFIG"]["api_access_without_key"]

    if white_list_enabled:
        if flask_request.remote_addr not in white_list_ips:
            abort(403, "unauthorized IP")
    if not api_access_without_key:
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
                root_dir(),
                path
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
    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count_all_events_by_date": int(
                    connector.honeypot_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.honeypot_events.estimated_document_count()
                ) + int(
                    connector.network_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.network_events.estimated_document_count()
                ) + int(
                    connector.credential_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.credential_event.estimated_document_count()
                ) + int(
                    connector.file_change_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.file_change_events.count_documents()
                ),
                "date": date
            }
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/count-honeypot-events", methods=["GET"])
def count_honeypot_events():
    """
    Get total number of honeypot events

    Returns:
        JSON/Dict number of honeypot events
    """
    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count_honeypot_events_by_date":
                    connector.honeypot_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.honeypot_events.estimated_document_count(),
                "date": date
            }
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/count-network-events", methods=["GET"])
def count_network_events():
    """
    Get total number of network events

    Returns:
        JSON/Dict number of network events
    """
    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count_network_events_by_date":
                    connector.network_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.network_events.estimated_document_count(),
                "date": date
            }
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events-ips", methods=["GET"])
def top_ten_ips_in_honeypot_events():
    """
    get top ten repeated ips in honeypot events

    Returns:
        JSON/Dict top ten repeated ips in honeypot events
    """
    date = get_value_from_request("date")
    country_ip_dest = get_value_from_request("country_ip_dest")
    top_ips_query = [
        top_ip_dests_groupby,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]

    if country_ip_dest and date:
        match_by_country_and_date = filter_by_match(
            {
                **filter_by_country_ip_dest(country_ip_dest),
                **filter_by_date(date)
            }
        )
        top_ips_query.insert(0, match_by_country_and_date)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif country_ip_dest:
        match_by_country = filter_by_match(
            filter_by_country_ip_dest(country_ip_dest)
        )
        top_ips_query.insert(0, match_by_country)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
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
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/network-events-ips", methods=["GET"])
def top_ten_ips_in_network_events():
    """
    get top ten repeated ips in network events

    Returns:
        JSON/Dict top ten repeated ips in network events
    """
    date = get_value_from_request("date")
    country_ip_dest = get_value_from_request("country_ip_dest")
    top_ips_query = [
        top_ip_dests_groupby,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if country_ip_dest and date:
        match_by_country_and_date = filter_by_match(
            {
                **filter_by_country_ip_dest(country_ip_dest),
                **filter_by_date(date)
            }
        )
        top_ips_query.insert(0, match_by_country_and_date)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif country_ip_dest:
        match_by_country = filter_by_match(
            filter_by_country_ip_dest(country_ip_dest)
        )
        top_ips_query.insert(0, match_by_country)
        top_ips_query.insert(2, sort_by_count_and_id)

    elif date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
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
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events-ports", methods=["GET"])
def top_ten_ports_in_honeypot_events():
    """
    get top ten repeated ports in honeypot events

    Returns:
        JSON/Dict top ten repeated ports in honeypot events
    """
    date = get_value_from_request("date")
    country_ip_dest = get_value_from_request("country_ip_dest")
    top_ports_query = [
        top_port_dests_groupby,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if country_ip_dest and date:
        match_by_country_and_date = filter_by_match(
            {
                **filter_by_country_ip_dest(country_ip_dest),
                **filter_by_date(date)
            }
        )
        top_ports_query.insert(0, match_by_country_and_date)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif country_ip_dest:
        match_by_country = filter_by_match(
            filter_by_country_ip_dest(country_ip_dest)
        )
        top_ports_query.insert(0, match_by_country)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
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
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/network-events-ports", methods=["GET"])
def top_ten_ports_in_network_events():
    """
    get top ten repeated ports in network events

    Returns:
        JSON/Dict top ten repeated ports in network events
    """
    date = get_value_from_request("date")
    country_ip_dest = get_value_from_request("country_ip_dest")
    top_ports_query = [
        top_port_dests_groupby,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if country_ip_dest and date:
        match_by_country_and_date = filter_by_match(
            {
                **filter_by_country_ip_dest(country_ip_dest),
                **filter_by_date(date)
            }
        )
        top_ports_query.insert(0, match_by_country_and_date)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif country_ip_dest:
        match_by_country = filter_by_match(
            filter_by_country_ip_dest(country_ip_dest)
        )
        top_ports_query.insert(0, match_by_country)
        top_ports_query.insert(2, sort_by_count_and_id)
    elif date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
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
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events", methods=["GET"])
def get_honeypot_events():
    """
    get honeypot events

    Returns:
        an array contain honeypot events
    """
    date = get_value_from_request("date")
    if date:
        try:
            return jsonify(
                [
                    i for i in
                    connector.honeypot_events.find(
                        {
                            **filter_by_date(date)
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
        except Exception:
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
        except Exception:
            return flask_null_array_response()


@app.route("/api/events/network-events", methods=["GET"])
def get_network_events():
    """
    get network events

    Returns:
        an array contain network events
    """
    date = get_value_from_request("date")
    if date:
        try:
            return jsonify(
                [
                    i for i in
                    connector.network_events.find(
                        {
                            **filter_by_date(date)
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
        except Exception:
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
        except Exception:
            return flask_null_array_response()


@app.route("/api/events/get-events-data", methods=["GET"])
def get_events_data():
    """
    get events data

    Returns:
        an array contain event data
    """
    event_type = get_value_from_request("event_type")
    module_name = get_value_from_request("module_name")
    # todo: rename the variable
    start_date = fix_date(
        get_value_from_request("start_date")
    )
    end_date = fix_date(
        get_value_from_request("end_date")
    )

    if event_type == "honeypot-event":
        db_collection_name = connector.honeypot_events
    elif event_type == "network-event":
        db_collection_name = connector.network_events
    elif event_type == "credential-event":
        db_collection_name = connector.credential_events
    elif event_type == "ics-honeypot-event":
        db_collection_name = connector.events_data
    elif event_type == "file-change-event":
        db_collection_name = connector.file_change_events
    else:
        return flask_null_array_response()

    if start_date and end_date:
        try:
            query = {
                "$gte": start_date[0],
                "$lte": end_date[1]
                # todo: fix
                # **filter_by_date(date)
            }
            if module_name:
                query["module_name"] = module_name

            return jsonify(
                [
                    i for i in
                    db_collection_name.find(
                        query,
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
        except Exception:
            return flask_null_array_response()
    else:
        try:
            query = {}
            if module_name:
                query = filter_by_module_name(module_name)

            return jsonify(
                [
                    i for i in
                    db_collection_name.find(
                        query,
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
        except Exception:
            return flask_null_array_response()


@app.route("/api/events/honeypot-events-countries", methods=["GET"])
def top_ten_countries_in_honeypot_events():
    """
    get top ten repeated countries in honeypot events

    Returns:
        JSON/Dict top ten repeated countries honeypot in events
    """
    date = get_value_from_request("date")
    top_countries_query = [
        top_countries_groupby,
        sort_by_count,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if date:
        match_by_date_and_country = {
            **filter_by_match(filter_by_exclude_unknown_country()),
            **filter_by_date(date)
        }
        top_countries_query.insert(0, match_by_date_and_country)
    else:
        match_by_country = filter_by_match(
            filter_by_exclude_unknown_country()
        )
        top_countries_query.insert(0, match_by_country)
    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_countries_query
            )
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/network-events-countries", methods=["GET"])
def top_ten_countries_in_network_events():
    """
    get top ten repeated countries in network events

    Returns:
        JSON/Dict top ten repeated countries in network events
    """
    date = get_value_from_request("date")
    top_countries_query = [
        top_countries_groupby,
        sort_by_count,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if date:
        match_by_date_and_country = filter_by_match(
            {
                **filter_by_exclude_unknown_country(),
                **filter_by_date(date)
            }
        )
        top_countries_query.insert(0, match_by_date_and_country)
    else:
        match_by_country = filter_by_match(
            filter_by_exclude_unknown_country()
        )
        top_countries_query.insert(0, match_by_country)
    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_countries_query
            )
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/network-events-machinenames", methods=["GET"])
def top_network_machine_names():
    """
    get top network machine names in network events

    Returns:
        JSON/Dict top network machine names in network events
    """
    date = get_value_from_request("date")
    top_machinenames_query = [
        top_machine_names_groupby,
        sort_by_count_and_id,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
        top_machinenames_query.insert(0, match_by_date)
    try:
        return jsonify(
            aggregate_function(
                connector.network_events,
                top_machinenames_query
            )
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/honeypot-events-machinenames", methods=["GET"])
def top_honeypot_machine_names():
    """
    get top honeypot machine names in honeypot events

    Returns:
        JSON/Dict top honeypot machine names
    """
    date = get_value_from_request("date")
    top_machinenames_query = [
        top_machine_names_groupby,
        sort_by_count_and_id,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if date:
        match_by_date = filter_by_match(
            filter_by_date(date)
        )
        top_machinenames_query.insert(0, match_by_date)
    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events,
                top_machinenames_query
            )
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/module-events", methods=["GET"])
def module_events():
    """
    Get total number of credential events according to module

    Returns:
        JSON/Dict of credential events according to module
    """
    module_name = get_value_from_request("module_name")
    module_query = [
        group_by_ip_dest,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if module_name:
        module_query.insert(
            0,
            filter_by_match(
                filter_by_module_name(module_name)
            )
        )
    try:
        return jsonify(
            aggregate_function(connector.credential_events, module_query)
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/most-usernames-used", methods=["GET"])
def top_usernames_used():
    """
    Get top usernames used according to module

    Returns:
        JSON/Dict of top usernames used
    """
    module_name = get_value_from_request("module_name")
    module_query = [
        group_by_ip_dest_and_username,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if module_name:
        module_query.insert(
            0,
            filter_by_match(
                filter_by_module_name(module_name)
            )
        )
    try:
        return jsonify(
            aggregate_function(connector.credential_events, module_query)
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/most-passwords-used", methods=["GET"])
def top_passwords_used():
    """
    Get top passwords used according to module

    Returns:
        JSON/Dict of top passwords used
    """
    module_name = get_value_from_request("module_name")
    module_query = [
        group_by_ip_dest_and_password,
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit"))
    ]
    if module_name:
        module_query.insert(
            0,
            filter_by_match(
                filter_by_module_name(module_name)
            )
        )
    try:
        return jsonify(
            aggregate_function(connector.credential_events, module_query)
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/module-names", methods=["GET"])
def all_module_names():
    """
    Get top passwords used according to module

    Returns:
        JSON/Dict of top passwords used
    """
    module_names = load_all_modules()
    try:
        return jsonify(
            {
                "module_names": module_names
            }
        ), 200
    except Exception:
        return flask_null_array_response()


def start_api_server():
    """
    start API server

    Returns:
        True
    """
    # Starting the API
    my_api_configuration = api_configuration()
    api_access_key = my_api_configuration["api_access_key"]
    api_access_without_key = my_api_configuration["api_access_without_key"]

    write_to_api_console(
        " * API access key: {0}\n".format(
            api_access_key if not api_access_without_key else "NOT REQUIRED!"
        )
    )

    app.config["OWASP_HONEYPOT_CONFIG"] = {
        "api_access_key": api_access_key,
        "api_client_white_list": my_api_configuration["api_client_white_list"]["enabled"],
        "api_client_white_list_ips": my_api_configuration["api_client_white_list"]["ips"],
        "api_access_log": my_api_configuration["api_access_log"]["enabled"],
        "api_access_log_filename": my_api_configuration["api_access_log"]["filename"],
        "api_access_without_key": api_access_without_key,
        "language": "en"
    }
    app.run(
        host=my_api_configuration["api_host"],
        port=my_api_configuration["api_port"],
        debug=my_api_configuration["api_debug_mode"],
        threaded=True
    )
    return True
