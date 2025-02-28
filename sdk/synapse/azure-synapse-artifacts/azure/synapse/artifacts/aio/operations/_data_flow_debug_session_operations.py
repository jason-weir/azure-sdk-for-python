# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import functools
from typing import Any, AsyncIterable, Callable, Dict, Generic, Optional, TypeVar, Union
import warnings

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.polling import AsyncLROPoller, AsyncNoPolling, AsyncPollingMethod
from azure.core.polling.async_base_polling import AsyncLROBasePolling
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._data_flow_debug_session_operations import build_add_data_flow_request, build_create_data_flow_debug_session_request_initial, build_delete_data_flow_debug_session_request, build_execute_command_request_initial, build_query_data_flow_debug_sessions_by_workspace_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class DataFlowDebugSessionOperations:
    """DataFlowDebugSessionOperations async operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.synapse.artifacts.models
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

    async def _create_data_flow_debug_session_initial(
        self,
        request: "_models.CreateDataFlowDebugSessionRequest",
        **kwargs: Any
    ) -> Optional["_models.CreateDataFlowDebugSessionResponse"]:
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.CreateDataFlowDebugSessionResponse"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(request, 'CreateDataFlowDebugSessionRequest')

        request = build_create_data_flow_debug_session_request_initial(
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._create_data_flow_debug_session_initial.metadata['url'],
        )
        request = _convert_request(request)
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = None
        response_headers = {}
        if response.status_code == 200:
            deserialized = self._deserialize('CreateDataFlowDebugSessionResponse', pipeline_response)

        if response.status_code == 202:
            response_headers['location']=self._deserialize('str', response.headers.get('location'))
            

        if cls:
            return cls(pipeline_response, deserialized, response_headers)

        return deserialized

    _create_data_flow_debug_session_initial.metadata = {'url': '/createDataFlowDebugSession'}  # type: ignore


    @distributed_trace_async
    async def begin_create_data_flow_debug_session(
        self,
        request: "_models.CreateDataFlowDebugSessionRequest",
        **kwargs: Any
    ) -> AsyncLROPoller["_models.CreateDataFlowDebugSessionResponse"]:
        """Creates a data flow debug session.

        :param request: Data flow debug session definition.
        :type request: ~azure.synapse.artifacts.models.CreateDataFlowDebugSessionRequest
        :keyword api_version: Api Version. The default value is "2020-12-01". Note that overriding this
         default value may result in unsupported behavior.
        :paramtype api_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncLROBasePolling. Pass in False
         for this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either CreateDataFlowDebugSessionResponse
         or the result of cls(response)
        :rtype:
         ~azure.core.polling.AsyncLROPoller[~azure.synapse.artifacts.models.CreateDataFlowDebugSessionResponse]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, azure.core.polling.AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.CreateDataFlowDebugSessionResponse"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._create_data_flow_debug_session_initial(
                request=request,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            response = pipeline_response.http_response
            deserialized = self._deserialize('CreateDataFlowDebugSessionResponse', pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized


        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }

        if polling is True: polling_method = AsyncLROBasePolling(lro_delay, path_format_arguments=path_format_arguments, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        else:
            return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_create_data_flow_debug_session.metadata = {'url': '/createDataFlowDebugSession'}  # type: ignore

    @distributed_trace
    def query_data_flow_debug_sessions_by_workspace(
        self,
        **kwargs: Any
    ) -> AsyncIterable["_models.QueryDataFlowDebugSessionsResponse"]:
        """Query all active data flow debug sessions.

        :keyword api_version: Api Version. The default value is "2020-12-01". Note that overriding this
         default value may result in unsupported behavior.
        :paramtype api_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either QueryDataFlowDebugSessionsResponse or the result
         of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.synapse.artifacts.models.QueryDataFlowDebugSessionsResponse]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.QueryDataFlowDebugSessionsResponse"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_query_data_flow_debug_sessions_by_workspace_request(
                    api_version=api_version,
                    template_url=self.query_data_flow_debug_sessions_by_workspace.metadata['url'],
                )
                request = _convert_request(request)
                path_format_arguments = {
                    "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
                }
                request.url = self._client.format_url(request.url, **path_format_arguments)

            else:
                
                request = build_query_data_flow_debug_sessions_by_workspace_request(
                    api_version=api_version,
                    template_url=next_link,
                )
                request = _convert_request(request)
                path_format_arguments = {
                    "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
                }
                request.url = self._client.format_url(request.url, **path_format_arguments)

                path_format_arguments = {
                    "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
                }
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("QueryDataFlowDebugSessionsResponse", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.CloudErrorAutoGenerated, pipeline_response)
                raise HttpResponseError(response=response, model=error)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    query_data_flow_debug_sessions_by_workspace.metadata = {'url': '/queryDataFlowDebugSessions'}  # type: ignore

    @distributed_trace_async
    async def add_data_flow(
        self,
        request: "_models.DataFlowDebugPackage",
        **kwargs: Any
    ) -> "_models.AddDataFlowToDebugSessionResponse":
        """Add a data flow into debug session.

        :param request: Data flow debug session definition with debug content.
        :type request: ~azure.synapse.artifacts.models.DataFlowDebugPackage
        :keyword api_version: Api Version. The default value is "2020-12-01". Note that overriding this
         default value may result in unsupported behavior.
        :paramtype api_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AddDataFlowToDebugSessionResponse, or the result of cls(response)
        :rtype: ~azure.synapse.artifacts.models.AddDataFlowToDebugSessionResponse
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.AddDataFlowToDebugSessionResponse"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(request, 'DataFlowDebugPackage')

        request = build_add_data_flow_request(
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.add_data_flow.metadata['url'],
        )
        request = _convert_request(request)
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.CloudErrorAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('AddDataFlowToDebugSessionResponse', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    add_data_flow.metadata = {'url': '/addDataFlowToDebugSession'}  # type: ignore


    @distributed_trace_async
    async def delete_data_flow_debug_session(
        self,
        request: "_models.DeleteDataFlowDebugSessionRequest",
        **kwargs: Any
    ) -> None:
        """Deletes a data flow debug session.

        :param request: Data flow debug session definition for deletion.
        :type request: ~azure.synapse.artifacts.models.DeleteDataFlowDebugSessionRequest
        :keyword api_version: Api Version. The default value is "2020-12-01". Note that overriding this
         default value may result in unsupported behavior.
        :paramtype api_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(request, 'DeleteDataFlowDebugSessionRequest')

        request = build_delete_data_flow_debug_session_request(
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.delete_data_flow_debug_session.metadata['url'],
        )
        request = _convert_request(request)
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.CloudErrorAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        if cls:
            return cls(pipeline_response, None, {})

    delete_data_flow_debug_session.metadata = {'url': '/deleteDataFlowDebugSession'}  # type: ignore


    async def _execute_command_initial(
        self,
        request: "_models.DataFlowDebugCommandRequest",
        **kwargs: Any
    ) -> Optional["_models.DataFlowDebugCommandResponse"]:
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.DataFlowDebugCommandResponse"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(request, 'DataFlowDebugCommandRequest')

        request = build_execute_command_request_initial(
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self._execute_command_initial.metadata['url'],
        )
        request = _convert_request(request)
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = None
        response_headers = {}
        if response.status_code == 200:
            deserialized = self._deserialize('DataFlowDebugCommandResponse', pipeline_response)

        if response.status_code == 202:
            response_headers['location']=self._deserialize('str', response.headers.get('location'))
            

        if cls:
            return cls(pipeline_response, deserialized, response_headers)

        return deserialized

    _execute_command_initial.metadata = {'url': '/executeDataFlowDebugCommand'}  # type: ignore


    @distributed_trace_async
    async def begin_execute_command(
        self,
        request: "_models.DataFlowDebugCommandRequest",
        **kwargs: Any
    ) -> AsyncLROPoller["_models.DataFlowDebugCommandResponse"]:
        """Execute a data flow debug command.

        :param request: Data flow debug command definition.
        :type request: ~azure.synapse.artifacts.models.DataFlowDebugCommandRequest
        :keyword api_version: Api Version. The default value is "2020-12-01". Note that overriding this
         default value may result in unsupported behavior.
        :paramtype api_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncLROBasePolling. Pass in False
         for this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either DataFlowDebugCommandResponse or the
         result of cls(response)
        :rtype:
         ~azure.core.polling.AsyncLROPoller[~azure.synapse.artifacts.models.DataFlowDebugCommandResponse]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2020-12-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]
        polling = kwargs.pop('polling', True)  # type: Union[bool, azure.core.polling.AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.DataFlowDebugCommandResponse"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._execute_command_initial(
                request=request,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            response = pipeline_response.http_response
            deserialized = self._deserialize('DataFlowDebugCommandResponse', pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized


        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, 'str', skip_quote=True),
        }

        if polling is True: polling_method = AsyncLROBasePolling(lro_delay, path_format_arguments=path_format_arguments, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        else:
            return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_execute_command.metadata = {'url': '/executeDataFlowDebugCommand'}  # type: ignore
