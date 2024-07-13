from builders.builder import Builder
from builders.pack.jsonTemplateBuilder import JsonTemplateBuilder
from builders.pack.packTemplateWebsiteBuilder import PackTemplateWebsiteBuilder
from builders.website.homeBuilder import HomeBuilder
from builders.website.rulesBuilder import RulesBuilder

# A dict of all builder names to those actual builders
builders: dict[str, type[Builder]] = {
    "RulesBuilder": RulesBuilder,
    "HomeBuilder": HomeBuilder,
    "JsonTemplateBuilder": JsonTemplateBuilder,
    "PackTemplateWebsiteBuilder": PackTemplateWebsiteBuilder
}
