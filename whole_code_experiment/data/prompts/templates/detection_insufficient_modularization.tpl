# Task

You are a software engineering expert in software refactoring.

Your task is to detect the smell: Insufficient Modularization.

Definition:
Insufficient Modularization arises when a class represents an abstraction that has not been adequately decomposed, resulting in excessive size, complexity, or a bloated interface. Such classes are difficult to understand, maintain, and evolve, and often concentrate responsibilities that could be separated into smaller, more cohesive abstractions.

# Constraints
- Perform the analysis should happen in the class provided in the **##Input** field.
- Use the package data only as contextual information to support class-level judgments.
- Give the answer exactly in the structure defined in the **#Successful Output** section.
- Do not include comments, explanations, or text outside the defined output format.
- All fields in the **#Successful Output** are mandatory.

# Input

Assess whether the following class has the smell Insufficient Modularization:

```java
{INPUT_DATA}
```

# Successful Output

Provide the output in this structure:

```json
{
    "smell": "{SMELL_NAME}",
    "class": [class name],
    "detection": [true/false],
    "justification": [Reasons for the detection result, citing the elements that justify the decision]
}
```