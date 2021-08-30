target_image的原图为img_show.png，尺寸为(600*800), query_image的原图为query_show.jpg,尺寸为(128,128)。
在one-shot object detection中，target_image经过特征提取网络，得到了38*50的特征feature_t,
query_image经过特征提取网络，得到16*16的特征feature_q。
将feature_q以及feature_t进行相乘，得到特征张量tensor，尺寸为(16*16*38*50),将其拍扁成(256,1900),保存为tensor.tiff。
将tensor.tiff读入，做归一化，记为mat。mat[i][j]代表feature_q中第i个元素和feature_t中第j个元素的乘积。
举例说明：比如mat[38][1274]的值，代表了第38个feature_q的元素和第1274个feature_t的元素的乘积。
第38个feature_q的元素的意义：int(38/16)=2, 38%16=6， 代表feature_q中第2行第6列的元素
第1274个feature_t的元素的意义：int(1274/50)=25, 1274%50=24, 代表feature_t中第25行第24列的元素
设置一个threshold，例如0.8，所有大于0.8的mat元素值都会保留，否则置零。
取出所有被保留的元素的坐标。比如mat[38][1274]就被保留了下来，这说明：
feature_q中第2行第6列的元素 和 feature_t中第25行第24列的元素 有很好的相应。
从feature_q映射回query要放大16倍，从feature_t映射回target要放大8倍。
以mat[38][1274]为例，我们将feature_q[2][6]做resize放大，映射回query_image相应的位置，
将feature_t[25][24]做resize放大，映射回target_image相应的位置,将这两个在对应特征上相应很好的像素点连线。
把所有符合条件的点连线，保存在save.jpg中。