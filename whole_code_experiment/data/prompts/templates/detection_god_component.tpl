# Task

You are a software engineering expert in software refactoring.

Your task is to detect the smell: God Component

Definition:
God Component arise when a component is **excessively** large either in terms of Lines Of Code or the number of classes.

# Constraints

- Give the answer exactly in the structure defined in the **#Successful Output** section, without any comments or explanations.
- The **justification** field must summarize the key elements that support the detection result.
- Only perform the analysis if you deem the information in the **#Input** section sufficient.
- All fields in the **#Successful Output** are mandatory.

# Input

The following metrics and dependencies are available at package and class levels:

```java
{INPUT_DATA}
```

# Successful Output

Provide the output in this structure:

```json
{
    "smell": "God Component",
    "package": [package name],
    "detection": [true/false],
    "justification": [Reasons for the detection result, citing the elements that justify the decision]
}
```