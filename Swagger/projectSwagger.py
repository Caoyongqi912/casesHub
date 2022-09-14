from pydantic import BaseModel, Field


class AddProjectSwagger(BaseModel):
    name: str = Field(description="项目名称")
    desc: str = Field(description="项目描述", required=False)
    adminID: int = Field(description="管理员ID")


class PageSwagger(BaseModel):
    pageSize: str = Field(description="数")
    current: str = Field(description="页")
    sort: str = Field(description="排序字段")


class UpdateProjectSwagger(BaseModel):
    id: int = Field(description="project ID")
    name: str = Field(description="项目名称")
    desc: str = Field(description="项目描述", required=False)


class DeleteProjectSwagger(BaseModel):
    id: int = Field(description="project ID")