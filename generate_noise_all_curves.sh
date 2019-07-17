
for file in "images"/*; do

    IFS='/' # space is set as delimiter
    read -ra ADDR <<< "$file" # str is read into an array as tokens separated by IFS
    IFS=' '

    image=${ADDR[1]%".png"}

    echo $image
    if [ "$image" != "calibration" ] || [ "$image" != *"min_max_values"* ]; then

        #for metric in {"lab","mscn_revisited","low_bits_2","low_bits_3","low_bits_4","low_bits_5","low_bits_6","low_bits_4_shifted_2"}; do
        for metric in {"lab","low_bits_5","low_bits_4_shifted_2"}; do
            for noise in {"cauchy","gaussian","laplace","log_normal","mut_white","white","salt_pepper"}; do
                for mode in {"svdn","svdne"}; do
                    for error in {"MAE","MSE"}; do

                        filename_prefix="${image}_${noise}_1_to_1000_B30_E800_${metric}_S30_norm"
                        filename_suffix="_${mode}_${error}"

                        if [ ! -f "curves_pictures/${filename_prefix}0${filename_suffix}.png" ]; then

                            python display/noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "30, 800" --step 30 --norm 0 --ylim "0, 0.05" --error ${error}
                        else
                            echo "Already generated.."
                        fi

                        if [ ! -f "curves_pictures/${filename_prefix}1${filename_suffix}.png" ]; then
                            python display/noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "30, 800" --step 30 --norm 1 --ylim "0, 0.1" --error ${error}
                        else
                            echo "Already generated.."
                        fi


                        if [ ! -f "curves_pictures/${filename_prefix}0${filename_suffix}_color.png" ]; then
                            python display/noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "30, 800" --step 30 --norm 0 --color 1 --ylim "0, 0.05" --error ${error}
                        else
                            echo "Already generated.."
                        fi

                        if [ ! -f "curves_pictures/${filename_prefix}1${filename_suffix}_color.png" ]; then
                            python display/noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "30, 800" --step 30 --norm 1 --color 1 --ylim "0, 0.1" --error ${error}

                        else
                            echo "Already generated.."

                        fi
                    done
                done
            done
    done
    fi
done
