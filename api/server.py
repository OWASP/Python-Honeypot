#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import binascii
import io
from flask import (Flask,
                   Response,
                   abort,
                   jsonify,
                   render_template,
                   send_file)
from flask import request as flask_request
from api.database_queries import (
    filter_by_date,
    filter_by_fields,
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
from config import (
    api_configuration,
    user_configuration)
from core.alert import write_to_api_console
from core.exit_helper import exit_failure
from core.get_modules import load_all_modules
from database.connector import elasticsearch_events
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from core.messages import load_messages

DOCS_URL = '/api/docs'
API_URL = 'http://localhost:5000/docs-configuration'

documentation_settings = get_swaggerui_blueprint(
    DOCS_URL,
    API_URL,
    config={
        'app_name': "Python Honeypot Api"
    },
)

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
    Get a value from GET, POST or COOKIES

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
    data = load_messages().message_contents
    return render_template("index.html", data=data, encoded_data=data)


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
    Get total number of events based on event type
    ---
    parameters:
        - in: path
          name: event_type
          schema:
            type: string
          required: true
          enum:
            - all
            - honeypot
            - network
            - credential
            - file
            - data
            - pcap
        - in: query
          name: date
          schema:
            type: date
          required: false
          description: Date to filter records for particular day
    responses:
        '200':
          description: Ok
          examples:
            application/json: { "count": 293879, "date": null}
        '404':
          description: Not Found
          examples:
            application/json: { "msg": "file/path not found!","status": "error"}
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
    Get top ten repeated "elements" as defined in database_queries in "event_type"
    ---
    parameters:
        - in: path
          name: event_type
          schema:
            type: string
          required: true
          enum:
            - honeypot
            - network
            - credential
            - file
            - data
            - pcap
        - in: path
          name: element
          schema:
            type: string
          required: true
          enum:
            - ip
            - country
            - port
            - module_name
            - username
            - password
            - machine_name
        - in: query
          name: date
          schema:
            type: date
          required: false
          description: Date to filter records for particular day
        - in: query
          name: country
          schema:
            type: string
          required: false
          description: used for filtering events by country
    responses:
        '200':
          description: Ok
          examples:
              application/json: [{"count":1703,"country":"DE"}]
        '404':
          description: Not Found
          examples:
            application/json: { "msg": "file/path not found!", "status": "error"}

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
    Get events data
    ---
    parameters:
        - in: path
          name: event_type
          schema:
            type: string
          required: true
          enum:
            - honeypot
            - network
            - credential
            - file
            - data
            - pcap
        - in: query
          name: date
          schema:
            type: date
          required: false
          description: Date to filter records for particular day
        - in: query
          name: module_name
          schema:
            type: string
          required: false
          enum:
            - ftp/strong_password
            - ftp/weak_password
            - http/basic_auth_strong_password
            - http/basic_auth_weak_password
            - ics/veeder_root_guardian_ast
            - smtp/strong_password
            - ssh/strong_password
            - ssh/weak_password
          description: one of the module names supported by the framework
        - in: query
          name: filter
          schema:
            type: string
          example: ip_dest=192.16.1.1&ip_src=192.168.0.*
          description: filter on serverside by query (regex)
          required: false
        - in: query
          name: skip
          schema:
            type: number
          example: 0
          description: skip the number of records from start
          required: false
        - in: query
          name: limit
          schema:
            type: number
          example: 100
          description: number of records to fetch
          required: false
    responses:
        '200':
          description: Ok
          examples:
              application/json:
                  {
                    "data": [
                        {
                          "country_ip_dest": "US",
                          "country_ip_src": "-",
                          "date": "2021-06-15 16:39:54",
                          "ip_dest": "142.250.183.131",
                          "ip_src": "192.168.0.106",
                          "machine_name": "stockholm_server_1",
                          "module_name": "http/basic_auth_strong_password",
                          "port_dest": 80,
                          "port_src": 59984,
                          "protocol": "TCP"
                        }
                    ],
                    "total": 614
                  }
        '404':
          description: Not Found
          examples:
            application/json: { "msg": "file/path not found!","status": "error"}
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
    ---
    parameters:
        - in: query
          name: md5
          schema:
            type: string
          required: true
          description: value of the PCAP file to download
          example: 282e14c5b89ff2af63f4146fbd0a6c68
    responses:
        '200':
          description: Ok
        '404':
          description: Not Found
          examples:
            application/json: { "msg": "file/path not found!","status": "error"}
    """
    try:
        md5_value = get_value_from_request("md5")
        abort(404) if not md5_value else md5_value

        fs = elasticsearch_events.search(
            index='ohp_file_archive',
            body=filter_by_fields(md5_value, ['md5'])
        )['hits']['hits'][0]['_source']
        return send_file(
            io.BytesIO(binascii.a2b_base64(fs['content'])),
            attachment_filename=fs['filename'],
            as_attachment=True,
            mimetype='application/cap'
        ), 200

    except Exception as e:
        print(e)
        return abort(404)


@app.route("/api/core/list/modules", methods=["GET"])
def all_module_names():
    """
    Get the list of modules
    ---
    responses:
        '200':
          description: Ok
          examples:
            application/json:
                [
                    "ftp/strong_password",
                    "ftp/weak_password",
                    "http/basic_auth_strong_password",
                    "http/basic_auth_weak_password",
                    "ics/veeder_root_guardian_ast",
                    "smtp/strong_password",
                    "ssh/strong_password",
                    "ssh/weak_password"
                ]
        '500':
          description: Internal Server Error
          examples:
            application/json: { "msg": "file/path not found!", "status": "error" }
    """
    try:
        return jsonify(
            load_all_modules()
        ), 200
    except Exception:
        abort(500)


@app.route("/docs-configuration")
def spec():
    """
    Get Api documentation in Open Api format
    """
    docs = swagger(app)
    docs['info']['version'] = "1.0"
    docs['info']['title'] = "Python Honeypot Api's"
    return jsonify(docs)


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
        **user_configuration()
    }
    app.register_blueprint(documentation_settings)

    try:
        app.run(
            host=my_api_configuration["api_host"],
            port=my_api_configuration["api_port"],
            debug=my_api_configuration["api_debug_mode"],
            threaded=True
        )
    except Exception as e:
        exit_failure(str(e))
    return True
