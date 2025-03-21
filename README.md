# Dual-Domain-Diffusion
# Dual-domain-CineMRI-using-optical-and-conditional-diffusion
## Project description：
1. Input Image Sequence: The input consists of a set of three consecutive image frames $\left(i_{t-1}, i_t, i_{t+1}\right)$, which are disturbed by adding noise through the "Noised" module. Below is another set of frame sequences $\left(k_{t-1}, k_t, k_{t+1}\right)$, also disturbed by the "Noised" module.
2. FlowNet Module: In the upper branch, the noisy image sequence passes through the "FlowNet" module, which is used to estimate motion vectors (i.e., optical flow) and outputs the information of the preceding and following frames corresponding to $i_t$ (i.e., $i_{t-1}^{\prime}$ and $i_{t+1}^{\prime}$ ).
3. Optical Flow Calculation: The lower branch uses optical flow calculation, where the corresponding image frames are processed through the "MASK" module. This module is used to fuse or filter the optical flow information with the noisy images, generating a new set of feature maps $z_T$.
4. QKV Mechanism: The generated optical flow images are transformed into frequency domain data through the inverse Fourier transform, guiding the image reconstruction in the frequency domain using an attention mechanism. After $T$ repetitions, the reconstructed image is generated.

   ### Model structure
![modell](https://github.com/user-attachments/assets/195c15f8-3f22-4ae9-b05b-bcb78cc05e82)

## in master branch, flownet2 is used to calculate optical flow between to frame, and by running
      fm.py 
   to get the optical feature maps

## Three parts of the model needed to be trained:
1. Unet for ddpm
2. transformer for optical features maps and origin images
3. transformer for dct images and images reconed above
   

### Run conditional diffusion to training Unet on dct transformed image:
      python model.py

the logic of adding the mask is in utils/mask_utils.py
