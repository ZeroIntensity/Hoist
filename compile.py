import os

path: str = './src'
out: str = './hoist'

if not os.path.exists(out):
    os.mkdir(out)

for i in os.listdir(path):
    current = os.path.join(path, i)

    if os.path.isfile(current):
        with open(current) as f:
            read = f.read()
        
        resp: str = ''
        in_ref_docstring: bool = False

        for x in read.split('\n'):

            if in_ref_docstring:
                if x == '"""':
                    in_ref_docstring = False
                    resp += x + '\n'

                continue

            no_spaces = x.replace(' ', '')
            
            if no_spaces.startswith('"""') and (not no_spaces.endswith('"""')):
                in_ref_docstring: bool = True
                resp += x
            else:
                resp += x + '\n'
        

        with open(os.path.join(out, i), 'w') as f:
            f.write(resp)