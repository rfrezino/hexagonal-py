# Hexagonal Sanity Check

This project checks if the dependency flow between the layers of the Hexagonal architecture defined 
for this project was respected.

### How to install

It can be easily installed via pip: `pip install hexagonal-sanity-check`

### How to configure your project

First it's necessary to define your hexagonal layers and their order.
The tool expects a default file name on your source folder dir with the name `hexagonal_config.py`.

1. First you create the Hexagonal Layers you have on your system via the class name HexagonalLayer.
There are two arguments: 
   - `name`: It can be any name, `domain`, `frontend`, `infrastructure`, or any name you used for your layers.
   - `usecases`: This is the name of the directory the files related to this layer as storage. It's not the full path, 
just the directory name.

2. Import `hexagonal_config` on your file, and define the order with `+` (add layers)
then `>>`(set the sequence of the layers). The most to the left layers is the most outer layer, while
the most to the right layer is the most inner layer.

Example, for this folder structure:
```
. src
├── __init__.py
├── hexagonal_config.py
├── domain
│   ├── __init__.py
│   ├── __pycache__
│   └── person.py
├── infrastructure
│   ├── __init__.py
│   └── person_mysql_repository.py
├── main.py
├── services
│   ├── __init__.py
│   └── person_repository.py
└── usecases
    ├── __init__.py
    └── create_person_usecase.py
```
The file:
```python
from hexagonal.domain.hexagonal_layer import HexagonalLayer
from hexagonal.main import hexagonal_config

infrastructure_layer = HexagonalLayer(name='infrastructure', directories=['infrastructure'])
use_cases_layer = HexagonalLayer(name='use_cases', directories=['usecases'])
services_layer = HexagonalLayer(name='services', directories=['services'])
domain_layer = HexagonalLayer(name='domain', directories=['domain'])

hexagonal_config + infrastructure_layer >> use_cases_layer >> services_layer >> domain_layer
```


### Generating the Project Diagram
This command generate a visual diagram show the composition of your hexagonal layers.

#### Pre requisites
To generate the Hexagonal Diagram of the project, it's necessary to have Graphviz installed in the machine.  
For Mac you can ``brew install graphviz``.  
For other, check the documentation https://graphviz.org/download/. 

#### CMD
`hexagonal diagram --source_path ./` 

### Checking Project's Hexagonal Integrity 
This checks if the correct flow of the dependencies -from outer to inner layer- was respected.

#### CMD
`hexagonal check --source_path ./`

