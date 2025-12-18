"""
Chat相关的类型定义
兼容OpenAI SDK的类型结构
"""
from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息"""

    role: Literal["user", "assistant", "system"] = Field(
        description="消息角色：user-用户，assistant-助手，system-系统"
    )
    content: str = Field(description="消息内容")


class ChatCompletionRequest(BaseModel):
    """Chat completion请求参数"""

    model: Literal["yuanbao", "gemini"] = Field(
        default="yuanbao", description="模型类型：yuanbao(元宝) 或 gemini"
    )
    messages: List[ChatMessage] = Field(description="对话消息列表")
    image_url: Optional[str] = Field(default=None, description="图片URL（可选）")
    image_data: Optional[str] = Field(
        default=None, description="图片Base64数据（可选）"
    )
    deep_research: bool = Field(default=False, description="是否进行深度研究")
    generate_image: bool = Field(default=False, description="是否生成图片")

    class Config:
        # 允许使用驼峰命名和下划线命名
        populate_by_name = True


class Choice(BaseModel):
    """单个选择结果"""

    index: int = Field(description="选择索引")
    message: ChatMessage = Field(description="生成的消息")
    finish_reason: Optional[str] = Field(
        default=None, description="结束原因：stop, length等"
    )


class Usage(BaseModel):
    """Token使用统计"""

    prompt_tokens: int = Field(default=0, description="输入token数")
    completion_tokens: int = Field(default=0, description="输出token数")
    total_tokens: int = Field(default=0, description="总token数")


class ChatCompletion(BaseModel):
    """Chat completion响应"""

    id: str = Field(description="任务ID")
    object: str = Field(default="chat.completion", description="对象类型")
    created: int = Field(description="创建时间戳")
    model: str = Field(description="使用的模型")
    choices: List[Choice] = Field(description="生成的选择列表")
    usage: Optional[Usage] = Field(default=None, description="Token使用统计")
