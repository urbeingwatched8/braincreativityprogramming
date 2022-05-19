import glob
import os

import mne
import sys
sys.path.append('../../../')
# import configuration
import numpy as np
#mindlink

def raw_features(trial_path):
    '''
        This method return raw feature from one trial. It was implemented canse
        I want to see the whether the feature extracting could make a different 
        and it did.
        
        Arguments:
           
            trial_path: the path in file system of the trial
        
        Returns:
            
            The raw features. numpy-array-like.
        
    '''
    raw_obj = mne.io.read_raw_fif(trial_path + 'EEG.raw.fif', preload=True, verbose='ERROR')
    raw_obj = add_asymmetric(raw_obj) 
    total_time = int(raw_obj.times.max())
    features = []
    for i in range(0, total_time-1):
        sub_raw_obj = raw_obj.copy().crop(i, i+1)
        data = np.mean(sub_raw_obj.get_data(), axis = 1)
        features.append(data)
    return np.array(features)


def get_average_psd(sub_raw_obj, fmin, fmax):
    '''
    This method returns a the average log psd feature for a MNE raw object
    
    Arguments:
        
        sub_raw_obj: a raw object from MNE library
        
        fmin: the minium frequency you are intreseted
        
        fmax: the maximum frequency you are intreseted
        
    Returns:
        
        average_psd: the required psd features, numpy array like. 
        shape: (the number of the features, )
    
    '''
    try:
        psds, freq = mne.time_frequency.psd_multitaper(sub_raw_obj, fmin=fmin, fmax=fmax, n_jobs=4, verbose='ERROR')
        # print("psds:\n", type(psds), "\n", psds.shape)
        # print("psds:\n", psds)
    except:
        print("get_avg_psds error")
        return False
    # preventing overflow
    psds[psds <= 0] = 1
    psds = 10 * np.log10(psds)
    average_psd = np.mean(psds, axis=1)
    return average_psd


def extract_average_psd_from_a_trial(raw_obj, average_second, overlap):
    '''
    This method returns the average log psd features for a trial
    
    Arguments:
        
        raw_obj: a MNE raw object contains the information from a trial.
        
        average_second: the time unit for average the psd.
        
        overlap: how much overlap will be used.
        
    Returns:
        features: the features of multiply sample.
        shape (the sample number, the feature number)
    
    '''
    
    assert overlap >= 0 and overlap < 1
    
    total_time = int(raw_obj.times.max())
    features = []
    move = average_second * (1 - overlap)
    for start_second in np.arange(0, total_time, move):
        if (start_second + average_second > total_time):
            break
        sub_raw_obj = raw_obj.copy().crop(start_second, 
                                  start_second + average_second)
        
        theta_average_psd = get_average_psd(sub_raw_obj, 4, 7.5)
        alpha_average_psd = get_average_psd(sub_raw_obj, 7.5, 14)
        beta_1_average_psd = get_average_psd(sub_raw_obj, 14, 20)
        beta_2_average_psd = get_average_psd(sub_raw_obj, 20, 30)
        #if ((theta_average_psd is False) 
        #        or (alpha_average_psd is False) or (beta_1_average_psd is False)
        #        or (beta_2_average_psd is False)):
        #    return False

        #feature = np.concatenate((theta_average_psd,
         #                         alpha_average_psd, beta_1_average_psd, 
          #                        beta_2_average_psd), axis=None)
        features.append(beta_2_average_psd)
    
    return np.array(features)


def get_a_channel_data_from_raw(raw_obj, channel_name):
    '''
        Arguments:
            
            raw_obj: raw object from MNE library.
            
            channel_name: the name of the channel.
            
        Returns:
            
            the numpy array data for the channel.
    
    '''
    return np.array(raw_obj.copy().pick_channels([channel_name]).get_data()[0])


def raw_to_numpy_one_trial(EEG_path, save_path):
    '''
        read one-trial raw EEG from hard dick, extract the feature and write it
        back.
        
        Arguments:
            
            path: the trial's path
        
    '''
    # print("\nsave_path:\n", save_path, "\n")
    # EEG_path = path + 'EEG.raw.fif'
    raw = mne.io.read_raw_fif(EEG_path, preload=True, verbose='ERROR')
    
    #raw = add_asymmetric(raw)
    data = extract_average_psd_from_a_trial(raw, 1, 0.5)
    # error_path = save_path
    if data is False:
        return save_path
    number0 = EEG_path.split(".")
    number1 = number0[0].split("Trial")
    length0 = len(number1)
    detail = number1[length0-1]
    # save_path = save_path+'/'+detail+'/'
    save_path = save_path + '/'
    np.save(save_path+'EEG.npy', data)
    return True


def exist_nan_data(EEG_path):
    '''
        check whether NAN data exist after extracting the feature
        
        Arguments:
            
            path: the trial path
            
        Returns:
            
            True if NAN data exist else False.
    '''
    # EEG_path = path + 'EEG.npy'
    import os
    if os.path.exists(EEG_path) == False:
        return True
    data = np.load(EEG_path)
  
    return True if np.sum(np.isnan(data)) > 0 else False


def exist_inf_data(EEG_path):
    '''
    
        check whether INF data exist after extracting the feature
        
        Arguments:
            
            path: the trial path
            
        Returns:
            
            True if INF data exist else False.
    
    '''
    # EEG_path = path + 'EEG.npy'
    import os
    if os.path.exists(EEG_path) == False:
        return True
    data = np.load(EEG_path)
    
    return True if np.sum(np.isinf(data)) > 0 else False


if __name__ == '__main__':
    # ROOT_PATH = configuration.DATASET_PATH + 'newMAHNOB_HCI/'
    # dataset_path = configuration.DATASET_PATH + "newMAHNOB_HCI/*"
    dataset_path = 'D:\experiments'
    dirPath = glob.iglob(dataset_path)
    path = dataset_path.replace('/*', '')
    # print(dirPath)
    num_of_folder = 0
    num_of_fif = 0
    num_of_success_fif = 0
    error_list = []
    # test = 0

    for big_file in dirPath:
        num_of_folder += 1
        print("num_of_folder: ", num_of_folder)
        files = os.listdir(big_file)
        #print('here are files')
        #print(files)
        for file in files:
            if file.endswith(".fif"):
                print('foundone')
                # test += 1

                num_of_fif += 1
                file_path = os.path.join(big_file, file)  # 路径+文件名
                file_path = file_path.replace('\\', '/')
                print(file_path)
                result = raw_to_numpy_one_trial(file_path, big_file.replace('\\', '/'))
                num_of_success_fif += 1
                if result is not True:
                    print("error error error !!! !!!\n", result)
                    num_of_success_fif -= 1
                    error_list.append(result)




    print("num_of_fif: ", num_of_fif)
    print("num_of_success_fif: ", num_of_success_fif)
    print("num_of_folder: ", num_of_folder)
    print("error list:\n", error_list)
    print("main.end......")