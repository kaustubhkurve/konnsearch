import pytest


@pytest.fixture()
def sample_event():
    return {
            "before": None,
            "after": {
                "key": "c/5cc359ab-f698-42a2-be2a-d0c04671beb1/o/node/81699782-77b4-4f4b-9274-af69464ff74f",
                "value": {
                    "type": 3,
                    "object": {
                        "id": "81699782-77b4-4f4b-9274-af69464ff74f",
                        "type": "kong-proxy",
                        "labels": {
                            "region": "us-east-2",
                            "provider": "aws",
                            "managed-by": "Konnect",
                            "network-id": "b2b7a7c2-d358-461f-ab1b-fad7efd113cd",
                            "dp-group-id": "1d51afff-7fe5-4fa5-a769-d531e210bd60"
                        },
                        "version": "3.4.3.3",
                        "hostname": "dataplane-1d51afff-7fe5-4fa5-a769-d531e210bd60-6s4ps-76d7fqc8zt",
                        "last_ping": 1706837758,
                        "created_at": 1706733198,
                        "updated_at": 1706837758,
                        "config_hash": "a67894e276cfa3dba67894e276cfa3db",
                        "process_conf": {
                            "plugins": ["bundled"],
                            "lmdb_map_size": "2048m",
                            "router_flavor": "traditional_compatible",
                            "cluster_max_payload": 16777216
                        },
                        "connection_state": {"is_connected": False},
                        "data_plane_cert_id": "1ca698f3-5601-4f81-9e5f-6aa7a31ca366"
                    }
                }
            },
            "op": "c",
            "ts_ms": 1706837894379
        }


@pytest.fixture()
def sample_events(sample_event):
    return [sample_event] * 12
