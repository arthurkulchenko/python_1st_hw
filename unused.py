def get_all_names(trees):
    for t in trees:
        names = [ node.id for node in ast.walk(t) if isinstance(node, ast.Name)]
    return filter(None, names)

def split_snake_case_names_into_words(from_list):
    nested_array = [i.split('_') for i in from_list]
    return list(flattening(nested_array))