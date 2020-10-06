# KIPI

Business image analyzer with the purpose of tracking good practices in work using artificial intelligence.

## Installation

For tagging we need tkinter: https://www.activestate.com/products/tcl/downloads/

Then we can create a venv (I have linked python3.7 with virtualenv) with tkinter with:

```bash
python3.7 -m venv venv
```

Activate the venv:

```bash
source venv/bin/activate
```

Install requirements in the venv:

```bash
pip install -r requirements.txt
```

Next you can add your virtual environment to Jupyter by typing:

```bash
python -m ipykernel install --user --name=venv
```

## Jupyter Lab Configuration

In a different terminal

```bash
jupyter lab
```

To check jupyter kernel list

```bash
jupyter kernelspec list
```

To uninstall a kernel

```bash
jupyter kernelspec uninstall venv
```

## Model Training

```bash
cd yolo
python train.py --model_config_path ./config/yolov3_custom.cfg --data_config_path ./config/coco_custom.data --class_path ./config/coco_custom.names
```

```bash
cd yolov4
python train.py -train_label_path ../../data/shopfront/train.txt -val_label_path ../../data/shopfront/val.txt -dir /Users/jrc/Desktop/Jorge/Otros/Coding/Kipi/kipi/models/yolov4 -classes 3 -pretrained ./cfg/yolov4.conv.137.pth
```

How to update yolo files:

- change classes in [yolo] (3 times)
- change filters before [yolo] (3 times)
- filters = (classes + 5) x 3

## References:

- https://towardsdatascience.com/training-yolo-for-object-detection-in-pytorch-with-your-custom-dataset-the-simple-way-1aa6f56cf7d9
- https://github.com/cfotache/pytorch_custom_yolo_training
- https://github.com/Tianxiaomo/pytorch-YOLOv4

## Versioning

1.0

## Authors

- **https://github.com/jramirezc93/**
- **https://github.com/aolea/**

## License

Private
