#read_params.py

def params():
    file=["parameters.dat"]
    params=[0]
    for workingfile in file:
        with open(workingfile,'r') as f:
            for line in f:
                linestring=line.split()
                if linestring[0]=="P":
                    params.append(linestring[1])
                    params.append(linestring[2])
                    params.append(linestring[3])
                    params.append(linestring[4])
                    params.append(linestring[5])
        f.closed
        True
        params.pop(0) #removes the first point (zero) in the list
    return params

def tangent_params():
    file=["parameters.dat"]
    tangent_params=[0]
    for workingfile in file:
        with open(workingfile,'r') as f:
            for line in f:
                linestring=line.split()
                if linestring[0]=="T":
                    tangent_params.append(linestring[1])
                    tangent_params.append(linestring[2])
                    tangent_params.append(linestring[3])
        f.closed
        True
        tangent_params.pop(0) #removes the first point (zero) in the list
    return tangent_params

def chord_params():
    file=["parameters.dat"]
    chord_params=[0]
    for workingfile in file:
        with open(workingfile,'r') as f:
            for line in f:
                linestring=line.split()
                if linestring[0]=="C":
                    chord_params.append(linestring[1])
                    chord_params.append(linestring[2])
                    chord_params.append(linestring[3])
                    chord_params.append(linestring[4])
        f.closed
        True
        chord_params.pop(0) #removes the first point (zero) in the list
    return chord_params