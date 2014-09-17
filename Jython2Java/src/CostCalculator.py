from org.jython.book.interfaces import CostCalculatorType
from munkres import Munkres, print_matrix

class CostCalculator(CostCalculatorType, object):
    ''' Cost Calculator Utility '''

    def __init__(self):
        print 'Initializing'
        pass

    # The implementation for the definition contained in the Java interface
    def calculateCost(self, salePrice, tax):
        matrix = [[5, 9, 1],
                  [10, 3, 2],
                  [8, 7, 4]]
        m = Munkres()
        indexes = m.compute(matrix)
        print_matrix(matrix, msg='Lowest cost through this matrix:')
        total = 0
        for row, column in indexes:
            value = matrix[row][column]
            total += value
            print '(%d, %d) -> %d' % (row, column, value)
        print 'total cost: %d' % total           
        return salePrice + (salePrice * tax)