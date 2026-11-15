# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Tasks."""

from csv import DictReader
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory
from typing import cast
from zipfile import ZipFile

from celery import shared_task
from invenio_access.permissions import system_identity
from invenio_app.helpers import obj_or_import_string
from invenio_records_marc21.services.record import create_record
from invenio_records_marc21.services.record.metadata import Marc21Metadata

from ..proxies import current_catalogue_marc21


def build_data_from_csv_row(row: dict, mapper_cls: type) -> tuple[Marc21Metadata, str]:
    """Build data from csv row.

    columns: id,doi,filename,title,year,authors
    """
    record = Marc21Metadata()
    convertor = mapper_cls(record)
    convertor.convert(row, record)
    return record, convertor.filename


def import_from_csv(pid: str, mapper_cls: str) -> None:
    """Import from csv."""
    records_service = current_catalogue_marc21.records_service
    files_service = current_catalogue_marc21.draft_files_service
    files = files_service.list_files(system_identity, pid)

    data_objs = []
    archive: ZipFile | None = None
    mapper_cls = obj_or_import_string(mapper_cls)

    for file_ in files.entries:
        # improve naming
        file__ = files_service.get_file_content(system_identity, pid, file_["key"])
        match file_["mimetype"]:
            case "text/csv":
                with file__.open_stream("r") as fp:
                    reader = DictReader(fp)
                    data_objs = [
                        build_data_from_csv_row(row, mapper_cls) for row in reader
                    ]
            case "application/zip":
                zip_fp = file__.get_stream("rb")
                archive = ZipFile(zip_fp)

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for metadata, filename in data_objs:
            file_path = temp_path / Path(filename).name

            # TODO: catch possible wrong mapping!
            with (
                cast(ZipFile, archive).open(filename, "r") as src,
                file_path.open("wb") as dst,
            ):
                copyfileobj(src, dst)

            data = metadata.json

            data["catalogue"] = {
                "root": pid,
                "parent": pid,
                "children": [],
            }

            create_record(
                service=records_service,
                data=data,
                file_paths=[file_path],
                identity=system_identity,
                do_publish=False,  # True: should that really be true?
            )

            # this frees the disk space, good for large zip files
            file_path.unlink()


@shared_task
def import_task(pid: str, mapper_cls: str, params: dict[str, str]) -> None:
    """Process."""
    # TODO: check how to use params as dict[str, str] in the resource config
    match params["type"]:
        case ["csv"]:
            import_from_csv(pid, mapper_cls)
