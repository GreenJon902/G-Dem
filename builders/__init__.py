from builders.builder import Builder
from builders.pack.craftingTemplateBuilder import CraftingTemplateBuilder
from builders.website.homeBuilder import HomeBuilder
from builders.website.rulesBuilder import RulesBuilder

# A dict of all builder names to those actual builders
builders: dict[str, type[Builder]] = {
    "RulesBuilder": RulesBuilder,
    "HomeBuilder": HomeBuilder,
    "CraftingTemplateBuilder": CraftingTemplateBuilder
}
