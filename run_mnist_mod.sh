#!/bin/bash

# Define the beta values
beta_values="0.01 0.1 0.3 0.5"

# Run the command for each beta value
for beta in $beta_values
do
    # Format the beta value by removing the decimal point
    beta_formatted=$(printf "%.2f" $beta | tr -d '.')

    if [ "$beta_formatted" = "" ]; then
        beta_formatted="0"
    fi
    
    # Set the step size based on the beta value
    if (( $(echo "$beta < 0.1" | bc -l) )); then
        t_step_size=0.1
    else
        t_step_size=1.0
    fi

    # Run the command and save the output to a file
    output_file="mnist_mod_$beta_formatted"

    # Uncomment the following line to run the actual command
    CUDA_VISIBLE_DEVICES=0 python3 -m advbench.scripts.train --dataset MNIST --algorithm CVaR_Modified_SGD --output_dir train-output/$output_file --cvar_sgd_beta $beta --cvar_sgd_t_step_size $t_step_size  --evaluators Clean PGD Augmented
done