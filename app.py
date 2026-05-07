from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def run_bankers_algorithm(available, max_demand, allocation):
    """
    available: list[int]
    max_demand: list[list[int]]
    allocation: list[list[int]]
    returns dict with keys: safe bool, sequence list, steps list, deadlock process list
    """
    n = len(max_demand)
    m = len(available)

    need = []
    for i in range(n):
        need.append([max_demand[i][j] - allocation[i][j] for j in range(m)])

    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    steps = []

    k = 0
    while len(safe_sequence) < n:
        found = False
        k += 1

        for i in range(n):
            if not finish[i]:
                can_allocate = all(need[i][j] <= work[j] for j in range(m))

                step_info = {
                    'iteration': k,
                    'process': f'P{i}',
                    'process_id': i,
                    'work': work.copy(),
                    'need': need[i].copy(),
                    'allocation': allocation[i].copy(),   
                    'can_allocate': can_allocate,
                    'result': None,
                    'finish': finish.copy(),              
                    'safe_so_far': safe_sequence.copy()
                }

                if can_allocate:
                    old_work = work.copy()
                    work = [work[j] + allocation[i][j] for j in range(m)]
                    finish[i] = True
                    safe_sequence.append(f'P{i}')
                    found = True

                    step_info['result'] = 'PASS'
                    step_info['new_work'] = work.copy()
                    step_info['message'] = f"P{i} can run! Need {need[i]} <= Work {old_work}. P{i} completes. Work becomes {work}"
                else:
                    step_info['result'] = 'WAIT'
                    step_info['new_work'] = work.copy()
                    step_info['message'] = f"P{i} must wait. Need {need[i]} > Work {work}"

                steps.append(step_info)

        if not found:
            deadlock_processes = [f'P{i}' for i in range(n) if not finish[i]]

            steps.append({
                'iteration': k,
                'process': 'SYSTEM',
                'process_id': -1,
                'work': work.copy(),
                'need': [],                          
                'allocation': [],
                'can_allocate': False,
                'result': 'DEADLOCK',
                'new_work': work.copy(),
                'finish': finish.copy(),
                'safe_so_far': safe_sequence.copy(),
                'message': f"DEADLOCK DETECTED! No process can proceed. Deadlocked: {deadlock_processes}"
            })

            return {
                'safe': False,
                'sequence': [],
                'steps': steps,
                'deadlock_processes': deadlock_processes,
                'need_matrix': need,
                'allocation_matrix': allocation,
                'max_matrix': max_demand,
                'available': available
            }

    steps.append({
        'iteration': k + 1,
        'process': 'SYSTEM',
        'process_id': -1,
        'work': work.copy(),
        'need': [],
        'allocation': [],
        'can_allocate': True,
        'result': 'SAFE',
        'new_work': work.copy(),
        'finish': [True] * n,
        'safe_so_far': safe_sequence.copy(),
        'message': f"SAFE STATE! Sequence: {' -> '.join(safe_sequence)}"
    })

    return {
        'safe': True,
        'sequence': safe_sequence,
        'steps': steps,
        'deadlock_processes': [],
        'need_matrix': need,
        'allocation_matrix': allocation,
        'max_matrix': max_demand,
        'available': available
    }


EXAMPLES = {
    'safe': {
        'name': 'Safe State Example',
        'description': 'Classic safe state - all processes can complete',
        'available': [3, 3, 2],
        'max_demand': [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ],
        'allocation': [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
    },
    'unsafe': {
        'name': 'Unsafe State Example',
        'description': 'Unsafe but not deadlocked - system should refuse new requests',
        'available': [1, 0, 0],
        'max_demand': [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ],
        'allocation': [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
    },
    'deadlock': {
        'name': 'Deadlock Example',
        'description': 'Circular wait - classic deadlock scenario',
        'available': [0, 0, 0],
        'max_demand': [
            [8, 5, 3],
            [3, 2, 3],
            [9, 0, 4],
        ],
        'allocation': [
            [3, 1, 0],
            [1, 1, 1],
            [2, 0, 2],
        ]
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/examples', methods=['GET'])
def get_examples():
    return jsonify({
        'examples': [
            {'id': k, 'name': v['name'], 'description': v['description']}
            for k, v in EXAMPLES.items()
        ]
    })


@app.route('/api/example/<example_id>', methods=['GET'])
def get_example(example_id):
    if example_id in EXAMPLES:
        return jsonify(EXAMPLES[example_id])
    return jsonify({'error': 'Example not found'}), 404


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    try:
        available = data['available']
        max_demand = data['max_demand']
        allocation = data['allocation']

        if not all(isinstance(x, list) for x in [available, max_demand, allocation]):
            return jsonify({'error': 'Invalid data format'}), 400

        result = run_bankers_algorithm(available, max_demand, allocation)
        return jsonify(result)

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/resource-graph', methods=['POST'])
def resource_graph():
    data = request.get_json()

    try:
        available = data['available']
        max_demand = data['max_demand']
        allocation = data['allocation']

        n = len(max_demand)
        m = len(available)

        need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

        nodes = []
        edges = []

        for i in range(n):
            nodes.append({
                'id': f'P{i}',
                'type': 'process',
                'label': f'P{i}',
                'x': 100,
                'y': 100 + i * 120
            })

        for j in range(m):
            nodes.append({
                'id': f'R{j}',
                'type': 'resource',
                'label': f'R{j}\\nTotal: {sum(allocation[i][j] for i in range(n)) + available[j]}',
                'x': 400,
                'y': 100 + j * 150
            })

        for i in range(n):
            for j in range(m):
                if allocation[i][j] > 0:
                    edges.append({
                        'from': f'P{i}',
                        'to': f'R{j}',
                        'type': 'holds',
                        'label': str(allocation[i][j]),
                        'weight': allocation[i][j]
                    })

        for i in range(n):
            for j in range(m):
                if need[i][j] > 0:
                    edges.append({
                        'from': f'R{j}',
                        'to': f'P{i}',
                        'type': 'waits',
                        'label': str(need[i][j]),
                        'weight': need[i][j]
                    })

        return jsonify({'nodes': nodes, 'edges': edges})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)