import math
from typing import Iterable

from builders import Builder
from builders.builder import BuiltFile

section_separator = "\n---\n"
parameterization_set_separator = "\n--\n"
parameterization_separator = "\n-\n"


def replace_all(strings: Iterable[str], replace_info: dict[str, str]):
    for string in strings:
        for replacee, replacer in replace_info.items():
            string = string.replace(replacee, replacer)
        yield string


class JsonTemplateBuilder(Builder):
    @classmethod
    def build(cls, path: str, data: str) -> list[BuiltFile]:
        # Separate the input file into the path, template, and parameterization sets
        output_path_format, output_contents_format, string_parameterization_sets = data.split(section_separator)

        # Then for each parameterization_set, we need to extract each parameter
        parameterization_sets: list[list[dict[str, str]]] = []
        for string_parameterization_set in string_parameterization_sets.split(parameterization_set_separator):
            new_set = []
            for string_parameterization in string_parameterization_set.split(parameterization_separator):
                # Now split the lines of "<key>=<value>" into a dict mapping "{<key>}" to "<value>"
                new_set.append({"{" + part[0] + "}": part[1] for part in
                                (line.split("=", 1) for line in string_parameterization.split("\n"))})
            parameterization_sets.append(new_set)

        # Now as the doc says, we need to choose one dict from each of the lists in parameterization_sets
        # To do this we can assign each possible combination a number, and then extract that combination using % and //
        for i in range(math.prod(map(len, parameterization_sets))):  # So loop for the product of the lengths of the lists
            replacement_information_of_selected_sets = {}
            for parameterization_set in parameterization_sets:
                # So now for each set, we figure out which set to use and add the replacement information to the dict
                replacement_information_of_selected_sets.update(parameterization_set[i % len(parameterization_set)])
                # and then divide i accordingly
                i //= len(parameterization_set)  # This could probably be a normal divide but double slash is more fun

            # Now use those parameters on the template and return the BuiltFile
            yield BuiltFile(*replace_all((output_path_format, output_contents_format),
                                         replacement_information_of_selected_sets))

