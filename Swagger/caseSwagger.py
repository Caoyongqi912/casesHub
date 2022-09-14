from typing import List, Dict, Any

from pydantic import BaseModel, Field

from Enums import CaseTag, CaseLevel, CaseType


class CaseSwagger(BaseModel):
    title: str = Field(description="标题")
    desc: str = Field(description="注释")
    setup: str = Field(description="前置")
    tag: CaseTag = Field(description="标签")
    case_level: CaseLevel = Field(description="等级")
    case_type: CaseType = Field(description="类型")
    platformID: int = Field(description="所属平台ID")
    projectID: int = Field(description="项目ID")
    partID: int = Field(description="所属模块ID")
    versionID: int = Field(description="所属版本ID")
    info: List[Dict[str, Any]] = Field(description="用例步骤")
