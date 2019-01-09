from ipfml.filters import noise as nf
import sys, os, getopt
from PIL import Image

from modules.utils import config as cfg
from modules import noise

noise_list       = cfg.noise_labels
generated_folder = cfg.generated_folder
filename_ext     = cfg.filename_ext

def generate_noisy_image(p_image, p_n, p_noise, p_identical, p_output, p_param):

    image_folder = p_image.filename.split('/')[-1].replace('.' + filename_ext, '')

    output_path = os.path.join(os.path.join(generated_folder, image_folder), p_noise)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_image_path = os.path.join(output_path, p_output)

    if not filename_ext in output_image_path:
        output_image_path = output_image_path + filename_ext

    if not os.path.exists(output_image_path):

        noisy_image = noise.get_noise_result(p_image, p_n, _noise_choice=p_noise, _identical=p_identical, _p=p_param)
        noisy_image = Image.fromarray(noisy_image)

        noisy_image.save(output_image_path)

        print("Image saved at... '%s'" % output_image_path)
    else:
        print("Image already exists... '%s'" % output_image_path)



def main():

    # by default..
    p_param = None
    p_all = False

    if len(sys.argv) < 1:
        print('python noise_computation.py --noise xxxx --image path/to/image.png --n 100 --identical 0 --output image_name --all 1 --p 0.1')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:n:i:n:i:o:a:p", ["help=", "noise=", "image=", "n=", "identical=", "output=", "all=", "p="])
    except getopt.GetoptError:
        # print help information and exit:
        print('python noise_computation.py --noise xxxx --image path/to/image.png --n 100 --identical 0 --output image_name --all 1 --p 0.1')
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            print('python noise_computation.py --noise xxxx --image path/to/image.png --n 100 --identical 0 --output image_name --all 1 --p 0.1')
            sys.exit()
        elif o in ("-n", "--noise"):
            p_noise = a

            if not p_noise in noise_list:
                assert False, "Unknow noise parameter %s, %s " % (p_noise, noise_list)

        elif o in ("-i", "--image"):
            p_image_path = a
        elif o in ("-n", "--n"):
            p_n = int(a)

        elif o in ("-i", "--identical"):
            p_identical = int(a)
        elif o in ("-o", "--output"):
            p_output = a
        elif o in ("-a", "--all"):
            p_all = int(a)
        elif o in ("-p", "--p"):
            p_param = float(a)
        else:
            assert False, "unhandled option"

    img = Image.open(p_image_path)

    if p_all:

        split_output = p_output.split('.')

        for i in range(1, p_n):
            p_filename = split_output[0] + "_" + str(i) + "." + filename_ext

            generate_noisy_image(img, i, p_noise, p_identical, p_filename, p_param)

    else:
        generate_noisy_image(img, p_n, p_noise, p_identical, p_output, p_param)

if __name__== "__main__":
    main()
