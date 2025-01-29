import os

def read_psi_info():
    # File paths for CPU, memory, and IO pressure stats
    psi_paths = {
        'cpu': '/proc/pressure/cpu',
        'memory': '/proc/pressure/memory',
        'io': '/proc/pressure/io'
    }

    psi_data = {'cpu' : None,
                'memory' : None,
                'io' : None}

    for resource, path in psi_paths.items():
        if os.path.exists(path):
            try:
                data = [['name', 'avg10', 'avg60', 'avg300', 'total'],
                ['some', None, None, None, None],
                ['full', None, None, None, None]]

                with open(path, 'r') as f:
                    lines = f.readlines()

                if not lines:
                    print(f"Warning: {resource} pressure data is empty.")
                    psi_data[resource] = None
                else:
                    for i in range(len(lines)):
                        parts = lines[i].strip().split(' ')
                        for j in range(len(parts)):
                            if j != 0:
                                data[i + 1][j] = float(parts[j].split('=')[1])
                    psi_data[resource] = data
            except Exception as e:
                print(f"Error reading {resource} pressure data: {str(e)}")
                psi_data[resource] = None
        else:
            print(f"Warning: {resource} pressure file does not exist.")
            psi_data[resource] = None

    return psi_data

def format_resource(psi_data, resource):
    return '\n'.join([str(line) for line in psi_data[resource]])

def format_all_resources(psi_data):
    return "cpu:\n" + format_resource(psi_data, 'cpu') + "\n\nmemory:\n" + format_resource(psi_data, 'memory') + "\n\nio:\n" + format_resource(psi_data, 'io')

# Example usage
if __name__ == '__main__':
    psi_info = read_psi_info()
    print(format_all_resources(psi_info))
