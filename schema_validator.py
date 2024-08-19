#!/usr/bin/env python
# coding: utf-8

import json

valid_types = {"object": dict, "array": list, "string": str, "integer": int, "number": float}

def validate(config, schema):
    # check structure of schema
    
    if "type" in schema:
        type = schema["type"]
        status = validate_type(type, config)
        if not status:
            return False

        if type == "object":
            return validate_object(config, schema)
        elif type == "array":
            return validate_array(config, schema)
        elif type in ["string", "integer", "number"]:
            return validate_primitives(config, schema)

    return False

def validate_type(dtype, config):
    if dtype not in valid_types:
        print(f"schema mismatch type {dtype} not a valid type")
        return False

    python_type = valid_types[dtype]
    if not isinstance(config, python_type):
        print(f"schema mismatch expected type {dtype} got {type(config)}")
        return False

    return True

def validate_object(config, schema):
    valid_object_keys = ["type", "properties", "required", "additionalProperties", "anyOf"]

    for schema_key in schema.keys():
        if schema_key not in valid_object_keys:
            print(f"mismatch invalid key {schema_key}\n", schema)
            return False

    if not check_required_properties(config, schema):
        return False

    if not check_additional_properties(config, schema):
        return False  
            
    if "properties" in schema:
        schema_proph = schema["properties"]
        cnf_props = config.keys()  
        
        for prop in config.keys():
            if prop in schema_proph:
                prop_schema = schema_proph[prop]
                prop_config = config[prop]

                prop_status = validate(prop_config, prop_schema)
                if not prop_status:
                    print(f"mismatch for property : {prop}\n", prop_schema)
                    return False
    
    return True

def check_required_properties(config, schema):
    if "required" not in schema:
        return True
        
    required_sch = schema["required"]
    
    if not isinstance(required_sch, list):
        print(f"schema mismatch wrong use of 'required' in ", required_sch)
        return False

    for prop in required_sch:
        if prop not in config:
            print(f"schema mismatch: required property {prop} not found ", required_sch)
            return False

    return True

def check_additional_properties(config, schema):
    if "additionalProperties" not in schema:
        return True
    
    additional_properties_enabled = schema["additionalProperties"]
    
    if additional_properties_enabled:
        return True

    schema_prop = set(schema["properties"].keys())
    conf_prop = config.keys()

    extra_props = conf_prop - schema_prop
    if extra_props:
        print(f"additionalProperties found {extra_props} for schema\n", schema)
        return False

    return True

def validate_array(config, schema):
    valid_object_keys = ["type", "items", "minItems"]

    for schema_key in schema.keys():
        if schema_key not in valid_object_keys:
            print(f"mismatch invalid key {schema_key}\n", schema)
            return False

    item_schema = schema["items"]
    
    for cnf_item in config:
        status = validate(cnf_item, item_schema)
        if not status:
            print(f"mismatch for item {cnf_item} \n config {config}")
            return False

    return True

def validate_primitives(config, schema):
    valid_object_keys = ["type", "description"]
    
    for schema_key in schema.keys():
        if schema_key not in valid_object_keys:
            print(f"mismatch invalid key {schema_key}\n", schema)
            return False

    schema_type = schema["type"]
    python_type = valid_types[schema_type]

    if not isinstance(config, python_type):
        print(f"mismatch invalid type for {config}. Expected {schem_type}")
        return False
        
    return True


with open('schema.txt') as fd:
    schema = json.load(fd)

print(json.dumps(schema, indent=4))

config = {
    "content_validation_definition": [
        {
            "name": "dbagent_wallet_loc_in_creg",
            "condition": "'${CLOUD_REGISTRY/GRID_CREG/GRID_INI/dbagent_wallet_loc}' == '/var/opt/oracle/dbaas_acfs/dbagent/dbagent_wallet'",
            "source": "${CLOUD_REGISTRY/GRID_CREG/GRID_INI/__SOURCE__}"
        }
    ]
}

validate(config, schema)

config = {
    "content_validation_definition": [
        {
            "name": "dbagent_wallet_loc_in_creg",
            "condition": "'${CLOUD_REGISTRY/GRID_CREG/GRID_INI/dbagent_wallet_loc}' == '/var/opt/oracle/dbaas_acfs/dbagent/dbagent_wallet'",
            "source": "${CLOUD_REGISTRY/GRID_CREG/GRID_INI/__SOURCE__}"
        }
    ],
    "asdjf": 'slkdjf'
}

validate(config, schema)

config = {
    "content_validation_definition": [
        {
            "condition": "'${CLOUD_REGISTRY/GRID_CREG/GRID_INI/dbagent_wallet_loc}' == '/var/opt/oracle/dbaas_acfs/dbagent/dbagent_wallet'",
            "source": "${CLOUD_REGISTRY/GRID_CREG/GRID_INI/__SOURCE__}"
        }
    ]
}

validate(config, schema)

