import os

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER", "10.129.150.90:9092")

CIRAM_URL = os.getenv("CIRAM_URL", "http://localhost:5050/getDetections")

FUSION_GEO = os.getenv("FUSION_GEO", "http://localhost:8000/")

NATIONAL_DB_BASE_URL = os.getenv("NATIONAL_DB_BASE_URL", "10.129.150.90:8282")


REDIS_HOST = os.getenv("REDIS_HOST", "redis")

REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


KAFKA_TOPICS = (
    "TOP22_11_LPR_DONE",
    "TOP12_04_LPR_ALERT",
    "TOP22_02_OBJECT_RECO_DONE",
    "TOP10_02_COD_ALERT",
    "TOP22_05_FACE_RECO_DONE",
    "TOP21_01_COMMAND_CENTER_MISSION",
    "TOP12_05_VEHICLE_COUNT_EVENT",
    "TOP22_08_ACTIVITY_RECO_DONE"
)

OFFSET_RESET = "latest"

NATIONAL_DB_URL = (
    "http://"
    + NATIONAL_DB_BASE_URL
    + "/national-suspects-information/api/mock/get-suspect-by-license-plate/"
)

CIRCLING_THRESHOLD = 60

SUSPECT_ATTRS_SET = {
    "id",
    "firstName",
    "lastName",
    "nickname",
    "age",
    "lastKnownAddress",
    "profession",
    "email",
    "photo",
}

VEHICLE_ATTRS_SET = {
    "id",
    "manufacturer",
    "model",
    "color",
    "type",
    "vin",
    "year",
    "licenseState",
    "licenseNumber",
    "icon",
    "description",
    "registeredOwner",
}
