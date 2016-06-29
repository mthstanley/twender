#!/usr/bin/env python
"""
collect_names.py
used to collect names with gender and occurrence from 
http://www.ssa.gov/oact/babynames/limits.html dataset this module takes the data
stored in these text files and accumulates them into a dictionary which will
be stored as a json file, to allow easy conversion from file to dictionary

the text files are expected to follow the following convention:
    each line in the file is a comma-seperated 3-tuple name,{M,F},occurrence
"""
import json
import sys

USAGE = 'collect_names <filename> <data_files>\n' + \
        '\tfilename: where json version of data will be stored\n' + \
        '\tdata_file: one or more files with format name,{M,F},occurrence\n'


def load_data(filename): 
    """
    param:
        filename: file containing data stored in json format
    return:
        python dict containing data loaded from json file
    description:
        load json data stored in file with filename into a python dictionary
    """
    with open(filename+'.json', 'r') as data_file:
        data = json.load(data_file)
    return data


def write_data(filename, data):
    """
    param:
        filename: name of file to store json data
        data: python dictionary to store in file
    return:
        None
    description:
        write dictionary data to a file in json format   
    """
    with open(filename+'.json', 'w') as data_file:
        json.dump(data, data_file)


def add_data_entry(name, data, data_entry):
    """
    param:
        name:
            key for data_entry to be added to data
        data:
            python dictionary containing name and gender info
        data_entry:
            {gender:'M/F', num_occur:'num'} to be added to data
    return:
        1 if name is not in dict 0 if merged
    description:
         merges data_entry into data, if the name is not in the data then 
         just add entry, if the name is in data then merge with male or female
         entry
    """
    unique = 0
    if name in data:
        gender = data_entry['gender']
        if gender in data[name]:
            # if the num_occur for data_entry's gender is already in data[name]
            # add data_entry's num_occur
            total_num_occur = int(data[name][gender]['num_occur'])
            num_occur = int(data_entry['num_occur'])

            data[name][gender]['num_occur'] = str(total_num_occur + num_occur)
        else:
            #otherwise store data_entry under its gender
            data[name][data_entry['gender']] = data_entry
    else:
        # store data_entry under gender so we 
        # can have both male and female
        data[name] = {data_entry['gender']:data_entry}
        unique = 1
    return unique

def collect_data(filename, data):
    """
    param:
        filename: name of file containing name data must be of format 
                    name,{M,F},occurrence
        data: python dictionary to store data read from file
                this dictionary will be updated with the new data read
                from the file
    return:
        number of unique names added to the dictionary
    description:
        reads data contained in file with filename and stores it in 
        a python dictionary of the following format:
        {name:{'M':{gender:'M', num_occur:'num'}, 'F':{gender:'F', num_occur:'num'}}
    """
    with open(filename, 'r') as data_file:
        num_names = 0
        for line in data_file:
            # strip whitespace and split by comma into list of 3 elements
            data_elements = line.strip().split(',')
            # assign list elements to respective variables
            name, gender, num_occur = data_elements
            # create the data entry
            data_entry = {'gender':gender, 'num_occur':num_occur}
            # merge the data entry into data dictionary
            num_names += add_data_entry(name, data, data_entry)
    return num_names


def prune_genders(data, threshold): 
    """
    param:
        data: dictionary containing names as keys and the following as values
        {name:{'M':{gender:'M', num_occur:'num'}, 'F':{gender:'F', num_occur:'num'}}
        threshold: names that contain percentage male or female occurrences less
                    than this threshold will be discarded
    return:
        tuple: (data where each entry is pruned to a single gender, number pruned)
    description:
        if a name in data is labeled both female and male, check to see if the 
        percentage male or female is above the given threshold, if not discard 
        the name, otherwise label the name as the gender with the higher percentage
    """
    num_pruned = 0
    new_data = {} 
    for name, data_entry in data.items():

        if 'M' in data_entry and 'F' in data_entry:
            total_occur = int(data_entry['M']['num_occur']) + int(data_entry['F']['num_occur'])
            male_occur = int(data_entry['M']['num_occur'])
            female_occur = int(data_entry['F']['num_occur'])

            percent_male = male_occur/total_occur
            percent_female = female_occur/total_occur

            if percent_male > threshold:
                new_data[name] = data_entry['M']
            elif percent_female > threshold:
                new_data[name] = data_entry['F']
            else: 
                num_pruned += 1
                continue
        else:
            if 'M' in data_entry:
                new_data[name] = data_entry['M']
            else:
                new_data[name] = data_entry['F']
    
    return new_data, num_pruned


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(USAGE)
    else:
        filename = sys.argv[1]
        # create a list of data filenames
        data_files = sys.argv[2:]
        threshold = 0.75
        
        print('collecting names from {num_files} file(s) named {filenames}'.format(num_files=len(data_files),
            filenames=data_files))
        # create new dictionary to hold name data
        data = {}
        num_added = 0
        for data_file in data_files:
            num_added += collect_data(data_file, data)

        print('collected {num_names} unique names'.format(num_names=num_added))
        print('pruning names with {threshold} threshold'.format(threshold=threshold))
        
        pruned_data, num_pruned = prune_genders(data, 0.75)
       
        print('went from {num_before} to {num_after} pruned {num_pruned}'.format(num_before=len(data.keys()), 
                    num_after=len(pruned_data.keys()), num_pruned=num_pruned))

        write_data(filename, pruned_data)
