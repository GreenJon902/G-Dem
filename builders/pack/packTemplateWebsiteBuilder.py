import itertools
import json
import os.path

from builders.builder import BuiltFile
from builders.pack.jsonTemplateBuilder import JsonTemplateBuilder, section_separator
from builders.website.rulesBuilder import pre_rules, rule_start, rule_end, RulesBuilder, post_rules


class PackTemplateWebsiteBuilder(JsonTemplateBuilder):
    previous_htmls: dict[str, str] = {}
    previous_numbers: dict[str, int] = {}

    @classmethod
    def build(cls, path: str, data: str) -> list[BuiltFile]:
        # Get our extra data from it, and make a new entry if this html_path doesn't already exist
        website_action, html_path, name, data = data.split(section_separator, 3)
        if html_path not in cls.previous_htmls:
            cls.previous_htmls[html_path] = pre_rules.replace("{0}", "Datapack")
            cls.previous_numbers[html_path] = 1

        # Build all the separate json files
        built_files = list(super().build(path, data))

        # Now to build the next part of the site, it is easiest for me to just overwrite the last version every time
        # that we get a new pack template to build. (Yes I apologise for how dum this is)
        # We also just use the rules page because it has everything we need - the dropdowns

        # Set the id to the name of the buildme file add start the rule construction
        id_ = os.path.basename(path)
        cls.previous_htmls[html_path] += rule_start.format(id_, cls.previous_numbers[html_path], name)

        if website_action == "render":
            # For this one we are going to create crafting grids for each BuiltFile

            for built_file in built_files:
                # Get a title
                title = "<b>" + os.path.basename(built_file.file_path) + "</b>:"
                cls.previous_htmls[html_path] += RulesBuilder.write_rule_lines((title,))

                # Parse the crafting recipe
                recipe = json.loads(built_file.file_contents)

                # Then render it depending on its type
                if recipe['type'] == "minecraft:crafting_shapeless":
                    # For this we just write the ingredients, their amounts and the output (+amount)

                    # Get just names as strings in list
                    raw_ingredient_names = list(map(lambda x: x["item"], recipe['ingredients']))

                    ingredient_counts = ({  # Map the ingredient name to the count of it. set(r.i.n) so unique
                        ingredient: raw_ingredient_names.count(ingredient) for ingredient in set(raw_ingredient_names)})

                    # Create ingredients string
                    text = "\t"
                    for ingredient, count in ingredient_counts.items():
                        text += ingredient.replace("_", " ").title()
                        text += f" x{count}"
                        text += ", "
                    text = text.rstrip(", ")  # Remove last ", "

                    # Add output
                    text += " => "
                    text += recipe["result"]["id"].replace("_", " ").title()
                    text += f" x{recipe['result']['count']}"

                    cls.previous_htmls[html_path] += RulesBuilder.write_rule_lines((text,))

                elif recipe['type'] == "minecraft:crafting_shaped":
                    # For this we write the pattern, then the result in the middle (second) line. Then write the key
                    # underneath

                    # Write pattern and result
                    text = "\t"
                    for i, line in enumerate(recipe["pattern"]):
                        text += line
                        if i == 1:  # If second line then write result too
                            text += " => "
                            text += recipe["result"]["id"].replace("_", " ").title()
                            text += f" x{recipe['result']['count']}"
                        text += "\n\t"

                    # Write key
                    for key_name, value_json in recipe["key"].items():
                        text += key_name + " = " + value_json["item"].replace("_", " ").title()
                        text += ", "
                    text = text.rstrip(", ")

                    cls.previous_htmls[html_path] += RulesBuilder.write_rule_lines(text.split("\n"))

                else:
                    # In this case just log that we don't know what it is and paste the json in?
                    print(f"PackTemplateWebsiteBuilder does not support {recipe['type']}, pasting JSON instead")

                    # Replace 4 spaces with tabs so indentation works, then split into lines and run the rule function
                    json_lines = built_file.file_contents.replace(" "*4, "\t").split("\n")
                    cls.previous_htmls[html_path] += RulesBuilder.write_rule_lines(json_lines)

        elif website_action.startswith("replace "):
            replacement_text = website_action.removeprefix("replace ")

            # For this one we just use the replacement text as the only text
            cls.previous_htmls[html_path] += RulesBuilder.write_rule_lines(replacement_text.split("\\n"))
        else:
            raise ValueError("PackTemplateWebsiteBuilder expected \"render\" or \"replace ...\", not \"",
                             website_action, "\"")

        # Increment the number and add the ending
        cls.previous_numbers[html_path] += 1
        cls.previous_htmls[html_path] += rule_end

        # Create the built file, with the ending html added
        built_files = list(itertools.chain(built_files, (BuiltFile(html_path, cls.previous_htmls[html_path] + post_rules),)))
        return built_files
