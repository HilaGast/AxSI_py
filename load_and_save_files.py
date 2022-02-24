import nibabel as nib
import numpy as np
import os


def save_nifti(fname,img,affine):

    file_img = nib.Nifti1Image(img,affine)
    nib.save(file_img,fname)


def load_diff_files(subj_folder, file_names):
    from dipy.io import read_bvals_bvecs

    # Load diff nii file:
    diff_file = nib.load(os.path.join(subj_folder,file_names['data']))
    diff_img = diff_file.get_fdata()  # i1
    info_nii = diff_file.header
    data = np.asarray(diff_img, dtype='float64')
    data[data < 0] = 0
    affine = diff_file.affine

    # Load bval/bvec:
    bval, bvec = read_bvals_bvecs(os.path.join(subj_folder,file_names['bval']), os.path.join(subj_folder,file_names['bvec']))
    bvec = np.reshape(bvec, [len(bval), -1]);

    # Round bval to closest 50 and divide by 1000:
    bval2 = 2 * np.asarray(bval)
    bval2 = bval2.round(-2)
    bval = bval2 / 2000

    # Remove bval<1000 from calc:
    blow_locs = np.intersect1d(np.where(bval > 0)[0], np.where(bval < 1)[0])
    bval = np.delete(bval, blow_locs)
    bvec = np.delete(bvec, blow_locs, 0)
    data = np.delete(data, blow_locs, 3)

    # Load mask:
    mask = nib.load(os.path.join(subj_folder,file_names['mask'])).get_fdata()

    return data, affine, info_nii, bval, bvec, mask

