# Hexagonal Coherence Check

This project checks if the dependency flow between the layers of the Hexagonal architecture defined 
for this project was respected.

### How to install

It can be easily installed via pip: `pip install hexagonal-py`

### How to configure your project

There are two ways to configure `hexagonal-py`:
1. Using `pyproject.toml` (recommended)
2. Using `hexagonal_config.py`, which is expected to be on your main source folder. 

It's necessary to define your hexagonal layers and their order.
Given for example, the project structure below:
```
pyproject.toml (Optinal)
. src
├── __init__.py
├── hexagonal_config.py (Optional)
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
.tests    
```
General aspects:
1. Existing layers: `domain`, `infrastructure`, `services`, `usecases`.
2. Which should respect the following dependency flow: `infrastructure` -> `usecases` -> `services` -> `domain`
3. Exclude `tests` from checks

If you are using `pyproject.toml`, you would have this:
```toml
[tool.hexagonalpy]
excluded_dirs = ['/tests']

[tool.hexagonalpy.layer.1]
name = 'Domain'
directories_groups = [['/domain']]

[tool.hexagonalpy.layer.2]
name = 'Services'
directories_groups = [['/services']]

[tool.hexagonalpy.layer.3]
name = 'Use Cases'
directories_groups = [['/usecases']]

[tool.hexagonalpy.layer.4]
name = 'Infrastructure'
directories_groups = [['/infrastructure']]
```

If you are using `hexagonal_config.py`:
```python
from hexagonal.hexagonal_config import hexagonal_config

hexagonal_config.add_inner_layer_with_dirs(layer_name='infrastructure', directories=['/infrastructure'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='use_cases', directories=['/use_cases'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='services', directories=['/services'])
hexagonal_config.add_inner_layer_with_dirs(layer_name='domain', directories=['/domain'])

hexagonal_config.excluded_dirs = ['/tests']
```

#### Extra content

1. excluded_dirs  
List of directories that you want to exclude from the `hexagonal-py` validation.  
Syntax: `excluded_dirs = ['/tests', '/another_folder', '/another_folder2']`


2. Layers  
List of layers you defined in your project. 
There are 3 aspects you need to fill in for a layer: `layer order`, `name`, `directories_groups`.

2.1. Layer order: The number of the layers tells the order of the dependency flow between them. 
Where the most inner layer is `1` and the most outer layer is the greater number. Example:

```toml
[tool.hexagonalpy.layer.1] # Layer 1, as it's the most inner layer, and it can't point to any other layer but all the 
                           # other layers can point to it.
name = 'domain'
directories_groups = [['/domain']]
```

2.2. Name: The readable name of the layer, that will be used for documentation, internal messages etc.

2.3. Directories_groups: It's a list of a list. You can specify which folders belong to the given layer, and you can also 
define that some folders can't point to other folders inside the same layer. For instance, the `MySql` and `Postgres` 
components belongs to `Infrastructure Layer` but **can't** refer to each other.

```toml
[tool.hexagonalpy.layer.4] 
name = 'Infrastructure'
directories_groups = [['/Infrastructure/MySql'],['Infrastructure/Postgres']]
```

### Generating the Project Diagram
This command generate a visual diagram show the composition of your hexagonal layers.

#### Pre requisites
To generate the Hexagonal Diagram of the project, it's necessary to have Graphviz installed in the machine.  
For Mac you can ``brew install graphviz``.  
For other, check the documentation https://graphviz.org/download/. 

#### CMD
`hexagonal diagram --project_path ./ --source_path ./src` 

### Checking Project's Hexagonal Integrity 
This checks if the correct flow of the dependencies -from outer to inner layer- was respected.

#### CMD
`hexagonal check --project_path ./ --source_path ./src`

