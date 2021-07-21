#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import (Flask,
                   Response,
                   abort,
                   jsonify,
                   render_template,
                   send_file)
from flask import request as flask_request
from api.database_queries import (
    filter_by_date,
    filter_by_module_name,
    filter_by_regex,
    event_types,
    group_by_elements,
    filter_by_element)
from api.utility import (
    all_mime_types,
    fix_limit,
    fix_skip,
    fix_filter_query,
    msg_structure,
    root_dir)
from config import api_configuration
from core.alert import write_to_api_console
from core.get_modules import load_all_modules
from database.connector import elasticsearch_events

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


@app.errorhandler(500)
def error_500(error):
    del error
    return jsonify(
        msg_structure(status="error", msg="something went wrong!")
    ), 500


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

    Eg. <API_URL>/api/events/count/honeypot/ip?date=2021-06-30

    Returns:
        JSON/Dict number of all events
    """
    abort(404) if event_type not in event_types else None

    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count": int(
                    elasticsearch_events.count(
                        index=event_types[event_type],
                        body=filter_by_date(date)
                    )['count']
                    if date else
                    elasticsearch_events.count(index=event_types[event_type])['count']
                ),
                "date": date
            } if event_type != "all" else {
                "count": sum(
                    [
                        int(
                            elasticsearch_events.count(
                                index=event_types[event],
                                body=filter_by_date(date)
                            )['count']
                            if date else
                            elasticsearch_events.count(index=event_types[event])['count']
                        )
                        for event in event_types if event != "all"
                    ]
                ),
                "date": date,
            }
        ), 200
    except Exception:
        abort(500)


@app.route("/api/events/count/groupby/<event_type>/<element>", methods=["GET"])
def groupby_element(event_type, element):
    """
    get top ten repeated "elements" as defined in database_queries
    in "event type".

    Eg. <API_URL>/api/events/count/groupby/honeypot/ip?date=2020-08-01

    Returns:
        JSON/Dict top ten element in event type
    """
    abort(404) if (event_type not in event_types or element not in group_by_elements) else True
    date = get_value_from_request("date")
    filter_by = get_value_from_request('filter_by')
    element_value = get_value_from_request(filter_by)
    conditions = [condition for condition in [
        filter_by_date(date)['query'],
        filter_by_element(filter_by, element_value)['query']
    ] if condition]
    query = {
        "query": {
            "bool": {
                "must": conditions
            }
        },
        "aggs": {
            "ips": {
                "terms": {
                    "field": element
                }
            }
        }
    }

    try:
        return jsonify(
            {
                record["key"]: record["doc_count"] for record in
                elasticsearch_events.search(index=event_types[event_type],
                                            body=query,
                                            size=0)["aggregations"]["ips"]["buckets"]
            }
        ), 200
    except Exception:
        abort(500)


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
    filter_by = get_value_from_request("filter")

    try:
        query = {
            "query": {
                "bool": {
                    "must": [
                        filter_by_date(date)['query']
                    ] if date else [],
                    "filter": []
                }
            }
        }
        if module_name:
            query['query']['bool']['must'].append(
                filter_by_module_name(module_name))
        if filter_by:
            for key in fix_filter_query(filter_by):
                filter_query = filter_by_regex(
                    key,
                    fix_filter_query(filter_by)[key]
                )
                query['query']['bool']['filter'].append(filter_query)
        records = []
        if get_value_from_request("limit") == "infinite":
            data = elasticsearch_events.search(
                index=event_types[event_type],
                body=query,
                scroll="2m",
                size=10000
            )
            scroll_id = data['_scroll_id']
            scroll_size = len(data['hits']['hits'])
            while scroll_size > 0:
                for record in data['hits']['hits']:
                    records.append(record['_source'])
                data = elasticsearch_events.scroll(scroll_id=scroll_id, scroll='2m')
                scroll_id = data['_scroll_id']
                scroll_size = len(data['hits']['hits'])
        else:
            records = [
                record['_source'] for record in elasticsearch_events.search(
                    index=event_types[event_type],
                    body=query,
                    from_=fix_skip(
                        get_value_from_request("skip")
                    ),
                    size=fix_limit(
                        get_value_from_request("limit")
                    )
                )['hits']['hits']
            ]
        return jsonify({
            "total": int(
                elasticsearch_events.count(
                    index=event_types[event_type],
                    body=query
                )['count']),
            "data": records
        }), 200
    except Exception:
        abort(500)


@app.route("/api/pcap/download", methods=["GET"])
def download_file():
    """
    Download PCAP files
    """
    try:
        md5_value = get_value_from_request("md5")
        abort(404) if not md5_value else md5_value

        fs = elasticsearch_events(index='ohp_file_archive').find_one(
            {
                "md5": md5_value
            }
        )

        return send_file(
            fs,
            attachment_filename=fs.filename,
            as_attachment=True,
            mimetype=fs.content_type
        ), 200

    except Exception:
        return abort(404)


@app.route("/api/core/list/modules", methods=["GET"])
def all_module_names():
    """
    Get the list of modules

    Returns:
        JSON/List of the modules
    """
    try:
        return jsonify(
            load_all_modules()
        ), 200
    except Exception:
        abort(500)


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
