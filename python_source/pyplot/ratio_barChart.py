import matplotlib.pyplot as plt
import numpy as np

data = [
        ['test', 25, 25, 50, 0],
        ['test2', 30, 40, 10, 20],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        ]

# unpack data
trains, ideal, correct, deficient, without = zip(*data)

print ideal

N = len(trains)  # -- Number of trains
ind = np.arange(N)  # the x locations for the groups
width = 0.35  # the width of the bars: can also be len(x) sequence
labels = []

p1 = plt.bar(ind, ideal, width, color='green', hatch='X')
labels.append(r'%s' % ('idle'))
print ideal
p2 = plt.bar(ind, correct, width, color='yellow', bottom=ideal)
p3 = plt.bar(ind, deficient, width, color='red', bottom=tuple(sum(x) for x in zip(ideal, correct)))
p4 = plt.bar(ind, without, width, color="grey", bottom=tuple(sum(x) for x in zip(ideal, correct, deficient)))

plt.legend(labels, ncol=1, loc='upper center', fontsize=12,
                  bbox_to_anchor=[0.5, 1.137],
                  )
plt.ylabel('%')
plt.title('Qualite du rabattement par depart de train')
plt.xticks(ind + width / 2., trains)
plt.yticks(np.arange(0, 100, 25))

plt.show()
