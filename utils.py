def convert_type(type_str):
    mapping = {
        "string": "String",
        "int": "Integer",
        "float": "Double",
        "decimal": "Double",
        "bool": "Boolean",
        "uuid": "UUID",
        "datetime": "LocalDateTime"
    }
    return mapping.get(type_str.lower(), type_str)

def format_class_name(name):
    return name[0].upper() + name[1:]

def format_variable_name(name):
    return name[0].lower() + name[1:]
