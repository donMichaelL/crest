from kafka import KafkaConsumer
from random import random

from settings import BOOTSTRAP_SERVER, KAFKA_TOPICS, OFFSET_RESET
from controllers import TOP12_05_VEHICLE_COUNT_EVENT, TOP22_11_LPR_DONE, TOP22_02_OBJECT_RECO_DONE

from command_mission.controllers import TOP21_01_COMMAND_CENTER_MISSION
from activity_reco.controllers import TOP22_08_ACTIVITY_RECO_DONE
from face_reco.controllers import TOP22_05_FACE_RECO_DONE
from cod_reco.controllers import TOP10_02_COD_ALERT
from lpr_alert.controllers import TOP12_04_LPR_ALERT


class Application:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer
    
    def run(self):
        self.consumer.subscribe(KAFKA_TOPICS)
        for message in consumer:
            topic_class = {
                "TOP21_01_COMMAND_CENTER_MISSION": TOP21_01_COMMAND_CENTER_MISSION,
                "TOP12_04_LPR_ALERT": TOP12_04_LPR_ALERT,
                "TOP22_05_FACE_RECO_DONE": TOP22_05_FACE_RECO_DONE,
                "TOP10_02_COD_ALERT": TOP10_02_COD_ALERT,
                "TOP22_02_OBJECT_RECO_DONE": TOP22_02_OBJECT_RECO_DONE,
                "TOP22_11_LPR_DONE": TOP22_11_LPR_DONE,
                "TOP12_05_VEHICLE_COUNT_EVENT": TOP12_05_VEHICLE_COUNT_EVENT,
                "TOP22_08_ACTIVITY_RECO_DONE": TOP22_08_ACTIVITY_RECO_DONE,
            }.get(message.topic)

            topic_class(message.value).execute()


if __name__ == "__main__":
    consumer = KafkaConsumer(
        group_id=str(random()),
        auto_offset_reset=OFFSET_RESET,
        bootstrap_servers=BOOTSTRAP_SERVER,
    )
    app = Application(consumer)
    app.run()
