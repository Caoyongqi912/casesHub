# @Time : 2022/7/5 21:11 
# @Author : cyq
# @File : projectConfig.py 
# @Software: PyCharm
# @Desc: 项目配置类


class ProjectConfig:
    pass


class DevelopmentConfig(ProjectConfig):
    pass


class TestingConfig(ProjectConfig):
    pass


class ProductionConfig(ProjectConfig):
    pass


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "pro": ProjectConfig,
    "default": DevelopmentConfig
}
