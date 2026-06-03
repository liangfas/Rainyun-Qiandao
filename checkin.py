import os
  import sys
  import logging

  sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

  from rainyun.config import Config
  from rainyun.main import run_with_config


  def main():
      logging.basicConfig(
          level=logging.INFO,
          format="%(asctime)s - %(levelname)s - %(message)s",
      )

      user = os.environ.get("RAINYUN_USER", "")
      pwd = os.environ.get("RAINYUN_PWD", "")
      api_key = os.environ.get("RAINYUN_API_KEY", "")

      if not user or not pwd:
          logging.error("RAINYUN_USER and RAINYUN_PWD are required")
          return 1

      config = Config.from_env(os.environ)
      config = config.__class__(
          **{
              **config.__dict__,
              "rainyun_user": user,
              "rainyun_pwd": pwd,
              "rainyun_api_key": api_key,
              "linux_mode": True,
              "max_delay": int(os.environ.get("MAX_DELAY", "0")),
              "cookie_file": "data/cookies/cookies_github.json",
          }
      )

      cookie_dir = os.path.dirname(config.cookie_file)
      if cookie_dir:
          os.makedirs(cookie_dir, exist_ok=True)
      os.makedirs("data", exist_ok=True)
      os.makedirs("temp", exist_ok=True)

      logging.info("===== Rainyun Checkin (GitHub Actions) =====")
      success = run_with_config(config)
      logging.info("===== Result: %s =====", "SUCCESS" if success else "FAILED")
      return 0 if success else 1


  if __name__ == "__main__":
      sys.exit(main())
