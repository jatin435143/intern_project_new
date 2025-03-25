import re
import subprocess
import utils

def analyze_code(filename: str, code: str):
    if filename.endswith(".py"):
        language = "python"
    elif filename.endswith(".js"):
        language = "javascript"
    else:
        language = filename.split(".")[-1]
    
    if language not in ["python", "javascript"]:
        raise ValueError(f"Unsupported language: {language}")

    score = 100
    recommendations = []
    dict1, dict2, dict3, dict4, dict5, dict6 = {}, {}, {}, {}, {}, {}

    print("🔍 Analyzing code for:", filename)  # Debugging print

    # Naming conventions check
    if language == "python":
        dict1=utils.check_naming_conventions_from_string(code)
        dict2=utils.analyze_function_length_and_modularity(code)
        dict3=utils.analyze_comments_and_docstrings(code)
        dict4=utils.analyze_formatting_and_indentation(code)
        dict5=utils.analyze_reusability_and_dry(code)
        dict6=utils.analyze_web_dev_best_practices(code)

    elif language == "javascript":
        dict1=utils.analyze_js_naming_conventions(code)
        dict2=utils.analyze_js_function_modularity(code)
        dict3=utils.analyze_js_comments(code)
        dict4=utils.analyze_js_formatting(code)
        dict5=utils.analyze_js_reusability(code)
        dict6=utils.analyze_js_best_practices(code)

    # Ensure the score is never negative
    analysis_dicts = {
        "Naming Conventions": dict1,
        "Function Modularity": dict2,
        "Comments & Docstrings": dict3,
        "Formatting & Indentation": dict4,
        "Reusability (DRY)": dict5,
        "Best Practices": dict6
    }

    # Sum up all scores
    total_score = sum(d.get("score", 0) for d in analysis_dicts.values())

    # Collect all issues into a list
    all_issues = []
    for d in analysis_dicts.values():
        if "issues" in d:
            all_issues.extend(d["issues"])  # Append issues to the list

    # Prepare metrics list
    metrics = [{"name": section, "score": d.get("score", 0)} for section, d in analysis_dicts.items()]

    return {
        "overall_score": total_score,
        "metrics": metrics,  # List of dictionaries with names and scores
        "issues": all_issues
    }
