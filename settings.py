import os

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER", "10.129.150.90:9092")

CIRAM_URL = os.getenv("CIRAM_URL", "http://localhost:5050/getDetections")

FUSION_GEO = os.getenv("FUSION_GEO", "http://localhost:8000/")

NATIONAL_DB_BASE_URL = os.getenv("NATIONAL_DB_BASE_URL", "10.129.150.90:8282")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

MINIMAL = int(os.getenv("MINIMAL", 0))

KAFKA_TOPICS = (
    "TOP22_11_LPR_DONE",
    "TOP12_04_LPR_ALERT",
    "TOP22_02_OBJECT_RECO_DONE",

    "TOP21_01_COMMAND_CENTER_MISSION",
    "TOP12_05_VEHICLE_COUNT_EVENT",
    "TOP22_08_ACTIVITY_RECO_DONE"
)

if MINIMAL == 0:
    KAFKA_TOPICS += (
        "TOP10_02_COD_ALERT",
        "TOP22_05_FACE_RECO_DONE",
    )

OFFSET_RESET = "latest"

NATIONAL_DB_URL = (
    "http://"
    + NATIONAL_DB_BASE_URL
    + "/national-suspects-information/api/mock/get-suspect-by-license-plate/"
)

NATIONAL_DB_VEHICLE = (
    "http://"
    + "10.129.150.90:8283"
    + "/national-vehicles-information/api/mock/get-vehicle-by-license-plate/"
)

VEHICLE_COLOUR_LIST = {
    "color:car Red", 
    "color:car Blue", 
    "color:car Green", 
    "color:car White", 
    "color:car Black", 
    "color:car Yellow", 
    "color:car Gray", 
    "color:car Cyan"
}

CIRCLING_THRESHOLD = 60

CIRCLING_THRESHOLD_NUMBER = 3

CONVOY_THRESHOLD_TIME = 1

CONVOY_THRESHOLD_NUMBER = 3

FORBIDDEN_VEHICLE_CATEGORIES = [
    "truck"
]

PERSON_LINGERING_THRESHOLD = 10

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
