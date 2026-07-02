# Multi-Agent Refactoring

## Requirements
- Apache Maven 3.9.12
- Java 22+ (to run Designite)
- Java version compatible with the repository to be refactored.
- Python 3.13

In addition to the requirements listed above, you need to run the command below in the repository root to install the dependencies required to run the scripts.

```bash
pip install -r requirements.txt
```

## Repository Structure

This repository is divided as follows:

```text
multiagent_refactoring/
├── mvp/
├── data/
├── orchestrator/
└── tools/
```

### mvp
The *mvp* directory contains three modules:
- **planner**: responsible for generating a refactoring plan.
- **source_refactor**: responsible for executing a refactoring plan.
- **quality_checker**: responsible for analysing refactoring comparing metrics, code smells, and operations.

Each module is independent of the others and can be run separately. However, their design also allows them to work together.

### data
The modules in this repository access a path for reading Java projects and writing script execution logs. This path can be customized in the modules configuration files; however, the *data* directory is the default path.

Within *data*, the following directories exist:
- **repositories**: Java repositories that will be the target of refactoring.
- **runs**: logs and metadata from each refactoring execution.

### orquestrator
All modules in our repository generate a contract as system output, in addition to other artifacts. A module's contract is also input for another module. This way, it's possible to connect them all in a single workflow: plan, execute, and finally check.

The automation of this workflow is implemented in the scripts located in the *orchestrator* directory.

### tools
The *tools* directory contains third-party tools that are executed by the scripts of the *DesigniteJava* and *RefactoringMiner* modules.

## Configuration

### MVP Planner Configuration (mvp/planner/config.yml)

First, you need to change all 'absolute_path_to' values ​​to the absolute path to your repository.

The following planner attributes need to be configured:
- **prompts/smell**: each smell has a distinct prompt, therefore you must choose the absolute path to one of them 'mvp/planner/prompts/planner_(IM|HM|GC).md'.
- **designite/java_path**: path to your Java +22 installation (e.g., /usr/lib/jvm/jdk-22.0.2-oracle-x64/bin/java).
- **models/planner (optional)**: by default, 'gpt-5-mini' is being used, but it is possible to change to other models if desired.

*Important: A valid license is required to run DesigniteJava.*

The other attributes do not need to be changed, unless you wish to customize your repository.

### MVP Source Refactor Configuration (mvp/source_refactor/config.yml)

First, you need to change all 'absolute_path_to' values ​​to the absolute path to your repository.

No other configuration attributes of the MVP source refactor need to be changed, unless you wish to customize your scripts. Furthermore, it's possible to define which model to use in both the plan executor and the code repairer via the **models/executor and repair** attributes.

### MVP Quality Checker Configuration (mvp/quality_checker/config.yml)

First, you need to change all 'absolute_path_to' values ​​to the absolute path to your repository.

No other configuration attributes of the MVP source refactor need to be changed, unless you wish to customize your scripts.

### Orquestrator (orchestrator/config.yml)
The following orchestrator attributes need to be configured:

- **project**: Defines the *name* and *repo_path* of the repository to be refactored.
- **runs**: Defines the number of refactoring attempts. Each attempt runs the full cycle: planning, execution, and verification.
- **target**: Defines the smell to be refactored and the refactoring target. The *smell* attribute accepts: `IM`, `HM`, and `GC`. The *smell_name* attribute accepts: `Insufficient Modularization`, `Hub-like Modularization`, and `God Component`. The *target_type* attribute accepts: `class` or `package`. The *target_name* attribute must be written in the FQN format of the package or class to be refactored.

### OpenAI token (.env)
You also need to define your OpenAI token in the *.env* file in order to make inferences through the API.

## Run

After configuring the MVPs and the orchestrator, run the following command to start the refactoring:

```bash
python -m orchestrator.run --config orchestrator/config.yml
```