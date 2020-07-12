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

## Next steps with jupyter lab

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

## Train model

```bash
cd yolo
python train.py --model_config_path ./config/yolov3_custom.cfg --data_config_path ./config/coco_custom.data --class_path ./config/coco_custom.names
```

change classes in [yolo] (3 times)
change filters before [yolo] (3 times)
filters = (classes + 5) x 3