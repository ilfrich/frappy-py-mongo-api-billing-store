from datetime import datetime, time
from typing import List, Union, Optional
from frappyapibilling import Usage, AbstractUsageStore
from pbu import AbstractMongoStore, AbstractMongoDocument


class MongoUsage(Usage, AbstractMongoDocument):
    def __init__(self):
        super(MongoUsage, self).__init__()

    @staticmethod
    def from_json(json: dict):
        usage = MongoUsage()
        usage.extract_system_fields(json)
        return usage

    def get_attribute_mapping(self) -> dict:
        return {
            "timestamp": "timestamp",
            "credits": "credits",
            "client_id": "clientId",
        }


def _compose_query(client_id: Union[str, int], start_datetime: Optional[datetime],
                   end_datetime: Optional[datetime]) -> dict:
    # compose query
    query = {"clientId": client_id}
    # handle timestamps
    if start_datetime is not None or end_datetime is not None:
        query["timestamp"] = {}
    if start_datetime is not None:
        query["timestamp"]["$gte"] = round(start_datetime.timestamp())
    if end_datetime is not None:
        query["timestamp"]["$lte"] = round(end_datetime.timestamp())
    return query


class UsageStore(AbstractMongoStore, AbstractUsageStore):
    """
    MongoDB implementation of the AbstractUsageStore methods.
    """

    def __init__(self, mongo_url, mongo_db, collection_name):
        AbstractUsageStore.__init__(self)
        AbstractMongoStore.__init__(self, mongo_url, mongo_db, collection_name, MongoUsage, 1)

    def track_usage(self, client_id: Union[str, int], credits_used: Union[int, float]):
        new_usage = MongoUsage()
        new_usage.client_id = client_id
        new_usage.timestamp = round(datetime.now().timestamp())
        new_usage.credits = credits_used
        self.create(new_usage)

    def get_total_usage(self, client_id: Union[str, int], start_datetime: Optional[datetime] = None,
                        end_datetime: Optional[datetime] = None) -> Union[float, int]:
        # run query
        items = self.query(_compose_query(client_id, start_datetime, end_datetime))
        # just sum up used credits overall
        return sum(list(map(lambda x: x.credits, items)))

    def get_daily_usage(self, client_id: Union[str, int], start_datetime: Optional[datetime] = None,
                        end_datetime: Optional[datetime] = None) -> List[Usage]:
        # run query
        items = self.query(_compose_query(client_id, start_datetime, end_datetime))

        # process query result
        result_map = {}
        for item in items:
            # get timestamp
            ts = round(datetime.combine(datetime.fromtimestamp(item.timestamp).date(), time()).timestamp())
            if ts not in result_map:
                # create new usage element
                new_usage = Usage()
                new_usage.timestamp = ts
                new_usage.client_id = client_id
                result_map[ts] = new_usage

            # increment by used credits
            result_map[ts].credits += item.credits

        # return sorted (by timestamp) list of usage elements
        return list(sorted(result_map.values(), key=lambda x: x.timestamp))

    def delete_client_usage(self, client_id: Union[str, int], start_datetime: Optional[datetime] = None,
                            end_datetime: Optional[datetime] = None):
        # compose query
        query = _compose_query(client_id, start_datetime, end_datetime)
        # finally execute the delete
        self.delete_many(query)
