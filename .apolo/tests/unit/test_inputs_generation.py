import pytest
from apolo_app_types.protocols.common import ApoloSecret, IngressHttp, Preset
from apolo_app_types_fixtures.constants import (
    APP_ID,
    APP_SECRETS_NAME,
    DEFAULT_NAMESPACE,
    DEFAULT_POSTGRES_CREDS,
)
from apolo_apps_superset.types import (
    SupersetInputs,
    SupersetPostgresConfig,
    SupersetUserConfig,
    WebConfig,
    WorkerConfig,
)


@pytest.mark.asyncio
async def test_superset_basic_values_generation(setup_clients, mock_get_preset_cpu):
    from apolo_apps_superset.inputs_processor import SupersetInputsProcessor

    apolo_client = setup_clients
    processor = SupersetInputsProcessor(apolo_client)
    helm_params = await processor.gen_extra_values(
        input_=SupersetInputs(
            worker_config=WorkerConfig(preset=Preset(name="cpu-large")),
            web_config=WebConfig(preset=Preset(name="cpu-large")),
            ingress_http=IngressHttp(),
            postgres_config=SupersetPostgresConfig(preset=Preset(name="cpu-large")),
            redis_preset=Preset(name="cpu-large"),
        ),
        app_name="superset",
        namespace=DEFAULT_NAMESPACE,
        app_secrets_name=APP_SECRETS_NAME,
        app_id=APP_ID,
    )

    assert helm_params["supersetNode"] == {
        "affinity": {
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "platform.neuromation.io/nodepool",
                                    "operator": "In",
                                    "values": ["cpu_pool"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "apolo_app_id": APP_ID,
        "connections": {
            "db_host": helm_params["postgresql"]["fullnameOverride"],
            "redis_host": f"{helm_params['redis']['fullnameOverride']}-headless",
        },
        "podLabels": {
            "platform.apolo.us/component": "app",
            "platform.apolo.us/preset": "cpu-large",
        },
        "preset_name": "cpu-large",
        "resources": {
            "limits": {"cpu": "4000.0m", "memory": "0M"},
            "requests": {"cpu": "4000.0m", "memory": "0M"},
        },
        "tolerations": [
            {
                "effect": "NoSchedule",
                "key": "platform.neuromation.io/job",
                "operator": "Exists",
            },
            {
                "effect": "NoExecute",
                "key": "node.kubernetes.io/not-ready",
                "operator": "Exists",
                "tolerationSeconds": 300,
            },
            {
                "effect": "NoExecute",
                "key": "node.kubernetes.io/unreachable",
                "operator": "Exists",
                "tolerationSeconds": 300,
            },
        ],
    }
    assert helm_params["postgresql"] == {
        "fullnameOverride": helm_params["postgresql"]["fullnameOverride"],
        "primary": {
            "affinity": {
                "nodeAffinity": {
                    "requiredDuringSchedulingIgnoredDuringExecution": {
                        "nodeSelectorTerms": [
                            {
                                "matchExpressions": [
                                    {
                                        "key": "platform.neuromation.io/nodepool",
                                        "operator": "In",
                                        "values": ["cpu_pool"],
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            "resources": {
                "limits": {"cpu": "4000.0m", "memory": "0M"},
                "requests": {"cpu": "4000.0m", "memory": "0M"},
            },
            "tolerations": [
                {
                    "effect": "NoSchedule",
                    "key": "platform.neuromation.io/job",
                    "operator": "Exists",
                },
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "tolerationSeconds": 300,
                },
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "tolerationSeconds": 300,
                },
            ],
            "apolo_app_id": APP_ID,
            "podLabels": {
                "platform.apolo.us/component": "app",
                "platform.apolo.us/preset": "cpu-large",
            },
            "preset_name": "cpu-large",
        },
    }
    assert helm_params["redis"] == {
        "fullnameOverride": helm_params["redis"]["fullnameOverride"],
        "master": {
            "preset_name": "cpu-large",
            "apolo_app_id": APP_ID,
            "podLabels": {
                "platform.apolo.us/component": "app",
                "platform.apolo.us/preset": "cpu-large",
            },
            "affinity": {
                "nodeAffinity": {
                    "requiredDuringSchedulingIgnoredDuringExecution": {
                        "nodeSelectorTerms": [
                            {
                                "matchExpressions": [
                                    {
                                        "key": "platform.neuromation.io/nodepool",
                                        "operator": "In",
                                        "values": ["cpu_pool"],
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            "resources": {
                "limits": {"cpu": "4000.0m", "memory": "0M"},
                "requests": {"cpu": "4000.0m", "memory": "0M"},
            },
            "tolerations": [
                {
                    "effect": "NoSchedule",
                    "key": "platform.neuromation.io/job",
                    "operator": "Exists",
                },
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "tolerationSeconds": 300,
                },
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "tolerationSeconds": 300,
                },
            ],
        },
    }
    assert helm_params["supersetWorker"] == {
        "apolo_app_id": APP_ID,
        "affinity": {
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "platform.neuromation.io/nodepool",
                                    "operator": "In",
                                    "values": ["cpu_pool"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "podLabels": {
            "platform.apolo.us/component": "worker",
            "platform.apolo.us/preset": "cpu-large",
        },
        "preset_name": "cpu-large",
        "resources": {
            "limits": {"cpu": "4000.0m", "memory": "0M"},
            "requests": {"cpu": "4000.0m", "memory": "0M"},
        },
        "tolerations": [
            {
                "effect": "NoSchedule",
                "key": "platform.neuromation.io/job",
                "operator": "Exists",
            },
            {
                "effect": "NoExecute",
                "key": "node.kubernetes.io/not-ready",
                "operator": "Exists",
                "tolerationSeconds": 300,
            },
            {
                "effect": "NoExecute",
                "key": "node.kubernetes.io/unreachable",
                "operator": "Exists",
                "tolerationSeconds": 300,
            },
        ],
    }
    assert helm_params["init"] == {
        "adminUser": {
            "email": "admin@superset.com",
            "firstname": "Superset",
            "lastname": "Admin",
            "password": "admin",
            "username": "admin",
        }
    }
    assert helm_params["extraSecretEnv"]["SUPERSET_SECRET_KEY"]

    # Verify Superset gets ONLY auth middleware (no strip headers)
    assert (
        helm_params["ingress"]["annotations"][
            "traefik.ingress.kubernetes.io/router.middlewares"
        ]
        == "platform-platform-control-plane-ingress-auth@kubernetescrd"
    )

    assert helm_params["postgresql"]["fullnameOverride"].startswith("superset-")
    assert helm_params["redis"]["fullnameOverride"].startswith("superset-")
    assert (
        helm_params["postgresql"]["fullnameOverride"]
        != helm_params["redis"]["fullnameOverride"]
    )


def test_superset_resource_names_are_short_and_unique():
    from apolo_apps_superset.inputs_processor import _make_short_resource_name

    long_app_id = "super-long-app-id-" + ("x" * 80)
    postgres_fullname = _make_short_resource_name(long_app_id, "postgresql")
    redis_fullname = _make_short_resource_name(long_app_id, "redis")

    assert len(postgres_fullname) <= 63
    assert len(redis_fullname) <= 63
    assert postgres_fullname != redis_fullname
    assert postgres_fullname.startswith("superset-")
    assert redis_fullname.startswith("superset-")


@pytest.mark.asyncio
async def test_superset_values_generation_with_postgres_integration(
    setup_clients, mock_get_preset_cpu
):
    from apolo_apps_superset.inputs_processor import SupersetInputsProcessor

    apolo_client = setup_clients
    processor = SupersetInputsProcessor(apolo_client)
    helm_params = await processor.gen_extra_values(
        input_=SupersetInputs(
            worker_config=WorkerConfig(preset=Preset(name="cpu-large")),
            web_config=WebConfig(preset=Preset(name="cpu-large")),
            ingress_http=IngressHttp(),
            postgres_config=DEFAULT_POSTGRES_CREDS,
            redis_preset=Preset(name="cpu-large"),
        ),
        app_name="superset",
        namespace=DEFAULT_NAMESPACE,
        app_secrets_name=APP_SECRETS_NAME,
        app_id=APP_ID,
    )
    assert not helm_params["postgresql"]["enabled"]
    assert helm_params["supersetNode"]["connections"] == {
        "db_host": "pgbouncer_host",
        "db_name": "db_name",
        "db_pass": ApoloSecret(key="pgvector_password"),
        "db_port": 4321,
        "db_user": "pgvector_user",
        "redis_host": f"{helm_params['redis']['fullnameOverride']}-headless",
    }


@pytest.mark.asyncio
async def test_superset_values_generation_with_custom_admin_user(
    setup_clients, mock_get_preset_cpu
):
    from apolo_apps_superset.inputs_processor import SupersetInputsProcessor

    apolo_client = setup_clients
    processor = SupersetInputsProcessor(apolo_client)
    custom_admin_password = "".join(["My", "Crazy", "Pass"])
    helm_params = await processor.gen_extra_values(
        input_=SupersetInputs(
            worker_config=WorkerConfig(preset=Preset(name="cpu-large")),
            web_config=WebConfig(preset=Preset(name="cpu-large")),
            ingress_http=IngressHttp(),
            admin_user=SupersetUserConfig(
                username="some_other_admin_user",
                firstname="Superset",
                lastname="Admin",
                password=custom_admin_password,
                email="admin@mail.ua",
            ),
            postgres_config=SupersetPostgresConfig(preset=Preset(name="cpu-large")),
            redis_preset=Preset(name="cpu-large"),
        ),
        app_name="superset",
        namespace=DEFAULT_NAMESPACE,
        app_secrets_name=APP_SECRETS_NAME,
        app_id=APP_ID,
    )
    assert helm_params["init"]["adminUser"] == {
        "email": "admin@mail.ua",
        "firstname": "Superset",
        "lastname": "Admin",
        "password": "MyCrazyPass",
        "username": "some_other_admin_user",
    }
