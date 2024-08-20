# Preparing DOTA Dataset

<!-- [DATASET] -->

```bibtex
@InProceedings{Xia_2018_CVPR,
author = {Xia, Gui-Song and Bai, Xiang and Ding, Jian and Zhu, Zhen and Belongie, Serge and Luo, Jiebo and Datcu, Mihai and Pelillo, Marcello and Zhang, Liangpei},
title = {DOTA: A Large-Scale Dataset for Object Detection in Aerial Images},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2018}
}
```

## download dota dataset

The dota dataset can be downloaded from [here](https://captain-whu.github.io/DOTA/dataset.html).

The data structure is as follows:

```none
mmrotate
├── mmrotate
├── tools
├── configs
├── data
│   ├── DOTA
│   │   ├── train
│   │   ├── val
│   │   ├── test
```

## split dota dataset

Please crop the original images into 1024×1024 patches with an overlap of 200 by run

```shell
python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ss_trainval.json

python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ss_test.json
```

If you want to get a multiple scale dataset, you can run the following command.

```shell
python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ms_trainval.json

python tools/data/dota/split/img_split.py --base-json \
  tools/data/dota/split/split_configs/ms_test.json
```

Please change the `img_dirs` and `ann_dirs` in json. (Forked from [BboxToolkit](https://github.com/jbwang1997/BboxToolkit), which is faster then DOTA_Devkit.)

## change root path in base config

Please change `data_root` in `configs/_base_/datasets/dotav1.py` to split DOTA dataset.
## 参数说明
gaps:

裁剪图像块之间的重叠区域。这里设置为200，表示相邻图像块之间有200像素的重叠。
rates:

缩放比例列表。这里设置为1.0，表示图像不会进行缩放，按原始尺寸进行裁剪。
img_rate_thr:

图像块的保留阈值。如果裁剪后图像块中有效图像的占比（即未被裁剪到的边缘部分）低于这个阈值，该图像块将被丢弃。这里设置为0.6，表示图像块中至少60%的区域需要包含有效图像内容。
iof_thr:

与标注文件相关的阈值（Intersection over Foreground）。用于判断裁剪后的图像块是否保留标注的对象。这里设置为0.7，表示当裁剪块中保留的标注对象面积与原始对象面积的比率大于70%时，保留该块。
no_padding:

控制是否对裁剪后的图像块进行填充。这里设置为false，表示如果图像块不足1024×1024像素，则用指定的填充值进行填充。
padding_value:

如果启用了填充（no_padding=false），此字段指定填充的像素值。这里设置为[104, 116, 124]，表示填充值的RGB颜色分别为104、116、124。