import os
import pytest
from definitions import OPENAPI_CONFIG_PATH, OPENAPI_SCHEMA
from logic.Layer_manager_server_REST import LayerManagerValidationClient


@pytest.mark.parametrize("server", [('layer_rest_server_url')])
def test_add_layers(get_function_name, get_log, get_config, server, get_status):
    generator = LayerManagerValidationClient(endpoint=get_config["SERVICES"][server],
                                             schema=os.path.abspath(OPENAPI_SCHEMA),
                                             generator_config=os.path.abspath(OPENAPI_CONFIG_PATH),
                                             headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                             log=get_log)

    assert generator.check_add_layer_valid()
    assert generator.check_add_layer_invalid()

@pytest.mark.parametrize("server", [('layer_rest_server_url')])
def test_layers_query(get_function_name, get_log, get_config, server, get_status):
    generator = LayerManagerValidationClient(endpoint=get_config["SERVICES"][server],
                                             schema=os.path.abspath(OPENAPI_SCHEMA),
                                             generator_config=os.path.abspath(OPENAPI_CONFIG_PATH),
                                             headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                             log=get_log)

    assert generator.check_layer_query_valid()
    assert generator.check_layer_query_invalid()

@pytest.mark.parametrize("server", [('layer_rest_server_url')])
def test_layers_change(get_function_name, get_log, get_config, server, get_status):
    generator = LayerManagerValidationClient(endpoint=get_config["SERVICES"][server],
                                             schema=os.path.abspath(OPENAPI_SCHEMA),
                                             generator_config=os.path.abspath(OPENAPI_CONFIG_PATH),
                                             headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                             log=get_log)

    assert generator.check_layer_change_valid()
    assert generator.check_layer_change_invalid()

@pytest.mark.parametrize("server", [('layer_rest_server_url')])
def test_add_entity_to_layer(get_function_name, get_log, get_config, server, get_status):
    generator = LayerManagerValidationClient(endpoint=get_config["SERVICES"][server],
                                             schema=os.path.abspath(OPENAPI_SCHEMA),
                                             generator_config=os.path.abspath(OPENAPI_CONFIG_PATH),
                                             headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                             log=get_log)

    assert generator.check_add_entity_to_layer_valid()
    assert generator.check_add_entity_to_layer_invalid()