"""
  GitHub Actions 定时签到入口脚本。
  从环境变量读取账号配置，直接调用签到核心逻辑，无需 Web 面板和 Docker。

  环境变量说明：
    RAINYUN_USER       - 雨云账号用户名（必填）
    RAINYUN_PWD        - 雨云账号密码（必填）
    RAINYUN_API_KEY    - 雨云 API Key（可选，用于服务器管理/积分查询）
    MAX_DELAY          - 最大随机延时分钟数（默认 0，GitHub Actions 建议设 0）
    CHROME_BIN         - Chromium 路径（默认自动检测）
    CHROMEDRIVER_PATH  - chromedriver 路径（默认自动检测）
    DEBUG              - 调试模式（默认 false）
  """

  import os
  import sys
  import logging

  # 将项目根目录加入 sys.path，确保 rainyun 包可被导入
  sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

  from rainyun.config import Config
  from rainyun.main import run_with_config


  def main() -> int:
      logging.basicConfig(
          level=logging.INFO,
          format="%(asctime)s - %(levelname)s - %(message)s",
      )

      user = os.environ.get("RAINYUN_USER", "")
      pwd = os.environ.get("RAINYUN_PWD", "")
      api_key = os.environ.get("RAINYUN_API_KEY", "")

      if not user or not pwd:
          logging.error("请在 GitHub Secrets 中设置 RAINYUN_USER 和 RAINYUN_PWD")
          return 1

      # 基于 from_env 读取运行层变量，再覆写账号信息
      config = Config.from_env(os.environ)
      config = config.__class__(
          **{
              **config.__dict__,
              "rainyun_user": user,
              "rainyun_pwd": pwd,
              "rainyun_api_key": api_key,
              # GitHub Actions 环境为 Linux，启用 headless
              "linux_mode": True,
              # 不做随机延时，Actions 有 6 小时限制，直接执行
              "max_delay": int(os.environ.get("MAX_DELAY", "0")),
              # 确保必要的目录存在
              "cookie_file": "data/cookies/cookies_github.json",
          }
      )

      # 创建 cookies 目录
      cookie_dir = os.path.dirname(config.cookie_file)
      if cookie_dir:
          os.makedirs(cookie_dir, exist_ok=True)
      os.makedirs("data", exist_ok=True)
      os.makedirs("temp", exist_ok=True)

      logging.info("========== 雨云自动签到 (GitHub Actions) ==========")
      success = run_with_config(config)
      logging.info("========== 签到结果: %s ==========", "成功" if success else "失败")
      return 0 if success else 1


  if __name__ == "__main__":
      sys.exit(main())
