# Max Payne 1 and Max Payne 2 LDB (Game Levels) Importer plugin for Maya 2022/2023/2024

<img src="./docs/images/max_img.jpg" />

# Specifications

[Files specifications](./docs/specification/INDEX.MD)

See the [code review and validation scope](docs/REVIEW.md),
[PCX/SCX image support](docs/specification/IMAGES.MD), and [remaining work](TODO.md).

Development checks (no Maya or additional packages required):

```console
python -m unittest discover -s tests -v
```

# Prerequisites:

You will need:
- Maya 2022/2023/2024 with Python 3 support

# Maya Configuration:

- Go to Maya's menu ```Windows > Settigns/Preferences > Preferences```
- Set ```Up axis``` to ```Y```
- Set ```Working Units``` to ```centimeter```
<img src="./docs/images/Screenshot_7.png" />

# Installation:

No additional Python packages are required. PCX and SCX textures are decoded
by the bundled SDK and written as TGA images for Maya.

Put both ```max_payne_sdk_ldb_importer.py``` and ```max_payne_sdk_kf2_importer.py``` files into the ```plug-ins``` directory:

Windows:

```
C:\Users\<username>\Documents\maya\<version>\plug-ins\
```

Mac OSX:

```
/Users/Shared/Autodesk/maya/<version>/plug-ins/
```

Linux:

```
/home/<username>/maya/<version>/plug-ins/
```

Put the ```max_payne_sdk``` and the ```max_payne_maya``` into the ```scripts``` directory:

Windows:

```
C:\Users\<username>\Documents\maya\<version>\scripts\
```

Mac OSX:

```
/Users/Shared/Autodesk/maya/<version>/scripts/
```

Linux:

```
/home/<username>/maya/<version>/scripts/
```

Start Maya and enable the plugin:

<img src="./docs/images/Screenshot_5.png" />
<img src="./docs/images/Screenshot_6.png" />

# Import:

- Go to Maya's menu ```File > Import...```
- Select ```Max Payne LDB Import```

<img src="./docs/images/Screenshot_8.png" />
<img src="./docs/images/Screenshot_9.png" />
