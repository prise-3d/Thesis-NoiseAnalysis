import sys, os, getopt
from PIL import Image

from ipfml import processing

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

def main():

    p_step = 1
    max_value_svd = 0
    min_value_svd = sys.maxsize

    if len(sys.argv) <= 1:
        print('python noise_svd_visualization.py --prefix path/with/prefix --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --output filename')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:m:m:n:i:s:o", ["help=", "prefix=", "metric=", "mode=", "n=", "interval=", "step=", "output="])
    except getopt.GetoptError:
        # print help information and exit:
        print('python noise_svd_visualization.py --prefix path/with/prefix --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --output filename')
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            print('python noise_svd_visualization.py --prefix path/with/prefix --metric lab --mode svdn --n 300 --interval "0, 200" --step 30 --output filename')
            sys.exit()
        elif o in ("-p", "--prefix"):
            p_prefix = a
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
        elif o in ("-i", "--interval"):
            p_interval = list(map(int, a.split(',')))
        elif o in ("-s", "--step"):
            p_step = int(a)
        elif o in ("-o", "--output"):
            p_output = a
        else:
            assert False, "unhandled option"


    noise_name = p_prefix.split('/')[1].replace('_', '')

    file_path = p_prefix + "{}." + filename_ext

    begin, end = p_interval
    all_svd_data = []

    svd_data = []
    image_indices = []

    # get all data from images
    for i in range(1, p_n):

        image_path = file_path.format(str(i))
        img = Image.open(image_path)

        svd_values = dt.get_svd_data(p_metric, img)
        svd_values = svd_values[begin:end]
        all_svd_data.append(svd_values)

        # update min max values
        min_value = svd_values.min()
        max_value = svd_values.max()

        if min_value < min_value_svd:
            min_value_svd = min_value

        if max_value > min_value_svd:
            max_value_svd = max_value

        print('%.2f%%' % ((i + 1) / p_n * 100))
        sys.stdout.write("\033[F")

    print("Generation of output figure...")
    for id, data in enumerate(all_svd_data):

        if id % p_step == 0:

            current_data = data
            if p_mode == 'svdn':
                current_data = processing.normalize_arr(current_data)

            if p_mode == 'svdne':
                current_data = processing.normalize_arr_with_range(current_data, min_value_svd, max_value_svd)

            svd_data.append(current_data)
            image_indices.append(id)

    # display all data using matplotlib

    plt.title(noise_name  + ' noise, interval information ['+ str(begin) +', '+ str(end) +'], ' + p_metric + ' metric, step ' + str(p_step), fontsize=20)
    plt.ylabel('Importance of noise [1, 999]', fontsize=14)
    plt.xlabel('Vector features', fontsize=16)

    for id, data in enumerate(svd_data):

        p_label = p_prefix + str(image_indices[id])
        plt.plot(data, label=p_label)

    plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.2, fontsize=14)
    plt.ylim(0, 0.1)
    plt.show()

    output_filename = noise_name + "1_to_" + str(p_n) + "_B" + str(begin) + "_E" + str(end) + "_" + p_metric + "_S" + str(p_step) + "_" + p_mode
    output_path = os.path.join(pictures_folder, output_filename)

    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    plt.savefig(output_path)



if __name__== "__main__":
    main()
