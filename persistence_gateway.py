class PersistenceGateway:
    def __init__(self, client):
        self.client = client
        self.db = self.client["mydatabase"]

    def update(self, collection, id_, data_dictionary):
        data_dictionary["_id"] = id_
        result = self.db[collection].replace_one({"_id": id_}, data_dictionary)
        if result.matched_count == 0:
            raise ItemNotFound()