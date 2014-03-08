from matplotlib.pyplot import *
subplot(211)
plot([1,2,3], label="test1")
plot([3,2,1], label="test2")
legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
ncol=2, mode="expand", borderaxespad=0.)
subplot(223)
plot([1,2,3], color = 'blue', ls = 'o', label="test1")
plot([3,2,1], label="test2")
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
show()



'''
# Multiple Legend

p1, = plot([1,2,3])
p2, = plot([3,2,1])
legend([p1], ["Test1"], loc=1)
legend([p2], ["Test2"], loc=4)
However, the above code only shows the second legend. When the legend command is called, a new legend
instance is created and old ones are removed from the axes. Thus, you need to manually add the removed
legend.
from matplotlib.pyplot import *
p1, = plot([1,2,3], label="test1")
p2, = plot([3,2,1], label="test2")
l1 = legend([p1], ["Label 1"], loc=1)
l2 = legend([p2], ["Label 2"], loc=4) # this removes l1 from the axes.
gca().add_artist(l1) # add l1 as a separate artist to the axes
show()
'''