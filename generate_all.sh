for noise in {"cauchy","gaussian","laplace","log_normal","mut_white","white"}; do

    for identical in {"0","1"}; do

        if [ ${identical} == "1" ]; then
            python noise_computation.py --noise ${noise} --image images/calibration.png --n 999 --identical ${identical} --output ${noise}.png --all 1
        else
            python noise_computation.py --noise ${noise} --image images/calibration.png --n 999 --identical ${identical} --output ${noise}_color.png --all 1
        fi

    done
done


# specifig for salt and pepper noise
for identical in {"0","1"}; do
    if [ ${identical} == "1" ]; then
        python noise_computation.py --noise salt_pepper --image images/calibration.png --n 999 --identical ${identical} --output ${noise}_B.png --all 1 --p 0.1
        python noise_computation.py --noise salt_pepper --image images/calibration.png --n 999 --identical ${identical} --output ${noise}_A.png --all 1 --p 0.01
    else
        python noise_computation.py --noise salt_pepper --image images/calibration.png --n 999 --identical ${identical} --output ${noise}_A_color.png --all 1 --p 0.01
        python noise_computation.py --noise salt_pepper --image images/calibration.png --n 999 --identical ${identical} --output ${noise}_B_color.png --all 1 --p 0.1
    fi
done
