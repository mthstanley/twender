#!/usr/bin/env python
"""
names.py
used to collect names with gender and occurrence from
http://www.ssa.gov/oact/babynames/limits.html dataset this module takes the data
stored in these text files and accumulates them into a dictionary which will
be stored as a json file, to allow easy conversion from file to dictionary

the text files are expected to follow the following convention:
    each line in the file is a comma-seperated 3-tuple name,{M,F},occurrence
"""


def parse_name_data(line):
    """
    param:
        line: a line of text to parse
    return:
        a dict containing parse data
    description:
        take a line of data in the following format name,gender,occurrence
        and parse into the dict {name:'', gender:'', occurs:int(num)}
    """
    data = {}
    data['name'], data['gender'], data['occurs'] = line.strip().split(',')
    data['occurs'] = int(data['occurs'])
    return data


def read_names(filenames):
    """
    param:
        filenames: list of filenames to extract name,gender,occurrence data
    return:
        a list of names, possibly non-unique
    description:
        extract data from the given filenames using parse_name_data function
        and return as a list
    """
    names = []
    for filename in filenames:
        with open(filename, 'r') as fp:
            for line in fp:
                names.append(parse_name_data(line))
    return names


def collapse_duplicates(names_list):
    """
    param:
        names_list: list of dicts [{name:'', gender:'M/F', occurs:int(num)}, ...]
    return:
        dict of unique names and associated data {'M': {occurs:int(num)},
        'F': {occurs:int(num)}}, data may include one or both genders
    description:
        take a list of names, possibly with duplicates, and collapse down to a dict
        where keys are unique names
    """
    names_dict = {}
    for data in names_list:
        name, gender, occurs = data['name'], data['gender'], data['occurs']
        if name in names_dict:
            if gender in names_dict[name]:
                names_dict[name][gender]['occurs'] += occurs
            else:
                names_dict[name][gender] = {'occurs': occurs}
        else:
            names_dict[name] = {
                gender: {
                    'occurs': occurs
                }
            }
    return names_dict


def prune_genders(names_dict, threshold):
    """
    param:
        data: dictionary containing names as keys and the following as values
        {name:{'M': {occurs:int(num)}, 'F': {occurs:int(num)}}
        threshold: names that contain percentage male or female occurrences less
                    than this threshold will be discarded
    return:
        dict: data where each entry is pruned to a single gender
        {name: {gender: 'M/F', occurs:int(num)}}
    description:
        if a name in data is labeled both female and male, check to see if the
        percentage male or female is above the given threshold, if not discard
        the name, otherwise label the name as the gender with the higher percentage
    """
    pruned = {}
    for name, data in names_dict.items():
        if len(data.keys()) == 2: # 2 genders labels exist
            gender1, gender2 = data.items()
            max_occurs = max(data.items(), key=lambda item: item[1]['occurs'])
            total_occurs = gender1[1]['occurs'] + gender2[1]['occurs']
            percent = max_occurs[1]['occurs'] / total_occurs
            if percent >= threshold:
                pruned[name] = {
                    'gender': max_occurs[0],
                    'occurs': max_occurs[1]['occurs']
                }
        else:
            gender = list(data)[0]
            occurs = data[gender]['occurs']
            pruned[name] = {
                'gender': gender,
                'occurs': occurs
            }
    return pruned



def valid_names(filenames, threshold):
    """
    param:
        filenames: a list of filename strings
        threshold: a float value
    return:
        dict of valid names
    description:
        extract name and gender data from given files, if the name appears
        with both genders select the gender that has the higher percentage
        of occurrences if it is higher than the given threshold
    """
    names_list = read_names(filenames)
    names_dict = collapse_duplicates(names_list)
    pruned = prune_genders(names_dict, threshold)

    return pruned
