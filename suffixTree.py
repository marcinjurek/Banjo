import pdb
import sys

class SuffixNode:

    def __init__(self, depth=0, K=1, suffix_link = None):

        self._K = K
        self._distinct_identifiers = 2**K
        self._depth = depth
        self.children = {}
        if suffix_link is not None:
            self.suffix_link = suffix_link
        else:
            self.suffix_link = self

    def add_link( self, c, v):
        self.children[ c ] = v


    def delete( self ):
        for c, v in self._children.items():
            v.delete()
            del self._children[c]

    def get_depth( self ):
        return self._depth


def build_suffix_tree( s ):

    assert len(s) > 0

    no_strings = len(s.split("$"))

    Root = SuffixNode(depth=0, K=no_strings)
    Longest = SuffixNode( suffix_link = Root )
    Root.add_link( s[0], Longest )

    for c in s[1:]:
        Current = Longest
        Previous = None
        while c not in Current.children:

            r1 = SuffixNode( depth=Current.get_depth() + 1, K=Current._K )
            Current.add_link(c, r1)

            if Previous is not None:
                Previous.suffix_link = r1

            Previous = r1
            Current = Current.suffix_link

        if Current is Root:
            Previous.suffix_link = Root
        else:
            Previous.suffix_link = Current.children[ c ]

        Longest = Longest.children[ c ]

    return Root





def prune_generalized_tree( Tree ):

    for c, v in Tree.children.items():
        if c.startswith("$_"):
            v.delete()

    get_distinct_identifiers_in_children( Tree )
    return Tree
            
    


def get_distinct_identifiers_in_children( Tree ):
    
    for c, v in Tree.children.items():
        if c.startswith("$_"):
            ind = c.split("_")[1]
            Tree._distinct_identifiers[ ind ] = 1
        else:
            child_identifiers = get_distinct_identifiers_in_children( v )
            Tree._distinct_identifiers |= child_identifiers



    
def get_node_list( Tree ):

    node_list = []
    node_list.append( Tree )
    for v in Tree.children.values():
        node_list.extend( get_node_list( v ) )
    return node_list






def get_common_strings_table( s_list ):

    print "Hello"
    s_list = ["grata", "fiata"]
    combined = ""
    for idx, s in enumerate(s_list):
        combined += "$_" + str(idx) + "_" + s
    Tree = build_suffix_tree( combined )
    Tree = prune_generalized_tree( Tree )


    node_list = get_node_list( Tree )

    pdb.set_trace()

    V_k = [0]*len(s_list)

    for node in node_list:
        s = sum( node._distinct_identifiers )
        assert( s>0 )
        V_k[s][0] = max(V_k[s][0], node._depth)


    return V_k
        









if __name__=='__main__':

    tb = get_common_strings_table( ["sandollar", "sandlot", "handler", "grand", "pantry"] )
    print tb
