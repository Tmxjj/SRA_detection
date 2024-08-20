# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser

from mmdet.apis import inference_detector, init_detector, show_result_pyplot

import mmrotate  # noqa: F401
from tqdm import tqdm

def parse_args(img,config,checkpoint,out_file):
    parser = ArgumentParser()
    parser.add_argument('--img',default=img, help='Image file')
    parser.add_argument('--config', default = config , help='Config file')
    parser.add_argument('--checkpoint', default = checkpoint ,help='Checkpoint file')
    parser.add_argument('--out-file', default=out_file, help='Path to output file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--palette',
        default='dota',
        choices=['dota', 'sar', 'hrsc', 'hrsc_classwise', 'random'],
        help='Color palette used for visualization')
    parser.add_argument(
        '--score-thr', type=float, default=0.3, help='bbox score threshold')
    args = parser.parse_args()
    return args


def main(args):
    # build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint, device=args.device)
    # test a single image
    result = inference_detector(model, args.img)
    # show the results
    show_result_pyplot(
        model,
        args.img,
        result,
        palette=args.palette,
        score_thr=args.score_thr,
        out_file=args.out_file)


if __name__ == '__main__':
    i = 18
        
    args = parse_args(
        img = f'data/demo/{i}.jpg',
        config = 'mmrotate/configs/redet/redet_re50_refpn_1x_dota_ms_rr_le90.py',
        checkpoint = 'mmrotate/configs/redet/redet_re50_fpn_1x_dota_ms_rr_le90-fc9217b5.pth',
        out_file = f'data/demo/out_{i}.jpg'
    )
    main(args)
