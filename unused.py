def get_all_names(trees):
    for t in trees:
        names = [ node.id for node in ast.walk(t) if isinstance(node, ast.Name)]
    return filter(None, names)

def split_snake_case_name_to_words(name):
    nested_array = [n.split('_') for n in name]
    return list(flattening(nested_array))