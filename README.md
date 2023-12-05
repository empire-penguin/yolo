# Yolo for Culinary

## API Documentation

[empire-penguin.github.io/yolo](https://empire-penguin.github.io/yolo/)

## Build Documentation

```bash
cd docs
make html
```

## Installation Instructions

### Clone Repo

```bash
git clone https://github.com/empire-penguin/yolo
cd yolo
```

### Create a new virtual environment

```bash
python3 -m venv venv
```

### Activate the virtual environment

* On Windows:

    ```bash
    venv\Scripts\activate
    ```

* On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

### Install requirements

```bash
pip3 install -r requirements.txt
```

### Install pytorch

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Install yolo

```bash
pip3 install .
```

### Getting dataset

```bash
wget -P dataset http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar 

tar -xvf VOCtrainval_11-May-2012.tar
```

## Usage

### Run unit tests

```bash
python3 -m unittest
```

this will download the VOCdevkit used by yolo to train and find the features for the decision making process
edict.py

### *Todo*

Create / find a dataset to do transfer learning of grocery items
