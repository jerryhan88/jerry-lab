def characters_counting(s):
        return len(s)

def text_characters_counting(txtPath):
	with open('%s' % (txtPath), 'r') as fp:
		ls = [w.strip() for w in fp.readlines()]
		return sum([characters_counting(l) for l in ls])

def remaining_characters(limitation, current):
        print 'Limitation: %d, Current: %d, Remaining: %d' % (limitation, current, limitation - current)
