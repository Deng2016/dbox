import pytest
from unittest.mock import patch, MagicMock
from dbox.git import git_clone, git_pull, git_push, git_commit, git_branch, git_checkout, git_merge, git_status, git_log


class TestGit:
    """测试Git相关函数"""

    @patch("dbox.git.subprocess.run")
    def test_git_clone_success(self, mock_run):
        """测试成功克隆仓库"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_clone("https://github.com/test/repo.git", "local_path")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_clone_failure(self, mock_run):
        """测试克隆仓库失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_clone("https://github.com/test/repo.git", "local_path")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_pull_success(self, mock_run):
        """测试成功拉取更新"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_pull("local_path")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_pull_failure(self, mock_run):
        """测试拉取更新失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_pull("local_path")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_push_success(self, mock_run):
        """测试成功推送"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_push("local_path", "origin", "main")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_push_failure(self, mock_run):
        """测试推送失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_push("local_path", "origin", "main")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_commit_success(self, mock_run):
        """测试成功提交"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_commit("local_path", "test commit message")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_commit_failure(self, mock_run):
        """测试提交失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_commit("local_path", "test commit message")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_branch_success(self, mock_run):
        """测试成功创建分支"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_branch("local_path", "new_branch")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_branch_failure(self, mock_run):
        """测试创建分支失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_branch("local_path", "new_branch")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_checkout_success(self, mock_run):
        """测试成功切换分支"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_checkout("local_path", "main")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_checkout_failure(self, mock_run):
        """测试切换分支失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_checkout("local_path", "nonexistent_branch")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_merge_success(self, mock_run):
        """测试成功合并分支"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = git_merge("local_path", "feature_branch")
        assert result is True
        mock_run.assert_called_once()

    @patch("dbox.git.subprocess.run")
    def test_git_merge_failure(self, mock_run):
        """测试合并分支失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_merge("local_path", "feature_branch")
        assert result is False

    @patch("dbox.git.subprocess.run")
    def test_git_status_success(self, mock_run):
        """测试成功获取状态"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = b"On branch main\nnothing to commit, working tree clean"
        mock_run.return_value = mock_result

        result = git_status("local_path")
        assert result == "On branch main\nnothing to commit, working tree clean"

    @patch("dbox.git.subprocess.run")
    def test_git_status_failure(self, mock_run):
        """测试获取状态失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_status("local_path")
        assert result is None

    @patch("dbox.git.subprocess.run")
    def test_git_log_success(self, mock_run):
        """测试成功获取日志"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = b"commit abc123\nAuthor: Test User\nDate: 2023-01-01"
        mock_run.return_value = mock_result

        result = git_log("local_path")
        assert "commit abc123" in result

    @patch("dbox.git.subprocess.run")
    def test_git_log_failure(self, mock_run):
        """测试获取日志失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = git_log("local_path")
        assert result is None

    def test_git_clone_invalid_url(self):
        """测试克隆无效URL"""
        result = git_clone("invalid_url", "local_path")
        assert result is False

    def test_git_clone_empty_path(self):
        """测试克隆到空路径"""
        result = git_clone("https://github.com/test/repo.git", "")
        assert result is False

    def test_git_pull_empty_path(self):
        """测试从空路径拉取"""
        result = git_pull("")
        assert result is False

    def test_git_push_empty_path(self):
        """测试推送到空路径"""
        result = git_push("", "origin", "main")
        assert result is False

    def test_git_commit_empty_message(self):
        """测试提交空消息"""
        result = git_commit("local_path", "")
        assert result is False

    def test_git_branch_empty_name(self):
        """测试创建空名称分支"""
        result = git_branch("local_path", "")
        assert result is False

    def test_git_checkout_empty_branch(self):
        """测试切换到空分支"""
        result = git_checkout("local_path", "")
        assert result is False

    def test_git_merge_empty_branch(self):
        """测试合并空分支"""
        result = git_merge("local_path", "")
        assert result is False

    def test_git_status_empty_path(self):
        """测试获取空路径状态"""
        result = git_status("")
        assert result is None

    def test_git_log_empty_path(self):
        """测试获取空路径日志"""
        result = git_log("")
        assert result is None
