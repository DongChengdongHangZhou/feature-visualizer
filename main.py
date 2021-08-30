import numpy as np
import cv2
import tifffile as tiff


def main(threshold,feature_map,target_img,query_img):

    matrix = feature_map
    # matrix[0] = 0
    matrix[0:28,:]=0
    matrix[29:64,:]=0
    def normalize(mat):
        # mean = mat.mean()
        # std = mat.std()
        # mat = (mat-mean)/std
        # mat = 1/(1+np.exp(-mat)) #用numpy实现sigmoid
        mat = (mat-mat.min())/(mat.max()-mat.min())
        return mat
    matrix = normalize(matrix)
    location_x, location_y = np.where(matrix>threshold)  
    num_point_pair = location_x.size
    query_mat = np.zeros((2,num_point_pair))
    target_mat = np.zeros((2,num_point_pair))
    query_mat[0], query_mat[1] = np.floor(location_x/8)+0.5, location_x%8 +0.5
    target_mat[0], target_mat[1] = np.floor(location_y/50)+0.5, location_y%50 +0.5
    query_mat, target_mat = np.floor(query_mat*16), np.floor(target_mat*16)
    concat_target_query = np.ones((600,928,3))*255
    concat_target_query[0:600,0:800,:] = target_img
    concat_target_query[0:128,800:928,:] = query_img
    for i in range(num_point_pair):
        # print(query_mat[:,i],target_mat[:,i])
        q_x = int(query_mat[0][i])
        q_y = int(query_mat[1][i]+800)
        t_x = int(target_mat[0][i])
        t_y = int(target_mat[1][i])
        print(t_y,t_x,q_y,q_x)
        cv2.line(concat_target_query,(t_y,t_x),(q_y,q_x),(0,0,255),1)
    cv2.imwrite('save.jpg',concat_target_query)


if __name__ == '__main__':
    threshold = 0.65
    feature_map = tiff.imread('tensor.tiff')[0]
    target_img = cv2.imread('small.jpg')
    query_img = cv2.imread('query_vis.jpg')
    main(threshold,feature_map,target_img,query_img)