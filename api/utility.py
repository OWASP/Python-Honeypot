#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def msg_structure(status="", msg=""):
    """
    basic JSON message structure

    Args:
        status: status (ok, failed)
        msg: the message content

    Returns:
        a JSON message
    """
    return {
        "status": status,
        "msg": msg
    }


def all_mime_types():
    """
    contains all mime types for HTTP request

    Returns:
        all mime types in json
    """
    return {
        ".aac": "audio/aac",
        ".abw": "application/x-abiword",
        ".arc": "application/octet-stream",
        ".avi": "video/x-msvideo",
        ".azw": "application/vnd.amazon.ebook",
        ".bin": "application/octet-stream",
        ".bz": "application/x-bzip",
        ".bz2": "application/x-bzip2",
        ".csh": "application/x-csh",
        ".css": "text/css",
        ".csv": "text/csv",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.\
                                        wordprocessingml.document",
        ".eot": "application/vnd.ms-fontobject",
        ".epub": "application/epub+zip",
        ".gif": "image/gif",
        ".htm": ".htm",
        ".html": "text/html",
        ".ico": "image/x-icon",
        ".ics": "text/calendar",
        ".jar": "application/java-archive",
        ".jpeg": ".jpeg",
        ".jpg": "image/jpeg",
        ".js": "application/javascript",
        ".json": "application/json",
        ".mid": ".mid",
        ".midi": "audio/midi",
        ".mpeg": "video/mpeg",
        ".mpkg": "application/vnd.apple.installer+xml",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".oga": "audio/ogg",
        ".ogv": "video/ogg",
        ".ogx": "application/ogg",
        ".otf": "font/otf",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.\
                                        presentationml.presentation",
        ".rar": "application/x-rar-compressed",
        ".rtf": "application/rtf",
        ".sh": "application/x-sh",
        ".svg": "image/svg+xml",
        ".swf": "application/x-shockwave-flash",
        ".tar": "application/x-tar",
        ".tif": ".tif",
        ".tiff": "image/tiff",
        ".ts": "application/typescript",
        ".ttf": "font/ttf",
        ".vsd": "application/vnd.visio",
        ".wav": "audio/x-wav",
        ".weba": "audio/webm",
        ".webm": "video/webm",
        ".webp": "image/webp",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".xhtml": "application/xhtml+xml",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.\
                                                spreadsheetml.sheet",
        ".xml": "application/xml",
        ".xul": "application/vnd.mozilla.xul+xml",
        ".zip": "application/zip",
        ".3gp": "video/3gpp",
        "audio/3gpp": "video",
        ".3g2": "video/3gpp2",
        "audio/3gpp2": "video",
        ".7z": "application/x-7z-compressed",
        ".pcap": "application/cap"
    }


def root_dir():
    """
    find the root directory for web static files

    Returns:
        root path for static files
    """
    return os.path.join(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "web"
        ),
        "static"
    )


def fix_date(date):
    """
    fix date value from user input

    Args:
        date: date value - user input

    Returns:
        an array with fixed date value or original date
    """
    if date:
        if date.count(":") == 2:
            return [
                date,
                "{0} 23:59:59".format(
                    date.rsplit()[0]
                )
            ]
        elif date.count("|") == 1 and date.count(":") == 4:
            return date.rsplit("|")
        elif date.count("|") == 1 and date.count(":") == 0:
            return [
                "{0} 00:00:00".format(
                    date.rsplit("|")[0]
                ),
                "{0} 23:59:59".format(
                    date.rsplit("|")[1]
                )
            ]
        else:
            return "{0} 00:00:00|{0} 23:59:59".format(date).rsplit("|")
    return date


def fix_limit(limit):
    """
    fix limit integer from user

    Args:
        limit: limit integer - default 10

    Returns:
        limit integer or 10
    """
    if limit:
        try:
            if int(limit) > 10000:
                return 10000
            return int(limit)
        except Exception:
            pass
    return 10


def fix_skip(skip):
    """
    fix skip integer from user

    Args:
        skip: skip integer - default 0

    Returns:
        skip integer or 0
    """
    if skip:
        try:
            return int(skip)
        except Exception:
            pass
    return 0


def fix_filter_query(filter):
    """
    fix filter query from user
    Args:
        filter: filter from users

    Returns:
        dict
    """
    if filter:
        try:
            filter = {
                _.split("=")[0]: _.split("=")[1] for _ in list(
                    set(
                        str(filter).split("&")
                    )
                )
            }
        except Exception:
            return {}
    return filter


def aggregate_function(data_connection, agr_query):
    """
    uses aggregate function of mongodb

    Args :
    data connection object on which to aggregate on
    aggregated query in a list

    Returns:
         the aggregated data in a list
    """
    return list(
        data_connection.aggregate(
            agr_query,
            allowDiskUse=True
        )
    )
