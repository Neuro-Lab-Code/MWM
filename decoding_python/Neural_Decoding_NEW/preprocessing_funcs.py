import numpy as np
from scipy.stats import circmean
import math
######## BIN_SPIKES ########
def bin_spikes(spike_times,dt,wdw_start,wdw_end):
    """
    Function that puts spikes into bins

    Parameters
    ----------
    spike_times: an array of arrays
        an array of neurons. within each neuron's array is an array containing all the spike times of that neuron
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for putting spikes in bins
    wdw_end: number (any format)
        the end time for putting spikes in bins

    Returns
    -------
    neural_data: a matrix of size "number of time bins" x "number of neurons"
        the number of spikes in each time bin for each neuron
    """
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    num_neurons=spike_times.shape[0] #Number of neurons
    neural_data=np.empty([num_bins,num_neurons]) #Initialize array for binned neural data
    #Count number of spikes in each bin for each neuron, and put in array
    for i in range(num_neurons):
        neural_data[:,i]=np.histogram(spike_times[i],edges)[0]
    return neural_data


######## BIN_SPIKES ##################### Mina Added, using df/f instead of spikes
def bin_spikes_hist(spike_times,df,dt,wdw_start,wdw_end):
    """
    Function that puts spikes into bins

    Parameters
    ----------
    spike_times: an array of arrays
        an array of neurons. within each neuron's array is an array containing all the spike times of that neuron
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for putting spikes in bins
    wdw_end: number (any format)
        the end time for putting spikes in bins

    Returns
    -------
    neural_data: a matrix of size "number of time bins" x "number of neurons"
        the number of spikes in each time bin for each neuron
    """
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    num_neurons=spike_times.shape[0] #Number of neurons
    neural_data=np.empty([num_bins,num_neurons]) #Initialize array for binned neural data
    
    
    for i in range(num_neurons):            
        xbins=edges
        A=[]
        A=np.array(df['Time'])
        B=[]
        B=np.array(df[i+1])
        keep=[]
        keep = ~np.isnan(B)
        n, XX = np.histogram(A, bins=xbins)
        sy, _ = np.histogram(A, bins=xbins, weights=B)
        neural_data[:,i] = sy / n
    return neural_data

def bin_spikes2(spike_times,df,dt,wdw_start,wdw_end):
    """
    Function that puts spikes into bins

    Parameters
    ----------
    spike_times: an array of arrays
        an array of neurons. within each neuron's array is an array containing all the spike times of that neuron
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for putting spikes in bins
    wdw_end: number (any format)
        the end time for putting spikes in bins

    Returns
    -------
    neural_data: a matrix of size "number of time bins" x "number of neurons"
        the number of spikes in each time bin for each neuron
    """
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    num_neurons=spike_times.shape[0] #Number of neurons
    neural_data=np.empty([num_bins,num_neurons]) #Initialize array for binned neural data
    #neural_data[:]=np.NaN
    #Count number of spikes in each bin for each neuron, and put in array
    #for i in range(num_neurons):
        #neural_data[:,i]=np.histogram(spike_times[i],edges)[0]
    for t in range((len(edges)-1)):
        temp=[]
        temp=(df['Time']>=edges[t]) & (df['Time']<edges[t+1])
        for i in range(num_neurons):
            temp2=[]
            temp2=df.loc[temp, i+1].mean()
            if np.isnan(temp2):
                neural_data[t,i]=np.NaN
               # neural_data[t,i]=0
            else:
                neural_data[t,i]=temp2
    return neural_data


######## BIN_OUTPUT #######
def bin_output(outputs,output_times,dt,wdw_start,wdw_end,downsample_factor=1):
    """
    Function that puts outputs into bins

    Parameters
    ----------
    outputs: matrix of size "number of times the output was recorded" x "number of features in the output"
        each entry in the matrix is the value of the output feature
    output_times: a vector of size "number of times the output was recorded"
        each entry has the time the output was recorded
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for binning the outputs
    wdw_end: number (any format)
        the end time for binning the outputs
    downsample_factor: integer, optional, default=1
        how much to downsample the outputs prior to binning
        larger values will increase speed, but decrease precision

    Returns
    -------
    outputs_binned: matrix of size "number of time bins" x "number of features in the output"
        the average value of each output feature in every time bin
    """

    ###Downsample output###
    #We just take 1 out of every "downsample_factor" values#
    if downsample_factor!=1: #Don't downsample if downsample_factor=1
        downsample_idxs=np.arange(0,output_times.shape[0],downsample_factor) #Get the idxs of values we are going to include after downsampling
        outputs=outputs[downsample_idxs,:] #Get the downsampled outputs
        output_times=output_times[downsample_idxs] #Get the downsampled output times

    ###Put outputs into bins###
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    output_dim=outputs.shape[1] #Number of output features
    outputs_binned=np.empty([num_bins,(output_dim)]) #Initialize matrix of binned outputs
    #Loop through bins, and get the mean outputs in those bins
    print('thisdis df')
    for i in range(num_bins): #Loop through bins
        idxs=np.where((np.squeeze(output_times)>=edges[i]) & (np.squeeze(output_times)<edges[i+1]))[0] #Indices to consider the output signal (when it's in the correct time range)
        '''
        for j in (range(output_dim)): #Loop through output features
            outputs_binned[i,j]=np.mean(outputs[idxs,j])
        '''   
        for j in range((output_dim)): #Loop through output features
           # outputs_binned[i,j]=np.mean(outputs[idxs,j])
            B=[]
            B=outputs[idxs,j];
            bb=[]
            for b in B:
                #bb.append(math.radians(b))
                bb.append(b)
               # L_M=math.degrees(circmean(bb))
            L_M=[]
            pi = np.pi
            L_M=[circmean(bb,high=pi, low=-pi)]
            
            xwrap=np.remainder(L_M, 2*np.pi)
            mask = np.abs(xwrap)>np.pi
            xwrap[mask] -= 2*np.pi * np.sign(xwrap[mask])
            outputs_binned[i,0]=math.sin(xwrap)
            outputs_binned[i,1]=math.cos(xwrap)
            #outputs_binned[i,2]=xwrap
            
           
    return outputs_binned
######## BIN_OUTPUT ####### Mina Added, decoing the position separatey
def bin_output_pos(outputs,output_times,dt,wdw_start,wdw_end,downsample_factor=1):
    """
    Function that puts outputs into bins

    Parameters
    ----------
    outputs: matrix of size "number of times the output was recorded" x "number of features in the output"
        each entry in the matrix is the value of the output feature
    output_times: a vector of size "number of times the output was recorded"
        each entry has the time the output was recorded
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for binning the outputs
    wdw_end: number (any format)
        the end time for binning the outputs
    downsample_factor: integer, optional, default=1
        how much to downsample the outputs prior to binning
        larger values will increase speed, but decrease precision

    Returns
    -------
    outputs_binned: matrix of size "number of time bins" x "number of features in the output"
        the average value of each output feature in every time bin
    """

    ###Downsample output###
    #We just take 1 out of every "downsample_factor" values#
    if downsample_factor!=1: #Don't downsample if downsample_factor=1
        downsample_idxs=np.arange(0,output_times.shape[0],downsample_factor) #Get the idxs of values we are going to include after downsampling
        outputs=outputs[downsample_idxs,:] #Get the downsampled outputs
        output_times=output_times[downsample_idxs] #Get the downsampled output times

    ###Put outputs into bins###
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    output_dim=outputs.shape[1] #Number of output features
    outputs_binned=np.empty([num_bins,(output_dim)]) #Initialize matrix of binned outputs
    outputs_binned[:]=np.NaN
    #Loop through bins, and get the mean outputs in those bins
    print('thisdis dfmina')
    for i in range(num_bins): #Loop through bins
        idxs=np.where((np.squeeze(output_times)>=edges[i]) & (np.squeeze(output_times)<edges[i+1]))[0] #Indices to consider the output signal (when it's in the correct time range)
        
        for j in (range(output_dim)): #Loop through output features
            outputs_binned[i,j]=np.mean(outputs[idxs,j])
        '''   
        for j in range((output_dim)): #Loop through output features
           # outputs_binned[i,j]=np.mean(outputs[idxs,j])
            B=[]
            B=outputs[idxs,j];
            bb=[]
            for b in B:
                #bb.append(math.radians(b))
                bb.append(b)
               # L_M=math.degrees(circmean(bb))
            L_M=[]
            pi = np.pi
            L_M=[circmean(bb,high=pi, low=-pi)]
            
            xwrap=np.remainder(L_M, 2*np.pi)
            mask = np.abs(xwrap)>np.pi
            xwrap[mask] -= 2*np.pi * np.sign(xwrap[mask])
            outputs_binned[i,0]=math.sin(xwrap)
            outputs_binned[i,1]=math.cos(xwrap)
            #outputs_binned[i,2]=xwrap
         '''   
           
    return outputs_binned
######## BIN_OUTPUT ####### Mina Added, decoing the distance separatey


######## BIN_OUTPUT ####### Mina Added, decoing the all (pos,HD,Anchor,distance) separatey
def bin_output_all(outputs,output_times,dt,wdw_start,wdw_end,downsample_factor=1):
    """
    Function that puts outputs into bins

    Parameters
    ----------
    outputs: matrix of size "number of times the output was recorded" x "number of features in the output"
        each entry in the matrix is the value of the output feature
    output_times: a vector of size "number of times the output was recorded"
        each entry has the time the output was recorded
    dt: number (any format)
        size of time bins
    wdw_start: number (any format)
        the start time for binning the outputs
    wdw_end: number (any format)
        the end time for binning the outputs
    downsample_factor: integer, optional, default=1
        how much to downsample the outputs prior to binning
        larger values will increase speed, but decrease precision

    Returns
    -------
    outputs_binned: matrix of size "number of time bins" x "number of features in the output"
        the average value of each output feature in every time bin
    """
############################### position
    ###Downsample output###
    #We just take 1 out of every "downsample_factor" values#
    if downsample_factor!=1: #Don't downsample if downsample_factor=1
        downsample_idxs=np.arange(0,output_times.shape[0],downsample_factor) #Get the idxs of values we are going to include after downsampling
        outputs=outputs[downsample_idxs,:] #Get the downsampled outputs
        output_times=output_times[downsample_idxs] #Get the downsampled output times

    ###Put outputs into bins###
    edges=np.arange(wdw_start,wdw_end,dt) #Get edges of time bins
    num_bins=edges.shape[0]-1 #Number of bins
    output_dim=outputs.shape[1] #Number of output features
    outputs_binned=np.empty([num_bins,(output_dim)]) #Initialize matrix of binned outputs
    outputs_binned[:]=np.NaN
    #Loop through bins, and get the mean outputs in those bins
    print('this is all position')
    for i in range(num_bins): #Loop through bins
        idxs=np.where((np.squeeze(output_times)>=edges[i]) & (np.squeeze(output_times)<edges[i+1]))[0] #Indices to consider the output signal (when it's in the correct time range)
        
        for j in (range(2)): #Loop through output features
            outputs_binned[i,j]=np.mean(outputs[idxs,j])
        '''   
        for j in range((output_dim)): #Loop through output features
           # outputs_binned[i,j]=np.mean(outputs[idxs,j])
            B=[]
            B=outputs[idxs,j];
            bb=[]
            for b in B:
                #bb.append(math.radians(b))
                bb.append(b)
               # L_M=math.degrees(circmean(bb))
            L_M=[]
            pi = np.pi
            L_M=[circmean(bb,high=pi, low=-pi)]
            
            xwrap=np.remainder(L_M, 2*np.pi)
            mask = np.abs(xwrap)>np.pi
            xwrap[mask] -= 2*np.pi * np.sign(xwrap[mask])
            outputs_binned[i,0]=math.sin(xwrap)
            outputs_binned[i,1]=math.cos(xwrap)
            #outputs_binned[i,2]=xwrap
      
      '''   
      
    
   
    return outputs_binned
######## BIN_OUTPUT ####### Mina Added, decoing the all (pos,HD,Anchor,distance) separatey

###$$ GET_SPIKES_WITH_HISTORY #####
def get_spikes_with_history(neural_data,bins_before,bins_after,bins_current=1):
    """
    Function that creates the covariate matrix of neural activity

    Parameters
    ----------
    neural_data: a matrix of size "number of time bins" x "number of neurons"
        the number of spikes in each time bin for each neuron
    bins_before: integer
        How many bins of neural data prior to the output are used for decoding
    bins_after: integer
        How many bins of neural data after the output are used for decoding
    bins_current: 0 or 1, optional, default=1
        Whether to use the concurrent time bin of neural data for decoding

    Returns
    -------
    X: a matrix of size "number of total time bins" x "number of surrounding time bins used for prediction" x "number of neurons"
        For every time bin, there are the firing rates of all neurons from the specified number of time bins before (and after)
    """

    num_examples=neural_data.shape[0] #Number of total time bins we have neural data for
    num_neurons=neural_data.shape[1] #Number of neurons
    surrounding_bins=bins_before+bins_after+bins_current #Number of surrounding time bins used for prediction
    X=np.empty([num_examples,surrounding_bins,num_neurons]) #Initialize covariate matrix with NaNs
    X[:] = np.NaN
    #Loop through each time bin, and collect the spikes occurring in surrounding time bins
    #Note that the first "bins_before" and last "bins_after" rows of X will remain filled with NaNs, since they don't get filled in below.
    #This is because, for example, we cannot collect 10 time bins of spikes before time bin 8
    start_idx=0
    for i in range(num_examples-bins_before-bins_after): #The first bins_before and last bins_after bins don't get filled in
        end_idx=start_idx+surrounding_bins; #The bins of neural data we will be including are between start_idx and end_idx (which will have length "surrounding_bins")
        X[i+bins_before,:,:]=neural_data[start_idx:end_idx,:] #Put neural data from surrounding bins in X, starting at row "bins_before"
        start_idx=start_idx+1;
    return X
