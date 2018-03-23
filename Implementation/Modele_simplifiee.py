# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:32:22 2018

@author: 3702980
"""

import numpy as np
import random

N = 5 #number of neurons
seuil = 60 #the threshold of activation of neuron, in mV, global variable, used in functions
Vmax = 120
nb_steps = 10 #number of simulation

def init_syst_links():
    """Create a matrix of 2 dimensions which shows the connections between neurons in the system.
    Initiated randomly and stay the same always. (a transpose matrix of the regular matrix)
    syst_links[i][j] = 1: j connects and can send signal to i, not in reverse
    syst_links[i][j] = 0: j doesnt connect to i
    syst_links[i][i] = k: the decrease factor of potential of the neuron i"""
    syst_links = np.random.rand(N,N)
    for i in range(N):
        for j in range(N):
            if i != j:
                syst_links[i][j] = random.choice([0.0, 1.0])
            else:
                syst_links[i][j] = random.uniform(0.9,0.95)
    syst_links.transpose()
    return syst_links

def init_syst_potentiel():
    """Create a matrix of 2D which shows the potential of each neuron at time t of the simulation.
    Initiated randomly.
    syst_potentiel[i][j] = 0 for every i != j;
    syst_potentiel[i][i] = value of potential of neuron i"""

    syst_potentiel = np.zeros((N,N))
    return syst_potentiel


def init_syst_state():
    """Create a matrix of size(nb_neuron,1) which shows the state of activation of a neuron.
    Initiated randomly.
    syst_act[i][0] = 0: neuron i isnt activated, it cant send signal to others
    syst_act[i][0] = 1: neuron i is activated and can send signal to others
    When the potential of a neuron i passes the threshold, syst_act[i][0] = 1 at the next step
    After release all its potential, syst_act[i][0] = 0 at the next step"""

    syst_state = np.zeros((N,1))
    return syst_state

    
def matrix_Ni(i):
    """Create a matrix 2D which helps keeping the potential of each neuron of the previous step to the next step
    Size: (nb_neuron,1)
    Only the i of the neuron in current execution is set to 1. All the others elements are 0."""

    matrix_Ni = np.zeros((N,1))
    matrix_Ni[i][0] = 1
    return matrix_Ni


def func_act(val_poten):
    """float => float
    If the potential of a neuron is superior than the threshold, it's activated.
    When a neuron is activated, its potential increase immediately to Vmax"""
    if val_poten < seuil:
        return val_poten
    else:
        return Vmax
    

def start_syst(syst_potentiel, syst_state):
    """Send in the information in form electric ranged between 0 and Vmax (mV)
     to kick off the system.
     Return a matrix of the potentials of the system and a matrix of the neurons' states"""

    kicked_off = syst_potentiel
    state_chaged = syst_state
    for i in range(N):
        kicked_off[i][i] = func_act(syst_potentiel[i][i] + random.uniform(0, Vmax))
        if kicked_off[i][i] > seuil:
            state_chaged[i][0] = 1
        else:
            state_chaged[i][0] = 0
    return (kicked_off, state_chaged)


def update_system(syst_potentiel, syst_links, syst_state):
    """matrix(N,N) * matrix(N,N) * matrix(N,1) -> tuple(matrix(N,N), matrix(N,1))
    Calculate the potentials of all the neurons at the time t+1 and also update theirs state at time t+1 (activated or not)
    All neurons will be update simultaneously.
    Return the potentials and their states of the whole system in form matrix."""
    new_syst_potentiel = syst_potentiel
    new_syst_state = syst_state
    var = 0 #variable temporary
    for i in range(N):
        if syst_potentiel[i][i] == Vmax:
            new_syst_potentiel[i][i] = 0
            new_syst_state[i][0] = 0
        else:
            #print((-1) ** syst_state[i][0])
            var = np.dot(syst_links[i], np.dot(syst_potentiel, syst_state + matrix_Ni(i)))
            var = func_act(var)
            if var == Vmax:
                new_syst_state[i][0] = 1
            else:
                new_syst_state[i][0] = 0
            new_syst_potentiel[i][i] = var

    return (new_syst_potentiel, new_syst_state)
    


def non_transmittable(syst_state):
    """Verify if there is no neuron that can transmit signal to others
    return a bool"""
    res = True
    for i in range(N):
        if syst_state[i][0] == 1:
            res = False
            break
    return res


def simulation(syst_potentiel, syst_links, syst_state, nb_steps):
    """Return a list of all the matrixes, each matrix shows the potentials of the system
    at moment t"""
    #res: list[matrix(N,N)]
    res = []
    new_p = syst_potentiel
    res.append(new_p.copy())
    new_s = syst_state
    for i in range(nb_steps):
        if non_transmittable(new_s):
            new_p, new_s = start_syst(new_p, new_s)
        else:
            new_p, new_s = update_system(new_p, syst_links, new_s)
        res.append(new_p.copy())
    return res



####Start the program

Vt = init_syst_potentiel()
C = init_syst_links()
Tt = init_syst_state()
Vt, Tt = start_syst(Vt, Tt)
res = simulation(Vt,C, Tt, nb_steps)

print(res)
