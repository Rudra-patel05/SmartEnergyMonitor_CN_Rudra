import logging
import sys

# Configure logger
logger = logging.getLogger("smart_energy_audit")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[AUDIT LOG] %(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Output to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def log_auth_success(username: str, role: str, ip: str):
    logger.info(f"Successful user login. Username: '{username}', Role: '{role}', IP: {ip}")

def log_auth_failure(username: str, ip: str, reason: str):
    logger.warning(f"Failed authentication attempt. Attempted Username: '{username}', IP: {ip}, Reason: {reason}")

def log_invalid_payload(endpoint: str, details: str, ip: str):
    logger.warning(f"Rejected malformed request payload at endpoint '{endpoint}'. Details: {details}, IP: {ip}")

def log_device_auth_failure(device_id: str, ip: str):
    logger.warning(f"Device authentication failed. Device ID: '{device_id}', IP: {ip}")

def log_inference_failure(model_name: str, device_id: str, error: str):
    logger.error(f"Inference run failed. Model: '{model_name}', Device: '{device_id}', Error: {error}")
