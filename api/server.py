#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import (Flask,
                   Response,
                   abort,
                   jsonify,
                   render_template)
from flask import request as flask_request
from api.database_queries import (sort_by_count,
                                  filter_by_date,
                                  filter_by_skip,
                                  filter_by_limit,
                                  filter_by_country_ip_dest,
                                  filter_by_module_name,
                                  filter_by_match,
                                  event_types,
                                  group_by_elements)
from api.utility import (aggregate_function,
                         all_mime_types,
                         fix_limit,
                         fix_skip,
                         flask_null_array_response,
                         msg_structure,
                         root_dir)
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


@app.route("/api/events/count/<event_type>", methods=["GET"])
def count_events(event_type):
    """
    Get total number of events

    Returns:
        JSON/Dict number of all events
    """
    abort(404) if event_type not in event_types else event_type

    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count": int(
                    int(
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
                        ) if date else connector.credential_events.estimated_document_count()
                    ) + int(
                        connector.file_change_events.count_documents(
                            {
                                **filter_by_date(date)
                            }
                        ) if date else connector.file_change_events.estimated_document_count()
                    )
                ) if event_type == "all" else int(
                    connector.honeypot_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.honeypot_events.estimated_document_count()
                ) if event_type == "honeypot" else int(
                    connector.network_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.network_events.estimated_document_count()
                ) if event_type == "network" else int(
                    connector.credential_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.credential_events.estimated_document_count()
                ) if event_type == "credential" else int(
                    connector.file_change_events.count_documents(
                        {
                            **filter_by_date(date)
                        }
                    ) if date else connector.file_change_events.estimated_document_count()
                ) if event_type == "file" else abort(404),
                "date": date
            }
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/count/groupby/<event_type>/<element>", methods=["GET"])
def groupby_element(event_type, element):
    """
    get top ten repeated ips in honeypot events

    Returns:
        JSON/Dict top ten repeated ips in honeypot events
    """
    abort(404) if event_type not in event_types[1:-1] else event_type

    date = get_value_from_request("date")
    country_ip_dest = get_value_from_request("country_ip_dest")
    top_ips_query = [
        group_by_elements[element],
        filter_by_skip(get_value_from_request("skip")),
        filter_by_limit(get_value_from_request("limit")),
        sort_by_count
    ]

    top_ips_query.insert(
        0,
        filter_by_match(
            {
                **filter_by_country_ip_dest(country_ip_dest),
                **filter_by_date(date)
            }
        ) if country_ip_dest and date else filter_by_match(
            filter_by_country_ip_dest(country_ip_dest)
        ) if country_ip_dest else filter_by_match(
            filter_by_date(date)
        ) if date else {}
    )

    try:
        return jsonify(
            aggregate_function(
                connector.honeypot_events if event_types == "honeypot" else connector.network_events if
                event_type == "network" else connector.credential_events,
                top_ips_query
            )
        ), 200
    except Exception:
        return flask_null_array_response()


@app.route("/api/events/explore/<event_type>", methods=["GET"])
def get_events_data(event_type):
    """
    get events data

    Returns:
        an array contain event data
    """
    abort(404) if event_type not in event_types else event_type

    module_name = get_value_from_request("module_name")
    date = get_value_from_request("date")

    if event_type == "honeypot":
        db_collection_name = connector.honeypot_events
    elif event_type == "network":
        db_collection_name = connector.network_events
    elif event_type == "credential":
        db_collection_name = connector.credential_events
    elif event_type == "file":
        db_collection_name = connector.file_change_events
    elif event_type == "data":
        db_collection_name = connector.data_events
    else:
        abort(404)

    try:
        query = filter_by_date(date) if date else {}
        query.update(filter_by_module_name(module_name) if module_name else {})

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


@app.route("/api/core/list/modules", methods=["GET"])
def all_module_names():
    """
    Get top passwords used according to module

    Returns:
        JSON/Dict of top passwords used
    """
    try:
        return jsonify(
            load_all_modules()
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
