from constants.secrets import DEVICES

DEVICES = {
  "home": [{"id": entry["id"], "default": entry["default"]} for entry in DEVICES["home"]],
  "mobile": [{"id": entry["id"], "default": entry["default"]} for entry in DEVICES["mobile"]]
}