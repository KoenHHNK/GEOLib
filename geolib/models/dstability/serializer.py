from abc import ABCMeta, abstractmethod
from io import BytesIO
from typing import get_args, get_origin
from zipfile import ZIP_DEFLATED, ZipFile

from pydantic import DirectoryPath, FilePath

from geolib.errors import NotConcreteError
from geolib.models.serializers import BaseSerializer
from geolib.models.utils import get_filtered_type_hints

from .internal import DStabilityStructure


class DStabilityBaseSerializer(BaseSerializer, metaclass=ABCMeta):
    """Serializer to folder/file structure."""

    ds: DStabilityStructure

    def serialize(self) -> dict:
        serialized_datastructure: dict = {}

        for field, fieldtype in get_filtered_type_hints(self.ds):
            # If fieldtype is a list[X], handle as a folder
            if get_origin(fieldtype) is list:
                element_type = get_args(fieldtype)[0]  # Extract element type

                folder = element_type.structure_group()
                serialized_datastructure[folder] = {}

                for i, data in enumerate(getattr(self.ds, field)):
                    suffix = f"_{i}" if i > 0 else ""
                    fn = f"{element_type.structure_name()}{suffix}.json"
                    serialized_datastructure[folder][fn] = data.model_dump_json(
                        indent=4
                    )

            # Otherwise it is a single .json in the root folder
            else:
                fn = f"{fieldtype.structure_name()}.json"
                serialized_datastructure[fn] = getattr(self.ds, field).model_dump_json(
                    indent=4
                )

        return serialized_datastructure

    @abstractmethod
    def write(self, path):
        raise NotConcreteError


class DStabilityInputSerializer(DStabilityBaseSerializer):
    def write(self, filepath: DirectoryPath) -> DirectoryPath:
        serialized_datastructure = self.serialize()

        for filename, data in serialized_datastructure.items():
            if isinstance(data, dict):
                folder = filepath / filename
                folder.mkdir(parents=True, exist_ok=True)

                for ffilename, fdata in data.items():
                    fn = folder / ffilename
                    with fn.open("wb") as io:
                        io.write(fdata.encode("utf-8"))
            else:
                fn = filepath / filename
                with fn.open("wb") as io:
                    io.write(data.encode("utf-8"))

        return filepath


class DStabilityInputZipSerializer(DStabilityBaseSerializer):
    """DStabilSerializer for zipped.stix files."""

    def write(self, filepath: FilePath | BytesIO) -> FilePath | BytesIO:
        with ZipFile(filepath, mode="w", compression=ZIP_DEFLATED) as zip:
            serialized_datastructure = self.serialize()

            for filename, data in serialized_datastructure.items():
                if isinstance(data, dict):
                    folder = filename
                    for ffilename, fdata in data.items():
                        if folder[-1] == "/":
                            fn = folder + ffilename
                        else:
                            fn = folder + "/" + ffilename
                        with zip.open(fn, "w") as io:
                            io.write(fdata.encode("utf-8"))
                else:
                    with zip.open(filename, "w") as io:
                        io.write(data.encode("utf-8"))

            for zfile in zip.filelist:
                zfile.create_system = 0

        return filepath
