from unittest.mock import Mock

import pytest

import src.commoncrawl.wat as cc_wat  # Replace 'your_module_name' with the actual module name


@pytest.mark.parametrize(
    "rec_type, content_type",
    [
        ("metadata", "application/json"),
    ],
)
def test_is_wat_json_record_true(rec_type, content_type):
    # Mocking an ArcWarcRecord instance
    record = Mock()
    record.rec_type = rec_type
    record.content_type = content_type

    assert cc_wat.is_wat_json_record(record) == True


@pytest.mark.parametrize(
    "rec_type, content_type",
    [
        ("metadata", "text/html"),
        ("resource", "application/json"),
        ("resource", "text/html"),
    ],
)
def test_is_wat_json_record_false(rec_type, content_type):
    # Mocking an ArcWarcRecord instance
    record = Mock()
    record.rec_type = rec_type
    record.content_type = content_type

    assert cc_wat.is_wat_json_record(record) == False


def test_get_links_valid_input():
    wat_record = {
        "Envelope": {
            "Payload-Metadata": {
                "HTTP-Response-Metadata": {
                    "HTML-Metadata": {
                        "Links": [
                            {"url": "https://example.com"},
                            {"url": "https://example.org"},
                        ]
                    }
                }
            }
        }
    }
    expected_links = ["https://example.com", "https://example.org"]
    assert cc_wat.get_links(wat_record) == expected_links


def test_get_links_missing_keys():
    wat_record = {"Envelope": {"Payload-Metadata": {"HTTP-Response-Metadata": {}}}}
    # Since the required keys are missing, the function should return an empty list
    assert cc_wat.get_links(wat_record) == []


def test_get_links_empty_input():
    wat_record = {}
    # An empty input should also result in an empty list
    assert cc_wat.get_links(wat_record) == []


# Add more tests as needed, for example, to test the 'Head' logic once it's implemented
