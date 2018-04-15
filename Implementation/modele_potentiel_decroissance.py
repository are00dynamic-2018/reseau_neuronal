
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

N = 20 #number of neurons
Vseuil = 60 #the threshold of activation of neuron, in mV, global variable, used in functions
Vmax = 120 #Vmax maximum can be attained
Vmin= -20 #Vmin minimum can be attained
Vmin_ma = -20
tau_min = 10
tau_max=20
tPA = 1
deltaT = 0.1
tPH = 0.6
tH = 1.2
alpha = 1
nb_steps = 20 #number of simulation
beta=0.55 #beta*Vmax




### Functions for initiations


###Create matrix link C with coefficients equal to 1,0 or -1
def init_syst_links():
    """Create a matrix of 2 dimensions which shows the connections between neurons in the system.
    Initiated randomly and stay the same always. (a transpose matrix of the regular matrix)
    syst_links[i][j] = 1: j connects and can send signal to i, not in reverse
    syst_links[i][j] = 0: j doesnt connect to i
    syst_links[i][i] = k: the decrease factor of potential of the neuron i"""
    syst_links = np.random.rand(N, N)
    for i in range(N):
        for j in range(N):
            if i != j:
                syst_links[i][j] = random.choice([0.0, 1.0]) * (-1) * random.choice([0, 1])
            else:
                syst_links[i][j] = 1./beta
                #syst_links[i][j] is not equal to 1 because in the calculation of the new potentiel of a neuron 
                #the result of Lc,i*Vt*[ Tt+Ni -Vseuil*Tt] is then mutiplie by beta, so C[i][i] must be equal to 1/beta 
                #to have later beta*C[i][i]=1 (in order to have 1*V_i(t)+ Sum(Potentiel_other_neurons) 
                #and not (1/beta)*V_i(t)+ Sum(Potentiel_other_neurons)
    syst_links.transpose()
    return syst_links





###Create the matrix which takes into accounts the weights of transmission from a neuron to others
def decomposer_1(n):
    """int -> list[float]
    Return a list of n random floats whose sum is 1"""
    res = np.random.random(size = n)
    res /= res.sum()
    return res

def compter_connections(connection):
    """list[int] -> int
    Take a list of interger (0 or 1) and return the number of elements equal to 1 in the list."""
    k = 0
    for i in range(len(connection)):
        if connection[i] == 1:
            k+= 1
    return k 

def pre_init_syst_links_weights():
    """Create a matrix of 2 dimensions which shows the connections between neurons in the system.
    Initiated randomly and stay the same always. (a transpose matrix of the regular matrix)
    syst_links[i][j] = 1: j connects and can send signal to i, not in reverse
    syst_links[i][j] = 0: j doesnt connect to i"""
    syst_links = np.zeros((N,N), dtype = float)
    for i in range(N):
        for j in range(N):
            if i != j:
                syst_links[i][j] = random.choice([0.0, 1.0])
            else:
                syst_links[i][j] = 1./beta
    syst_links= syst_links.transpose()
    return syst_links


def init_syst_links_weights():
    systPoids = pre_init_syst_links_weights()
    systPoids = np.transpose(systPoids)
    L = [] #list of float whose sum equals to 1
    for i in range(N):
        L = decomposer_1(compter_connections(systPoids[i]))
        k = 0
        for j in range(N):
            if i != j and systPoids[i][j] == 1:
                systPoids[i][j] = L[k] * (-1) ** random.choice([0.0,1.0])
                k = k + 1
    systPoids = np.transpose(systPoids)
    return systPoids





###Decompose the matrix C into three other matrix Cn,Ce,Ci in order to take in consideration 
###of alcohol in the network

def list_of_active_entry(C,i):
    '''Return the index of all row i (i!=j) in the columb j that are different from 0 '''
    L=[]
    for k in range(N):
        if(k!=i and C[i][k]!=0 ):
            L.append(k)

    return L



def increase_of_alcohol_concentration(C,Cn,Ce,Ci,nb_entry_exc,nb_entry_inh):
    for i in range(N):
        Lcolumb=list_of_active_entry(Cn,i) 
        #list that contains the index of row i (i!=k) from the columb k in C that are note equal to 0 
        #(>0 for Lrow_exc and <0 for Lrow_inh)
        random.shuffle(Lcolumb)
        
        min_inh=min( len(Lcolumb),nb_entry_inh )
        min_exc=min( len(Lcolumb),nb_entry_exc )
        
        for l in range( max(min_exc,min_inh) ):
            
            if(l<min_inh):
                j=Lcolumb[l]
                Ci[i][j]=Cn[i][j]
                Cn[i][j]=0
            if(l<min_exc):
                j=Lcolumb[l]
                Ce[i][j]=Cn[i][j]
                Cn[i][j]=0
                
                
    return (Cn, Ce, Ci)


def decrease_of_alcohol_concentration(C,Cn,Ce,Ci,nb_entry_exc,nb_entry_inh):
    for i in range(N):
        Lcolumb_exc=list_of_active_entry(Ce,i) 
        Lcolumb_inh=list_of_active_entry(Ci,i)
        #list that contains the index of row i (i!=k) from the columb k in C that are note equal to 0 
        #(>0 for Lrow_exc and <0 for Lrow_inh)
        random.shuffle(Lcolumb_exc)
        random.shuffle(Lcolumb_inh)
        
        min_inh=min( len(Lcolumb_inh),nb_entry_inh )
        min_exc=min( len(Lcolumb_exc),nb_entry_exc )
        
        for l in range( max(min_exc,min_inh) ):
            
            if(l<min_inh):
                j=Lcolumb_inh[l]
                Cn[i][j]=Ci[i][j]
                Ci[i][j]=0
            if(l<min_exc):
                j=Lcolumb_exc[l]
                Cn[i][j]=Ce[i][j]
                Ce[i][j]=0
                
                
    return (Cn, Ce, Ci)


def decompose_syst_links_alcohol(C,Cn,Ce,Ci,old_ca,ca):
    #Ce is the matrix links that contains the links which are affect by alcohol in an excitatrice way
    #Ce is the matrix links that contains the links which are affect by alcohol in an inhibitrice way
    #Cn is the matrix links that contains the other links
    #At this point, C = Cn + Ce +Ci
    #c_a (between 0 and 1) is the concentration of alcohol in the network (the number of entry affect by alcohol). 
    #    each neuron is affected in the same way (the same number of entries are affected for all the neuron)
    
    if(len(Cn)==0):
        Cn=copy.deepcopy(C)
        Ce=np.zeros((N,N),dtype=float)
        Ci=np.zeros((N,N),dtype=float)
    
    nb_entry=int( np.ceil( abs(old_ca-ca)*N) ) #number of entries affected by alcohol for one neuron
    
    if(nb_entry==0):
        return (Cn,Ce,Ci)
    
    nb_entry_inh=random.randint(0,nb_entry)
    nb_entry_exc=nb_entry-nb_entry_inh
    
    
    if(old_ca<ca):
        Cn, Ce, Ci = increase_of_alcohol_concentration(C,Cn,Ce,Ci,nb_entry_exc,nb_entry_inh)
    elif(old_ca>ca):
        Cn, Ce, Ci = decrease_of_alcohol_concentration(C,Cn,Ce,Ci,nb_entry_exc,nb_entry_inh)
      
    
    return (Cn, Ce, Ci)





def init_syst_potentiel():
    """Create a matrix of 2D which shows the potential of each neuron at time t of the simulation.
    Initiated randomly.
    syst_potentiel[i][j] = 0 for every i != j;
    syst_potentiel[i][i] = value of potential of neuron i"""

    syst_potentiel = np.zeros((N, N), dtype=float)
    return syst_potentiel


def init_syst_state():
    """Create a matrix of size(nb_neuron,1) which shows the state of activation of a neuron.
    Initiated randomly.
    syst_act[i][0] = 0: neuron i isnt activated, it cant send signal to others
    syst_act[i][0] = 1: neuron i is activated and can send signal to others
    When the potential of a neuron i passes the threshold, syst_act[i][0] = 1 at the next step
    After release all its potential, syst_act[i][0] = 0 at the next step"""

    syst_state = np.zeros((N,1), dtype=int)
    return syst_state




def matrix_Ni(i):
    """Create a matrix 2D which helps keeping the potential of each neuron of the previous step to the next step
    Size: (nb_neuron,1)
    Only the i of the neuron in current execution is set to 1. All the others elements are 0."""

    matrix_Ni = np.zeros((N,1), dtype=int)
    matrix_Ni[i][0] = 1

    return matrix_Ni


def init_syst_phase():
    """Create a matrix of size (N,1) which keeps tracks of the phase of all the neurons in the system.
    There are 5 phases stated in the document of algorithme."""

    syst_phase = np.zeros((N, 1), dtype=int)
    return syst_phase



def init_syst_lambda():
    """Create a matrix of size (N,1) which helps keep tracks of the coefficient lambda which decides the pourcentage
    of Vmax can be attained in the next depolarisation."""

    syst_lambda = np.ones((N, 1), dtype=float)
    return syst_lambda



def init_time_rest():
    """Create a matrix of size (N,1) which count the steps taken by all neurons of the system after they were depolarised"""

    time_rest = np.zeros((N, 1), dtype=float)
    return time_rest



###Fonctions to update value of maximum reachable potentiel during a depolarization


def give_time_ar(lamb):
    #We need to have (1-lamb) and not lamb because when the neuron depolarize for the first time for a long moment
    #the time of post-hyperpolarization and hyperpolarisation reach their minimun value 
    #(which is 1*[(tPH + tH) + deltaT)] for lamb=1). So when lamb=1 we must have math.exp(alpha * (1 - lamb))=1
    #And with lamb=1, (1 - lamb)=0, so math.exp(alpha * (1 - lamb))=1
    return math.exp(alpha * (1 - lamb)) * (tPH + tH) + deltaT


def update_lamb(lamb, time_rest):
    new_lamb = lamb * (1 - (time_rest / (math.exp(alpha * (1-lamb)) * (tPH + tH) + deltaT)))
    return new_lamb




###Functions to operate system


### All func_act functions is to calculate the final output potential of a neuron for the current step after the period
### of transmission between neurons.
### Create different activate functions for each phase reduces the number of comparisons required later which will
### improve the execution time
def func_act_0(potentiel):
    """float -> float
    The function activate of the system is to modify the potential of each neuron corresponding
    to its current phase = 0 and depending on its sum of reception from others"""
    #V_new: potential of neuron after affected by the activate function
    V_new = 0
    if potentiel > 0:
        if potentiel < Vseuil:
            V_new = potentiel * math.exp(-1. / (tau_min+tau_max*potentiel/Vseuil) * math.log(100 * Vseuil))
        else:
            V_new = Vseuil
    elif potentiel < 0:
        if potentiel >= Vmin_ma :
            V_new = potentiel * math.exp(-1. / (tau_min+tau_max*potentiel/Vseuil) * math.log(100 * abs(Vmin_ma)))
        else :
            V_new = Vmin_ma
    return V_new

def func_act_1(potentiel, lamb):
    """float -> float
    The function activate of the system is to modify the potential of each neuron corresponding
    to its current phase = 1 and depending on its sum of reception from others"""
    #V_new: potential of neuron after affected by the activate function
    V_new = potentiel + (2. * lamb * (Vmax - Vseuil) * deltaT / (tPA - deltaT))
    var = lamb * (Vmax - Vseuil) + Vseuil  # var temporary to stock the value of Vmax of the current depolarisation
    if V_new >= var:
        V_new = var
    return V_new

def func_act_2(potentiel, lamb):
    """float -> float
    The function activate of the system is to modify the potential of each neuron corresponding
    to its current phase = 2 and depending on its sum of reception from others"""
    #V_new: potential of neuron after affected by the activate function
    V_new = potentiel - (2. * lamb * (Vmax - Vseuil) * deltaT / (tPA - deltaT))
    if V_new <= Vseuil:
        V_new = Vseuil
    return V_new

def func_act_3(potentiel, lamb):
    """float -> float
    The function activate of the system is to modify the potential of each neuron corresponding
    to its current phase = 3 and depending on its sum of reception from others"""
    #V_new: potential of neuron after affected by the activate function
    V_new = potentiel - deltaT*(Vseuil - lamb * Vmin) / (math.exp(alpha * (1-lamb)) * tPH)
    if V_new < lamb * Vmin:
        V_new = lamb * Vmin
    return V_new

def func_act_4(potentiel, lamb):
    """float -> float
    The function activate of the system is to modify the potential of each neuron corresponding
    to its current phase = 4 and depending on its sum of reception from others"""
    #V_new: potential of neuron after affected by the activate function
    V_new = potentiel - (lamb * Vmin * deltaT / (math.exp(alpha * (1-lamb)) * tH))
    if V_new > 0:
        V_new = 0
    return V_new



def start_syst(syst_potentiel, syst_state, syst_phase):
    """Send in the information in form electric ranged between 0 and (Vseuil + Vmax)/2 (mV) to kick off the system.
    we suppose that this function will only be called when there are no transmission in between the neurons and all the
    neurons are at phase 0 (we still wait until the neurones at phase 3 and 4 rest at 0 and turns to phase 0,
    meanwhile, others neurons at phase 0 will still decrease as defined)
     Return None as the parametres given to the function is already modified"""

    for i in range(N):
        syst_potentiel[i][i] = func_act_0(syst_potentiel[i][i] + random.uniform(0, (Vseuil + Vmax)/2))
        if syst_potentiel[i][i] == Vseuil:
            syst_state[i][0] = 1
            syst_phase[i][0] = 1

    return None

def start_syst_1(syst_potentiel, syst_state, syst_phase, syst_lambda, time_rest):
    """Send in the information in form electric ranged between 0 and Vseuil (mV) to kick off the system.
    we suppose that this function will only be called when there are no transmission in between the neurons which means
    all neurons are at phase {0,3,4}. Indeed, if a neuron in phase 3 or 4 is activated after this functions is called,
    the new Vmax will be calculated, else, we have to set its lambda back to 1
    Return None as the parametres given to the function is already modified"""

    for i in range(N):
        syst_potentiel[i][i] = func_act_0(syst_potentiel[i][i] + random.uniform(0, Vseuil))
        if syst_potentiel[i][i] == Vseuil:
            if syst_phase[i][0] == 3 or syst_phase[i][0] == 4:
                syst_lambda[i][0] = update_lamb(syst_lambda[i][0], time_rest[i][0])
            syst_state[i][0] = 1
            syst_phase[i][0] = 1
        else:
            syst_lambda[i][0] = 1
            syst_phase[i][0] = 0
    return None

def non_transmittable(syst_state, syst_phase):
    """Verify if there is no transmission between neurons and all neurons are at phase 0
    This function is compatible with the function start_syst
    return a bool"""
    res = True
    for i in range(N):
        if syst_state[i][0] == 0 or syst_phase[i][0] != 0:
            res = False
            break
    return res

def non_transmittable_1(syst_state):
    """Verify if there is no transmission between neurons
    This function is compatible with the function start_syst_1
    return a bool"""
    res = True
    for i in range(N):
        if syst_state[i][0] == 1:
            res = False
            break
    return res


def update_system(syst_potentiel, syst_links_n,syst_links_e, syst_state, syst_phase, syst_lambda, time_rest):
    """matrix(N,N) ^2 * matrix(N,1) ^5 -> tuple(matrix(N,N), matrix(N,1))
    Calculate the potentials of all the neurons at the time t+1 and also update theirs state at time t+1 (activated or not)
    All neurons will be update simultaneously.
    Return the potentials and their states of the whole system in form matrix."""
    new_syst_potentiel = init_syst_potentiel()
    new_syst_state = copy.deepcopy(syst_state)
    var = 0 #variable temporary
    digits=5 #number of digits to keep from a value
    for i in range(N):
        if syst_state[i][0] == 0:
            #if a neuron is not in the potential of action, it will receive from others (phase = {0,3,4})
            var = beta * np.dot(syst_links_n[i], np.dot(syst_potentiel,
                                                      syst_state + matrix_Ni(i)) + (-Vseuil) * syst_state)
            +np.dot(syst_links_e[i],beta*(Vmax-Vmin)*np.ones((N,1),dtype=float))
                  #+np.dot(syst_links_i[i],np.zeros((N,N),dtype=float)), but not useful because of np.zeros(())

            var=round(var,digits) 
            #only to solve rounding error of pyhton :
            #for few values of beta, (1./beta)*beta is not realy 1.0 but 1.000000000001 for exemple). 
            #Then it will affect all the conditions tests (in fact 1.000000000001!=1.0)
            #especially useful for the instruction func_act_0(var) 
            
            #manipulate the time_rest of neuron as it's in phase {0,3,4}
            if time_rest[i][0] > 0:
                #time_rest will be subtracted every step as long as syst_state[i][0] == 0
                time_rest[i][0] -= deltaT
            else:
                #the neuron i has waited enough time to reach the Vmax again, time_rest will be set at 0 until it will
                #be reset when the neuron depolarise again
                syst_lambda[i][0] = 1
                time_rest[i][0] = 0

        else:
            #else it will not receive transmission from others and behaves as defined ( phase = {1,2})
            var = syst_potentiel[i][i]
        #var stocks the sum of potential that a neuron has after receiving from others (period of transmission between
        #neurones) and before affected by func_act


        #In the code below, the lambda will only be updated when a neuron depolarise, no matter which phase it's in
        if syst_phase[i][0] == 0:
            new_syst_potentiel[i][i] = func_act_0(var)
            if new_syst_potentiel[i][i] == Vseuil:
                new_syst_state[i][0] = 1
                syst_phase[i][0] = 1
                #update syst_lamb. No need to consider the conditions as we already update it above
                syst_lambda[i][0] = update_lamb(syst_lambda[i][0], time_rest[i][0])
                # as the neuron is depolarised again, the time will be reset but this step will take place when
                # the neuron finishes its 2nd phase (decrese from Vmax to Vseuil)

        elif syst_phase[i][0] == 1:
            new_syst_potentiel[i][i] = func_act_1(var, syst_lambda[i][0])
            Vmax_current = syst_lambda[i][0] * (Vmax - Vseuil) + Vseuil
            if new_syst_potentiel[i][i] == Vmax_current:
                syst_phase[i][0] = 2

        elif syst_phase[i][0] == 2:
            new_syst_potentiel[i][i] = func_act_2(var, syst_lambda[i][0])
            if new_syst_potentiel[i][i] == Vseuil:
                new_syst_state[i][0] = 0
                syst_phase[i][0] = 3
                time_rest[i][0] = give_time_ar(syst_lambda[i][0])

        elif syst_phase[i][0] == 3:
            #because var=round(var,5), we also have to compare var with a rounding potentiel
            if var != round(syst_potentiel[i][i],digits):
                #the neuron in phase 3 receives potential non zero from others so it breaks off from the
                #phase 3 and return into a neuron of phase 0
                syst_phase[i][0] = 0
                new_syst_potentiel[i][i] = func_act_0(var)
                if new_syst_potentiel[i][i] == Vseuil:
                    #if its potential increase directly to pass the Vseuil, it steps into phase 1 but with new value of
                    #Vmax calculated after coeff lambda correspondant
                    new_syst_state[i][0] = 1
                    syst_phase[i][0] = 1
                    #the neurone is depolarised for a new period when it's still in phase 3 so we recalculate lambda
                    syst_lambda[i][0] = update_lamb(syst_lambda[i][0], time_rest[i][0])
                    #as the neuron is depolarised again, the time will be reset but this step will take place when
                    #the neuron finishes its 2nd phase (decrese from Vmax to Vseuil)

                #else: the coeff lambda will be updated after, when the neuron depolarise again
            else:
                #the neuron in phase 3 doesn't receive any potential from others so it will continue to decrease by the
                #function defined for this phase
                new_syst_potentiel[i][i] = func_act_3(var, syst_lambda[i][0])
                if new_syst_potentiel[i][i] == syst_lambda[i][0] * Vmin:
                    syst_phase[i][0] = 4

        elif syst_phase[i][0] == 4:
            #same mecanisme as phase 3
            if var != round(syst_potentiel[i][i],digits):
                syst_phase[i][0] = 0
                new_syst_potentiel[i][i] = func_act_0(var)
                if new_syst_potentiel[i][i] == Vseuil:
                    new_syst_state[i][0] = 1
                    syst_phase[i][0] = 1
                    syst_lambda[i][0] = update_lamb(syst_lambda[i][0], time_rest[i][0])
            else:
                new_syst_potentiel[i][i] = func_act_4(var, syst_lambda[i][0])
                if new_syst_potentiel[i][i] == 0:
                    #after a neuron of phase 4 reaches 0, everything is set back to starting point
                    syst_phase[i][0] = 0
    return (new_syst_potentiel, new_syst_state)



def simulation(syst_potentiel, syst_links_n,syst_links_e,syst_links_i, syst_state, syst_phase, syst_lambda, time_rest, nb_steps):
    """Return a list of all the matrixes, each matrix shows the potentials of the system
    at moment t"""
    # res_potentiels: list[matrix(N,N)]
    #res_states: list[matrix(N,1)]
    res_potentiels = []
    res_states = []

    new_p = syst_potentiel
    res_potentiels.append(copy.deepcopy(new_p))
    new_s = syst_state
    res_states.append(copy.deepcopy(new_s))

    for i in range(nb_steps):
        if non_transmittable_1(new_s):
            #normally it's improbable for this condition to occur when the neural network contains millions of neurons
            #but in the system with a small number of neuron, this condition makes sure the system will run continuously
            start_syst_1(new_p, new_s, syst_phase, syst_lambda, time_rest)
        else:
            new_p, new_s = update_system(new_p, syst_links_n,syst_links_e, new_s, syst_phase, syst_lambda, time_rest)

        res_potentiels.append(copy.deepcopy(new_p))
        res_states.append(copy.deepcopy(new_s))
    return (res_potentiels, res_states)


####Start the program

Vt = init_syst_potentiel()
C = init_syst_links()
Tt = init_syst_state()
E = init_syst_phase()
lamb = init_syst_lambda()
Tar = init_time_rest()
Cn,Ce,Ci=decompose_syst_links_alcohol(C,np.array([]),np.array([]),np.array([]),0,0)


start_syst(Vt, Tt, E)
res_potentials, res_states = simulation(Vt, Cn,Ce,Ci, Tt, E, lamb, Tar, nb_steps)

###Evolution le potentiel d'un neurone
beta=1

res_pot=[]
r=[]

Vt[0][0]=0
Vt[1][1]=0
Tt[0][0]=0
Tt[1][0]=0
E[0][0]=0
E[1][0]=0
new_p = copy.deepcopy(Vt)
new_s = copy.deepcopy(Tt)

for k in range(N):
    if(k!=0):
        C[0][k]=0
        C[k][0]=0
C[0][1]=1
C[0][2]=1
#set only one entry for the neuron one
res_pot=[]
Lstimu=[]
compt=0

i = 0

stimu1 = i  # stimu=1 : simulate an entry / stimu=0 no entry for the neuron one
stimu2 = i

if stimu1 == 1:
    if (new_s[1][0] != 1):
        new_p[1][1] = Vseuil
        new_s[1][0] = 1
        E[1][0] = 1
        lamb[1][0] = 1
        print("neurone 1 : fin de dépolarisation")
        if compt not in L:
            Lstimu.append(compt)

if stimu2 == 1:
    if (new_s[2][0] != 1):
        new_p[2][2] = Vseuil
        new_s[2][0] = 1
        E[2][0] = 1
        lamb[2][0] = 1
        print("neurone 2 : fin de dépolarisation")
        if compt not in L:
            Lstimu.append(compt)

compt += 1

if (new_s[0][0] == 1):
    print("dépolarisation")
    for k in range(int(tPA / deltaT)):
        new_p, new_s = update_system(new_p, C, new_s, E, lamb, Tar)
        res_pot.append(new_p[0][0])
else:
    new_p, new_s= update_system(new_p, C, new_s, E, lamb, Tar)
    res_pot.append(new_p[0][0])

print("potentiel neurone 0 : " + str(new_p[0][0]))

import matplotlib.lines as mlines

temps=[i for i in range(len(res_pot))]

fig=plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
ax.set_xlabel('Temps (ms)\n10 ud = 1 ms ')
ax.set_ylabel('Potentiel (mV)')
for k in range(len(res_pot)-1):
    if(k in Lstimu):
        plt.plot([temps[k],temps[k+1]],[res_pot[k],res_pot[k+1]],color='red',marker="^",markerfacecolor="darkviolet",markeredgecolor="dimgrey",markevery=2,markersize=6)
    else:
        plt.plot([temps[k],temps[k+1]],[res_pot[k],res_pot[k+1]],color='red')


marker = mlines.Line2D([], [], color='darkviolet', marker='^', markersize=6,markerfacecolor="darkviolet",markeredgecolor="dimgrey",linestyle='None',label="Stimulation d'une ou de plusieurs entrees")
line=mlines.Line2D([], [], color='red',label="Courbe simulee")

ax.legend(handles=[line,marker])
plt.show()
fig.savefig("courbe_demo_modelisation.pdf")






def in_list(L,element,radius):
    res=False
    for k in range(len(L)):
        if((element[0]-L[k][0])**2+(element[1]-L[k][1])**2<=radius**2):
            res=True
    return res


def annimate_network_ini(resultat_potentials, resultat_states, C, radius=2):
    N = 2 * len(resultat_states[0])  # N= number of neurons in the network
    Lo = []

    for i in range(N):
        E = [random.uniform(0, N), random.uniform(0, N)]
        while in_list(Lo, E, radius):
            E = [random.uniform(0, N), random.uniform(0, N)]
        Lo.append(E)
    print("Organisation spatiale faite")
    # Lo contains the coordinates of 2D array that will help to have a spacial organization of the ntework

    LcoordX = []
    LcoordY = []
    Lpotent = []

    for k in range(len(resultat_states)):
        Lx = []  # temporary variable
        Ly = []
        Lp = []
        for l in range(len(resultat_states[k])):
            if (resultat_states[k][l] == 1):  # the l neurons has been activated on the previous step
                # Below, we want to show the link beteween the neuro which was activated and the neurons which will receive the signal
                for i in range(len(C)):
                    if (C[i][l] != 0 and l != i):
                        Lx.append([Lo[l][0], Lo[i][0]])
                        # L.append([coord_x_neuron_l,coord_y_neuron_l],[coord_x_neuron_i,coord_y_neuron_i])
                        # After we will plot a line between the neuron l and i
                        Ly.append([Lo[l][1], Lo[i][1]])

                        Lp.append([resultat_potentials[k][l][l], abs(C[i][l]) * resultat_potentials[k][l][l]])
            else:
                Lx.append([Lo[l][0], -1])
                Ly.append([Lo[l][1], -1])
                Lp.append([resultat_potentials[k][l][l], -1])

        LcoordX.append(copy.deepcopy(Lx))
        LcoordY.append(copy.deepcopy(Ly))
        Lpotent.append(copy.deepcopy(Lp))
        # On a single step of the animation we have to plot all the link between neurons which were activated

    print("FIN")

    return LcoordX, LcoordY, Lpotent, N

LcoordX,LcoordY,Lpotent,N = annimate_network_ini(res_potentials,res_states,C,radius=1)

i=0
s=len(LcoordX[i])
for k in range(s):
    plt.plot(LcoordX[i][k][0],LcoordY[i][k][0],marker='o',markeredgecolor='red')
    plt.plot(LcoordX[i][k][1],LcoordY[i][k][1],marker='o',markeredgecolor='red')
plt.show()

Lvars = [0, beta * Vmax, 10, 5, 1]  # [max_object_line,beta*Vmax,markersize_max,markersize_min,line_size_max]
for L in LcoordX:
    if len(L) > Lvars[0]:
        Lvars[0] = len(L)
# We have to plot Lvars[0] line. So we have to create Lvars[0] object line
fig, ax = plt.subplots()

for k in range(Lvars[0]):
    vars()['line' + str(k)], = ax.plot(0, 0, color='k')
    eval('line' + str(k)).axes.axis([0 - Lvars[2], N + Lvars[2], 0 - Lvars[2], N + Lvars[2]])
    # initialization of the Lvars[0] object line
    ax.set_facecolor("dimgrey")


def animate(i):
    t = ()  # tuple

    s = len(LcoordX[i])
    for k in range(Lvars[0]):
        if (k < s):
            markersize = abs(Lpotent[i][k][0]) * (Lvars[2] - Lvars[3]) / Lvars[1] + Lvars[3]

            X = LcoordX[i][k]
            Y = LcoordY[i][k]

            if (LcoordX[i][k][1] == -1):
                X = [LcoordX[i][k][0], LcoordX[i][k][0] + markersize]
                Y = [LcoordY[i][k][0], LcoordY[i][k][0] + markersize]
                linesize = 0

                if Lpotent[i][k][0] > 0:
                    color = "yellowgreen"
                else:
                    color = "c"
            else:
                linesize = Lpotent[i][k][1] * Lvars[4] / Lvars[1]
                color = "orangered"

            eval('line' + str(k)).set_data(LcoordX[i][k], LcoordY[i][k])
            eval('line' + str(k)).set_marker('o')
            eval('line' + str(k)).set_markersize(markersize)
            eval('line' + str(k)).set_markerfacecolor(color)
            eval('line' + str(k)).set_markeredgecolor(color)
            eval('line' + str(k)).set_markevery(2)
            # allow to plot marker only on the start of the line (the neuron which has been activated)
            # the value is equal to 2 because we plot line by line (just with 2 points)
            eval('line' + str(k)).set_linewidth(linesize)
            eval('line' + str(k)).set_color("orange")

        else:
            eval('line' + str(k)).set_data(0, 0)
            eval('line' + str(k)).set_markersize(0)
        # update data of objects lines

        t = t + (eval('line' + str(k)),)
        # cmap2 = colors.LinearSegmentedColormap.from_list('my_colormap',['dimgrey','dimgrey','dimgrey'],256)

    return t

    # eval(name) get variable by string name
    # vars()[name] set variable by string name

ani = animation.FuncAnimation(fig, animate, nb_steps, blit=True,)
FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
ani.save("test.mp4",writer= FFwriter)
print("FAIT")