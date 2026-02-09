#!/usr/bin/env python3
"""
飞书配置检查脚本
用于验证飞书多维表格集成所需的配置是否正确
"""

import os
import sys
import requests
from typing import Dict, List, Tuple

# 配置项
REQUIRED_VARS = {
    "FEISHU_APP_ID": "飞书应用 ID",
    "FEISHU_APP_SECRET": "飞书应用密钥",
    "FEISHU_BITABLE_APP_TOKEN": "多维表格 App Token",
    "FEISHU_BITABLE_TABLE_ID": "表格 Table ID"
}

BASE_URL = "https://open.feishu.cn/open-apis"


class ConfigChecker:
    """配置检查器"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []

    def check_env_vars(self) -> bool:
        """检查环境变量是否配置"""
        print("\n[1/5] 检查环境变量配置...")
        all_configured = True

        for var_name, var_desc in REQUIRED_VARS.items():
            value = os.getenv(var_name, "")
            if value:
                masked_value = value[:10] + "..." if len(value) > 10 else value
                self.success.append(f"  ✓ {var_desc} ({var_name}): {masked_value}")
            else:
                self.errors.append(f"  ✗ {var_desc} ({var_name}): 未配置")
                all_configured = False

        return all_configured

    def check_app_credentials(self) -> Tuple[bool, str]:
        """检查应用凭证是否有效"""
        print("\n[2/5] 验证应用凭证...")

        app_id = os.getenv("FEISHU_APP_ID", "")
        app_secret = os.getenv("FEISHU_APP_SECRET", "")

        if not app_id or not app_secret:
            self.errors.append("  ✗ 应用凭证未配置，跳过验证")
            return False, ""

        url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
        payload = {"app_id": app_id, "app_secret": app_secret}

        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("code") == 0:
                token = data.get("tenant_access_token", "")
                self.success.append("  ✓ 应用凭证有效，成功获取访问令牌")
                return True, token
            else:
                error_msg = data.get("msg", "未知错误")
                self.errors.append(f"  ✗ 应用凭证无效: {error_msg}")
                return False, ""
        except requests.exceptions.Timeout:
            self.errors.append("  ✗ 请求超时，请检查网络连接")
            return False, ""
        except Exception as e:
            self.errors.append(f"  ✗ 验证失败: {str(e)}")
            return False, ""

    def check_app_permissions(self, token: str) -> bool:
        """检查应用权限"""
        print("\n[3/5] 检查应用权限...")

        if not token:
            self.errors.append("  ✗ 无访问令牌，跳过权限检查")
            return False

        # 尝试访问多维表格 API，检查权限
        app_token = os.getenv("FEISHU_BITABLE_APP_TOKEN", "")
        table_id = os.getenv("FEISHU_BITABLE_TABLE_ID", "")

        if not app_token or not table_id:
            self.warnings.append("  ⚠ 表格信息未配置，无法验证权限")
            return False

        url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()

            if data.get("code") == 0:
                self.success.append("  ✓ 应用有权限访问多维表格")
                return True
            elif data.get("code") == 99991663:
                self.errors.append("  ✗ 应用无权限访问该多维表格")
                self.errors.append("    请在多维表格设置中授权该应用")
                return False
            else:
                error_msg = data.get("msg", "未知错误")
                self.errors.append(f"  ✗ 权限检查失败: {error_msg}")
                return False
        except Exception as e:
            self.errors.append(f"  ✗ 权限检查失败: {str(e)}")
            return False

    def check_table_fields(self, token: str) -> bool:
        """检查表格字段是否正确"""
        print("\n[4/5] 检查表格字段配置...")

        if not token:
            self.errors.append("  ✗ 无访问令牌，跳过字段检查")
            return False

        app_token = os.getenv("FEISHU_BITABLE_APP_TOKEN", "")
        table_id = os.getenv("FEISHU_BITABLE_TABLE_ID", "")

        if not app_token or not table_id:
            self.errors.append("  ✗ 表格信息未配置，跳过字段检查")
            return False

        url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()

            if data.get("code") != 0:
                self.errors.append(f"  ✗ 获取字段列表失败: {data.get('msg')}")
                return False

            # 获取字段列表
            fields = data.get("data", {}).get("items", [])
            field_names = {field.get("field_name"): field.get("type") for field in fields}

            # 检查必需字段
            required_fields = {
                "标题": 1,  # 1 = 文本
                "内容": 1,  # 1 = 文本
                "创建时间": 5  # 5 = 日期
            }

            all_fields_ok = True
            for field_name, expected_type in required_fields.items():
                if field_name in field_names:
                    actual_type = field_names[field_name]
                    if actual_type == expected_type:
                        type_name = {1: "文本", 5: "日期"}.get(expected_type, "未知")
                        self.success.append(f"  ✓ 字段 '{field_name}' 存在且类型正确 ({type_name})")
                    else:
                        type_name = {1: "文本", 5: "日期"}.get(expected_type, "未知")
                        self.warnings.append(f"  ⚠ 字段 '{field_name}' 类型不匹配 (期望: {type_name})")
                        all_fields_ok = False
                else:
                    self.errors.append(f"  ✗ 缺少必需字段: '{field_name}'")
                    all_fields_ok = False

            if all_fields_ok:
                return True

            # 显示当前字段列表供参考
            if fields:
                print("\n  当前表格字段列表:")
                for field in fields:
                    type_map = {1: "文本", 2: "数字", 5: "日期", 7: "多选", 11: "人员"}
                    type_name = type_map.get(field.get("type"), f"类型{field.get('type')}")
                    print(f"    - {field.get('field_name')} ({type_name})")

            return False

        except Exception as e:
            self.errors.append(f"  ✗ 字段检查失败: {str(e)}")
            return False

    def test_write_operation(self, token: str) -> bool:
        """测试写入操作"""
        print("\n[5/5] 测试写入操作...")

        if not token:
            self.errors.append("  ✗ 无访问令牌，跳过写入测试")
            return False

        app_token = os.getenv("FEISHU_BITABLE_APP_TOKEN", "")
        table_id = os.getenv("FEISHU_BITABLE_TABLE_ID", "")

        if not app_token or not table_id:
            self.errors.append("  ✗ 表格信息未配置，跳过写入测试")
            return False

        url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        from datetime import datetime
        test_data = {
            "fields": {
                "标题": f"配置检查测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "内容": "这是一条测试记录，用于验证飞书多维表格集成配置是否正确。",
                "创建时间": int(datetime.now().timestamp() * 1000)
            }
        }

        try:
            resp = requests.post(url, headers=headers, json=test_data, timeout=10)
            data = resp.json()

            if data.get("code") == 0:
                record_id = data.get("data", {}).get("record", {}).get("record_id")
                self.success.append(f"  ✓ 写入测试成功，记录ID: {record_id}")
                self.success.append("  ✓ 请在飞书多维表格中查看测试记录")
                return True
            else:
                error_msg = data.get("msg", "未知错误")
                self.errors.append(f"  ✗ 写入测试失败: {error_msg}")
                return False
        except Exception as e:
            self.errors.append(f"  ✗ 写入测试失败: {str(e)}")
            return False

    def print_summary(self):
        """打印检查摘要"""
        print("\n" + "="*60)
        print("配置检查摘要")
        print("="*60)

        if self.success:
            print("\n✅ 成功项:")
            for msg in self.success:
                print(msg)

        if self.warnings:
            print("\n⚠️  警告项:")
            for msg in self.warnings:
                print(msg)

        if self.errors:
            print("\n❌ 错误项:")
            for msg in self.errors:
                print(msg)

        print("\n" + "="*60)

        if not self.errors:
            print("🎉 所有检查通过！飞书集成配置正确。")
        else:
            print("⚠️  发现配置问题，请根据上述错误信息进行修复。")
            print("\n配置指南:")
            print("  ~/.agents/skills/feynman/references/feishu-setup-guide.md")

        print("="*60 + "\n")

    def run(self):
        """运行完整的配置检查"""
        print("\n" + "="*60)
        print("飞书多维表格集成 - 配置检查工具")
        print("="*60)

        # 1. 检查环境变量
        if not self.check_env_vars():
            print("\n⚠️  环境变量配置不完整，请先配置所有必需的环境变量。")
            self.print_summary()
            return False

        # 2. 验证应用凭证
        valid, token = self.check_app_credentials()
        if not valid:
            self.print_summary()
            return False

        # 3. 检查应用权限
        self.check_app_permissions(token)

        # 4. 检查表格字段
        self.check_table_fields(token)

        # 5. 测试写入操作
        if not self.errors:  # 只有在没有错误时才进行写入测试
            self.test_write_operation(token)

        # 打印摘要
        self.print_summary()

        return len(self.errors) == 0


def main():
    """主函数"""
    checker = ConfigChecker()
    success = checker.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
