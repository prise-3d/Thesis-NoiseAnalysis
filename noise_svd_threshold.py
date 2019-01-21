import sys, os, getopt
from PIL import Image

from ipfml import processing, utils

from modules.utils import config as cfg
from modules.utils import data_type as dt
from modules import noise

import matplotlib.pyplot as plt

noise_list            = cfg.noise_labels
generated_folder      = cfg.generated_folder
filename_ext          = cfg.filename_ext
metric_choices        = cfg.metric_choices_labels
normalization_choices = cfg.normalization_choices
pictures_folder       = cfg.pictures_output_folder

step_picture          = 10

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

    # default values
    p_step = 1
    p_color = 0
    p_norm = 0
    p_ylim = (0, 1)
    p_n = 1000

    if len(sys.argv) <= 1:
        print('python noise_svd_threshold.py --prefix generated/scene --file threshold_file --metric lab --mode svdn --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1"')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:f:m:m:i:s:c:n:y", ["help=", "prefix=", "file=", "metric=", "mode=", "interval=", "step=", "color=", "norm=", "ylim="])
    except getopt.GetoptError:
        # print help information and exit:
        print('python noise_svd_threshold.py --prefix generated/scene --file threshold_file --metric lab --mode svdn --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1"')
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            print('python noise_svd_threshold.py --prefix generated/scene --file threshold_file --metric lab --mode svdn --interval "0, 200" --step 30 --color 1 --norm 1 --ylim "0, 1"')
            sys.exit()
        elif o in ("-p", "--prefix"):
            p_path = a
        elif o in ("-f", "--file"):
            p_data_file = a

        elif o in ("-m", "--mode"):
            p_mode = a

            if not p_mode in normalization_choices:
                assert False, "Unknown normalization choice, %s" % normalization_choices

        elif o in ("-m", "--metric"):
            p_metric = a

            if not p_metric in metric_choices:
                assert False, "Unknown metric choice, %s" % metric_choices

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
        else:
            assert False, "unhandled option"


    p_prefix = p_path.split('/')[1].replace('_', '')

    if p_color:
        file_path = p_path + "{}/" + p_prefix + "_{}_color_{}." + filename_ext
    else:
        file_path = p_path + "{}/" + p_prefix + "_{}_{}." + filename_ext

    begin, end = p_interval

    svd_data = []
    final_svd_data = []
    image_indices = []
    min_max_list = {}

    threshold_data = []

    # read data threshold file
    with open(p_data_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            data = line.replace('\n', '').split(';')
            print(data)

            threshold = ThresholdData(data[0], float(data[1]), int(data[2]))
            threshold_data.append(threshold)

    # filter data if color or not
    threshold_data = [t for t in threshold_data if t.isColor() == p_color]

    for id, threshold in enumerate(threshold_data):

        current_noise = threshold.get_noise()
        current_threshold = threshold.get_threshold()

        min_max_list[current_noise] = (sys.maxsize, 0)
        threshold_found = False

        # get all data from images
        for i in range(1, p_n):

            if i % step_picture == 0:
                image_path = file_path.format(current_noise, current_noise, str(i))
                img = Image.open(image_path)

                svd_values = dt.get_svd_data(p_metric, img)

                if p_norm:
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

            print('%.2f%%' % (((i + 1) * 100 + (id * p_n * 100)) / (p_n * len(threshold_data))))
            sys.stdout.write("\033[F")

    for id, data in enumerate(svd_data):

        current_data = data

        threshold = threshold_data[id]
        min_value_svd, max_value_svd = min_max_list[threshold.get_noise()]

        if p_mode == 'svdn':
            current_data = utils.normalize_arr(current_data)

        if p_mode == 'svdne':
            current_data = utils.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

        final_svd_data.append(current_data)

    # display all data using matplotlib (configure plt)

    plt.rcParams['figure.figsize'] = (25, 18)

    plt.title(p_prefix  + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + p_metric + ' metric, step ' + str(p_step) + ' normalization ' + p_mode, fontsize=20)
    plt.ylabel('Importance of noise [1, 999]', fontsize=14)
    plt.xlabel('Vector features', fontsize=16)

    for id, data in enumerate(final_svd_data):

        p_label = p_prefix + '_' + threshold_data[id].get_noise() + str(image_indices[id])
        plt.plot(data, label=p_label)

    plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.2, fontsize=14)

    if not p_norm:
        plt.xlim(begin, end)

    # adapt ylim
    y_begin, y_end = p_ylim
    plt.ylim(y_begin, y_end)

    output_filename = p_prefix + "_threshold_1_to_" + str(p_n) + "_B" + str(begin) + "_E" + str(end) + "_" + p_metric + "_S" + str(p_step) + "_norm" + str(p_norm )+  "_" + p_mode

    if p_color:
        output_filename = output_filename + '_color'

    print("Generation of output figure... %s" % output_filename)
    output_path = os.path.join(pictures_folder, output_filename)

    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    plt.savefig(output_path, dpi=(200))



if __name__== "__main__":
    main()
