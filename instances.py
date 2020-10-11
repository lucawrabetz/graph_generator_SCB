from random import randint
from random import sample
import numpy as np 
import math
import os

# blocks = number of blocks created
# m_0 = m in first instance
# delta = m added to each next instance
# ratio1 = n/m (make it an int)
# ratio2*m = coverage size
# ratio3 = r/m

def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

def create_instance(m, block, index, ratio1, ratio2, ratio3):
    # create output file
    outputfile = "dat/informs2020/instance{}{}{}.graph".format(block, block, index)
    file = open(outputfile, 'w')
    # calculate parameters for blocks
    n = int(round(m*ratio1))
    coverage = int(round(n*ratio2))
    r = str(int(round(m*ratio3)))
    # write line 3 (lose target cost)
    k = []
    for i in range(n):
        k.append(randint(200, 400))
    k = ' '.join(map(str, k))
    file.write("{}\n".format(k))

    #define and write edges
    edges_created = 0
    target_list0 = list(range(n)) #list of n
    covered = [0 for i in range(n)] #start covered at 0 for every element
    subset_card = [0 for i in range(m)]
    
    for i in range(n):
        covering = sample(list(range(m)), coverage)
        for j in covering:
            file.write("{} {}\n".format(j,i))
            covered[j] += 1
            subset_card[j] += 1
    edges_created += n*coverage
    
    c = [0 for i in range(m)]

    for i in range(m):
        c[i] = 2*subset_card[i]

    file.close()

    # write line 2 (drone block cost)
    c = " ".join([str(j) for j in c])
    prepend_line(outputfile, "{}".format(c))

    # write line 1
    data1 = "{} {} {} {}".format(m, n, edges_created, r)
    prepend_line(outputfile, "{}".format(data1))

    avg_subset = 100*((sum(subset_card) / m) / n)
    avg_coverage = 100*((sum(covered) / n) / m)
    return [str(m), str(n), str(r), str(edges_created), str(avg_subset), str(avg_coverage)]


def generate(data, name):
    logfile = "dat/logfile1{}.txt".format(name)
    file = open(logfile, 'w')
    file2 = open("dat/testrun.sh", 'w')
    file3 = open("dat/testrun1.sh", 'w')
    for block, params in data.items():
        instances = params[0]
        m = params[1]
        ratio1 = params[2]
        ratio2 = params[3]
        ratio3 = params[4]

        for index in range(instances):
            call = "bin/main/ dat/informs2020/instance" + str(block) + str(index) + ".graph dat/informs2020/outputfiles/output" + str(block) + str(index) 
            call1 = "bin/main/ dat/informs2020/instance" + str(block) + str(block) + str(index) + ".graph dat/informs2020/outputfiles/output" + str(block) + str(block) + str(index)  
            file2.write(call+"\n") 
            file3.write(call1+"\n") 
            new_line = create_instance(m, block, index, ratio1, ratio2, ratio3) 
            new_line = ",".join(new_line)+"\n"
            file.write(new_line)   
            ratio1 -= 1
            ratio2 += .1
            ratio3 += .05

data = {
    "A": [5, 25, 5, 0.1, 0.45],
    "B": [5, 50, 5, 0.1, 0.45],
    "C": [5, 75, 5, 0.1, 0.45],
    "D": [5, 100, 5, 0.1, 0.45],
}
generate(data, "oct10set1")
