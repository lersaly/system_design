from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING

class MongoDBService:
    def __init__(self, connection_string="mongodb://mongodb:27017/", database="conference_db"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
        self.conference_logs = self.db.conference_logs
        self._create_indexes()

    def _create_indexes(self):
        # Create indexes for efficient querying
        index_models = [
            IndexModel([("conference_id", ASCENDING)]),
            IndexModel([("timestamp", ASCENDING)])
        ]
        self.conference_logs.create_indexes(index_models)

    def log_conference_activity(self, conference_id, action, details):
        log_entry = {
            "conference_id": conference_id,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        return self.conference_logs.insert_one(log_entry)

    def get_conference_logs(self, conference_id):
        return list(self.conference_logs.find({"conference_id": conference_id}))