import matplotlib.pyplot as plt
import os
import numpy as np
import itertools
from PIL import Image
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr, variation_of_information as vof, mean_squared_error as mse
from sewar.full_ref import uqi
import sklearn.preprocessing as preproc

############ Selection parameters #########
deviation_theshold = 0.99  # value < th
# High SSIM values = good quality image in terms of pixel movement (less movement)
SSIM_theshold = 0.1   # value > th
# Low SSIM's deviation values = good quality image in terms of pixel movement (less peaks of movement)
SSIM_deviation_theshold = 0.99  # value < th
############ End of election parameters #########

def deviation_trend(files, colors, markers, tmatsPath, results_path):
    # n images composed of m frames
    n = 0
    # xy_deviation = dictionary with the list of deviation (|t_x| * |t_y|) for each of the n images (keys)
    xy_deviation = {}
    
    fig = plt.figure()

    for file in files:
        file_name = file.split('_')[0]
        xy_deviation[file_name] = []
        # open the file corresponding to the n image and read the lines
        with open(tmatsPath+file) as f:
            lines = f.readlines()
        # for each line in the file, if is not a comment (starts with #) append the deviation to the list
        for line in lines:
            if line[0] != '#':
                x = int(line.split(',')[6])
                y = int(line.split(',')[7])
                dx = x - abs(int(line.split(',')[1]))
                dy = y - abs(int(line.split(',')[2]))
                distance = np.sqrt((x**2 - dx**2) + (y**2 - dy**2)) # √(x² - dx²) + (y² - dy²))
                max_distance = np.sqrt((x**2) + (y**2))
                #dev = abs(float(line.split(',')[1])) * abs(float(line.split(',')[2])) # |t_x| * |t_y|
                xy_deviation[file_name].append((max_distance-distance)/max_distance)
        # plot the n-th line corresponding to the n-th position    
        plt.plot(xy_deviation[file_name], label = file_name, color = next(colors), marker = next(markers))
        n += 1 
    
    # plotting
    plt.ylabel('offset')
    plt.xlabel('time point')
    plt.legend()
    plt.grid()
    fig.set_size_inches((12, 8), forward=False)
    plt.savefig(results_path+'offset_timecourse.png')
    plt.close()
    return xy_deviation
    
def axis_deviation(files, colors, markers, path, results_path):
    """
    input:  BF_files = list of txt files names with the registration results
            colors = list of rainbow colors for the plot
            marketrs = list of markers for the plot
    save:   plot with axis deviation
            plto with axis deviation trend
    output: chosen_files = list of the files names of the images which respect the threshold values
    """
    xy_deviation = deviation_trend(files, colors, markers, path, results_path)

    xy_lastdeviation = {}
    
    for key in list(xy_deviation.keys()):
        xy_lastdeviation[key] = xy_deviation[key][-1]
    xy_lastdeviation = dict(sorted(xy_lastdeviation.items(), key=lambda x:x[1], reverse=True))
    
    fig = plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.bar(list(xy_lastdeviation.keys()), xy_lastdeviation.values())
    plt.ylabel('offset')
    plt.xlabel('file')
    plt.grid(axis='y')
    fig.set_size_inches((15, 8), forward=False)
    plt.savefig(results_path+'offset_barchart.png')
    plt.close()
    

    ########### Threshold ###########
    chosen_files = [k for k, v in xy_lastdeviation.items() if v < deviation_theshold]
    chosen_files = sorted(chosen_files, key=lambda x:x[3:])
    return chosen_files

def evaluation(path, measure):
    """
    algorithm which evaluate all the m frames, one image at time, inside of the jumps_evaluation function
    
    input:  path = path to the multipage-tiff image
            measure =   MSE - Mean Squared Error
                        SSIM - Structural Similarity Measure
                        UQI - Universal Quality Image Index
                        PSNR - Peak Signal Noise Ratio
                        VOF - Variation of Information
                        deltaT - sum of abs differences of pixels / number of pixels
    output: list of the calculated measures between all the m frames of the tif image
    """
    print('Evaluation of file at the following path',path,'\n')
    img = Image.open(path)
    previous = 0
        
    MSEs = []
    SSIMs = []
    UQIs = []
    PSNRs = []
    VOFs = []
    deltas = []

    for i in range(img.n_frames):
        if i == 0:
            # if first pixel -> nothing to compare with, just save it
            img.seek(i)
            previous = np.array(img)

        else:
            img.seek(i)
            current = np.array(img)
            if measure == 'MSE':
                                MSEs.append(mse(current, previous))
                                res = MSEs
            elif measure == 'SSIM':
                                SSIMs.append(ssim(current, previous))
                                res = SSIMs
            elif measure == 'UQI':
                                UQIs.append(uqi(current, previous))
                                res = UQIs
            elif measure == 'PSNR':
                                PSNRs.append(psnr(current, previous))
                                res = PSNRs
            elif measure == 'VOF':
                                # conditional entropies of image1|image0 and image0|image1.
                                VOFs.append(vof(current, previous)[0])
                                res = VOFs
            elif measure == 'deltaT':
                                n_pixels = current.size
                                deltas.append( abs( np.sum(current != previous) ) / n_pixels )
                                res = deltas        
            previous = current
        
    return res

def jumps_evaluation(images, measure, colors, markers, imgPath, results_path):
    """
    input:  images = list file names of the registered images
    save:   plot with results
            csv file with results
    output: chosen_files = list of the files names of the images which respect the threshold values
    """
    evaluation_dict = {}
    chosen_files = []
    names = []
    stdevs = []
    means = []

    fig = plt.figure()

    for image in images:
        image_name = image.split('_')[0]
        evaluation_res = []
        evaluation_res = evaluation(imgPath+image, measure)
        evaluation_dict[image] = evaluation_res

        names.append(image_name)
        means.append(np.mean(evaluation_res))
        stdevs.append(np.std(evaluation_res))
        
        # to implement : plt.errorbar(name, mean, stdev, linestyle='None', marker='^')
        if np.mean(evaluation_res) > SSIM_theshold and np.std(evaluation_res) < SSIM_deviation_theshold:
            chosen_files.append(image)

        plt.plot(evaluation_res, label = image_name, color = next(colors), marker = next(markers))
    # save csv file with result data
    with open(results_path+measure+'_values.csv', 'w') as f:
        i = 0
        for row in (evaluation_dict.values()):
            header = list(evaluation_dict.keys())[i].split('_')[0]
            string_row = header +', '+ ', '.join(str(v) for v in row) + '\n'
            f.write(string_row)
            i += 1
    
    # save plot with graph
    plt.ylabel('SSMI')
    plt.xlabel('time point')
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=4)
    plt.grid()
    fig.set_size_inches((15, 11), forward=False)
    plt.savefig(results_path+measure+'_graph.png')
    plt.close()

    
    # save plot with error bar
    fig = plt.figure()
    plt.ylabel('SSMI normalized')
    plt.xlabel('file')
    plt.errorbar(names, means, stdevs, linestyle='None', marker='^')
    plt.grid()
    fig.set_size_inches((13, 8))
    plt.savefig(results_path+measure+'_errorBar.png')
    plt.close()

    chosen_files = sorted(chosen_files, key=lambda x:x[3:])
    return chosen_files
    

def main(pathsInventory, filesInventory): 
    markers = itertools.cycle((',', '+', '.', 'o', '*'))
    tmatsPath = pathsInventory['resultsTransformationMatricesFolder']
    imgPath = pathsInventory['resultsRegisteredImagesFolder']
    results_path = pathsInventory['resultsRegistrationAnalysesFolder']   
    if not os.path.isdir(results_path):
        os.makedirs(results_path)
    
    ######################### AXIS DEVIATION #########################
    list_files = os.listdir(pathsInventory['resultsTransformationMatricesFolder'])
    newfilesInventory = [i.split('_')[0] for i in filesInventory]
    txts = [i for i in list_files if i.endswith('.txt') if i.split('_')[0] in newfilesInventory]
    txts = sorted(txts, key=lambda x:int(x[3:5]))
    colors = iter(plt.cm.rainbow(np.linspace(0,1,len(txts))))
    chosen_dev_files = axis_deviation(txts, colors, markers, tmatsPath, results_path)
    text = '######################### DEVIATION FROM AXIS ########################\n'
    text += 'Percentage threshold used: '+str(deviation_theshold*100)+' %\n'
    text += 'Chosen files: '+str(', '.join(chosen_dev_files))+'\n'
    
    ######################### EVALUATION OF THE JUMPS IN BETWEEN FRAMES #########################
    #alignedReferenceFiles = filesInventory
    #images = [i for i in alignedReferenceFiles if not i.startswith('.')]
    list_images = os.listdir(pathsInventory['resultsRegisteredImagesFolder'])
    images = [i for i in list_images if i.endswith('.tif') if i.split('_')[0]+'_'+i.split('_')[1] in filesInventory]
    images = sorted(images, key=lambda x:int(x[3:5]))
    colors = iter(plt.cm.rainbow(np.linspace(0,1,len(images))))
    chosen_jumps_files = jumps_evaluation(images, 'SSIM', colors, markers, imgPath, results_path)
    text += '\n######################### JUMPS IN BETWEEN FRAMES #########################\n'
    text += 'SSMI Mean threshold used: '+str(SSIM_theshold)+'\n'
    text += 'SSMI Standard deviation threshold used: '+str(SSIM_deviation_theshold)+'\n'
    text += 'Chosen files: '+str(', '.join(chosen_jumps_files))+'\n'

    text += '\n######################### FILE TO CHOOSE #########################\n'
    final_files = list((set(chosen_dev_files).intersection(chosen_jumps_files)))
    final_files = sorted(final_files, key=lambda x:x[3:])
    text += str(', '.join(final_files))+'\n'

    with open(results_path+'_selection_suggestions.txt', 'a') as out:
        out.write(text)
     

if __name__ == "__main__": 
    pathsInventory = {'dataFolder': '/Users/aravera/Documents/CIG_Alexs/Registration/application/_VLSM_demoset/20230101_P0001_E0008_U003/', 'resultsMasterFolder': '/Users/aravera/Documents/CIG_Alexs/Registration/application/_VLSM_demoset/20230101_P0001_E0008_U003/20230101_P0001_E0008_U003_registrationResults/', 'resultsTransformationMatricesFolder': '/Users/aravera/Documents/CIG_Alexs/Registration/application/_VLSM_demoset/20230101_P0001_E0008_U003/20230101_P0001_E0008_U003_registrationResults/20230101_P0001_E0008_U003_transformationMatrices/', 'resultsRegisteredImagesFolder': '/Users/aravera/Documents/CIG_Alexs/Registration/application/_VLSM_demoset/20230101_P0001_E0008_U003/20230101_P0001_E0008_U003_registrationResults/20230101_P0001_E0008_U003_registeredImages/', 'resultsRegistrationAnalysesFolder': '/Users/aravera/Documents/CIG_Alexs/Registration/application/_VLSM_demoset/20230101_P0001_E0008_U003/20230101_P0001_E0008_U003_registrationResults/20230101_P0001_E0008_U003_registrationAnalyses/'}
    filesInventory = ['smp01_BF', 'smp02_BF', 'smp03_BF', 'smp07_BF']
    main(pathsInventory, filesInventory)

"""
OUTPUT EXAMPLE on 20220922

######################### DEVIATION FROM AXIS #########################
Percentage threshold used: 10.0 %
Chosen files: smp00, smp01, smp02, smp03, smp04, smp05, smp06, smp07, smp08, smp09, smp11, smp12, smp13

######################### JUMPS IN BETWEEN FRAMES #########################
SSMI Mean threshold used: 0.75
SSMI Standard deviation threshold used: 0.03
Chosen files: smp00, smp01, smp02, smp04, smp07, smp14

######################### FILE TO CHOOSE #########################
smp00, smp01, smp02, smp04, smp07
"""