#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书长连接服务
用于接收飞书平台推送的事件消息

使用说明：
1. 在飞书开发者后台「事件订阅」中选择「使用长连接接收事件」
2. 填写以下配置信息（从开发者后台获取）
3. 运行此脚本建立长连接
"""

import logging
import lark_oapi as lark
from lark_oapi.ws import Client as WsClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== 配置信息（请从飞书开发者后台获取） =====
APP_ID = "cli_a909801b4e78dbef"
APP_SECRET = "kgn18EBGfQzmUDShhc4vugsLUgMwlAQX"

# 以下两个参数在「事件订阅」-「配置信息」中获取
# 如果开发者后台未开启加密，可以留空字符串
ENCRYPT_KEY = ""  # 加密密钥（Encrypt Key）
VERIFICATION_TOKEN = ""  # 验证令牌（Verification Token）


def handle_im_message_receive(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    """
    处理接收到的消息事件

    Args:
        data: 消息事件数据
    """
    logger.info("=" * 50)
    logger.info("收到消息事件")
    logger.info(f"事件数据: {lark.JSON.marshal(data, indent=4)}")

    # 解析消息内容
    try:
        message = data.event.message
        logger.info(f"消息ID: {message.message_id}")
        logger.info(f"发送者ID: {message.sender.sender_id.user_id}")
        logger.info(f"消息类型: {message.message_type}")
        logger.info(f"消息内容: {message.content}")
    except Exception as e:
        logger.error(f"解析消息失败: {e}")

    logger.info("=" * 50)


def handle_message_recalled(data: lark.im.v1.P2ImMessageRecalledV1) -> None:
    """
    处理消息撤回事件

    Args:
        data: 消息撤回事件数据
    """
    logger.info("=" * 50)
    logger.info("收到消息撤回事件")
    logger.info(f"事件数据: {lark.JSON.marshal(data, indent=4)}")
    logger.info("=" * 50)


def handle_message_read(data: lark.im.v1.P2ImMessageMessageReadV1) -> None:
    """
    处理消息已读事件

    Args:
        data: 消息已读事件数据
    """
    logger.info("=" * 50)
    logger.info("收到消息已读事件")
    logger.info(f"事件数据: {lark.JSON.marshal(data, indent=4)}")
    logger.info("=" * 50)


def create_event_handler():
    """
    创建事件处理器

    Returns:
        EventDispatcherHandler: 配置好的事件处理器
    """
    logger.info("正在创建事件处理器...")

    # 使用 Builder 模式构建事件处理器
    event_handler = lark.EventDispatcherHandler.builder(
        ENCRYPT_KEY,           # 加密密钥
        VERIFICATION_TOKEN     # 验证令牌
    ) \
    .register_p2_im_message_receive_v1(handle_im_message_receive) \
    .register_p2_im_message_recalled_v1(handle_message_recalled) \
    .register_p2_im_message_message_read_v1(handle_message_read) \
    .build()

    # 如果需要处理更多事件类型，可以继续注册：
    # .register_p2_im_chat_member_bot_added_v1(your_handler_function) \
    # .register_p2_im_message_reaction_created_v1(your_handler_function) \

    logger.info("事件处理器创建完成")
    return event_handler


def main():
    """主函数 - 启动长连接服务"""
    try:
        logger.info("=" * 60)
        logger.info("飞书长连接服务启动中...")
        logger.info("=" * 60)
        logger.info(f"APP_ID: {APP_ID}")
        logger.info(f"加密密钥配置: {'已配置' if ENCRYPT_KEY else '未配置（明文传输）'}")
        logger.info(f"验证令牌配置: {'已配置' if VERIFICATION_TOKEN else '未配置'}")
        logger.info("-" * 60)

        # 创建事件处理器
        event_handler = create_event_handler()

        # 创建长连接客户端
        logger.info("正在创建 WebSocket 客户端...")
        ws_client = WsClient(
            app_id=APP_ID,
            app_secret=APP_SECRET,
            event_handler=event_handler
        )

        logger.info("长连接客户端创建成功")
        logger.info("=" * 60)
        logger.info("正在建立与飞书服务器的连接...")
        logger.info("请确保在飞书开发者后台已选择「使用长连接接收事件」")
        logger.info("=" * 60)

        # 启动长连接（会阻塞主线程）
        ws_client.start()

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("收到中断信号 (Ctrl+C)，正在关闭服务...")
        logger.info("=" * 60)
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"服务运行出错: {e}", exc_info=True)
        logger.error("=" * 60)
        logger.error("\n常见问题排查：")
        logger.error("1. 检查 APP_ID 和 APP_SECRET 是否正确")
        logger.error("2. 检查网络连接是否正常")
        logger.error("3. 检查飞书开发者后台是否已选择「使用长连接接收事件」")
        logger.error("4. 如果开启了加密，检查 ENCRYPT_KEY 和 VERIFICATION_TOKEN 是否正确")
    finally:
        logger.info("飞书长连接服务已停止")


if __name__ == "__main__":
    main()
