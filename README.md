# Frappy Python Mongo Store for API Billing

Python MongoDB Store Implementation for Tracking [API Billing](https://github.com/ilfrich/frappy-api-billing) Usage.

## Usage

```python
from frappymongoapibilling import UsageStore
from frappyapibilling import ApiBilling

# create the store instance
store = UsageStore(mongo_url="mongodb://localhost:27017", mongo_db="myDatabase", collection_name="apiUsage")

# pass the store instance to the api billing constructor
api_billing = ApiBilling(usage_store=store)
```

See [API Billing Usage](https://github.com/ilfrich/frappy-api-billing#usage) for details on how to use the module.
