class BNode:
    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.numOfAncestors = 0
        
    def countAncestors(self, child):
        ancestor = child.parent
        numOfAncestors = 0
        while ancestor:
            numOfAncestors += 1
            ancestor = ancestor.parent
        child.numOfAncestors = numOfAncestors
         
    def addLeft(self, left):
        self.left = left
        left.parent = self
        self.countAncestors(left)
    
    def addRight(self, right):
        self.right = right
        right.parent = self
        self.countAncestors(right)
    
    def __repr__(self):
        unit = '\t'
        unit = '    '
        space = unit * (self.numOfAncestors + 1)
        return '%s (\n%s%s\n%s%s)' % (self.value, space, self.left, space, self.right)
    
if __name__ == '__main__':
    root = BNode('root')
    root.addLeft(BNode('left'))
    root.addRight(BNode('right'))
    root.left.addLeft(BNode('left-left'))
    root.left.addRight(BNode('left-right'))
    
    print root
