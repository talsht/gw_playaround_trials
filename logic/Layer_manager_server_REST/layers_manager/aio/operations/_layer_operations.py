# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.2.4, generator: {generator})
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Generic, Optional, TypeVar
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse, HttpRequest

from ... import models as _models

T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class LayerOperations:
    """LayerOperations async operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~layers_manager.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    async def layer_id_entities_entity_id_get(
        self,
        layer_id: int,
        entity_id: int,
        **kwargs
    ) -> Optional["_models.Entity"]:
        """Get an entity by id.

        Get an entity by id.

        :param layer_id: The layer id.
        :type layer_id: int
        :param entity_id: The entity id.
        :type entity_id: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Entity, or the result of cls(response)
        :rtype: ~layers_manager.models.Entity or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.Entity"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        accept = "application/json"

        # Construct URL
        url = self.layer_id_entities_entity_id_get.metadata['url']  # type: ignore
        path_format_arguments = {
            'layerId': self._serialize.url("layer_id", layer_id, 'int', div=','),
            'entityId': self._serialize.url("entity_id", entity_id, 'int', div=','),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 400, 404, 500]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Entity', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    layer_id_entities_entity_id_get.metadata = {'url': '/layer/{layerId}/entities/{entityId}'}  # type: ignore

    async def layer_id_entities_entity_id_put(
        self,
        layer_id: int,
        entity_id: int,
        body: "_models.Entity",
        **kwargs
    ) -> Optional["_models.Entity"]:
        """Update an entity by id.

        Update an entity by id.

        :param layer_id: The layer id.
        :type layer_id: int
        :param entity_id: The entity id.
        :type entity_id: int
        :param body:
        :type body: ~layers_manager.models.Entity
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Entity, or the result of cls(response)
        :rtype: ~layers_manager.models.Entity or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.Entity"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.layer_id_entities_entity_id_put.metadata['url']  # type: ignore
        path_format_arguments = {
            'layerId': self._serialize.url("layer_id", layer_id, 'int', div=','),
            'entityId': self._serialize.url("entity_id", entity_id, 'int', div=','),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(body, 'Entity')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 400, 404, 500]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Entity', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    layer_id_entities_entity_id_put.metadata = {'url': '/layer/{layerId}/entities/{entityId}'}  # type: ignore

    async def layer_id_entities_entity_id_delete(
        self,
        layer_id: int,
        entity_id: int,
        **kwargs
    ) -> Optional["_models.Entity"]:
        """Delete an entity by id.

        Delete an entity by id.

        :param layer_id: The layer id.
        :type layer_id: int
        :param entity_id: The entity id.
        :type entity_id: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Entity, or the result of cls(response)
        :rtype: ~layers_manager.models.Entity or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.Entity"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        accept = "application/json"

        # Construct URL
        url = self.layer_id_entities_entity_id_delete.metadata['url']  # type: ignore
        path_format_arguments = {
            'layerId': self._serialize.url("layer_id", layer_id, 'int', div=','),
            'entityId': self._serialize.url("entity_id", entity_id, 'int', div=','),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 400, 404, 500]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Entity', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    layer_id_entities_entity_id_delete.metadata = {'url': '/layer/{layerId}/entities/{entityId}'}  # type: ignore