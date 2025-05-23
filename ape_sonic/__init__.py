from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from .ecosystem import SonicConfig

    return SonicConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    from .ecosystem import Sonic

    yield Sonic


@plugins.register(plugins.NetworkPlugin)
def networks():
    from ape.api.networks import (
        LOCAL_NETWORK_NAME,
        ForkedNetworkAPI,
        NetworkAPI,
        create_network_type,
    )

    from .ecosystem import NETWORKS

    for network_name, network_params in NETWORKS.items():
        yield "sonic", network_name, create_network_type(*network_params)
        yield "sonic", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for development providers, as they get chain_id from themselves
    yield "sonic", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape.api.networks import LOCAL_NETWORK_NAME
    from ape_node import Node
    from ape_test import LocalProvider

    from .ecosystem import NETWORKS

    for network_name in NETWORKS:
        yield "sonic", network_name, Node

    yield "sonic", LOCAL_NETWORK_NAME, LocalProvider


def __getattr__(name: str):
    if name == "NETWORKS":
        from .ecosystem import NETWORKS

        return NETWORKS

    elif name == "Sonic":
        from .ecosystem import Sonic

        return Sonic

    elif name == "SonicConfig":
        from .ecosystem import SonicConfig

        return SonicConfig

    else:
        raise AttributeError(name)


__all__ = [
    "NETWORKS",
    "Sonic",
    "SonicConfig",
]