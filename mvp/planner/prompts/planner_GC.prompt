# GOAL
Refactor ONE cohesive cluster from the TARGET PACKAGE to reduce the God Component smell.

A single run must move only ONE cluster. All classes in the selected cluster must be moved to the SAME new subpackage.

# INPUT DATA
- `target_files`: files currently in the target package.
- `internal_deps`: dependencies between classes inside the target package.
- `incoming_deps`: external classes that depend on classes in the target package.
- `outgoing_deps`: target package classes depending on external classes.

# TASK
Choose exactly ONE cohesive cluster of classes from the target package.

Then generate a refactoring plan where:
- all classes in the cluster move to the same new subpackage;
- the plan contains exactly ONE block;
- that block moves all classes in the selected cluster together;
- the block contains 2 to 10 MOVE_CLASS operations.

# CLUSTER MOVEMENT STRATEGY

For God Component refactoring, each block must move one cohesive cluster, not a single isolated class.

A cluster must contain 2 to 4 classes.

All classes in the selected cluster must be moved to the same destination package.

Prefer clusters whose classes have strong internal relationships and many package-private interactions with each other.

Avoid moving highly central parser/state-machine classes alone.

Avoid selecting clusters that would require exposing many package-private members from classes that remain in the original package.

Each block must contain:
- optionally one CREATE_PACKAGE operation;
- two to four MOVE_CLASS operations;
- no UPDATE_VISIBILITY operation. UPDATE_VISIBILITY will be added automatically later.

Do not create one block per class.

Do not move all package classes in one block.

Prefer small cohesive clusters that can compile after limited visibility updates.

# PACKAGE RULES
- Move classes only from the TARGET PACKAGE to a subpackage of the TARGET PACKAGE.
- All moved classes must use the same destination package.
- Do not move classes to unrelated packages.
- Do not introduce facades.
- API changes are allowed.

# BLOCK RULES
- The plan must contain exactly ONE block.
- This single block represents the whole selected cluster.
- The block must contain 2 to 4 MOVE_CLASS operations.
- All MOVE_CLASS operations must move classes to the same destination package.
- The block may include one CREATE_PACKAGE operation before the MOVE_CLASS operations.
- The block files list must include the original source file path of every moved class.
- Do not create one block per class.
- Do not split the selected cluster across multiple blocks.
- Do not update external files in the plan; OpenRewrite will handle references/imports later.
- The executor will handle minimal package-private visibility changes in related internal files.

# ALLOWED OPS
CREATE_PACKAGE, MOVE_CLASS, ADD_OR_UPDATE_IMPORTS, UPDATE_CALL_SITES, UPDATE_VISIBILITY, NO_OP.

# OUTPUT
Return ONLY valid JSON.

{
  "smell_type": "<copied from input>",
  "target_level": "package",
  "target": "<target_name from input>",
  "selected_cluster": [
    "<class FQN>"
  ],
  "destination_package": "<new subpackage FQN>",
  "cluster_reason": "<why this cluster is cohesive and relatively safe>",
  "risk": "low|medium|high",
  "blocks": [
    {
      "id": 1,
      "goal": "Move one class from the selected cluster.",
      "files": [
        "<source file path from target_files>"
      ],
      "ops": [
        {
          "op": "CREATE_PACKAGE",
          "inputs": [],
          "outputs": ["<destination package FQN>"],
          "details": "Create the destination subpackage if it does not exist.",
          "risk": "low",
          "api_change": false
        },
        {
          "op": "MOVE_CLASS",
          "inputs": ["<old class FQN>"],
          "outputs": ["<new class FQN>"],
          "details": "Move this class to the destination package.",
          "risk": "low|medium|high",
          "api_change": true
        }
      ]
    }
  ]
}

# INPUT
```json
{input}
```