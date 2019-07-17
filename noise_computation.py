# main imports
import sys, os, argparse

# image processing imports
from PIL import Image
from ipfml.filters import noise as nf

# modules and config imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from data_attributes import get_noise_result


# other variables
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

        noisy_image = get_noise_result(p_image, p_n, _noise_choice=p_noise, _identical=p_identical, _p=p_param)
        noisy_image = Image.fromarray(noisy_image)

        noisy_image.save(output_image_path)

        print("Image saved at... '%s'" % output_image_path)
    else:
        print("Image already exists... '%s'" % output_image_path)



def main():

    parser = argparse.ArgumentParser(description="Compute noise on specific image")

    parser.add_argument('--noise', type=str, help='Noise choice to apply', choices=cfg.noise_labels)
    parser.add_argument('--image', type=str, help='image path')
    parser.add_argument('--n', type=int, help='Number of images')
    parser.add_argument('--identical', type=int, help='Use of color or grey level', default=0)
    parser.add_argument('--output', type=int, help='Output image name', default=0)
    parser.add_argument('--step', type=int, help='Step of image indices to keep', default=1)
    parser.add_argument('--all', type=int, help='Use of all image until `n` or just `n`', default=1)
    parser.add_argument('--p', type=float, help='Distribution to use for noise', default=0.1)

    args = parser.parse_args()

    param_noise     = args.noise
    param_image     = args.image
    param_n         = args.n
    param_identical = args.identical
    param_output    = args.output
    param_step      = args.step
    param_all       = args.all
    param_p         = args.p

    img = Image.open(param_image)

    if param_all:

        split_output = param_output.split('.')

        for i in range(1, param_n):

            if i % param_step == 0:
                param_filename = split_output[0] + "_" + str(i) + "." + filename_ext

                generate_noisy_image(img, i, param_noise, param_identical, param_filename, param_p)

    else:
        generate_noisy_image(img, param_n, param_noise, param_identical, param_output, param_p)

if __name__== "__main__":
    main()
