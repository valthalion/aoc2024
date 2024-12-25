from operator import and_, or_, xor


testing = False
gates = {'AND': and_, 'OR': or_, 'XOR': xor}


def read_data():
    connections = {}
    values = {}
    with open(f'puzzle24-test{testing}.in' if testing else 'puzzle24.in', 'r') as f:
        while True:
            line = next(f).strip()
            if not line:
                break
            wire, value = line.split(': ')
            values[wire] = int(value)

        for line in f:
            gate_spec, output = line.strip().split(' -> ')
            input1, gate_type, input2 = gate_spec.split()
            connections[output] = (gates[gate_type], input1, input2)

    return connections, values


def eval_wire(wire, connections, values):
    if wire not in values:
        gate_type, *arg_names = connections[wire]
        args = (eval_wire(arg_name, connections, values) for arg_name in arg_names)
        values[wire] = gate_type(*args)
    return values[wire]


def flowchart(connections):
    gates_so_far = set()
    with open('puzzle24.out', 'w') as f:
        f.write('strict digraph {\n')
        for out, (gate, in1, in2) in connections.items():
            gate_type = 'AND' if gate is and_ else 'OR' if gate is or_ else 'XOR'
            gt = f'{gate_type}{in1}{in2}'
            if gt not in gates_so_far:
                gates_so_far.add(gt)
                f.write(f'{gt} [label="{gate_type}",shape="box"]\n')
            f.write(f'\t{in1} -> {gt}\n')
            f.write(f'\t{in2} -> {gt}\n')
            f.write(f'\t{gt} -> {out}\n')
        f.write('}\n')


def part_1():
    connections, values = read_data()
    z_outputs = sorted((wire for wire in connections if wire[0] == 'z'), reverse=True)  # from MSB to LSB
    total = 0
    for output in z_outputs:
        value = eval_wire(output, connections, values)
        total <<= 1
        total |= value
    return total


def part_2():
    connections, values = read_data()
    # Uncomment the next line to generate a graphviz graph of the operations
    # flowchart(connections)
    
    # From analyzing the graph, the following anomalies are seen in bits 7, 13, 18, and 26
    anomalies = (('z07', 'bjm'), ('z13', 'hsw'), ('z18', 'skf'), ('nvr', 'wkr'))
    return ','.join(sorted(node for anomaly in anomalies for node in anomaly))
