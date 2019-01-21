import numpy as np

zone_folder                     = "zone"
output_data_folder              = 'data'
threshold_map_folder            = 'threshold_map'
models_information_folder       = 'models_info'
saved_models_folder             = 'saved_models'
min_max_custom_folder           = 'custom_norm'
generated_folder                = 'generated'
pictures_output_folder          = 'curves_pictures'

csv_model_comparisons_filename  = "models_comparisons.csv"
seuil_expe_filename             = 'seuilExpe'
min_max_filename_extension      = "_min_max_values"
config_filename                 = "config"
filename_ext                    = 'png'
default_number_of_images        = 1000

models_names_list               = ["svm_model","ensemble_model","ensemble_model_v2"]

# define all scenes values
renderer_choices                = ['maxwell', 'igloo', 'cycle']

scenes_names                    = ['Appart1opt02', 'Bureau1', 'Cendrier', 'Cuisine01', 'EchecsBas', 'PNDVuePlongeante', 'SdbCentre', 'SdbDroite', 'Selles']
scenes_indices                  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

maxwell_scenes_names            = ['Appart1opt02', 'Cuisine01', 'SdbCentre', 'SdbDroite']
maxwell_scenes_indices          = ['A', 'D', 'G', 'H']

igloo_scenes_names              = ['Bureau1', 'PNDVuePlongeante']
igloo_scenes_indices            = ['B', 'F']

cycle_scenes_names              = ['EchecBas', 'Selles']
cycle_scenes_indices            = ['E', 'I']

normalization_choices           = ['svd', 'svdn', 'svdne']
zones_indices                   = np.arange(16)

metric_choices_labels           = ['lab', 'low_bits_2', 'low_bits_3', 'low_bits_4', 'low_bits_5', 'low_bits_6','low_bits_4_shifted_2']

# noise information
noise_labels                    = ['cauchy', 'gaussian', 'laplace', 'log_normal', 'mut_white', 'salt_pepper', 'white']
