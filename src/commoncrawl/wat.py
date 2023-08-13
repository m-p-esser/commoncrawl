""" Data Processing for WAT files """

from warcio.recordloader import ArcWarcRecord


def is_wat_json_record(record: ArcWarcRecord):
    """Return true if WARC record is a WAT record"""
    return record.rec_type == "metadata" and record.content_type == "application/json"


def get_payload_stream(record: ArcWarcRecord):
    """Get Payload as stream from record"""
    return record.content_stream()


def get_links(wat_record: dict) -> list:
    """Extract links which are URLs and HTML anchors, XPaths etc"""

    links = []

    try:
        http_response_meta = wat_record["Envelope"]["Payload-Metadata"][
            "HTTP-Response-Metadata"
        ]
        html_response_meta = http_response_meta["HTML-Metadata"]

        if "Links" in html_response_meta:
            l = html_response_meta["Links"]
            l = [i["url"] for i in l]
            links.extend(l)

        if "Head" in html_response_meta:
            pass  # Add logic here

    except KeyError:
        print(
            f"Payload for HTML Metadata is empty. Entity-Length: {http_response_meta['Entity-Length']}"
        )

    finally:
        return links
