# Task

You are a software engineering expert in software refactoring. Your task is to detect the smell: Hub-like Modularization.

Definition:
Hub-like Modularization  arises when an abstraction has dependencies (both incoming and outgoing) with a large number of other abstractions.

# Constraints
- Give the answer exactly in the structure defined in the **#Successful Output** section.
- Do not include comments, explanations, or text outside the defined output format.

# Input

```java
{INPUT_DATA}
```

# Output

Provide the output in this structure:

```json
{
    "class": [package name].[class name],
    "detection": [true/false],
    "justification": [Reasons for the detection result, citing the elements that justify the decision]
}
```