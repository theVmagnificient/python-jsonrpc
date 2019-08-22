#!/usr/bin/env python
# coding: utf-8
"""
Nosetests for *rpcrequest.py*.
"""

import json
import pyjsonrpc.rpcrequest

TESTMETHOD = "TESTMETHOD"
TESTID = "TESTID"


def test_create_request_dict_with_positional_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, "Ö", "ß"
    )
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": ("\xd6", "\xdf"),
        "id": TESTID
    }, "Unexpected result"


def test_create_request_dict_with_named_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, k1 = "Ä", k2 = "Ö"
    )
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": "\xc4", "k2": "\xd6"},
        "id": TESTID
    }, "Unexpected result"


def test_create_request_dict_with_positional_and_named_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, 1, 2, k1 = "Ä", k2 = "Ö"
    )
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": "\xc4", "k2": "\xd6", "__args": (1, 2)},
        "id": TESTID
    }, "Unexpected result"


def test_create_request_json_with_positional_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, "Ö", "ß"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": ["\xd6", "\xdf"],
        "id": TESTID
    }, "Unexpected result"


def test_create_request_json_with_named_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, k1 = "Ä", k2 = "Ö"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": "\xc4", "k2": "\xd6"},
        "id": TESTID
    }, "Unexpected result"


def test_create_request_json_with_positional_and_named_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, 1, 2, k1 = "Ä", k2 = "Ö"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": "\xc4", "k2": "\xd6", "__args": [1, 2]},
        "id": TESTID
    }, "Unexpected result"


def test_aliases():
    assert pyjsonrpc.rpcrequest.create_request_string
    assert pyjsonrpc.rpcrequest.parse_request_json


def test_request_with_positional_params():
    request = pyjsonrpc.rpcrequest.Request(
        method = TESTMETHOD,
        id = TESTID,
        params = [1, 2]
    )
    request_dict = request.to_dict()
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": [1, 2],
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result"


def test_request_with_named_params():
    request = pyjsonrpc.rpcrequest.Request(
        method = TESTMETHOD,
        id = TESTID,
        params = {"k1": "Ä", "k2": "Ö"}
    )
    request_dict = request.to_dict()
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": {"k1": "\xc4", "k2": "\xd6"},
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result"


def test_request_with_positional_and_named_params():
    request = pyjsonrpc.rpcrequest.Request(
        method = TESTMETHOD,
        id = TESTID,
        params = {"k1": "Ä", "k2": "Ö", "__args": [1, 2]}
    )
    request_dict = request.to_dict()
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": {"k1": "\xc4", "k2": "\xd6", "__args": [1, 2]},
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result"


def test_request_from_string():
    json_string = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, 1, 2, k1 = "Ä", k2 = "Ö"
    )
    request = pyjsonrpc.rpcrequest.Request.from_string(json_string)
    request_dict = request.to_dict()
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": {"k1": "\xc4", "k2": "\xd6", "__args": [1, 2]},
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result"


def test_multiple_requests_from_string():
    json_string = json.dumps([
        pyjsonrpc.rpcrequest.create_request_dict(TESTMETHOD, 1, 2),
        pyjsonrpc.rpcrequest.create_request_dict(
            TESTMETHOD, k1 = "Ä", k2 = "Ö"
        ),
        pyjsonrpc.rpcrequest.Request(
            method = TESTMETHOD, id = TESTID, params = {"k1": "Ä"}
        )
    ])
    requests = pyjsonrpc.rpcrequest.Request.from_string(json_string)
    # Test request 1
    request_dict = requests[0].to_dict()
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": [1, 2],
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result for request[0]"
    # Test request 2
    request_dict = requests[1].to_dict()
    assert "id" in request_dict, "No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": {"k1": "\xc4", "k2": "\xd6"},
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result for request[1]"
    # Test request 3
    request_dict = requests[2].to_dict()
    assert request_dict == {
        "jsonrpc": "2.0",
        "params": {"k1": "\xc4"},
        "method": "TESTMETHOD",
        "id": "TESTID"
    }, "Unexpected result for request[2]"


def test_request_to_string():
    request1 = pyjsonrpc.rpcrequest.Request(
        method = TESTMETHOD,
        id = TESTID,
        params = {"k1": "Ö", "k2": "Ü", "__args": [1, 2]},
    )
    request2 = pyjsonrpc.rpcrequest.Request.from_string(request1.to_string())
    assert request1 == request2, "Requests not equal"


def test_request_from_dict():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, k1 = "Ä", k2 = "Ö"
    )
    request = pyjsonrpc.rpcrequest.Request.from_dict(request_dict)
    assert request.to_dict() == request_dict

