# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:32:22 2018

@author: 3702980
"""

import numpy as np
import random

N = 10 #number of neurons
seuil = -10 #the threshold of activation of neuron, in mV, global variable, used in functions

def init_syst_links(nb_neuron):
    """Create a matrix of 2 dimensions which shows the connections between neurons in the system.
    Initiated randomly and stay the same always.
    syst_links[i][j] = 1: i connects and can send signal to j, not in reverse
    syst_links[i][j] = 0: i doesnt connect to j
    syst_links[i][i] = k: the decrease factor of potential of the neuron i"""
    syst_links = np.random.randint(2, size = (N,N))
    i = 0
    for i in range(N):
        syst_links[i][i] = random.randrange(0.9,0.95)
    return syst_links
    
def init_syst_potentiel(nb_neuron):
    """Create a matrix of 2D which shows the potential of each neuron at time t of the simulation.
    Initiated randomly.
    syst_potentiel[i][j] = 0 for every i != j;
    syst_potentiel[i][i] = value of potential of neuron i"""
    
    #A COMPLETER
    
    return syst_potentiel


def init_syst_state(nb_neuron):
    """Create a matrix of size(nb_neuron,1) which shows the state of activation of a neuron.
    Initiated randomly.
    syst_act[i][0] = 0: neuron i isnt activated, it cant send signal to others
    syst_act[i][0] = 1: neuron i is activated and can send signal to others
    When the potential of a neuron i passes the threshold, syst_act[i][0] = 1 at the next step
    After release all its potential, syst_act[i][0] = 0 at the next step"""
    
    return syst_state

    
def matrix_Ni(nb_neuron):
    """Create a matrix 2D which helps keeping the potential of chaque neuron of the previous step to the next step
    Size: (nb_neuron,1)
    Only the i of the neuron in current execution is set to 1. All the others elements are 0."""
    
    return matrix_Ni
    
    
def func_act(val_poten):
    """float => float
    Calculate the potential of a neuron at the time t  using the sigmoid function"""
    
    return poten_new
    

def update_syst_potentiel(syst_potentiel, syst_links, syst_state):
    """Calculate the potentials of all the neurons at the time t+1
    All neurons will be update simultaneously.
    Return the potentials of the whole system in form matrix."""
    
    return new_syst_potentiel
    

def update_syst_state(syst_potentiel, syst_state):
    """Take in to account the state of activation of all neurons in time t+1 
    which depends on its potential in this time t+1"""
    
    return new_syst_state
    


def simulation(syst_potentiel, syst_links, syst_state, duration):
    """Return a list of all the matrixes, each matrix shows the potentials of the system
    at moment t, 


    
