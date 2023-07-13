# -*- coding: utf-8 -*-
"""
Created on Wed May 10 16:44:00 2023

@author: tizia

A Daisyworld 3D project

NOTE for the 3D graphics: This model evolves and get to a certain stability
What u wwant to do is to creat a cool 3d rappresentation of the globe. 
You only need the % of white vrs black daisy. Starting with a random allocation of position for the flowers
at the next step, the total amount of white or black is changed
If the % is increased you keep the old position and fill in position close to the one already occupied by a certain color (of free ground). 
If one color is sourranded by the other type then, get a random position.
If the % is decreased you keep some position randomly and discard the remaining
"""

import random 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import Daisy_ as DW

def fill_daisy(D,w,b, w_old, b_old):
    
    '''
    This function take a the rate of growth for the black and white daisy and 
    convert it in a 2D matrix, considering the old positions and updating the 
    percentage of cover.
    
    Parameters
    ----------
    D : numpy.ndarray, 2x2 Matrix 
        Old positions of the daisy on the 2D space.
    w : float
        Updated percentage of white daisy.
    b : float
        Updated percentage of black daisy.

    Returns
    -------
    None.

    '''
    # Get old black daisy's pos
    b_i = np.where(D==-1)[0]
    b_j = np.where(D==-1)[1]
    b_idx = [(b_i[n],b_j[n]) for n in range(len(b_i))]
    
    # Get old white daisy's pos
    w_i = np.where(D==1)[0]
    w_j = np.where(D==1)[1]
    w_idx = [(w_i[n],w_j[n]) for n in range(len(w_i))]
    
    # Get old ground's positions
    g_i = np.where(D==0)[0]
    g_j = np.where(D==0)[1]    
    g_idx = [(g_i[n],g_j[n]) for n in range(len(g_i))]

    D_new = np.zeros((Nx,Ny))
    
    #UPDATE POSITION 
    
    # Old daisy died 
    if b_old > b :

        b_diff_no = (b_old - b)*Area # Number of total positios where daisy die
        #Sample from old position
        b_survive = random.sample(b_idx,int(b_old*Area - b_diff_no))
        
        new_ground = b_idx # remove black daisy if they die
        # Fill Black Daisy survived
        for pos in b_survive:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = -1
            
        # New ground has been created
            if pos in b_idx:
                new_ground.remove(pos)
        for pos in new_ground:
            g_idx.append(pos)  
            
            
    if w_old > w :

        w_diff_no = (w_old - w)*Area # Number of total positios where daisy die
        
        #Sample from old position
        w_survive = random.sample(w_idx,int(w_old*Area - w_diff_no))
        
        new_ground = w_idx # remove white daisy if they die

        # Fill White Daisy survived
        for pos in w_survive:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = 1
        
        # New ground has been created
            if pos in w_idx:
                new_ground.remove(pos)
        for pos in new_ground:
            g_idx.append(pos)           

#  Radom choice from ground available space
    if w_old < w :
        # Add old flower
        for pos in w_idx:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = 1
            
        w_diff_no = np.round((w - w_old)*Area) # Number of total new positios to fill
        
        pos_list = [] # Store the position close to which a new flower grow
        for n in range(int(w_diff_no)):                  
            # where the new daisy will appear ?        
            pos_temp = random.choice(g_idx)

            x_pos = pos_temp[0]
            y_pos = pos_temp[1]        
            D_new[x_pos,y_pos] = 1
            
            pos_list.append(pos_temp)
            
            g_idx.remove(pos_temp)
 

    if b_old < b :
        # Add old flower
        for pos in b_idx:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = -1

        b_diff_no = np.round((b - b_old)*Area) # Number of total new positios to fill
        
        pos_list = [] # Store the position close to which a new flower grow
        for n in range(int(b_diff_no)):                  
            # where the new daisy will appear ?        
            pos_temp = random.choice(g_idx)

            x_pos = pos_temp[0]
            y_pos = pos_temp[1]        
            D_new[x_pos,y_pos] = -1
            
            pos_list.append(pos_temp)
            g_idx.remove(pos_temp)
 
            
    # If the % of daisy is unchanged, then add old position
    
    if  b_old == b :              
        for pos in b_idx:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = -1 
            
    if  w_old == w :              
        for pos in w_idx:
            x_pos = pos[0]
            y_pos = pos[1]
            D_new[x_pos,y_pos] = 1 
            
    return D_new

#%%

def get_3D_DW(pattern,rotate=(45,45)):
    ''' 

    Parameters
    ----------
    pattern : numpy.ndarray, 2x2 Matrix
        Position of the daisy.
    rotate : tuple, optional
        Latitute and Longitude view point. The default is (45,45).

    Returns
    -------
    3D spherical proection.

    '''

    steps_x = Nx*1j ; steps_y = Ny*1j
    u, v = np.mgrid[0:2*np.pi:steps_x, 0:np.pi:steps_y]

    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    
    lat = rotate[0]
    long = rotate[1]
    
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(projection='3d')
    ax.set_axis_off()

    globe  = ax.scatter(x ,y ,z, c=pattern, s=14 , cmap = plt.cm.jet)

    ax.legend(*[globe.legend_elements()[0],['black','ground','white']], loc='best', fontsize=16) #,title="Legend")
    ax.view_init(lat, long)
    plt.show() 

def get_2D_DW(pattern, time_step):
    
    '''
    This plotting style is implemented for comparison purposes
    '''
    plt.figure(figsize=(10,10))
    plt.imshow(pattern,cmap='jet')
    plt.title(f'{time_step}')
    #plt.colorbar()
    plt.show()
    
#%%
pi = np.pi

# Call function evolution from Daisy_.py file
white_d , black_d, ground_d, T_globe = DW.evolve() 

N = len(white_d)

# Spatial grid
Lx = 1 ; Ly = 1
dx = 0.01 ; dy = 0.01
Nx = int(Lx/dx) ; Ny = int(Ly/dy)

x = np.arange(0, Lx, dx)
y = np.arange(0, Ly, dy)
z = np.ones(Nx)

X, Y = np.meshgrid(x,y)

w0 = white_d[0]
b0 = black_d[0]

Daisy = np.zeros(Nx*Ny)
Area = Nx*Ny
sample_pos_white = int(Area*w0)
sample_pos_black = int(Area*b0)

Daisy[:sample_pos_white] = 1

Daisy[sample_pos_white:sample_pos_white+sample_pos_black] = -1
np.random.shuffle(Daisy)
Daisy = Daisy.reshape((Nx,Ny))

#%%
for t in range(1,N):
    Daisy_copy = Daisy
    new_white =  np.round(white_d[t], 4); new_black = np.round(black_d[t],4)
    old_white =  np.round(white_d[t-1], 4); old_black = np.round(black_d[t-1], 4)
    Daisy_new = fill_daisy(Daisy,new_white, new_black, old_white, old_black)
    
    #print("%:",white_d[t], black_d[t], t)
    #print(np.count_nonzero(Daisy_new))
    
    Daisy = Daisy_new
    
    delta_t = 10  # Jump in the plotting  
    if t%delta_t == 0:
        print(t, np.count_nonzero(Daisy_new))
        # To Plot 2D version uncomment line "get_2D_DW(Daisy, t)"
        get_3D_DW(Daisy)
        #get_2D_DW(Daisy, t)

