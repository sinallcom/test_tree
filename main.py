import unittest


class SymbolTree:
    # This is a Node class that is internal to the tree class.
    class Node:

        def __init__(self, name=''):
            self.child_nodes = []
            self.name = name
            self.word_end = False

    def __init__(self, list_part=None):
        self.root_node = self.Node()
        if list_part is not None:
            self.parse_list(list_part)

    def find(self, word):
        return self._recursive_find(self.root_node, word)

    def print_nodes(self, parent_node=None, depth=0):
        if parent_node is None:
            parent_node = self.root_node
        s = 'Node: ' + str(parent_node.name) + ', word_end:' + str(parent_node.word_end) \
            + ', cnt:' + str(len(parent_node.child_nodes))
        s = str.rjust(s, len(s)+depth, '+')
        print(s)
        if len(parent_node.child_nodes) > 0:
            for item in parent_node.child_nodes:
                self.print_nodes(item, depth + 1)

    def get_max_level(self):
        return self._get_max_level(self.root_node, 0) + 1

    def walk_tree(self):
        result = []
        self._walk_tree(self.root_node, '', result)
        return result

    def parse_list(self, list_part):
        list_part.sort()
        self.root_node = self._parse_list('', list_part, 0)

    def _walk_tree(self, parent_node, prefix, result):
        if parent_node.word_end:
            result.append(str(prefix + parent_node.name))
        if len(parent_node.child_nodes) > 0:
            for item in parent_node.child_nodes:
                self._walk_tree(item, prefix + parent_node.name, result)

    def _get_max_level(self, parent_node, parent_maximum):
        maximum = parent_maximum
        if len(parent_node.child_nodes) > 0:
            for item in parent_node.child_nodes:
                maximum = max(maximum, self._get_max_level(item, parent_maximum + 1))
        return maximum

    def _recursive_find(self, parent_node=None, word='', prefix=''):
        if prefix + parent_node.name == word and parent_node.word_end:
            return True
        if len(parent_node.child_nodes) > 0:
            for item in parent_node.child_nodes:
                if self._recursive_find(item, word, prefix + parent_node.name):
                    return True
        return False

    def _parse_list(self,  parent_symbol, list_part, depth):
        if len(list_part) > 0:
            symbol = None  # current symbol that we are testing
            index_first = 0  # 1st index of slice
            can_continue = True
            node = self.Node(parent_symbol)

            while can_continue:  # this loop is for gathering same letters to 1 node: ['book','bot', ..] => 'b'+'o'+..
                can_continue = False

                for i, item in enumerate(list_part):  # this loop for elements of partial list

                    if len(item) - 1 < depth:
                        index_first = i + 1
                        node.word_end = True
                        continue

                    if not symbol:
                        symbol = item[depth]

                    if symbol != item[depth]:
                        child_node = self._parse_list(symbol, list_part[index_first:i], depth + 1)
                        if child_node is not None:
                            node.child_nodes.append(child_node)
                        index_first = i
                        symbol = item[depth]

                if index_first == 0:
                    # cannot found any list slice at this iteration.
                    if symbol is not None:
                        node.name += symbol
                        can_continue = True
                    depth += 1
                    index_first = 0
                    symbol = None
                else:
                    # we need to parse last slice if it exists (from previous to end)
                    child_node = self._parse_list(symbol, list_part[index_first:], depth + 1)
                    if child_node is not None:
                        node.child_nodes.append(child_node)

            return node
        else:
            return None


class TestTree(unittest.TestCase):
    def setUp(self):
        self.tree1 = SymbolTree(["book", "bookshelf"])
        self.tree2 = SymbolTree(["born", "book", "bookcase", "booking"])
        self.tree3 = SymbolTree(["born", "book", "bookcase", "booking", "booklet", "bookshelf", "boost"])

    def tearDown(self):
        pass

    def test_structure_1(self):
        self.assertEqual(["book", "bookshelf"], self.tree1.walk_tree())

    def test_structure_2(self):
        self.assertEqual(["book", "bookcase", "booking", "born"], self.tree2.walk_tree())

    def test_structure_3(self):
        self.assertEqual(["book", "bookcase", "booking", "booklet", "bookshelf", "boost", "born"],
                         self.tree3.walk_tree())

    def test_search_1(self):
        self.assertEqual(self.tree1.find('bo'), False)
        self.assertEqual(self.tree2.find('do'), False)
        self.assertEqual(self.tree3.find('booking1'), False)

    def test_search_2(self):
        self.assertEqual(self.tree1.find('book'), True)
        self.assertEqual(self.tree2.find('bookcase'), True)
        self.assertEqual(self.tree3.find('boost'), True)

    def test_max_level(self):
        self.assertEqual(self.tree1.get_max_level(), 2)
        self.assertEqual(self.tree2.get_max_level(), 3)
        self.assertEqual(self.tree3.get_max_level(), 4)


def main():
    words = ["born", "book", "bookcase", "booking", "booklet", "bookshelf", "boost",
             "boot", "booth", "border", "bore", "doring", "borrow", "dododring"]

    tree = SymbolTree(words)
    tree.print_nodes()

    print(tree.walk_tree())
    print(tree.find('bo'))
    print(tree.get_max_level())


if __name__ == "__main__":
    # main()
    unittest.main()
