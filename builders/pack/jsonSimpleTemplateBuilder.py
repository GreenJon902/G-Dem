from typing import Iterable

from builders import Builder
from builders.builder import BuiltFile

parameter_set_separator = "\n---\n"


def replace_all(strings: Iterable[str], replace_info: dict[str, str]):
    for string in strings:
        for replacee, replacer in replace_info.items():
            string = string.replace(replacee, replacer)
        yield string


class JsonSimpleTemplateBuilder(Builder):
    @classmethod
    def build(cls, path: str, data: str) -> list[BuiltFile]:
        # Separate the input file into the path, template, and parameter sets
        output_path_format, output_contents_format, *string_parameter_sets = data.split(parameter_set_separator)

        # Use the template on each set of parameters and return
        for string_parameter_set in string_parameter_sets:
            parameter_set = {"{" + part[0] + "}": part[1] for part in
                             (line.split("=", 1) for line in string_parameter_set.split("\n"))}
            yield BuiltFile(*replace_all((output_path_format, output_contents_format), parameter_set))

