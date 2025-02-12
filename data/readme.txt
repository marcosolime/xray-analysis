(1)
in data/ct_data/phase_ct/PhaseCT_reconst.tif there is a volume sent by acquisition team with shape (2302, 2304, 2304).
It clearly shows the solid electrolyte and voids (so they say).
It was reconstructed using FBP (Filtered Back Projection).
Here is how to interpret the values:
    <-100: Voids
    Around 0: Solid electrolyte
    >100: LiCoO₂

(2)
Multiple files are contained in data/ct_data/multiple_ct.
Measurements were conducted under several conditions (they say): 100, 150, 180, 300, 450, 600, 900, and 1800.


(3)
in data/ct_data/noise_ct there is "data for noise reduction of the CMOS camera".

    This is a side note that is quite unfamiliar to me I guess.
    For Your Information

        dark: State without X-ray exposure (no visible light either)
        incident_X-ray: Image of the incident X-ray
        chart_pattern: Chart pattern image exposed to X-rays
        visible_light: Measurement under visible light, but with the light set up in a transmission configuration

    Note: In the visible light data, fragments of SiN (the black part in the middle) and surface contamination, etc., are visible.

(4)
then data/z-volumes/fbp/FBP.tif is another reconstructed volume.
in data/z-volumes/osem/OSEM.tif is the same volume but reconstructed with OSEM.
Raw projections that we used to train our models come from this model.
Raw data from this volumes are in data/battery/3_clear/LCO_abs.tif

(5)
in data/id_volumes there are the volume that we generate in our experiments.
these are volumes labelled by ID.
    id_4                    regular raw volume (256x256x256)

    id_22.npy               raw volume generated using R2Gaus on 360 projections
    id_22_crop.npy          same as above but we have shape 256x160x160 (boundaries are removed)
    id_22_crop_enh.npy      same as above but we did color enhancement
    id_22_crop_bin.npy      it is the binary GT mask with shape 256x160x160

(6)
in data/id_volumes_pw there are the volumes of my project work.
all the volumes are computed with saxnerf
    ground truth
        gt.npy              it is the binary GT mask with shape 256x160x160 (id_22_crop_bin.npy)

    ablation 1
        id_1                    battery volume, raw summation, size 256x256x256

(7) in the first hard drive (the 8TB disk) there is an acquisition that dates to 2025.02.12

This is the message Imari sent on the slack group:
    I am sending you the CT-XAFS data obtained during the recent beamtime for the sample after charging (where the charge distribution is spatially non-uniform). I would be very pleased if this data could be useful for examining the effectiveness of the new reconstruction method using data from a different batch, as well as for investigating methods for analyzing spectral data from CT images.
    Due to the large data size, I have copied it onto an SSD, which was sent to Professor Sato, scheduled to arrive in the morning of February 12.
    Within the SSD, there is a folder named mtr-xz-regist, which contains subfolders numbered from 001 to 042. Each of these subfolders holds X-ray absorption coefficient images of the sample obtained at different energy (wavelength) levels.
    Inside each numbered folder, there are 1,800 raw image files (1024x1024, 32-bit real, offset 0), corresponding to X-ray absorption coefficient images acquired at various rotational angles ranging from -90 to 90 degrees. By reconstructing these images, a 3D representation of the sample at each wavelength can be obtained.
    Since the sample drifted while acquiring X-ray absorption coefficient images at different wavelengths, image alignment has been performed using the data from energy index 20 as the reference.
    Information on which energy each numbered folder corresponds to is recorded in the energy_table file within the same SSD.
    Additionally, details about the rotational angles at which each of the 1,800 raw image files was acquired are provided in the angle.log file, also located in the SSD.
    Best regards,
    Yuta Kimura
    Tohoku University
