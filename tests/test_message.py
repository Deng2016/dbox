import pytest
from unittest.mock import patch, MagicMock
from dbox.message import send_email, send_sms, send_wechat, send_dingtalk, send_feishu, send_slack, send_telegram


class TestMessage:
    """测试消息发送相关函数"""

    @patch("dbox.message.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        """测试成功发送邮件"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("sender@example.com", "receiver@example.com", "Test Subject", "Test Content")
        assert result is True
        mock_server.sendmail.assert_called_once()

    @patch("dbox.message.smtplib.SMTP")
    def test_send_email_failure(self, mock_smtp):
        """测试发送邮件失败"""
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = Exception("SMTP error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("sender@example.com", "receiver@example.com", "Test Subject", "Test Content")
        assert result is False

    def test_send_email_invalid_sender(self):
        """测试发送邮件-无效发件人"""
        result = send_email("", "receiver@example.com", "Test Subject", "Test Content")
        assert result is False

    def test_send_email_invalid_receiver(self):
        """测试发送邮件-无效收件人"""
        result = send_email("sender@example.com", "", "Test Subject", "Test Content")
        assert result is False

    def test_send_email_empty_subject(self):
        """测试发送邮件-空主题"""
        result = send_email("sender@example.com", "receiver@example.com", "", "Test Content")
        assert result is False

    def test_send_email_empty_content(self):
        """测试发送邮件-空内容"""
        result = send_email("sender@example.com", "receiver@example.com", "Test Subject", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_sms_success(self, mock_post):
        """测试成功发送短信"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0, "message": "success"}
        mock_post.return_value = mock_response

        result = send_sms("13800138000", "Test SMS content")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_sms_failure(self, mock_post):
        """测试发送短信失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"code": 1, "message": "failed"}
        mock_post.return_value = mock_response

        result = send_sms("13800138000", "Test SMS content")
        assert result is False

    def test_send_sms_invalid_phone(self):
        """测试发送短信-无效手机号"""
        result = send_sms("invalid_phone", "Test SMS content")
        assert result is False

    def test_send_sms_empty_content(self):
        """测试发送短信-空内容"""
        result = send_sms("13800138000", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_wechat_success(self, mock_post):
        """测试成功发送微信消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
        mock_post.return_value = mock_response

        result = send_wechat("test_user", "Test WeChat message")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_wechat_failure(self, mock_post):
        """测试发送微信消息失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"errcode": 1, "errmsg": "failed"}
        mock_post.return_value = mock_response

        result = send_wechat("test_user", "Test WeChat message")
        assert result is False

    def test_send_wechat_empty_user(self):
        """测试发送微信消息-空用户"""
        result = send_wechat("", "Test WeChat message")
        assert result is False

    def test_send_wechat_empty_message(self):
        """测试发送微信消息-空消息"""
        result = send_wechat("test_user", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_dingtalk_success(self, mock_post):
        """测试成功发送钉钉消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
        mock_post.return_value = mock_response

        result = send_dingtalk("test_user", "Test DingTalk message")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_dingtalk_failure(self, mock_post):
        """测试发送钉钉消息失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"errcode": 1, "errmsg": "failed"}
        mock_post.return_value = mock_response

        result = send_dingtalk("test_user", "Test DingTalk message")
        assert result is False

    def test_send_dingtalk_empty_user(self):
        """测试发送钉钉消息-空用户"""
        result = send_dingtalk("", "Test DingTalk message")
        assert result is False

    def test_send_dingtalk_empty_message(self):
        """测试发送钉钉消息-空消息"""
        result = send_dingtalk("test_user", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_feishu_success(self, mock_post):
        """测试成功发送飞书消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0, "msg": "success"}
        mock_post.return_value = mock_response

        result = send_feishu("test_user", "Test Feishu message")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_feishu_failure(self, mock_post):
        """测试发送飞书消息失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"code": 1, "msg": "failed"}
        mock_post.return_value = mock_response

        result = send_feishu("test_user", "Test Feishu message")
        assert result is False

    def test_send_feishu_empty_user(self):
        """测试发送飞书消息-空用户"""
        result = send_feishu("", "Test Feishu message")
        assert result is False

    def test_send_feishu_empty_message(self):
        """测试发送飞书消息-空消息"""
        result = send_feishu("test_user", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_slack_success(self, mock_post):
        """测试成功发送Slack消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        result = send_slack("test_channel", "Test Slack message")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_slack_failure(self, mock_post):
        """测试发送Slack消息失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"ok": False, "error": "failed"}
        mock_post.return_value = mock_response

        result = send_slack("test_channel", "Test Slack message")
        assert result is False

    def test_send_slack_empty_channel(self):
        """测试发送Slack消息-空频道"""
        result = send_slack("", "Test Slack message")
        assert result is False

    def test_send_slack_empty_message(self):
        """测试发送Slack消息-空消息"""
        result = send_slack("test_channel", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_telegram_success(self, mock_post):
        """测试成功发送Telegram消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        result = send_telegram("test_chat_id", "Test Telegram message")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_telegram_failure(self, mock_post):
        """测试发送Telegram消息失败"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"ok": False, "error_code": 1}
        mock_post.return_value = mock_response

        result = send_telegram("test_chat_id", "Test Telegram message")
        assert result is False

    def test_send_telegram_empty_chat_id(self):
        """测试发送Telegram消息-空聊天ID"""
        result = send_telegram("", "Test Telegram message")
        assert result is False

    def test_send_telegram_empty_message(self):
        """测试发送Telegram消息-空消息"""
        result = send_telegram("test_chat_id", "")
        assert result is False

    @patch("dbox.message.requests.post")
    def test_send_email_with_attachment(self, mock_post):
        """测试发送带附件的邮件"""
        with patch("dbox.message.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = send_email(
                "sender@example.com", "receiver@example.com", "Test Subject", "Test Content", attachments=["test.txt"]
            )
            assert result is True

    @patch("dbox.message.requests.post")
    def test_send_sms_with_template(self, mock_post):
        """测试使用模板发送短信"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0, "message": "success"}
        mock_post.return_value = mock_response

        result = send_sms("13800138000", "Test SMS content", template_id="template_123")
        assert result is True

    @patch("dbox.message.requests.post")
    def test_send_wechat_with_media(self, mock_post):
        """测试发送带媒体的微信消息"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
        mock_post.return_value = mock_response

        result = send_wechat("test_user", "Test WeChat message", media_type="image", media_id="media_123")
        assert result is True
