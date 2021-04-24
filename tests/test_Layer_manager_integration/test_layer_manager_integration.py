import time

import pytest
from bson import ObjectId
from faker import Faker
import random
from logging import Logger

from logic.Layer_manager_server_REST.layer_manager_utils import create_and_validate_layer, delete_layer, update_layer, \
    add_entities_to_layer, get_entity_in_layer, change_entity_in_layer, query_layers_for_entities
from logic.Layer_manager_server_REST.layers_manager.models import LayerRequest, LayerQueryRequest, EntityRequest, Point, \
    Feature
from infra.MongoDBUtils import MyMongoCollection
from logic.Layer_manager_gw_graphQL import LayerManagerGWClient

fake = Faker()

LAYER_NAME = "vehicles"

coordinates_and_headings = [
    (0, 85, 0),
    (0, -85, 180),
    (180, 0, 90),
    (-180, 0, 270)
]

def validate_layer_creation_in_db(mongodb_client: MyMongoCollection, layer_id, layer_name:str, get_log: Logger):
    docs = mongodb_client.get_doc_by_query(query={"_id": ObjectId(layer_id)})
    assert len(docs) == 1 and docs[0]["name"] == layer_name, get_log.error("unable to validate layer creation in Mongo")

def validate_layer_creation_in_gw(layer_manager_gw_client:LayerManagerGWClient, layer_id, layer_name:str, get_log: Logger):
    layers = layer_manager_gw_client.get_layers_as_feature(layers_subset=[str(layer_id)])
    assert len(layers) == 1 and layers[0].name == layer_name, get_log.error("unable to validate layer creation in GW")

def validate_entity_creation_in_db(mongodb_client_aircrafts: MyMongoCollection, get_log: Logger, entity_id, entity_name:str):
    entity = mongodb_client_aircrafts.get_doc_by_query(query={"_id": ObjectId(entity_id)})
    entities = mongodb_client_aircrafts.list_all_docs()

    assert len(entity) == 1 and entity[0]["name"] == entity_name, get_log.error("unable to validate entity creation in Mongo")

def validate_entity_creation_in_gw(layer_manager_gw_client:LayerManagerGWClient, layer_id, entity_id, entity_name:str, get_log: Logger):
    layers = layer_manager_gw_client.get_layers_as_feature(layers_subset=[str(layer_id)])

    for entity in layers[0].entities:
        if entity.name == entity_name and entity.id == entity_id:
            return

    assert False, get_log.error("unable to validate entity creation in GW")

@pytest.mark.integration
class Test_layer_manager():
    @staticmethod
    def test_create_and_validate_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log)
        validate_layer_creation_in_db(mongodb_client, layer_id, layer_name, get_log)
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)

    @staticmethod
    def test_read_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        for i in range(10):
            layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
            validate_layer_creation_in_db(mongodb_client, layer_id, layer_name, get_log)
            validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)

    @staticmethod
    def test_update_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)
        updated_layer_id, updated_layer_name = update_layer(layer_manager_client, layer_id, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        validate_layer_creation_in_db(mongodb_client, updated_layer_id, updated_layer_name, get_log)
        validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, updated_layer_name, get_log)

        try:
            validate_layer_creation_in_gw(layer_manager_gw_client, layer_id, layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False

    @staticmethod
    def test_delete_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=fake.unique.first_name()))
        deleted_layer_id, deleted_layer_name = delete_layer(layer_manager_client, layer_id=layer_id, get_log=get_log)

        try:
            validate_layer_creation_in_db(mongodb_client, deleted_layer_id, deleted_layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False

        try:
            validate_layer_creation_in_gw(layer_manager_gw_client, deleted_layer_id, deleted_layer_name, get_log)
        except AssertionError:
            assert True
        else:
            assert False


    @staticmethod
    def test_add_entity_to_layer(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, mongodb_client_aircrafts, layer_manager_gw_client, get_status):
        layer_id, layer_name = create_and_validate_layer(layer_manager_client, get_log, layer_body=LayerRequest(name=LAYER_NAME))
        for i in range(10):
            new_entity_name = f"{fake.unique.first_name()}_{i}"
            new_entity = EntityRequest(layer_id=layer_id,
                                       name=new_entity_name,
                                       type="BMW",
                                       geo_data=Feature(
                                           geometry=Point(coordinates=[random.randint(-180, 180), random.randint(-90, 90)]),
                                           properties={"heading": random.randint(0, 3) * 90}))

            new_entity_post_request = add_entities_to_layer(layer_manager_client=layer_manager_client,
                                                            get_log=get_log,
                                                            layer_id=layer_id,
                                                            entity_request_body_list=[new_entity])
            validate_entity_creation_in_gw(layer_manager_gw_client, layer_id, new_entity_post_request[0].id, new_entity_post_request[0].name, get_log)
            validate_entity_creation_in_db(mongodb_client_aircrafts, get_log, entity_id=new_entity_post_request[0].id, entity_name=new_entity_name)

@pytest.mark.e2e
class Test_scenaios(object):
    @staticmethod
    def test_scenario_add_random_entities(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        new_layer = LayerRequest(name=LAYER_NAME)
        layer_id, layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client,
                                                         get_log=get_log,
                                                         layer_body=new_layer)

        for i in range(20):
            new_entity_name = f"{fake.unique.first_name()}_{i}"
            new_entity = EntityRequest(layer_id=layer_id,
                                       name=new_entity_name,
                                       type="BMW",
                                       geo_data=Feature(geometry=Point(coordinates=[random.randint(-180, 180), random.randint(-90, 90)]),
                                                        properties={"heading": random.randint(0, 3) * 90}))
            new_entity_post_request = add_entities_to_layer(layer_manager_client=layer_manager_client,
                                                             get_log=get_log,
                                                             layer_id=layer_id,
                                                             entity_request_body_list=[new_entity])

        while (1):
            query = LayerQueryRequest(layers=[layer_id])
            query_results = query_layers_for_entities(layer_manager_client=layer_manager_client,
                                                      get_log=get_log,
                                                      layer_request=query)

            for entity in query_results[0].entities:
                coordinates = entity.geo_data["geometry"]["coordinates"]
                heading = entity.geo_data["properties"]["heading"]

                long_factor, lat_factor = decide_factors(heading)

                new_coordinates = [((coordinates[0] + long_factor * 0.1) % 180),
                                   ((coordinates[1] + lat_factor * 0.1) % 90)]
                changed_entity = EntityRequest(layer_id=layer_id, name=entity.name, type="BMW",
                                           geo_data=Feature(geometry=Point(coordinates=new_coordinates), properties={"heading": heading}))
                put_result = change_entity_in_layer(layer_manager_client=layer_manager_client,
                                                     get_log=get_log,
                                                     layer_id=layer_id,
                                                     entity_id=entity.id,
                                                     entity_request_body_change=changed_entity)

            time.sleep(1)

    @staticmethod
    def test_scenario_add_lots_of_planes_at_once(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        new_layer_id, new_layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client,
                                                                 get_log=get_log,
                                                                 layer_body=LayerRequest(name=LAYER_NAME))
        entity_list = {}
        for i in range(500):
            new_entity_name = f"target_{i}"
            entity_request_body_list = [EntityRequest(layer_id=new_layer_id,
                                                      name=new_entity_name,
                                                      type="BMW",
                                                      geo_data=Feature(geometry=Point(coordinates=[random.randint(-180, 180), random.randint(-90, 90)]),
                                                      properties={"heading": random.randint(0, 3) * 90}))]
            add_response = add_entities_to_layer(layer_manager_client=layer_manager_client,
                                                 get_log=get_log,
                                                 layer_id=new_layer_id,
                                                 entity_request_body_list=entity_request_body_list)
            entity_list[i] = {"id": add_response[0].id,
                              "long": add_response[0].geo_data["geometry"]["coordinates"][0],
                              "lat": add_response[0].geo_data["geometry"]["coordinates"][1],
                              "heading": add_response[0].geo_data["properties"]["heading"]}

        while (1):
            for i in range(500):
                entity_get = get_entity_in_layer(layer_manager_client=layer_manager_client,
                                                 get_log=get_log,
                                                 layer_id=new_layer_id,
                                                 entity_id=entity_list[i]["id"])

                assert entity_get.id == entity_list[i]["id"]
                heading = entity_get.geo_data["properties"]["heading"]
                x_factor, y_factor = decide_factors(heading)

                entity_list[i]["long"] = (entity_list[i]["long"] + x_factor * 0.1) % 180
                entity_list[i]["lat"] = (entity_list[i]["lat"] + y_factor * 0.1) % 90

                entity_change = change_entity_in_layer(layer_manager_client=layer_manager_client,
                                                       get_log=get_log,
                                                       layer_id=new_layer_id,
                                                       entity_id=entity_get.id,
                                                       entity_request_body_change=EntityRequest(name=entity_get.name,
                                                                                                layer_id=new_layer_id,
                                                                                                type=entity_get.type,
                                                                                                geo_data=Feature(geometry=Point(coordinates=[entity_list[i]["long"], entity_list[i]["lat"]]),
                                                                                                                 properties={"heading": heading})))

                assert entity_get.updated_at != entity_change.updated_at




    @staticmethod
    def test_scenario_add_multiple_of_planes_at_once_in_same_location(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        new_layer_id, new_layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client,
                                                                 get_log=get_log,
                                                                 layer_body=LayerRequest(name=LAYER_NAME))
        entity_list = {}
        for i in range(30):
            new_entity_name = f"target_{i}"
            entity_request_body_list = [EntityRequest(layer_id=new_layer_id,
                                                      name=new_entity_name,
                                                      type="BMW",
                                                      geo_data=Feature(geometry=Point(coordinates=[0.0001 * i , 0.0001 * i]),
                                                      properties={"heading": i % 4 * 90}))]
            add_response = add_entities_to_layer(layer_manager_client=layer_manager_client,
                                                 get_log=get_log,
                                                 layer_id=new_layer_id,
                                                 entity_request_body_list=entity_request_body_list)
            entity_list[i] = {"id": add_response[0].id,
                              "long": add_response[0].geo_data["geometry"]["coordinates"][0],
                              "lat": add_response[0].geo_data["geometry"]["coordinates"][1],
                              "heading": add_response[0].geo_data["properties"]["heading"]}



    @staticmethod
    def test_scenario_add_plane_near_map_borders(get_function_name, get_log, get_config, layer_manager_client, delete_db, mongodb_client, layer_manager_gw_client, get_status):
        new_layer_id, new_layer_name = create_and_validate_layer(layer_manager_client=layer_manager_client,
                                                                 get_log=get_log,
                                                                 layer_body=LayerRequest(name=LAYER_NAME))
        entity_list = {}
        for i in range(4):
            new_entity_name = f"target_{i}"
            entity_request_body_list = [EntityRequest(layer_id=new_layer_id,
                                                      name=new_entity_name,
                                                      type="BMW",
                                                      geo_data=Feature(geometry=Point(coordinates=[coordinates_and_headings[i%4][0], coordinates_and_headings[i%4][1]]),
                                                      properties={"heading": coordinates_and_headings[i%4][2]}))]
            add_response = add_entities_to_layer(layer_manager_client=layer_manager_client,
                                                 get_log=get_log,
                                                 layer_id=new_layer_id,
                                                 entity_request_body_list=entity_request_body_list)
            entity_list[i] = {"id": add_response[0].id,
                              "long": add_response[0].geo_data["geometry"]["coordinates"][0],
                              "lat": add_response[0].geo_data["geometry"]["coordinates"][1],
                              "heading": add_response[0].geo_data["properties"]["heading"]}

        while (1):
            for i in range(4):
                entity_get = get_entity_in_layer(layer_manager_client=layer_manager_client,
                                                 get_log=get_log,
                                                 layer_id=new_layer_id,
                                                 entity_id=entity_list[i]["id"])

                assert entity_get.id == entity_list[i]["id"]
                heading = entity_get.geo_data["properties"]["heading"]
                x_factor, y_factor = decide_factors(heading)

                entity_list[i]["long"] = (entity_list[i]["long"] + x_factor * 0.1) % 180
                entity_list[i]["lat"] = (entity_list[i]["lat"] + y_factor * 0.1) % 90

                entity_change = change_entity_in_layer(layer_manager_client=layer_manager_client,
                                                       get_log=get_log,
                                                       layer_id=new_layer_id,
                                                       entity_id=entity_get.id,
                                                       entity_request_body_change=EntityRequest(
                                                           name=entity_get.name,
                                                           layer_id=new_layer_id,
                                                           type=entity_get.type,
                                                           geo_data=Feature(geometry=Point(
                                                               coordinates=[entity_list[i]["long"],
                                                                            entity_list[i]["lat"]]),
                                                                            properties={"heading": heading})))

                assert entity_get.updated_at != entity_change.updated_at



def decide_factors(heading):
    x_factor, y_factor = 0, 0

    if heading == 0:
        y_factor = 1
    if heading == 180:
        y_factor = -1
    if heading == 90:
        x_factor = 1
    if heading == 270:
        x_factor = -1

    return x_factor, y_factor








