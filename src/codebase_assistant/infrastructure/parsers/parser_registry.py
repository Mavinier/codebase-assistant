from collections.abc import Mapping
from types import MappingProxyType

from codebase_assistant.domain.interfaces.parser import Parser as ParserProtocol
from codebase_assistant.domain.value_objects.source_format import SourceFormat


class ParserRegistry:
    def __init__(self, parsers: Mapping[SourceFormat, ParserProtocol]):
        self._parsers = MappingProxyType(dict(parsers))

    def get_parser(self, source_format: SourceFormat) -> ParserProtocol:
        try:
            return self._parsers[source_format]
        except KeyError as ex:
            raise KeyError(f"Not available parser for: {source_format}") from ex
