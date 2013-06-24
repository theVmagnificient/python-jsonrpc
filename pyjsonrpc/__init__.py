#!/usr/bin/env python
# coding: utf-8

import sys
import traceback
import errors
from jsontools import json, ParseError
from rpcrequest import parse_request_json, create_request_json
from rpcresponse import parse_response_json, Response


class JsonRpc(object):
    """
    JSON-RPC
    """

    def __init__(self, methods = None):
        """
        Initializes the JSON-RPC-Class

        :param methods: Json-RPC-Methods. `None` or dictionary with
            method names as keys and functions as values. Syntax::

                {
                    "<method_name>": <method_function>,
                    ...
                }
        """

        self.methods = methods or {}
        self.methods["system.describe"] = self.system_describe


    def call(self, json_request):
        """
        Do the work

        :param json_request: JSON-RPC-string with one or more JSON-RPC-requests

        :return: JSON-RPC-string with one or more responses.
        """

        # List for the responses
        responses = []

        # List with requests
        requests = parse_request_json(json_request)
        if not isinstance(requests, list):
            requests = [requests]

        # Every JSON-RPC request in a batch of requests
        for request in requests:

            # Request-Data
            jsonrpc = request.get("jsonrpc")
            id = request.get("id")
            method = str(request.get("method", ""))
            if not method in self.methods:
                # Method not found
                responses.append(
                    Response.from_error(
                        errors.MethodNotFound(jsonrpc = jsonrpc, id = id)
                    )
                )
                continue

            # split positional and named params
            positional_params = []
            named_params = {}
            params = request.get("params", [])
            if isinstance(params, list):
                positional_params = params
            elif isinstance(params, dict):
                positional_params = params.get("__args", [])
                if positional_params:
                    del params["__args"]
                named_params = params

            # Call the method with parameters
            try:
                rpc_function = self.methods[method]
                result = rpc_function(*positional_params, **named_params)
                # No return value is OK if we don´t have an ID (=notification)
                if result is None:
                    if id:
                        responses.append(
                            Response.from_error(
                                errors.InternalError(
                                    jsonrpc = jsonrpc,
                                    id = id,
                                    data = u"No result from JSON-RPC method."
                                )
                            )
                        )
                else:
                    # Successful response
                    responses.append(
                        Response(jsonrpc = jsonrpc, id = id, result = result)
                    )
            except TypeError, err:
                traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
                if "takes exactly" in unicode(err) and "arguments" in unicode(err):
                    responses.append(
                        Response.from_error(
                            errors.InvalidParams(
                                jsonrpc = jsonrpc,
                                id = id,
                                data = traceback_info
                            )
                        )
                    )
                else:
                    responses.append(
                        Response.from_error(
                            errors.InternalError(
                                jsonrpc = jsonrpc,
                                id = id,
                                data = traceback_info
                            )
                        )
                    )
            except BaseException, err:
                traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
                if hasattr(err, "data"):
                    error_data = err.data
                else:
                    error_data = None
                responses.append(
                    Response.from_error(
                        errors.InternalError(
                            jsonrpc = jsonrpc,
                            id = id,
                            data = error_data or traceback_info
                        )
                    )
                )

        # Convert responses to dictionaries
        responses_ = []
        for response in responses:
            responses_.append(response.to_dict())
        responses = responses_

        # Return as JSON-string (batch or normal)
        if len(requests) == 1:
            return json.dumps(responses[0])
        elif len(requests) > 1:
            return json.dumps(responses)
        else:
            return None


    def __call__(self, json_request):
        """
        Redirects the requests to *self.call*
        """

        return self.call(json_request)


    def __getitem__(self, key):
        """
        Gets back the method
        """

        return self.methods[key]


    def __setitem__(self, key, value):
        """
        Appends or replaces a method
        """

        self.methods[key] = value


    def __delitem__(self, key):
        """
        Deletes a method
        """

        del self.methods[key]


    def system_describe(self):
        """
        Returns a system description

        See: http://web.archive.org/web/20100718181845/http://json-rpc.org/wd/JSON-RPC-1-1-WD-20060807.html#ServiceDescription
        """

        # ToDo: not finished yet

        return u"[not finished]"