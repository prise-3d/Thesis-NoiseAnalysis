# main imports
import sys, os, argparse

# image processing imports
from PIL import Image
import matplotlib.pyplot as plt

from ipfml import processing, utils

# modules and config imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from data_attributes import get_image_features

# other variables
noise_list            = cfg.noise_labels
generated_folder      = cfg.generated_folder
filename_ext          = cfg.filename_ext
feature_choices       = cfg.features_choices_labels
normalization_choices = cfg.normalization_choices
pictures_folder       = cfg.pictures_output_folder

steparam_picture          = 10

def main():

    parser = argparse.ArgumentParser(description="Display svd of images with noise level")

    parser.add_argument('--prefix', type=str, help='Generated noise folder prefix (ex: `generated/prefix/noise`)')
    parser.add_argument('--mode', type=str, help='Kind of normalization', default=normalization_choices)
    parser.add_argument('--feature', type=str, help='feature choice', default=feature_choices)
    parser.add_argument('--n', type=int, help='Number of images')
    parser.add_argument('--color', type=int, help='Use of color or grey level', default=0)
    parser.add_argument('--norm', type=int, help='Use of normalization from interval or whole data vector', default=0)
    parser.add_argument('--interval', type=str, help='Interval data choice (ex: `0, 200`)', default="0, 200")
    parser.add_argument('--step', type=int, help='Step of image indices to keep', default=1)
    parser.add_argument('--ylim', type=str, help='Limite to display data (ex: `0, 1`)', default="0, 1")

    args = parser.parse_args()

    param_prefix   = args.prefix
    param_mode     = args.mode
    param_feature  = args.feature
    param_n        = args.n
    param_color    = args.color
    param_norm     = args.norm
    param_interval = list(map(int, args.interval.split(',')))
    param_step     = args.step
    param_ylim     = list(map(float, args.ylim.split(',')))


    param_prefix = param_prefix.split('/')[1].replace('_', '')
    noise_name = param_prefix.split('/')[2]

    if param_color:
        file_path = param_prefix + "/" + param_prefix + "_" + noise_name + "_color_{}." + filename_ext
    else:
        file_path = param_prefix + "/" + param_prefix + "_" + noise_name + "_{}." + filename_ext

    begin, end = param_interval
    all_svd_data = []

    svd_data = []
    image_indices = []

    # get all data from images
    for i in range(1, param_n):

        if i % steparam_picture == 0:

            image_path = file_path.format(str(i))
            img = Image.open(image_path)

            svd_values = get_image_features(param_feature, img)

            if param_norm:
                svd_values = svd_values[begin:end]

            all_svd_data.append(svd_values)

            # update min max values
            min_value = svd_values.min()
            max_value = svd_values.max()

            if min_value < min_value_svd:
                min_value_svd = min_value

            if max_value > max_value_svd:
                max_value_svd = max_value

            print('%.2f%%' % ((i + 1) / param_n * 100))
            sys.stdout.write("\033[F")

    for id, data in enumerate(all_svd_data):

        if (id * steparam_picture) % param_step == 0:

            current_data = data
            if param_mode == 'svdn':
                current_data = utils.normalize_arr(current_data)

            if param_mode == 'svdne':
                current_data = utils.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

            svd_data.append(current_data)
            image_indices.append(str(id * steparam_picture))

    # display all data using matplotlib (configure plt)

    plt.rcParams['figure.figsize'] = (25, 18)

    plt.title(param_prefix  + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + param_feature + ' feature, step ' + str(param_step) + ' normalization ' + param_mode, fontsize=20)
    plt.ylabel('Importance of noise [1, 999]', fontsize=14)
    plt.xlabel('Vector features', fontsize=16)

    for id, data in enumerate(svd_data):

        param_label = param_prefix + str(image_indices[id])
        plt.plot(data, label=param_label)

    plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.2, fontsize=14)

    if not param_norm:
        plt.xlim(begin, end)

    # adapt ylim
    y_begin, y_end = param_ylim
    plt.ylim(y_begin, y_end)

    output_filename = param_prefix + "_" + noise_name + "_1_to_" + str(param_n) + "_B" + str(begin) + "_E" + str(end) + "_" + param_feature + "_S" + str(param_step) + "_norm" + str(param_norm )+  "_" + param_mode

    if param_color:
        output_filename = output_filename + '_color'

    print("Generation of output figure... %s" % output_filename)
    output_path = os.path.join(pictures_folder, output_filename)

    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    plt.savefig(output_path, dpi=(200))


if __name__== "__main__":
    main()
