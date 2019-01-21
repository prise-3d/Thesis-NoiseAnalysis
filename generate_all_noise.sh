
for file in "images"/*; do

    IFS='/' # space is set as delimiter
    read -ra ADDR <<< "$file" # str is read into an array as tokens separated by IFS
    IFS=' '

    image=${ADDR[1]%".png"}


    for noise in {"cauchy","gaussian","laplace","log_normal","mut_white","white","salt_pepper"}; do

        for identical in {"0","1"}; do

            if [ ${identical} == "1" ]; then
                python noise_computation.py --noise ${noise} --image ${file} --n 1000 --identical ${identical} --output ${image}_${noise}.png --step 10 --all 1 &
            else
                python noise_computation.py --noise ${noise} --image ${file} --n 1000 --identical ${identical} --output ${image}_${noise}_color.png --step 10 --all 1 &
            fi

        done
    done
done
