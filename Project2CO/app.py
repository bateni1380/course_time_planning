import time_changer
import os
import gams

day_of_week = {'1': 'Saturday', '2': 'Sunday', '3': 'Monday', '4': 'Tuesday', '5': 'Wednesday'}
time_of_day = {'1': '8-10', '2': '10-12', '3': '13-15', '4': '15-17', '5': '7:45-9:15', '6': '9:15-10:45',
               '7': '10:45-12:15', '8': '13:30-15', '9': '15-16:30'}


lecturer_courses = []
lecturer_times = []

c_python = [str(c) for c in range(1,19)]
l_python = [str(l) for l in range(1,7)]
d_python = [str(d) for d in range(1,6)]
h_time = [(8,10),(10,12),(13,15),(15,17),(7.75,9.25),(9.25,10.75),(10.75,12.25),(13.5,15),(15,16.5)]

s_tuples = [("1","2","8","9","18"),("2","3","10","11","18"),("3","4","5","12","13","14"),("7","8","16","17"),("5","12","13","14","15","17")]
nc = [1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3] #len(nc) = c
hh_python = '3'
dd_python = '5'
k_python = 2

lecturer_courses.append(("1","2","18"))#lecturer 1
lecturer_courses.append(("3","8","9"))#lecturer 2
lecturer_courses.append(("4","10","11"))
lecturer_courses.append(("5","6","12"))
lecturer_courses.append(("7","13","14"))
lecturer_courses.append(("15","16","17"))

lecturer_times.append(("111100000","111100000","111100000","111100000","111100000"))
lecturer_times.append(("111100000","000000000","111100000","000000000","111100000"))
lecturer_times.append(("111000000","111000000","111000000","111000000","111000000"))
lecturer_times.append(("110000000","110000000","110000000","110000000","110000000"))
lecturer_times.append(("000000000","111100000","000000000","110000000","000000000"))
lecturer_times.append(("110000000","110000000","110000000","110000000","000000000"))


# PREPARING DATASET
# making sorted distinct end nodes for p(i)
end_nodes = [e[0] for e in h_time] + [e[1] for e in h_time]
end_nodes_distinct = []
for e in end_nodes:
    if e not in end_nodes_distinct:
        end_nodes_distinct.append(e)
end_nodes_distinct.sort()
end_nodes = end_nodes_distinct

i_python = [str(i) for i in range(1, len(end_nodes))]
j_python = [str(j) for j in range(1, len(s_tuples) + 1)]
h_python = [str(h) for h in range(1, len(h_time) + 1)]

# making {}_python variables
s_python = {}
for j in range(len(s_tuples)):
    for c in c_python:
        s_python[(j_python[j], c)] = (c in s_tuples[j])

p_python = {}


def does_share(class_time, sub_time):
    return class_time[0] <= sub_time[0] and class_time[1] >= sub_time[1]


for i in range(len(i_python)):
    for h in range(len(h_python)):
        p_python[(i_python[i], h_python[h])] = does_share(h_time[h], (end_nodes[i], end_nodes[i + 1]))

n_python = {}
for i in range(len(c_python)):
    n_python[c_python[i]] = nc[i]

a_python = {}
for l in range(len(lecturer_courses)):
    for c in c_python:
        a_python[(c, l_python[l])] = (c in lecturer_courses[l])

b_python = {}
for l in range(len(lecturer_times)):
    for d in range(len(lecturer_times[l])):
        for h in range(len(lecturer_times[l][d])):
            b_python[(l_python[l], d_python[d], h_python[h])] = int(lecturer_times[l][d][h])

# PREPARING GAMS
BASE_DIR = os.path.abspath('')

ws = gams.workspace.GamsWorkspace(working_directory=BASE_DIR)
db = ws.add_database()

# send sets
c_gams = db.add_set("c", 1)
for ip in c_python:
    c_gams.add_record(ip)

l_gams = db.add_set("l", 1)
for ip in l_python:
    l_gams.add_record(ip)

d_gams = db.add_set("d", 1)
for ip in d_python:
    d_gams.add_record(ip)

h_gams = db.add_set("h", 1)
for ip in h_python:
    h_gams.add_record(ip)

j_gams = db.add_set("j", 1)
for ip in j_python:
    j_gams.add_record(ip)

i_gams = db.add_set("i", 1)
for ip in i_python:
    i_gams.add_record(ip)

# send single value parameters
dd_gams = db.add_set("dd", 1)
dd_gams.add_record(dd_python).value = 'yes'

hh_gams = db.add_set("hh", 1)
hh_gams.add_record(hh_python).value = 'yes'

k_gams = db.add_parameter("k", 0)
k_gams.add_record().value = k_python

# send parameters
p_gams = db.add_parameter_dc("p", [i_gams, h_gams])
for ip in i_python:
    for jp in h_python:
        p_gams.add_record((ip, jp)).value = p_python[(ip, jp)]

s_gams = db.add_parameter_dc("s", [j_gams, c_gams])
for ip in j_python:
    for jp in c_python:
        s_gams.add_record((ip, jp)).value = s_python[(ip, jp)]

n_gams = db.add_parameter_dc("n", [c_gams])
for ip in c_python:
    n_gams.add_record((ip)).value = n_python[(ip)]

a_gams = db.add_parameter_dc("a", [c_gams, l_gams])
for ip in c_python:
    for jp in l_python:
        a_gams.add_record((ip, jp)).value = a_python[(ip, jp)]

b_gams = db.add_parameter_dc("b", [l_gams, d_gams, h_gams])
for ip in l_python:
    for jp in d_python:
        for kp in h_python:
            b_gams.add_record((ip, jp, kp)).value = b_python[(ip, jp, kp)]

# RUN MODEL (Z1)
opt = ws.add_options()
opt.defines["gdxincname"] = db.name
# db.export("C:\\Users\\rahim\\Desktop\\z1.gdx")
m = ws.add_job_from_file("z1.gms")

time_changer.win_back()
m.run(opt, databases=db)
# m.run()
time_changer.win_update()

# print result
print("final result1: ")

for rec in m.out_db["z1"]:
    z1_python = rec.level
    print(z1_python)

for i in m.out_db["stat"]:
    state = str(i).split("=")[-1]
    print("model state is: ", state)
    if state == "1.0":
        print("Optimal Solution Found!!!")

    elif state == "10.0":
        print("Solution Infeasible...")

# RUN MODEL (Z2)
z1_gams = db.add_parameter("z1", 0)
z1_gams.add_record().value = z1_python

opt = ws.add_options()
opt.defines["gdxincname"] = db.name
# db.export("C:\\Users\\rahim\\Desktop\\z2.gdx")
m = ws.add_job_from_file("z2.gms")

time_changer.win_back()
m.run(opt, databases=db)
# m.run()
time_changer.win_update()

# print result
print("final result z2: ")

for rec in m.out_db["z2"]:
    z2_python = rec.level
    print(z2_python)

for i in m.out_db["stat"]:
    state = str(i).split("=")[-1]
    print("model state is: ", state)
    if state == "1.0":
        print("Optimal Solution Found!!!")

    elif state == "10.0":
        print("Solution Infeasible...")

# RUN MODEL (Z3)
z2_gams = db.add_parameter("z2", 0)
z2_gams.add_record().value = z2_python

opt = ws.add_options()
opt.defines["gdxincname"] = db.name
# db.export("C:\\Users\\rahim\\Desktop\\z3.gdx")
m = ws.add_job_from_file("z3.gms")

time_changer.win_back()
m.run(opt, databases=db)
# m.run()
time_changer.win_update()

# print result
print("final result z3: ")

for rec in m.out_db["z3"]:
    z3_python = rec.level
    print(z3_python)

for i in m.out_db["stat"]:
    state = str(i).split("=")[-1]
    print("model state is: ", state)
    if state == "1.0":
        print("optimal solution found!!!")

    elif state == "10.0":
        print("solution infeasible...")

# PRINT WEEKLY SCHEDULE
delta_python = {}

for rec in m.out_db["delta"]:
    delta_python[(rec.key(0), rec.key(1), rec.key(2))] = rec.level

for d in d_python:
    print(day_of_week[d] + " :\t", end="")
    for h in h_python:
        courses = [c for c in c_python if delta_python[(c, d, h)] == 1]
        if len(courses) > 0:
            print(time_of_day[h] + "(", end="")
            for i in range(len(courses) - 1):
                print(courses[i] + ", ", end="")
            print(courses[-1] + ")\t", end="")
    print("\n", end="")
