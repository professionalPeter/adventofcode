"""Frequently useful functions"""
def split_by_size(the_list, chunk_size):
    return list(_chunks_generator(the_list, chunk_size))

def _chunks_generator(the_list, chunk_size):
    for i in range(0, len(the_list), chunk_size):
        yield the_list[i:i+chunk_size]
