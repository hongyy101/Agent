from pydantic import BaseModel,Field

class WeatherInput(BaseModel):
    city:str = Field(description="城市名，如'北京'、'上海'", max_length=20, min_length=2)

class WeatherOutput(BaseModel):
    city:str = Field(description="城市名")
    condition:str = Field(description="天气状况，如晴、雨")
    temperature_c:int = Field(description="温度，摄氏度")
    humidity_pct:int = Field(description="百分比")

class SearchInput(BaseModel):
    query:str = Field(min_length=1, description="搜索关键词")
    max_result:int = Field(default=2, ge=1, le=5, description="返回结果数量，1-5")

class SearchResultItem(BaseModel):
    title:str = Field(description="标题")
    snippet:str = Field(description="查询结果片段")

class SearchOutput(BaseModel):
    total:int = Field(description="结果总记录数")
    query:str = Field(description="用户查询的内容")
    results : list[SearchResultItem]
