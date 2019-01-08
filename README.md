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
- **mode** : level of normalization ['svd', 'svdn', 'svdne']
- **interval** : features to display from singular values vector
- **step** : interval of noise to keep for display 
- **norm** : normalization between only values kept from interval
- **ylim** : ylim to use in order to display curves



