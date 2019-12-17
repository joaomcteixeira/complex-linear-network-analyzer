""" Creates a very simple feedforward network with a testbench.

This is the example used in the basic usage guide.
The network topology is as follows:

A -> B > D
     v
     C

A testbench is used to inject time varying signals at node A and B.
"""

from colna.analyticnetwork import Network, Edge, Testbench
import numpy as np
import matplotlib.pyplot as plt

### Create the Network and add the nodes

net = Network()

net.add_node(name='a')
net.add_node(name='b')
net.add_node(name='c')
net.add_node(name='d')

net.add_edge(Edge(start='a',end='b',phase=1,attenuation=0.8,delay=1))
net.add_edge(Edge(start='b',end='c',phase=2,attenuation=0.6,delay=2))
net.add_edge(Edge(start='b',end='d',phase=3,attenuation=0.4,delay=3))

# net.visualize('simple_graph_with_tb')

### Create a testbench
tb = Testbench(network=net, timestep=0.1) # Timestep should be factor of all delays

x_in_a = np.sin(np.linspace(0,15,500))+1.5 # create the input signal (Dimensino N)
t_in = np.linspace(0, 10, num=501) # create the input time vector (Dimension N+1)

tb.add_input_sequence(node_name='a',x=x_in_a,t=t_in)

# add output nodes to testbench (nodes at which output signal should be recorded)
tb.add_output_node('c')
tb.add_output_node('d')

# evaluate the network (through the testbench)
tb.evaluate_network()

# Calculate the output signal at the output nodes
tb.calculate_output(n_threads=8) # uses multithreading with at most 8 threads
t, x = tb.t_out.transpose(), tb.x_out.transpose()

### Plot the signals

plt.plot(tb.input_t[0][:-1], np.abs(tb.input_x[0][:-1]), 'o') # Input signal
plt.plot(t, np.abs(x), 'x') # Output signal

plt.xlabel('Time')
plt.ylabel('|x|')
plt.legend(['Input', 'Output C', 'Output D'], loc='best')
plt.grid()
plt.show()
