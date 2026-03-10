import re


def strip_markdown_fences(code: str) -> str:
    """Remove any markdown code fences the model may have added."""
    code = re.sub(r"^```[a-zA-Z]*\n", "", code.strip())
    code = re.sub(r"\n```$", "", code)
    return code.strip()
