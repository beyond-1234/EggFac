# coding:utf-8
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator)



class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = "zh"
    CHINESE_TRADITIONAL = "hk"
    ENGLISH = "en"
    AUTO = "Auto"


class Config(QConfig):
    """ Config of application """

    # folders
    outputFolder = ConfigItem(
        "Folders", "Output", "app/output", FolderValidator())

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), EnumSerializer(Language), restart=True)

    # Material
    blurRadius  = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = 2023
AUTHOR = "beyond_1234"
VERSION = "v0.0.1"
REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"


cfg = Config()
qconfig.load('app/config/config.json', cfg)
