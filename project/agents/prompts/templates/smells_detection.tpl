# Task

You are a software engineering expert in software refactoring.

Your task is to detect the smell: {SMELL_NAME}

Definition: {SMELL_DEFINITION}

# Constraints

- Give the answer exactly in the structure defined in the **#Successful Output** section, without any comments or explanations.
- The **justification** field must summarize the key elements that support the detection result.
- Only perform the analysis if you deem the information in the **#Input** section sufficient. Otherwise, follow the guidelines in the **#Unsuccessful Output** section.
- All fields in the **#Successful Output** are mandatory.

# Input

The following metrics and dependencies are available at package and class levels:

```json
{INPUT_DATA}
```

# Successful Output

Provide the output in this structure:

```json
{
    "smell": "{SMELL_NAME}",
    "package": [package name],
    "detection": [true/false],
    "justification": [Reasons for the detection result, citing the elements that justify the decision]
}
```

# Unsucessfull Output

If the available data are insufficient to detect this smell, return:

```json
{
    "message": "It is impossible to detect {SMELL_NAME} with the available data."
}
```

