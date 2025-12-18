"""
AI SDK客户端测试
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_sdk import AIClient, AuthenticationError, InvalidRequestError, ChatMessage
from ai_sdk.types.chat import ChatCompletion, Choice


class TestAIClient:
    """AIClient测试类"""

    def test_client_init_with_params(self):
        """测试使用参数初始化客户端"""
        client = AIClient(
            api_token="test_token", base_url="http://test.com/api/v1", timeout=60
        )

        assert client.api_token == "test_token"
        assert client.base_url == "http://test.com/api/v1"
        assert client.timeout == 60
        client.close()

    def test_client_init_without_token(self):
        """测试没有token时抛出异常"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(AuthenticationError):
                AIClient()

    def test_client_init_without_base_url(self):
        """测试没有base_url时抛出异常"""
        with patch.dict("os.environ", {"AI_API_TOKEN": "test_token"}, clear=True):
            with pytest.raises(InvalidRequestError):
                AIClient()

    def test_context_manager(self):
        """测试上下文管理器"""
        with patch.dict(
            "os.environ",
            {
                "AI_API_TOKEN": "test_token",
                "AI_API_BASE_URL": "http://test.com/api/v1",
            },
        ):
            with AIClient() as client:
                assert client.api_token == "test_token"
                assert not client.session.closed
            # 退出上下文后，session应该被关闭

    @patch("ai_sdk.client.requests.Session")
    def test_chat_completions_create_validation(self, mock_session):
        """测试chat.completions.create参数验证"""
        with patch.dict(
            "os.environ",
            {
                "AI_API_TOKEN": "test_token",
                "AI_API_BASE_URL": "http://test.com/api/v1",
            },
        ):
            client = AIClient()

            # 测试空消息列表
            with pytest.raises(InvalidRequestError):
                client.chat.completions.create(model="yuanbao", messages=[])

            client.close()

    @patch("ai_sdk.client.requests.Session.request")
    def test_chat_completions_create_success(self, mock_request):
        """测试成功创建chat completion"""
        # Mock API响应
        mock_completion_response = Mock()
        mock_completion_response.status_code = 200
        mock_completion_response.text = '{"success": true, "data": {"id": "12345"}}'
        mock_completion_response.json.return_value = {
            "success": True,
            "data": {"id": "12345"},
        }

        mock_result_response = Mock()
        mock_result_response.status_code = 200
        mock_result_response.text = (
            '{"success": true, "data": {"status": 2, "answer": "测试回答"}}'
        )
        mock_result_response.json.return_value = {
            "success": True,
            "data": {"status": 2, "answer": "测试回答"},
        }

        # 设置mock返回值
        mock_request.side_effect = [mock_completion_response, mock_result_response]

        with patch.dict(
            "os.environ",
            {
                "AI_API_TOKEN": "test_token",
                "AI_API_BASE_URL": "http://test.com/api/v1",
            },
        ):
            with AIClient() as client:
                response = client.chat.completions.create(
                    model="yuanbao",
                    messages=[ChatMessage(role="user", content="测试")],
                )

                # 验证响应
                assert isinstance(response, ChatCompletion)
                assert response.id == "12345"
                assert response.model == "yuanbao"
                assert len(response.choices) == 1
                assert response.choices[0].message.content == "测试回答"
                assert response.choices[0].message.role == "assistant"

    def test_model_name_conversion(self):
        """测试模型名称转换"""
        from ai_sdk._utils import model_name_to_type

        assert model_name_to_type("yuanbao") == 1
        assert model_name_to_type("gemini") == 2
        assert model_name_to_type("unknown") == 1  # 默认返回1

    def test_extract_question_from_messages(self):
        """测试从消息列表提取问题"""
        from ai_sdk._utils import extract_question_from_messages

        messages = [
            ChatMessage(role="system", content="你是助手"),
            ChatMessage(role="user", content="问题1"),
            ChatMessage(role="assistant", content="回答1"),
            ChatMessage(role="user", content="问题2"),
        ]

        question = extract_question_from_messages(messages)
        assert "[System]: 你是助手" in question
        assert "问题1" in question
        assert "[Assistant]: 回答1" in question
        assert "问题2" in question


class TestExceptions:
    """异常测试类"""

    def test_authentication_error(self):
        """测试认证错误"""
        from ai_sdk.exceptions import AuthenticationError

        error = AuthenticationError("Invalid token", status_code=401)
        assert "Invalid token" in str(error)
        assert error.status_code == 401

    def test_invalid_request_error(self):
        """测试请求参数错误"""
        from ai_sdk.exceptions import InvalidRequestError

        error = InvalidRequestError("Missing parameter", status_code=400)
        assert "Missing parameter" in str(error)
        assert error.status_code == 400


# 运行测试的说明
"""
运行测试:
    pytest tests/test_client.py -v

运行测试并显示覆盖率:
    pytest tests/test_client.py -v --cov=ai_sdk --cov-report=html

运行特定测试:
    pytest tests/test_client.py::TestAIClient::test_client_init_with_params -v
"""
