# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 22:01:13 2021

@author: Muhammad Salman Kabir
@purpose: Reading and processing .edf file
@regarding: Internship 2021 LIPS
"""

## Importing necassary libraries
import mne
from mne.preprocessing import compute_proj_ecg, compute_proj_eog
import numpy as np

## Data loading
# Filename (change it according to your need)
Filename = "somefile.edf"

# Importing data
EDF_Object = mne.io.read_raw_edf(Filename)

## Marking and droping bad channels
# Data plotting before marking bad channels
EDF_Object.plot()

# Marking bad channels
EDF_Object.info["bads"] = ["EEG O2-Cz","EEG O1-Cz","EEG Fp1-Cz","EEG Fp2-Cz","EEG P3-Cz","EEG F3-Cz","event"]

# Data plotting after marking bad channels
EDF_Object.plot()

# Droping bad channels
EDF_Object.drop_channels(["EEG O2-Cz","EEG O1-Cz","EEG Fp1-Cz","EEG Fp2-Cz","EEG P3-Cz","EEG F3-Cz","event"])

## Artifacts removal: Heartbeat
ecg_projs, _ = compute_proj_ecg(EDF_Object,
                                         ch_name=("EEG F7-Cz"), 
                                         n_grad=0, 
                                         n_mag=0, 
                                         n_eeg=1, 
                                         reject=None)

EDF_Object.add_proj(ecg_projs)

# Data plotting after removing ECG
EDF_Object.plot()

## Artifacts removal: Ocular
eog_projs, _ = compute_proj_eog(EDF_Object,
                                         ch_name=("EEG F7-Cz"), 
                                         n_grad=0, 
                                         n_mag=0, 
                                         n_eeg=1, 
                                         reject=None)

EDF_Object.add_proj(eog_projs)

# Data plotting after removing EOG
EDF_Object.plot()


## Saving to .fif format
EDF_Object.save("somefile_Processed_raw.fif")

