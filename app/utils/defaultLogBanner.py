
import logging

# --------------------------------------------------------------------------
#
#
#
# --------------------------------------------------------------------------


def log_runBanner(msg: str) -> None:
    logging.log(logging.INFO, f"[+] Running {msg}...")
