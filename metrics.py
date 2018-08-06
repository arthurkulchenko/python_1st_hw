def the_most_common(objects, top_size=10):
    return collections.Counter(objects).most_common(top_size)