#coding:utf8
import os
from PIL import  Image
from torch.utils import data
import numpy as np
from torchvision import transforms as T

# 使用 Dataset提供数据集的封装，
# 再使用Dataloader实现数据并行加载
class DogCat(data.Dataset):
    
    def __init__(self,root,transforms=None,train=True,test=False):
        '''
        主要目标： 获取所有图片的地址，并根据训练，验证，测试划分数据
        '''
        self.test = test
        imgs = [os.path.join(root,img) for img in os.listdir(root)] 

        # test1: data/test1/8973.jpg
        # train: data/train/cat.10004.jpg 
        if self.test:
            imgs = sorted(imgs,key=lambda x:int(x.split('.')[-2].split('/')[-1]))
        else:
            imgs = sorted(imgs,key=lambda x:int(x.split('.')[-2]))
            
        imgs_num = len(imgs)
        
        # 对给定的数组进行重新排序主要有两种方式：
        # np.random.shuffle(x) 现场修改序列，改变自身内容。（类似洗牌，打乱顺序）
        # np.random.permutation(x) 返回一个随机排列
        # shuffle imgs
        np.random.seed(100)
        imgs = np.random.permutation(imgs)  # 随机排列一个序列，如果为多维数组，则只会沿着第一个索引随机排列
        
        # 划分训练、验证集，验证:训练 = 3:7
        if self.test:
            self.imgs = imgs
        elif train:
            self.imgs = imgs[:int(0.7*imgs_num)]  # 训练过程，使用 0.7×number的图像作为训练
        else :
            self.imgs = imgs[int(0.7*imgs_num):]  # 验证过程，使用 0.3×number的图像作为验证
            
    
        if transforms is None:
            # 数据转换操作，测试验证和训练的数据转换有所区别
            normalize = T.Normalize(mean = [0.485, 0.456, 0.406], 
                                     std = [0.229, 0.224, 0.225])

            # 测试集和验证集 : test= true or train = false;
            if self.test or not train: 
                self.transforms = T.Compose([
                    T.Resize(224),
                    T.CenterCrop(224),
                    T.ToTensor(),
                    normalize
                    ]) 
            else :
                # 训练阶段才会进入
                self.transforms = T.Compose([
                    T.Resize(256),
                    T.RandomResizedCrop(224),
                    T.RandomHorizontalFlip(),
                    T.ToTensor(),
                    normalize
                    ]) 
                
        
    def __getitem__(self,index):
        '''
        返回一张图片的数据
        对于测试集，没有label，返回图片id，如1000.jpg返回1000
        将文件读取等耗时的操作放在__getitem__函数中，利用多进程加速，
        同时，避免一次性将所有图像读入内存，不仅耗时也会占用大量内存，而且不易进行数据增强操作
        '''
        img_path = self.imgs[index]
        if self.test:
            label = int(self.imgs[index].split('.')[-2].split('/')[-1])
        else:
            label = 1 if 'dog' in img_path.split('/')[-1] else 0
        data = Image.open(img_path)
        data = self.transforms(data)
        return data, label
    
    def __len__(self):
        return len(self.imgs)
