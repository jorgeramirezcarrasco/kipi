import os

def read_from_env_file():
    """Function to read from env file

    Returns:
        dict -- env variables from file
    """

    with open('../.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('=='))
            for line in fh.readlines()
            if not line.startswith('#')
        )

    return vars_dict