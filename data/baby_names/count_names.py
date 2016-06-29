import sys

if __name__ == '__main__':

    filenames = sys.argv[1:]
    num_names = 0
    names = {}
    num_unique_names = 0
    for filename in filenames:
        with open(filename, 'r') as file_data:
            for line in file_data:
                data = line.strip().split(',')
                num_names += 1
                name = data[0]
                if not name in names:
                    num_unique_names += 1
                    names[name] = 1

    print('counted %d names\ncounted %d unique names' % (num_names, num_unique_names))
