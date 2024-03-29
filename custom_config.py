from modules.config.attributes_config import *

# store all variables from global config
context_vars = vars()

# folders
## min_max_custom_folder           = 'custom_norm'
## correlation_indices_folder      = 'corr_indices'
generated_folder                = 'generated'
pictures_output_folder          = 'curves_pictures'

# variables
## models_names_list               = ["svm_model","ensemble_model","ensemble_model_v2","deep_keras"]
## normalization_choices           = ['svd', 'svdn', 'svdne']
features_choices_labels         = ['lab', 'mscn', 'low_bits_2', 'low_bits_3', 'low_bits_4', 'low_bits_5', 'low_bits_6','low_bits_4_shifted_2', 'sub_blocks_stats', 'sub_blocks_area', 'sub_blocks_stats_reduced', 'sub_blocks_area_normed', 'mscn_var_4', 'mscn_var_16', 'mscn_var_64', 'mscn_var_16_max', 'mscn_var_64_max', 'ica_diff', 'svd_trunc_diff', 'ipca_diff', 'svd_reconstruct', 'highest_sv_std_filters', 'lowest_sv_std_filters', 'highest_wave_sv_std_filters', 'lowest_wave_sv_std_filters', 'highest_sv_std_filters_full', 'lowest_sv_std_filters_full', 'highest_sv_entropy_std_filters', 'lowest_sv_entropy_std_filters']
noise_labels                    = ['cauchy', 'gaussian', 'laplace', 'log_normal', 'mut_white', 'salt_pepper', 'white']
error_data_choices              = ['mae', 'mse', 'ssim', 'psnr']
filename_ext                    = 'png'

# parameters
## keras_epochs                    = 500
## keras_batch                     = 32
## val_dataset_size                = 0.2
default_number_of_images        = 1000