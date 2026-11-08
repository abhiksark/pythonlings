leaf = {"value": 7, "children": []}
single = {"value": 1, "children": []}
two_level = {"value": 1, "children": [{"value": 2, "children": []}, {"value": 3, "children": []}]}
deep = {"value": 1, "children": [{"value": 2, "children": [{"value": 3, "children": []}]}]}

assert tree_depth(single) == 1, f"tree_depth(single) should be 1, got {tree_depth(single)}"
assert tree_depth(two_level) == 2, f"tree_depth(two_level) should be 2, got {tree_depth(two_level)}"
assert tree_depth(deep) == 3, f"tree_depth(deep) should be 3, got {tree_depth(deep)}"

assert tree_search(leaf, 7) is True, f"tree_search(leaf, 7) should be True, got {tree_search(leaf, 7)}"
assert tree_search(leaf, 99) is False, f"tree_search(leaf, 99) should be False, got {tree_search(leaf, 99)}"
assert tree_search(two_level, 3) is True, f"tree_search(two_level, 3) should be True, got {tree_search(two_level, 3)}"
assert tree_search(deep, 3) is True, f"tree_search(deep, 3) should be True, got {tree_search(deep, 3)}"
assert tree_search(deep, 99) is False, f"tree_search(deep, 99) should be False, got {tree_search(deep, 99)}"
print("recursion8 ✓")
