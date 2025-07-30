import pytest
from unittest.mock import patch, MagicMock
from dbox.db_oper import (
    get_db_connect,
    execute_sql,
    execute_sql_with_params,
    execute_sql_with_dict,
    execute_sql_with_list,
    execute_sql_with_tuple,
    execute_sql_with_named_params,
    execute_sql_with_positional_params,
    execute_sql_with_mixed_params,
    execute_sql_with_custom_params,
    execute_sql_with_connection,
    execute_sql_with_cursor,
    execute_sql_with_transaction,
    execute_sql_with_rollback,
    execute_sql_with_commit,
    execute_sql_with_error_handling,
)


class TestDbOper:
    """测试数据库操作函数"""

    @patch("dbox.db_oper.pymysql.connect")
    def test_get_db_connect_success(self, mock_connect, mock_pymysql):
        """测试成功获取数据库连接"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        result = get_db_connect()
        assert result == mock_conn
        mock_connect.assert_called_once()

    @patch("dbox.db_oper.pymysql.connect")
    def test_get_db_connect_failure(self, mock_connect, mock_pymysql):
        """测试获取数据库连接失败"""
        mock_connect.side_effect = Exception("Connection failed")

        with pytest.raises(Exception):
            get_db_connect()

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_success(self, mock_get_connect, mock_pymysql):
        """测试成功执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "test"}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql("SELECT * FROM test_table")
        assert result == [{"id": 1, "name": "test"}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_failure(self, mock_get_connect, mock_pymysql):
        """测试执行SQL失败"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("SQL error")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        with pytest.raises(Exception):
            execute_sql("SELECT * FROM invalid_table")

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_params(self, mock_get_connect, mock_pymysql):
        """测试带参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = {"id": 1}
        result = execute_sql_with_params("SELECT * FROM test_table WHERE id = %(id)s", params)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_dict(self, mock_get_connect, mock_pymysql):
        """测试带字典参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "test"}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = {"id": 1, "name": "test"}
        result = execute_sql_with_dict("SELECT * FROM test_table WHERE id = %(id)s AND name = %(name)s", params)
        assert result == [{"id": 1, "name": "test"}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_list(self, mock_get_connect, mock_pymysql):
        """测试带列表参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = [1, "test"]
        result = execute_sql_with_list("SELECT * FROM test_table WHERE id = %s AND name = %s", params)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_tuple(self, mock_get_connect, mock_pymysql):
        """测试带元组参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = (1, "test")
        result = execute_sql_with_tuple("SELECT * FROM test_table WHERE id = %s AND name = %s", params)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_named_params(self, mock_get_connect, mock_pymysql):
        """测试带命名参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = {"id": 1, "name": "test"}
        result = execute_sql_with_named_params("SELECT * FROM test_table WHERE id = %(id)s AND name = %(name)s", params)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_positional_params(self, mock_get_connect, mock_pymysql):
        """测试带位置参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = [1, "test"]
        result = execute_sql_with_positional_params("SELECT * FROM test_table WHERE id = %s AND name = %s", params)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_mixed_params(self, mock_get_connect, mock_pymysql):
        """测试带混合参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        named_params = {"id": 1}
        positional_params = ["test"]
        result = execute_sql_with_mixed_params(
            "SELECT * FROM test_table WHERE id = %(id)s AND name = %s", named_params, positional_params
        )
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_custom_params(self, mock_get_connect, mock_pymysql):
        """测试带自定义参数执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        params = {"id": 1, "name": "test"}
        result = execute_sql_with_custom_params(
            "SELECT * FROM test_table WHERE id = %(id)s AND name = %(name)s", params
        )
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_connection(self, mock_get_connect, mock_pymysql):
        """测试使用指定连接执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_connection("SELECT * FROM test_table", mock_conn)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_cursor(self, mock_get_connect, mock_pymysql):
        """测试使用指定游标执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_cursor("SELECT * FROM test_table", mock_cursor)
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_transaction(self, mock_get_connect, mock_pymysql):
        """测试事务中执行SQL"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_transaction("SELECT * FROM test_table")
        assert result == [{"id": 1}]
        mock_conn.commit.assert_called_once()

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_rollback(self, mock_get_connect, mock_pymysql):
        """测试执行SQL时回滚"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("SQL error")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        with pytest.raises(Exception):
            execute_sql_with_rollback("SELECT * FROM invalid_table")
        mock_conn.rollback.assert_called_once()

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_commit(self, mock_get_connect, mock_pymysql):
        """测试执行SQL时提交"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_commit("SELECT * FROM test_table")
        assert result == [{"id": 1}]
        mock_conn.commit.assert_called_once()

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_error_handling(self, mock_get_connect, mock_pymysql):
        """测试带错误处理的SQL执行"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_error_handling("SELECT * FROM test_table")
        assert result == [{"id": 1}]

    @patch("dbox.db_oper.get_db_connect")
    def test_execute_sql_with_error_handling_failure(self, mock_get_connect, mock_pymysql):
        """测试带错误处理的SQL执行失败"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("SQL error")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connect.return_value = mock_conn

        result = execute_sql_with_error_handling("SELECT * FROM invalid_table")
        assert result is None
