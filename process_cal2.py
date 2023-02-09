#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 01 08:35:33 2022
@author: rivera

This is a text processor that allows to translate XML-based events to YAML-based events.
CAREFUL: You ARE NOT allowed using (i.e., import) modules/libraries/packages to parse XML or YAML
(e.g., yaml or xml modules). You will need to rely on Python collections to achieve the reading of XML files and the
generation of YAML files.
"""
import sys
import re
import datetime
import yaml
from operator import itemgetter

"""
This method writes the output onto the yaml file
"""
def outputYaml(z,c,b):
    file = open("output.yaml" , "w")
    file.write("events:")
    count = 0
    for i in z:
        if count == 0:
            so = datetime.date(int(i['year']), int(i['month']),int(i['day']))
            p = so.strftime('%d-%m-%Y')
            file.write("\n  - {}:".format(p))
            file.write("\n    - id: {}".format(i['id']))
            file.write("\n      description: {}".format(i['description']))
            for s in c:
                if s['id'] == i['location']:
                    file.write("\n      circuit: {} ({})".format(s['name'], s['direction']))
                    file.write("\n      location: {}".format(s['location']))
                    q = datetime.datetime.strptime(i['start'], "%H:%M")
                    a = datetime.datetime.strptime(i['end'], "%H:%M")                    
                    file.write("\n      when: {} - {}".format(q.strftime('%I:%M %p'), a.strftime('%I:%M %p')))
                    file.write(" {} ({})".format(so.strftime('%A, %B %d, %Y'), s['timezone']))
                    file.write("\n      broadcasters:\n")
                    sluv=i['broadcaster'].split(',')
                    for cv in sluv:
                        for zx in b:
                            if cv == zx['id']:
                                file.write("        - {}\n".format(zx['name']))
            count+=1
        elif count > 0:
            if z[count]['month'] == z[count - 1]['month'] and z[count]['day'] == z[count - 1]['day']:
                so = datetime.date(int(i['year']), int(i['month']),int(i['day']))
                p = so.strftime('%d-%m-%Y')
                file.write("    - id: {}".format(i['id']))
                file.write("\n      description: {}".format(i['description']))
                for s in c:
                    if s['id'] == i['location']:
                        file.write("\n      circuit: {} ({})".format(s['name'], s['direction']))
                        file.write("\n      location: {}".format(s['location']))
                        q = datetime.datetime.strptime(i['start'], "%H:%M")
                        a = datetime.datetime.strptime(i['end'], "%H:%M")                    
                        file.write("\n      when: {} - {}".format(q.strftime('%I:%M %p'), a.strftime('%I:%M %p')))
                        file.write(" {} ({})".format(so.strftime('%A, %B %d, %Y'), s['timezone']))
                        file.write("\n      broadcasters:\n")
                        sluv=i['broadcaster'].split(',')
                        for cv in sluv:
                            for zx in b:
                                if cv == zx['id']:
                                    file.write("        - {}\n".format(zx['name']))
                count+=1
            else:
                so = datetime.date(int(i['year']), int(i['month']),int(i['day']))
                p = so.strftime('%d-%m-%Y')
                file.write("  - {}:".format(p))
                file.write("\n    - id: {}".format(i['id']))
                file.write("\n      description: {}".format(i['description']))
                for s in c:
                    if s['id'] == i['location']:
                        file.write("\n      circuit: {} ({})".format(s['name'], s['direction']))
                        file.write("\n      location: {}".format(s['location']))
                        q = datetime.datetime.strptime(i['start'], "%H:%M")
                        a = datetime.datetime.strptime(i['end'], "%H:%M")                    
                        file.write("\n      when: {} - {}".format(q.strftime('%I:%M %p'), a.strftime('%I:%M %p')))
                        file.write(" {} ({})".format(so.strftime('%A, %B %d, %Y'), s['timezone']))
                        file.write("\n      broadcasters:\n")
                        sluv=i['broadcaster'].split(',')
                        for cv in sluv:
                            for zx in b:
                                if cv == zx['id']:
                                    file.write("        - {}\n".format(zx['name']))
                count+=1
"""
This method sorts the dictionary according to the month, day and begining of the event

"""         
def sorting_events(sleep,bm,bd,em,ed):
    slop = sleep
    slee = []
    cap = []
    for x in sorted(slop, key = itemgetter('month' , 'day' , 'start')):
        slee.append(x)
    
    bm = bm.zfill(2)
    bd = bd.zfill(2)
    ed = ed.zfill(2)
    em = em.zfill(2)

    for s in slee:
        if s['month'] >= bm and s['month'] <= em :
            if s['month'] == bm :
                if s['day'] >= bd :
                    cap.append(s)
            if s['month'] != bm and s['month'] != em:
                cap.append(s)
            if s['month'] == em:
                if s['day'] <= ed :
                    cap.append(s)
    return(cap)

"""
This method parses the event file

"""
def parse_event(broadcasters):
    broadcasters_array = []
    with open(broadcasters) as f:
        lines = f.readlines()
        current_broadcaster = -1
        for line in lines:
            line = line.strip()
            tag = re.search("<[a-z]*>", line)
            if tag != None:
                tag = tag.group()
            if tag == "<event>":
                current_broadcaster+=1
                broadcaster = {}
                broadcasters_array.append(broadcaster)
            elif tag != "<event>" and tag != None:
                data = re.search("\>(.*?)\<",line)
                if data:
                    data = data.group(1)
                    fill_events(broadcasters_array[current_broadcaster], tag, data)
    return broadcasters_array

def fill_events(current_broadcaster, tag, data):
    if tag == "<id>":
        current_broadcaster["id"] = data
    elif tag == "<description>":
        current_broadcaster["description"] = data
    elif tag == "<location>":
        current_broadcaster["location"] = data
    elif tag == "<day>":
        current_broadcaster["day"] = data
    elif tag == "<month>":
        current_broadcaster["month"] = data
    elif tag == "<year>":
        current_broadcaster["year"] = data
    elif tag == "<start>":
        current_broadcaster["start"] = data
    elif tag == "<end>":
        current_broadcaster["end"] = data
    elif tag == "<broadcaster>":
        current_broadcaster["broadcaster"] = data
"""
This method parses the circuit file

"""
def parse_circuits(broadcasters):
    broadcasters_array = []
    with open(broadcasters) as f:
        lines = f.readlines()
        current_broadcaster = -1
        for line in lines:
            line = line.strip()
            tag = re.search("<[a-z]*>", line)
            if tag != None:
                tag = tag.group()
            if tag == "<circuit>":
                current_broadcaster+=1
                broadcaster = {}
                broadcasters_array.append(broadcaster)
            elif tag != "<circuit>" and tag != None:
                data = re.search("\>(.*?)\<",line)
                if data:
                    data = data.group(1)
                    fill_circuit(broadcasters_array[current_broadcaster], tag, data)
    return broadcasters_array

def fill_circuit(current_broadcaster, tag, data):
    count = 0
    e = []
    if tag == "<id>":
        current_broadcaster["id"] = data
    elif tag == "<name>":
        current_broadcaster["name"] = data
    elif tag == "<location>":
        current_broadcaster["location"] = data
    elif tag == "<timezone>":
        current_broadcaster["timezone"] = data
    elif tag == "<direction>":
        current_broadcaster["direction"] = data

        e.append(current_broadcaster)
"""
This method parses the broadcaster file

"""
def parse_broadcasters(broadcasters):
    broadcasters_array = []
    with open(broadcasters) as f:
        lines = f.readlines()
        current_broadcaster = -1
        for line in lines:
            line = line.strip()
            tag = re.search("<[a-z]*>", line)
            if tag != None:
                tag = tag.group()
            if tag == "<broadcaster>":
                current_broadcaster+=1
                broadcaster = {}
                broadcasters_array.append(broadcaster)
            elif tag != "<broadcaster>" and tag != None:
                data = re.search("\>(.*?)\<",line)
                if data:
                    data = data.group(1)
                    fill_broadcaster(broadcasters_array[current_broadcaster], tag, data)
    return broadcasters_array

def fill_broadcaster(current_broadcaster, tag, data):
    count = 0
    if tag == "<id>":
        current_broadcaster["id"] = data
    elif tag == "<name>":
        current_broadcaster["name"] = data
    elif tag == "<cost>":
        current_broadcaster["cost"] = data
def main():
    """The main entry point for the program.
    """
    # Calling a dummy function to illustrate the process in Python
    begin = sys.argv[1]
    end = sys.argv[2]
    event = sys.argv[3]
    circuit = sys.argv[4]
    broadcaster = sys.argv[5]

    begins = begin.split('=')
    ends = end.split('=')
    events = event.split('=')
    circuits = circuit.split('=')
    broadcasters = broadcaster.split('=')
    start = begins[1].split("/")
    end = ends[1].split("/")

    beginyear = start[0]
    beginmonth = start[1]
    beginday = start[2]

    endyear = end[0]
    endmonth = end[1]
    endday = end[2]

    broadcasterss = broadcasters[1]
    circuitss = circuits[1]
    eventss = events[1]

    parse_broadcasters(broadcasterss)
    parse_circuits(circuitss)
    outputYaml(sorting_events(parse_event(eventss),beginmonth,beginday,endmonth,endday), parse_circuits(circuitss) , parse_broadcasters(broadcasterss))
    

if __name__ == '__main__':
    main()
