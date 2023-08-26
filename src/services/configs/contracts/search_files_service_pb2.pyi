from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SearchFilesRequest(_message.Message):
    __slots__ = ["file_to_search_pattern"]
    FILE_TO_SEARCH_PATTERN_FIELD_NUMBER: _ClassVar[int]
    file_to_search_pattern: str
    def __init__(self, file_to_search_pattern: _Optional[str] = ...) -> None: ...

class SearchFilesResponse(_message.Message):
    __slots__ = ["status_code", "files"]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, status_code: _Optional[int] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...
