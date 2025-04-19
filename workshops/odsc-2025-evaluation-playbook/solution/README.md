

Qdrant is now accessible:
- REST API: localhost:6333
- Web UI: localhost:6333/dashboard
- GRPC API: localhost:6334


Visualize:
```
{
  "limit": 500,
   "filter": {
        "must": [
            { "key": "metadata.philosopher_id", "match": { "value": "plato" } }
        ]
    }
}
```



Graph
```
{
  "sample": 400,
  "filter": {
        "must": [
            { "key": "metadata.philosopher_id", "match": { "value": "plato" } }
        ]
    }
}
```