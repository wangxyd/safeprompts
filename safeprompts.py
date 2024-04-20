# encoding:utf-8

import json
import os
import random

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
from config import global_config

from .lib.WordsSearch import WordsSearch


@plugins.register(
    name="Safeprompts",
    desire_priority=88,
    hidden=True,
    desc="简易的提示词保护插件。",
    version="1.0",
    author="空心菜",
)
class Safeprompts(Plugin):
    def __init__(self):
        super().__init__()
        try:
            # load config
            conf = super().load_config()
            curdir = os.path.dirname(__file__)
            if not conf:
                # 配置不存在则写入默认配置
                config_path = os.path.join(curdir, "config.json")
                if not os.path.exists(config_path):
                    conf = {"action": "ignore"}
                    with open(config_path, "w") as f:
                        json.dump(conf, f, indent=4)

            self.searchr = WordsSearch()
            self.action = conf["action"]
            safeprompts_path = os.path.join(curdir, "safeprompts.txt")
            with open(safeprompts_path, "r", encoding="utf-8") as f:
                prompts = []
                for line in f:
                    word = line.strip()
                    if word:
                        prompts.append(word)
            self.searchr.SetKeywords(prompts)
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            # 表情图片目录
            self.images_dir = conf.get("images_dir", os.path.join(curdir, "images"))
            logger.info("[Safeprompts] inited")
        except Exception as e:
            logger.warn("[Safeprompts] init failed, ignore or see https://github.com/zhayujie/chatgpt-on-wechat/tree/master/plugins/safeprompts .")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [ContextType.TEXT]:
            return

        content = e_context["context"].content
        logger.debug("[Safeprompts] on_handle_context. content: %s" % content)
        if self.is_admin(e_context["context"]):
            logger.debug("[Safeprompts] Skipped because of admin user.")
        elif self.action == "ignore":
            f = self.searchr.FindFirst(content)
            if f:
                logger.info("[Safeprompts] %s in message, ignored the message." % f["Keyword"])
                e_context.action = EventAction.BREAK_PASS
        elif self.action == "replace":
            if self.searchr.ContainsAny(content):
                image = self.get_random_image(self.images_dir)
                if image:
                    logger.info("[Safeprompts] Reply has been replaced to image: %s." % image)
                    reply = Reply(ReplyType.IMAGE, image)
                    e_context["reply"] = reply
                else:
                    logger.warn("[Safeprompts] Failed to replaced reply, ignored the message.")
                e_context.action = EventAction.BREAK_PASS

    def get_random_image(self, images_dir):
        if not os.path.isdir(images_dir):
            logger.warn(f"[Safeprompts] The directory {images_dir} does not exist.")
            return
        images = [img for img in os.listdir(images_dir) if
                  img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))]
        if not images:
            logger.warn(f"[Safeprompts] No images found in the directory {images_dir}.")
            return
        # 随机选择一张图片
        random_image = random.choice(images)
        return os.path.join(images_dir, random_image)

    def is_admin(self, context):
        if context["isgroup"]:
            return context.kwargs.get("msg").actual_user_id in global_config["admin_users"]
        else:
            return context["receiver"] in global_config["admin_users"]

    def get_help_text(self, **kwargs):
        return "简易的提示词保护插件。"
