import sys

import parse_lib as pl

def module_attr_relationship_table(module_attr_relationship_list):
    entries = []
    for module in module_attr_relationship_list:
        for attribute in module['attributes']:
            entries.append({
                'module': module['id'],
                'moduleDescription': module['description'],
                'path': attribute['id'],
                'tag': attribute['tag'],
                'type': attribute['type'],
                'linkToStandard': get_standard_link(module, attribute),
                'description': attribute['description']
            })
    return entries

def get_standard_link(module, attribute):
    if 'linkToStandard' not in attribute.keys():
        return module['linkToStandard']
    else:
        return attribute['linkToStandard']

if __name__ == "__main__":
    module_attr_list = pl.read_json_to_dict(sys.argv[1])
    module_attr_relationship_list = module_attr_relationship_table(module_attr_list)
    pl.write_pretty_json(module_attr_relationship_list)
