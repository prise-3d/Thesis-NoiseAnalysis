# NoiseAnalysis

## Description

Analysis of different noises using singular values vector obtained from SVD compression.

Noise list :
- cauchy
- gaussian
- laplace
- log_normal
- mut_white
- salt_pepper
- white


## Generate all data

### Step 1.

First of all you need to generate all noise of each images in **/generated** folder.

```
bash generate_all_noise.sh
```

### Step 2.

Once you had generate all noisy images from synthesis scenes, you need to extract features (SVD singular values) using different metrics.

```
python generate_all_data.py --metric all --step 40 --color 0
python generate_all_data.py --metric all --step 40 --color 1
```

### Step 3.

You can display curves of each noise for each scene :

```
bash generate_noise_all_curves.sh
```

This will give you some information about SVD singular values obtained from noise applied synthesis images. All these curves are available into **curves_pictures** folder after running script.

## Scripts

### noise_computation.py

This script is used to compute all noise for each image in the **images** folder.

```
python noise_computation.py --noise salt_pepper --image path/to/image.png --n 1000 --identical 1 --output image_salt_pepper.png --all 1 --p 0.1
```

Parameters :
- **noise** : specify the noise to use (one available from the list above)
- **image** : source path of the image we want to add noise
- **n** : level of noise to use
- **identical** : same noise or not for each chanel in case of RGB image
- **step** : interval of identifier between each image kept
- **output** : output image name wanted
- **all** : generate all level noise from 1 to **n**
- **p** : optional parameter only used for salt and pepper noise


### noise_svd_visualization.py

This script is used to display noise for each level of noise of image.

```
python noise_svd_visualization.py  --prefix generated/${image}/${noise} --metric lab --n 1000 --mode svdne --interval "0, 200" --step 40 --norm 0 --ylim "0, 0.05"
```

Parameters :
- **prefix** : specify the folder of image for specific noise 
- **metric** : metric choice to compute in order to extract SVD data
- **n** : limit identifier to use for image scene 
- **mode** : level of normalization ['svd', 'svdn', 'svdne']
- **interval** : features to display from singular values vector
- **step** : interval of noise to keep for display 
- **norm** : normalization between only values kept from interval
- **color** : specify if we use 3 chanels with different noise or with same noise
- **ylim** : ylim to use in order to display curves

### noise_svd_tend_visualization.py

Display information about tend of svd values for specific scene

### noise_svd_threshold.py

Display threshold information about scene for each noise perceived. It's necessary to have in scene folder one of this file :
- threshold_data_mean.csv
- threshold_data_median.csv

These files contains threshold information about a noise such that each row are written like that :
- noise;threshold;color(0, 1)


## LICENSE

[The MIT license](LICENSE)