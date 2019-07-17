# main imports
import sys, os, argparse
import numpy as np

# image processing imports
from PIL import Image
from ipfml import processing, utils
import matplotlib.pyplot as plt

# modules and config imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from data_attributes import get_image_features


noise_list            = cfg.noise_labels
generated_folder      = cfg.generated_folder
filename_ext          = cfg.filename_ext
feature_choices       = cfg.features_choices_labels
normalization_choices = cfg.normalization_choices
pictures_folder       = cfg.pictures_output_folder

steparam_picture          = 10

class ThresholdData():
    """
    A simple class to store threshold data
    """

    def __init__(self, noise, threshold, color):
        self.noise = noise
        self.threshold = threshold
        self.color = color

    def get_noise(self):
        return self.noise

    def get_threshold(self):
        return self.threshold

    def isColor(self):
        return self.color


def main():

    parser = argparse.ArgumentParser(description="Display threshold svd data")

    parser.add_argument('--prefix', type=str, help='Generated noise folder prefix (ex: `generated/prefix/noise`)')
    parser.add_argument('--file', type=str, help='Threshold file to use')
    parser.add_argument('--mode', type=str, help='Kind of normalization', default=normalization_choices)
    parser.add_argument('--feature', type=str, help='feature choice', default=feature_choices)
    parser.add_argument('--color', type=int, help='Use of color or grey level', default=0)
    parser.add_argument('--norm', type=int, help='Use of normalization from interval or whole data vector', default=0)
    parser.add_argument('--interval', type=str, help='Interval data choice (ex: `0, 200`)', default="0, 200")
    parser.add_argument('--step', type=int, help='Step of image indices to keep', default=1)
    parser.add_argument('--ylim', type=str, help='Limite to display data (ex: `0, 1`)', default="0, 1")

    args = parser.parse_args()

    param_prefix   = args.prefix
    param_file     = args.file
    param_mode     = args.mode
    param_feature  = args.feature
    param_n        = args.n
    param_color    = args.color
    param_norm     = args.norm
    param_interval = list(map(int, args.interval.split(',')))
    param_step     = args.step
    param_ylim     = list(map(float, args.ylim.split(',')))


    param_prefix = param_prefix.split('/')[1].replace('_', '')

    if param_color:
        file_path = param_prefix + "{}/" + param_prefix + "_{}_color_{}." + filename_ext
    else:
        file_path = param_prefix + "{}/" + param_prefix + "_{}_{}." + filename_ext

    begin, end = param_interval

    svd_data = []
    final_svd_data = []
    image_indices = []
    min_max_list = {}

    threshold_data = []

    # read data threshold file
    with open(param_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            data = line.replace('\n', '').split(';')
            print(data)

            threshold = ThresholdData(data[0], float(data[1]), int(data[2]))
            threshold_data.append(threshold)

    # filter data if color or not
    threshold_data = [t for t in threshold_data if t.isColor() == param_color]

    for id, threshold in enumerate(threshold_data):

        current_noise = threshold.get_noise()
        current_threshold = threshold.get_threshold()

        min_max_list[current_noise] = (sys.maxsize, 0)
        threshold_found = False

        # get all data from images
        for i in range(1, param_n):

            if i % steparam_picture == 0:
                image_path = file_path.format(current_noise, current_noise, str(i))
                img = Image.open(image_path)

                svd_values = get_image_features(param_feature, img)

                if param_norm:
                    svd_values = svd_values[begin:end]

                # only append data once
                if not threshold_found and current_threshold < i:
                    svd_data.append(svd_values)
                    image_indices.append(i)

                if current_threshold < i:
                    threshold_found = True

                # update min max values
                min_value = svd_values.min()
                max_value = svd_values.max()

                # update of min max values for noise
                current_min, current_max = min_max_list[current_noise]

                if min_value < current_min:
                    current_min = min_value

                if max_value > current_max:
                    current_max = max_value

                min_max_list[current_noise] = (current_min, current_max)

            print('%.2f%%' % (((i + 1) * 100 + (id * param_n * 100)) / (param_n * len(threshold_data))))
            sys.stdout.write("\033[F")

    for id, data in enumerate(svd_data):

        current_data = data

        threshold = threshold_data[id]
        min_value_svd, max_value_svd = min_max_list[threshold.get_noise()]

        if param_mode == 'svdn':
            current_data = utils.normalize_arr(current_data)

        if param_mode == 'svdne':
            current_data = utils.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

        final_svd_data.append(current_data)

    # display all data using matplotlib (configure plt)

    plt.rcParams['figure.figsize'] = (25, 18)

    plt.title(param_prefix  + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + param_feature + ' feature, step ' + str(param_step) + ' normalization ' + param_mode, fontsize=20)
    plt.ylabel('Importance of noise [1, 999]', fontsize=14)
    plt.xlabel('Vector features', fontsize=16)

    for id, data in enumerate(final_svd_data):

        param_label = param_prefix + '_' + threshold_data[id].get_noise() + str(image_indices[id])
        plt.plot(data, label=param_label)

    plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.2, fontsize=14)

    if not param_norm:
        plt.xlim(begin, end)

    # adapt ylim
    y_begin, y_end = param_ylim
    plt.ylim(y_begin, y_end)

    output_filename = param_prefix + "_threshold_1_to_" + str(param_n) + "_B" + str(begin) + "_E" + str(end) + "_" + param_feature + "_S" + str(param_step) + "_norm" + str(param_norm )+  "_" + param_mode

    if param_color:
        output_filename = output_filename + '_color'

    print("Generation of output figure... %s" % output_filename)
    output_path = os.path.join(pictures_folder, output_filename)

    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    plt.savefig(output_path, dpi=(200))



if __name__== "__main__":
    main()
