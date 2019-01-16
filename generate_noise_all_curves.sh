
for file in "images"/*; do

    IFS='/' # space is set as delimiter
    read -ra ADDR <<< "$file" # str is read into an array as tokens separated by IFS
    IFS=' '

    image=${ADDR[1]%".png"}

    echo $image
    if [ "$image" != "calibration" ] || [ "$image" != *"min_max_values"* ]; then

        #for metric in {"lab","mscn_revisited","low_bits_2","low_bits_3","low_bits_4","low_bits_5","low_bits_6","low_bits_4_shifted_2"}; do
        for metric in {"lab","low_bits_4","low_bits_5","low_bits_4_shifted_2"}; do
            for noise in {"cauchy","gaussian","laplace","log_normal","mut_white","white","salt_pepper"}; do
                for mode in {"svdn","svdne"}; do
                    for error in {"MAE","MSE"}; do

                        #echo "${image}_${metric}_${noise}_${mode}_${error}_norm0" >> output_test.txt
                        #echo "${image}_${metric}_${noise}_${mode}_${error}_norm1" >> output_test.txt
                        #echo "${image}_${metric}_${noise}_${mode}_${error}_norm0_color" >> output_test.txt
                        #echo "${image}_${metric}_${noise}_${mode}_${error}_norm1_color" >> output_test.txt

                        python noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "0, 800" --step 40 --norm 0 --ylim "0, 0.05" --error ${error}
                        python noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "0, 800" --step 40 --norm 1 --ylim "0, 0.1" --error ${error}
                        python noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "0, 800" --step 40 --norm 0 --color 1 --ylim "0, 0.05" --error ${error}
                        python noise_svd_tend_visualization.py  --prefix generated/${image}/${noise} --metric ${metric} --n 1000 --mode ${mode} --interval "0, 800" --step 40 --norm 1 --color 1 --ylim "0, 0.1" --error ${error}
                    done
                done
            done
    done
    fi
done
