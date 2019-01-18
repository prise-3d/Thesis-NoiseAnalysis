import sys, os, getopt
from PIL import Image

from ipfml import processing, utils

from modules.utils import config as cfg
from modules.utils import data_type as dt
from modules import noise
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')

noise_list            = cfg.noise_labels
generated_folder      = cfg.generated_folder
filename_ext          = cfg.filename_ext
metric_choices        = cfg.metric_choices_labels
normalization_choices = cfg.normalization_choices
pictures_folder       = cfg.pictures_output_folder

step_picture          = 10

error_data_choices    = ['MAE', 'MSE']

def compute_mae(previous_data, current_data):

    n = len(previous_data)
    mae_sum = 0.

    for id, x in enumerate(current_data):
        y = previous_data[id] # current data reduces error
        mae_sum += abs(x - y)

    return mae_sum / n

def compute_mse(previous_data, current_data):

    n = len(previous_data)
    mse_sum = 0.

    for id, x in enumerate(current_data):
        y = previous_data[id] # current data reduces error
        mse_sum += abs(x - y)

    return mse_sum / n

def main():

    # default values
    p_step = 1
    p_color = 0
    p_norm = 0
    p_ylim = (0, 1)

    max_value_svd = 0
    min_value_svd = sys.maxsize

    if len(sys.argv) <= 1:
        print('python noise_svd_mae_visualization.py --prefix generated/prefix/noise --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1" --error MAE')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:m:m:n:i:s:c:n:y:e", ["help=", "prefix=", "metric=", "mode=", "n=", "interval=", "step=", "color=", "norm=", "ylim=", "error="])
    except getopt.GetoptError:
        # print help information and exit:
        print('python noise_svd_mae_visualization.py --prefix generated/prefix/noise --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1" --error MAE')
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            print('python noise_svd_mae_visualization.py --prefix generated/prefix/noise --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1" --error MAE')
            sys.exit()
        elif o in ("-p", "--prefix"):
            p_path = a
        elif o in ("-m", "--mode"):
            p_mode = a

            if not p_mode in normalization_choices:
                assert False, "Unknown normalization choice, %s" % normalization_choices

        elif o in ("-m", "--metric"):
            p_metric = a

            if not p_metric in metric_choices:
                assert False, "Unknown metric choice, %s" % metric_choices

        elif o in ("-n", "--n"):
            p_n = int(a)
        elif o in ("-n", "--norm"):
            p_norm = int(a)
        elif o in ("-c", "--color"):
            p_color = int(a)
        elif o in ("-i", "--interval"):
            p_interval = list(map(int, a.split(',')))
        elif o in ("-s", "--step"):
            p_step = int(a)
        elif o in ("-y", "--ylim"):
            p_ylim = list(map(float, a.split(',')))
        elif o in ("-e", "--error"):
            p_error = a

            if p_error not in error_data_choices:
                assert False, "Unknow error choice to display %s" % error_data_choices
        else:
            assert False, "unhandled option"


    p_prefix = p_path.split('/')[1].replace('_', '')
    noise_name = p_path.split('/')[2]

    if p_color:
        file_path = os.path.join(p_path, p_prefix + "_" + noise_name + "_color_{}." + filename_ext)
    else:
        file_path = os.path.join(p_path, p_prefix + "_" + noise_name + "_{}." + filename_ext)

    begin, end = p_interval
    all_svd_data = []

    svd_data = []
    image_indices = []

    noise_indices = range(1, p_n)[::-1]

    # get all data from images
    for i in noise_indices:

        if i % step_picture == 0:

            image_path = file_path.format(str(i))

            img = Image.open(image_path)

            svd_values = dt.get_svd_data(p_metric, img)

            if p_norm:
                svd_values = svd_values[begin:end]

            all_svd_data.append(svd_values)

            # update min max values
            min_value = svd_values.min()
            max_value = svd_values.max()

            if min_value < min_value_svd:
                min_value_svd = min_value

            if max_value > min_value_svd:
                max_value_svd = max_value

        print('%.2f%%' % ((p_n - i + 1) / p_n * 100))
        sys.stdout.write("\033[F")

    previous_data = []
    error_data = [0.]

    for id, data in enumerate(all_svd_data):

        current_id = (p_n - ((id + 1) * 10))

        if current_id % p_step == 0:

            current_data = data
            if p_mode == 'svdn':
                current_data = utils.normalize_arr(current_data)

            if p_mode == 'svdne':
                current_data = utils.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

            svd_data.append(current_data)
            image_indices.append(current_id)

            if len(previous_data) > 0:
                current_mae = compute_mae(previous_data, current_data)
                error_data.append(current_mae)

            if len(previous_data) == 0:
                previous_data = current_data

    # display all data using matplotlib (configure plt)
    gridsize = (3, 2)

    # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(30, 22))
    fig = plt.figure(figsize=(30, 22))
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid(gridsize, (2, 0), colspan=2)

    ax1.set_title(p_prefix  + ', ' + noise_name + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + p_metric + ' metric, step ' + str(p_step) + ' normalization ' + p_mode)
    ax1.set_label('Importance of noise [1, 999]')
    ax1.set_xlabel('Vector features')

    for id, data in enumerate(svd_data):

        p_label = p_prefix + str(image_indices[id]) + " | MAE : " + str(error_data[id])
        ax1.plot(data, label=p_label)

    ax1.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.2, fontsize=12)

    if not p_norm:
        ax1.set_xlim(begin, end)

    # adapt ylim
    y_begin, y_end = p_ylim
    ax1.set_ylim(y_begin, y_end)

    output_filename = p_prefix + "_" + noise_name + "_1_to_" + str(p_n) + "_B" + str(begin) + "_E" + str(end) + "_" + p_metric + "_S" + str(p_step) + "_norm" + str(p_norm )+  "_" + p_mode + "_" + p_error

    if p_color:
        output_filename = output_filename + '_color'

    ax2.set_title(p_error + " information for : " + p_prefix  + ', ' + noise_name + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + p_metric + ' metric, step ' + str(p_step) + ', normalization ' + p_mode)
    ax2.set_ylabel('Mean Squared Error')
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
