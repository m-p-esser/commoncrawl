"""Flow to process WAT files"""

# import gzip
import json
import pathlib

# import requests
import warcio
from warcio.archiveiterator import ArchiveIterator

from commoncrawl.types import LinkCollection
from commoncrawl.wat import get_links, get_payload_stream, is_wat_json_record
from prefect import flow, get_run_logger, task
from prefect.task_runners import ConcurrentTaskRunner

# from io import BytesIO


# @task
# def construct_wat_path_gz_urls(url) -> list[str]:
#     """
#     Input: See See http://index.commoncrawl.org/collinfo.json
#     Example ouput url: `https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-23/wat.paths.gz`
#     """
#     logger = get_run_logger()

#     response = requests.get(url)
#     response.raise_for_status()
#     index_urls = response.json()

#     crawl_ids = [i["id"] for i in index_urls]

#     http_index_urls = []
#     for i in crawl_ids:
#         http_url = f"https://data.commoncrawl.org/crawl-data/{i}/wat.paths.gz"
#         http_index_urls.append(http_url)
#     logger.info(f"Constructed the following index urls: {http_index_urls}")

#     return http_index_urls


# @task
# def get_wat_path_gz_segments(url: str) -> list[str]:
#     """Get the WAT paths from the Common Crawl index server to actually download WAT files

#     Args:
#         url (str): The url of the WET paths gz file

#     Returns:
#         list[str]: A list of paths to the WET files
#     """
#     logger = get_run_logger()
#     logger.info(f"Getting WAT Path gz for url: {url}")

#     response = requests.get(url, stream=True)

#     response.raise_for_status()

#     # Decompress the file
#     bytes = response.content
#     bytes_buffer = BytesIO(bytes)
#     f = gzip.GzipFile(fileobj=bytes_buffer)

#     # Get the paths
#     paths_string = f.read().decode()
#     wat_path_gz_segments = paths_string.splitlines()

#     return wat_path_gz_segments


# @task
# def construct_wat_gz_download_urls(wat_path_gz_segment: list[str]):
#     wat_gz_download_urls = [
#         f"https://data.commoncrawl.org/{i}" for i in wat_path_gz_segment
#     ]

#     return wat_gz_download_urls


# @task
# def download_gz_file():
#     pass


@task
def process_record(record):
    """Process WAT file"""
    logger = get_run_logger()

    # Due to Prefect RuntimeError because validator for class can't be found
    if not isinstance(record, warcio.recordloader.ArcWarcRecord):
        raise TypeError(
            f"Expected argument to be of type `warcio.recordloader.ArcWarcRecord`, but got {type(record)} instead."
        )

    if is_wat_json_record(record):
        try:
            wat_record = json.loads(get_payload_stream(record).read())

            warc_header = wat_record["Envelope"]["WARC-Header-Metadata"]
            warc_target_uri = warc_header["WARC-Target-URI"]
            warc_record_id = warc_header["WARC-Record-ID"]

            links = get_links(wat_record)

            return LinkCollection(
                warc_record_id=warc_record_id,
                warc_target_uri=warc_target_uri,
                links=links,
            )

        except ValueError as e:
            logger.error(f"Failed to load JSON: {e}")
            logger.debug(f"Record Type: {record.rec_type}")
            logger.debug(f"Record Headers: {record.rec_headers}")
            logger.debug(record.content_stream().read().decode("utf-8"))
    else:
        logger.info("No WAT file. Not collecting any links")
        return LinkCollection(warc_record_id=None, warc_target_uri=None)


@flow(task_runner=ConcurrentTaskRunner)  # Main flow
def ingest_wat_files():
    """Process batch of WAT files"""
    logger = get_run_logger()

    total_link_count = 0  # Counter
    total_failed_records = 0  # Counter
    successful_records = []
    total_successful_records = 0  # Counter

    # # http_index_urls = construct_wat_path_gz_urls()
    # sample_url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-14/wat.paths.gz"
    # wat_path_gz_segments = get_wat_path_gz_segments(sample_url)
    # wat_gz_download_urls = construct_wat_gz_download_urls(wat_path_gz_segments)

    root_dir = pathlib.Path.cwd()
    data_dir = root_dir / "data"
    file_path_in = (
        data_dir / "00_raw" / "CC-MAIN-20230402105054-20230402135054-00799.warc.wat.gz"
    )

    with open(file_path_in, "rb") as f:
        archive_iterator = ArchiveIterator(f)
        record_counter = 0

        for record in archive_iterator:
            future = process_record.submit(record)
            link_collection = future.result(raise_on_failure=False)

            if future.get_state().is_completed():
                successful_records.append(link_collection)
                total_successful_records += 1
                total_link_count += link_collection.count_number_links()

            if future.get_state().is_failed():
                total_failed_records += 1

            record_counter += 1
            if record_counter > 8:
                break

    logger.info(f"Total Successful records: {total_successful_records}")
    logger.info(f"Total Failed records: {total_failed_records}")
    logger.info(f"Total Link count: {total_link_count}")

    logger.info(f"Sucessful records:")
    logger.info(successful_records)


if __name__ == "__main__":
    ingest_wat_files()
