# main imports
import sys, os, argparse
import numpy as np

# image processing imports
from PIL import Image
import matplotlib.pyplot as plt

from ipfml import utils
import ipfml.iqa.fr as fr_iqa

# modules and config imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from data_attributes import get_image_features


# others variables
noise_list            = cfg.noise_labels
generated_folder      = cfg.generated_folder
filename_ext          = cfg.filename_ext
feature_choices       = cfg.features_choices_labels
normalization_choices = cfg.normalization_choices
pictures_folder       = cfg.pictures_output_folder
error_data_choices    = cfg.error_data_choices

steparam_picture          = 10



def get_error_distance(param_error, y_true, y_test):

    function_name = param_error

    try:
        error_method = getattr(fr_iqa, function_name)
    except AttributeError:
        raise NotImplementedError("Error method `{}` not implement `{}`".format(fr_iqa.__name__, function_name))

    return error_method(y_true, y_test)


def main():

    max_value_svd = 0
    min_value_svd = sys.maxsize

    parser = argparse.ArgumentParser(description="Display svd tend of images with noise level")

    parser.add_argument('--prefix', type=str, help='Generated noise folder prefix (ex: `generated/prefix/noise`)')
    parser.add_argument('--mode', type=str, help='Kind of normalization', default=normalization_choices)
    parser.add_argument('--feature', type=str, help='feature choice', default=feature_choices)
    parser.add_argument('--n', type=int, help='Number of images')
    parser.add_argument('--color', type=int, help='Use of color or grey level', default=0)
    parser.add_argument('--norm', type=int, help='Use of normalization from interval or whole data vector', default=0)
    parser.add_argument('--interval', type=str, help='Interval data choice (ex: `0, 200`)', default="0, 200")
    parser.add_argument('--step', type=int, help='Step of image indices to keep', default=1)
    parser.add_argument('--ylim', type=str, help='Limite to display data (ex: `0, 1`)', default="0, 1")
    parser.add_argument('--error', type=str, help='Error used for information data', default=error_data_choices)

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
    param_error    = args.error


    param_prefix = param_prefix.split('/')[1].replace('_', '')
    noise_name = param_prefix.split('/')[2]

    if param_color:
        file_path = os.path.join(param_prefix, param_prefix + "_" + noise_name + "_color_{}." + filename_ext)
    else:
        file_path = os.path.join(param_prefix, param_prefix + "_" + noise_name + "_{}." + filename_ext)

    begin, end = param_interval
    all_svd_data = []

    svd_data = []
    image_indices = []

    noise_indices = range(1, param_n)[::-1]

    # get all data from images
    for i in noise_indices:

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

        print('%.2f%%' % ((param_n - i + 1) / param_n * 100))
        sys.stdout.write("\033[F")

    previous_data = []
    error_data = [0.]

    for id, data in enumerate(all_svd_data):

        current_id = (param_n - ((id + 1) * 10))

        if current_id % param_step == 0:

            current_data = data

            if param_mode == 'svdn':
                current_data = utils.normalize_arr(current_data)

            if param_mode == 'svdne':
                current_data = utils.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

            svd_data.append(current_data)
            image_indices.append(current_id)

            # use of whole image data for computation of ssim or psnr
            if param_error == 'ssim' or param_error == 'psnr':
                image_path = file_path.format(str(current_id))
                current_data = np.asarray(Image.open(image_path))

            if len(previous_data) > 0:

                current_error = get_error_distance(param_error, previous_data, current_data)
                error_data.append(current_error)

            if len(previous_data) == 0:
                previous_data = current_data

    # display all data using matplotlib (configure plt)
    gridsize = (3, 2)

    # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(30, 22))
    fig = plt.figure(figsize=(30, 22))
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid(gridsize, (2, 0), colspan=2)

    ax1.set_title(param_prefix  + ', ' + noise_name + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + param_feature + ' feature, step ' + str(param_step) + ' normalization ' + param_mode)
    ax1.set_label('Importance of noise [1, 999]')
    ax1.set_xlabel('Vector features')

    for id, data in enumerate(svd_data):

        param_label = param_prefix + str(image_indices[id]) + " | " + param_error + ": " + str(error_data[id])
        ax1.plot(data, label=param_label)

    ax1.legend(bbox_to_anchor=(0.75, 1), loc=2, borderaxespad=0.2, fontsize=12)

    if not param_norm:
        ax1.set_xlim(begin, end)

    # adapt ylim
    y_begin, y_end = param_ylim
    ax1.set_ylim(y_begin, y_end)

    output_filename = param_prefix + "_" + noise_name + "_1_to_" + str(param_n) + "_B" + str(begin) + "_E" + str(end) + "_" + param_feature + "_S" + str(param_step) + "_norm" + str(param_norm )+  "_" + param_mode + "_" + param_error

    if param_color:
        output_filename = output_filename + '_color'

    ax2.set_title(param_error + " information for : " + param_prefix  + ', ' + noise_name + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + param_feature + ' feature, step ' + str(param_step) + ', normalization ' + param_mode)
    ax2.set_ylabel(param_error + ' error')
    ax2.set_xlabel('Number of samples per pixels')
    ax2.set_xticks(range(len(image_indices)))
    ax2.set_xticklabels(image_indices)
    ax2.plot(error_data)

    print("Generation of output figure... %s" % output_filename)
    output_path = os.path.join(pictures_folder, output_filename)

    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    fig.savefig(output_path, dpi=(200))

if __name__== "__main__":
    main()
