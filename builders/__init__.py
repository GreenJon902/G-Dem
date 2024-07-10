import os

from builders.builder import Builder
from builders.web.homeBuilder import HomeBuilder
from builders.web.rulesBuilder import RulesBuilder

builders: dict[str, type[Builder]] = {
    "RulesBuilder": RulesBuilder,
    "HomeBuilder": HomeBuilder
}
