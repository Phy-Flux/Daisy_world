# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 13:31:23 2022

@author: Tiziana Comito

A Daisyworld 3D project

In this code all variables uses standard unit (W,K,m) SI

"""

# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

#%%
pi = np.pi

def evolve(init_white= 0.2,init_black =0.2, sl=800):
    
    def global_state(a_w,a_b):
        q = 20
        SL = sl #Wm^(-2) average solar flux incident on the Earth
        a_g = (1 - a_w - a_b) 
        
        A = a_g*A_g + a_w*A_w + a_b*A_b # Planetary albedo
        
        T = (SL*(1-A)/sigma)**(0.25)
        T_w = T + q*(A-A_w)
        T_b = T + q*(A-A_b)
    
        return(A,a_g,T_w,T_b, T)    

    def beta_fun_temp(T_loc):
        k = 17.5**(-2)
        T_e = 295.5
        if np.abs(T_loc - T_e) < k**(-1/2):
            beta = 1 - k*(T_loc - T_e)**2
        else:
            beta = 0
        return beta    

    def RHS(a_w,a_b,T_w,T_b):
        # Evolution growth equations for the daisy
        
        # gamma= deah rate is kept constant
        # Beta is the function that takes into acount local temp. 
        x = 1 - a_w - a_b
        
        beta_w = beta_fun_temp(T_w)    
        beta_b = beta_fun_temp(T_b)
    
        daw_dt = a_w*(x*beta_w - gamma)
        dab_dt = a_b*(x*beta_b - gamma)
    
        return(daw_dt,dab_dt)
    
    # Runge Kutta for time marching
    def RK(w,b,T_w,T_b):
    
        k1_w, k1_b = RHS(w,b,T_w,T_b)
        k2_w, k2_b = RHS(w + k1_w*dt/2,b + k1_b*dt/2,T_w,T_b)
        k3_w, k3_b = RHS(w + k2_w*dt/2,b + k2_b*dt/2,T_w,T_b)
        k4_w, k4_b = RHS(w + k3_w*dt, b + k3_b*dt,T_w,T_b)   
        w_new = w + ( k1_w/6 + k2_w/3 + k3_w/3 + k4_w/6)*dt 
        b_new = b + ( k1_b/6 + k2_b/3 + k3_b/3 + k4_b/6)*dt 
    
        return(w_new,b_new)
        
    
    # PARAMETERS-------------------------------------------------------------------
     
    sigma= 5.670*(10**(-8))#W m−2 K−4 (in SI units) Boltzmann Constant
    gamma = 0.2 # Death rate
    A_g = 0.5 ; A_w = 0.75 ; A_b = 0.25 # ground, white and black albedo
    
    # STORING the evolution's growth
    aw_list = []
    ab_list = []
    ag_list = []
    global_temp = []
    
    # Time marching
    dt = 0.1
    t_fin = 400
    
    a_w_old = init_white # Initial cover of white daisy
    a_b_old = init_black # Initial cover of black daisy
    
    for t in range(t_fin):
        
        A_old, a_g_old, T_w_old, T_b_old, T_g_old = global_state(a_w_old, a_b_old)
        
        aw_list.append(a_w_old)
        ab_list.append(a_b_old)
        ag_list.append(a_g_old)
        global_temp.append(T_g_old)    
            
        a_w_new, a_b_new = RK(a_w_old,a_b_old, T_w_old, T_b_old)
        
        a_w_old = a_w_new
        a_b_old = a_b_new
    
    return(aw_list,ab_list,ag_list, global_temp)

# The user can imput the solar incoming radiation. 
solar_radiation = float(input("Enter incoming solar radiation:"))

# Change initial percentace of daisy cover by setting: init_white, and init_black
aw_list,ab_list,ag_list,global_temp = evolve(init_white= 0.3,init_black =0.1)#,sl=solar_radiation)

#%%
# Plot rate of groth of the daisy
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,8))

ax1.plot(np.array(aw_list),c = 'red', label='white')
ax1.plot(np.array(ab_list),c = 'blue', label='back')
ax1.plot(np.array(ag_list),c = 'green', label='ground')
ax1.set(xlabel='dt', ylabel='%')
#ax1.xlabel('dt')
ax1.set_title('Daisy Groth Rate')
ax1.legend()

# Plot of the Global temperature
ax2.plot(np.array(global_temp),c = 'orange')
ax2.set_title('Global Temperature')
ax2.set(xlabel='dt', ylabel='K')

plt.show()