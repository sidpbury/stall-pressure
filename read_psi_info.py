import os

def read_psi_info():
    # File paths for CPU, memory, and IO pressure stats
    psi_paths = {
        'cpu': '/proc/pressure/cpu',
        'memory': '/proc/pressure/memory',
        'io': '/proc/pressure/io'
    }

    psi_data = {}

    for resource, path in psi_paths.items():
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    lines = f.readlines()

                    if not lines:
                        print(f"Warning: {resource} pressure data is empty.")
                        psi_data[resource] = None
                    else:
                        data = {}
                        for line in lines:
                            parts = line.strip().split(' ')
                            if len(parts) >= 2:  # Ensure there are at least two elements in the split
                                key = parts[0]
                                try:
                                    value = float(parts[1])
                                    data[key] = value
                                except ValueError:
                                    print(f"Warning: Unable to convert value '{parts[1]}' to float.")
                        psi_data[resource] = data
            except Exception as e:
                print(f"Error reading {resource} pressure data: {str(e)}")
                psi_data[resource] = None
        else:
            print(f"Warning: {resource} pressure file does not exist.")
            psi_data[resource] = None

    return psi_data


# Example usage
if __name__ == '__main__':
    psi_info = read_psi_info()
    print(psi_info)

