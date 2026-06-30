# Multi-Agent Refactoring

## Requirements
- Apache Maven 3.9.12
- Java 23.0.2
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

## Run

### Configuration

To run a refactoring, you need to adjust the settings in the *config.yml* file, located inside the *orchestrator* directory.

- **project**: Defines the *name* and *repo_path* of the repository to be refactored.
- **runs**: Defines the number of refactoring attempts. Each attempt runs the full cycle: planning, execution, and verification.
- **target**: Defines the smell to be refactored and the refactoring target. The *smell* attribute accepts: `IM`, `HM`, and `GC`. The *smell_name* attribute accepts: `Insufficient Modularization`, `Hub-like Modularization`, and `God Component`. The *target_type* attribute accepts: `class` or `package`. The *target_name* attribute must be written in the FQN format of the package or class to be refactored.

The remaining attributes refer to the default files used by the planner, source_executor, and quality_checker MVPs, as well as the scripts output directory. Only change these values if you are not going to use the default paths.

You also need to define your OpenAI token in the *.env* file in order to make inferences through the API.

### Execution

After configuring the orchestrator, run the following command to start the refactoring:

```bash
python -m orchestrator.run --config orchestrator/config.yml
```