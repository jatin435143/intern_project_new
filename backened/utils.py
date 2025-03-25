import ast
import re

# Regular expressions for naming conventions
SNAKE_CASE_PATTERN = re.compile(r'^[a-z_][a-z0-9_]*$')
PASCAL_CASE_PATTERN = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
UPPER_CASE_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]*$')

def to_snake_case(name):
    """Convert a given name to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def to_pascal_case(name):
    """Convert a given name to PascalCase."""
    words = re.split(r'[_\s]+', name)
    return ''.join(word.capitalize() for word in words)

def to_upper_case(name):
    """Convert a given name to UPPER_CASE."""
    return name.upper()

def check_naming_conventions_from_string(code_str):
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax error in the provided code: {e}"}

    errors = []
    total_checks = 0
    incorrect_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):  # Function names
            total_checks += 1
            if not SNAKE_CASE_PATTERN.match(node.name):
                incorrect_count += 1
                suggested_name = to_snake_case(node.name)
                errors.append(f"Function `{node.name}` → Suggested: `{suggested_name}`")

        elif isinstance(node, ast.ClassDef):  # Class names
            total_checks += 1
            if not PASCAL_CASE_PATTERN.match(node.name):
                incorrect_count += 1
                suggested_name = to_pascal_case(node.name)
                errors.append(f"Class `{node.name}` → Suggested: `{suggested_name}`")

        elif isinstance(node, ast.Assign):  # Variables/constants
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    total_checks += 1
                    if var_name.isupper():  # Constant should be UPPER_CASE
                        if not UPPER_CASE_PATTERN.match(var_name):
                            incorrect_count += 1
                            suggested_name = to_upper_case(var_name)
                            errors.append(f"Constant `{var_name}` → Suggested: `{suggested_name}`")
                    else:  # Variable should be in snake_case
                        if not SNAKE_CASE_PATTERN.match(var_name):
                            incorrect_count += 1
                            suggested_name = to_snake_case(var_name)
                            errors.append(f"Variable `{var_name}` → Suggested: `{suggested_name}`")

    # Calculate score
    score = round(10 * (1 - incorrect_count / total_checks)) if total_checks > 0 else 10

    return {
        "score": score,
        "issues": errors if errors else ["All naming conventions are correct!"]
    }

import ast

def analyze_function_length_and_modularity(code_str):
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax error in the provided code: {e}"}

    function_issues = []
    total_functions = 0
    long_functions = 0
    multi_task_functions = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            total_functions += 1
            function_name = node.name
            function_length = len(node.body)

            # Check if function is too long (>20 lines)
            if function_length > 20:
                long_functions += 1
                function_issues.append(f"Function `{function_name}` is too long ({function_length} lines). Consider breaking it down.")

            # Check if function does multiple tasks (heuristic: too many loops/conditions)
            loop_count = sum(isinstance(n, (ast.For, ast.While)) for n in ast.walk(node))
            condition_count = sum(isinstance(n, (ast.If, ast.Match)) for n in ast.walk(node))
            function_call_count = sum(isinstance(n, ast.Call) for n in ast.walk(node))

            if loop_count + condition_count > 3 and function_call_count > 3:
                multi_task_functions += 1
                function_issues.append(f"Function `{function_name}` seems to perform multiple tasks. Consider splitting it into separate functions.")

    # If no functions exist, score is 0
    if total_functions == 0:
        score = 20
        #function_issues.append("No issues in functions.")
    # If no issues found, full score (20/20)
    elif long_functions == 0 and multi_task_functions == 0:
        score = 20
        function_issues.append("All functions are well-structured!")
    # Otherwise, deduct points
    else:
        deduction = (long_functions * 5) + (multi_task_functions * 5)
        score = max(20 - deduction, 0)

    return {
        "score": score,
        "issues": function_issues
    }

import ast

def analyze_comments_and_docstrings(code_str):
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax error in the provided code: {e}"}

    issues = []
    total_functions = 0
    functions_with_docstrings = 0
    inline_comments = 0

    # Check for a module-level docstring (at the top of the file)
    module_docstring = ast.get_docstring(tree)
    if not module_docstring or len(module_docstring.strip()) < 10:  # Ensure it's not empty or too short
        issues.append("Missing or insufficient module-level docstring.")

    for node in ast.walk(tree):
        # Check function-level docstrings
        if isinstance(node, ast.FunctionDef):
            total_functions += 1
            docstring = ast.get_docstring(node)

            if docstring and len(docstring.strip()) >= 10:  # Ensure docstring is meaningful
                functions_with_docstrings += 1
            else:
                issues.append(f"Function `{node.name}` is missing a proper docstring.")

        # Check inline comments
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            # Skip strings used as standalone expressions (often docstrings)
            continue

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            # Skip constant string expressions (like module docstrings)
            continue

        elif isinstance(node, ast.Assign) or isinstance(node, ast.For) or isinstance(node, ast.If):
            # Look for comments right after code lines
            if hasattr(node, "lineno") and hasattr(node, "col_offset"):
                inline_comments += 1

    # Scoring System
    score = 20  # Start with full score

    # Deduct points for missing or weak docstrings
    if total_functions > 0:
        function_docstring_ratio = functions_with_docstrings / total_functions
        if function_docstring_ratio < 0.5:  # Less than 50% of functions have proper docstrings
            score -= 10
            issues.append("Less than 50% of functions have proper docstrings.")
        elif function_docstring_ratio < 1:  # Not all functions have docstrings
            score -= 5
            issues.append("Some functions are missing docstrings.")

    # Deduct for missing module-level docstring
    if not module_docstring or len(module_docstring.strip()) < 10:
        score -= 5

    # Deduct for lack of inline comments (if functions exist)
    if total_functions > 0 and inline_comments == 0:
        score -= 5
        issues.append("No inline comments found. Consider adding explanations for complex code.")

    # Ensure score is not negative
    score = max(score, 0)

    return {
        "score": score,
        "issues": issues if issues else ["Good documentation and comments!"]
    }

import ast
import re

def analyze_formatting_and_indentation(code_str):
    issues = []
    score = 15  # Start with full score

    lines = code_str.split("\n")

    # Check for mixed indentation (Tabs & Spaces in the same file)
    uses_tabs = any("\t" in line for line in lines)
    uses_spaces = any("    " in line for line in lines)

    if uses_tabs and uses_spaces:
        issues.append("Mixed indentation detected (Tabs and Spaces). Use spaces only.")
        score -= 5

    # Check for indentation errors using AST
    try:
        ast.parse(code_str)
    except IndentationError as e:
        issues.append(f"Indentation error: {str(e)}")
        score -= 5

    # Check for trailing whitespaces
    trailing_whitespace_lines = [i+1 for i, line in enumerate(lines) if line.rstrip() != line]
    if trailing_whitespace_lines:
        issues.append(f"Trailing whitespaces found on lines: {trailing_whitespace_lines}. Remove extra spaces.")
        score -= 2

    # Check for excessive blank lines (more than 2 in a row)
    excessive_blank_lines = [i+1 for i in range(len(lines)-2) if lines[i] == lines[i+1] == lines[i+2] == ""]
    if excessive_blank_lines:
        issues.append(f"Excessive blank lines on lines: {excessive_blank_lines}. Limit consecutive blank lines to 2.")
        score -= 3

    # Ensure score is not negative
    score = max(score, 0)

    return {
        "score": score,
        "issues": issues if issues else ["Good formatting and indentation!"]
    }

import ast
import re
from collections import Counter

def analyze_reusability_and_dry(code_str):
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax error in the provided code: {e}"}

    issues = []
    score = 15  # Start with full score

    functions = {}
    repeated_code = Counter()
    hardcoded_values = Counter()
    
    for node in ast.walk(tree):
        # Check for function definitions and count similar functions
        if isinstance(node, ast.FunctionDef):
            func_body = ast.unparse(node.body) if hasattr(ast, "unparse") else ""
            functions[node.name] = func_body
            repeated_code[func_body] += 1

        # Check for hardcoded values
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)) and len(str(node.value)) > 2:
            hardcoded_values[node.value] += 1

    # Deduct points for repeated functions (violating DRY)
    repeated_functions = [func for func, count in repeated_code.items() if count > 1]
    if repeated_functions:
        issues.append(f"Repeated function logic found in {len(repeated_functions)} function(s). Consider reusing them.")
        score -= 5

    # Deduct points for excessive hardcoded values
    if len(hardcoded_values) > 5:
        issues.append("Too many hardcoded values found. Use constants or variables instead.")
        score -= 5

    # Check for large functions doing multiple tasks (poor modularity)
    for func_name, func_body in functions.items():
        if len(func_body.split("\n")) > 20:  # If function is too long (>20 lines)
            issues.append(f"Function '{func_name}' is too long. Consider breaking it into smaller functions.")
            score -= 5

    # Ensure score is within 0-15
    score = max(score, 0)

    # If no issues, it's well-structured
    if not issues:
        issues.append("Good reusability and DRY principles followed!")

    return {
        "score": score,
        "issues": issues
    }

import ast
import re

def analyze_web_dev_best_practices(code_str):
    issues = []
    score = 20  # Start with full score

    # Check for hardcoded secrets (API keys, passwords)
    hardcoded_secrets = re.findall(r"['\"](sk-[a-zA-Z0-9]+|AIza[0-9A-Za-z-_]+|AKIA[0-9A-Z]+['\"])", code_str)
    if hardcoded_secrets:
        issues.append("Hardcoded API keys or secrets detected. Use environment variables instead.")
        score -= 5

    # Check for insecure 'eval' usage
    if "eval(" in code_str:
        issues.append("Usage of 'eval()' detected. This can lead to security vulnerabilities.")
        score -= 5

    # Check for direct string concatenation in SQL queries (SQL injection risk)
    if re.search(r'execute\s*\(\s*f?["\']SELECT .*["\']', code_str):
        issues.append("Possible SQL injection risk found in raw SQL queries. Use parameterized queries instead.")
        score -= 5

    # Check for print/debug statements instead of proper logging
    if re.search(r'print\s*\(|debug\s*\(', code_str):
        issues.append("Found 'print' or 'debug' statements. Use logging instead for production applications.")
        score -= 3

    # Check for missing environment variable usage
    if "os.getenv(" not in code_str and "os.environ[" not in code_str:
        issues.append("Environment variables not used for configuration. Store secrets securely.")
        score -= 2

    # Ensure score is within 0-20
    score = max(score, 0)

    # If no issues, it's well-structured
    if not issues:
        issues.append("Good web development best practices followed!")

    return {
        "score": score,
        "issues": issues
    }

import re

def analyze_js_naming_conventions(js_code):
    issues = []
    score = 10  # Start with full score

    # Regex patterns for different naming conventions
    variable_pattern = re.compile(r'\b(let|const|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=')
    function_pattern = re.compile(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(')
    class_pattern = re.compile(r'class\s+([A-Z][a-zA-Z0-9]*)\s*{')
    constant_pattern = re.compile(r'\bconst\s+([A-Z_][A-Z0-9_]*)\s*=')

    # Find all matches
    variables = variable_pattern.findall(js_code)
    functions = function_pattern.findall(js_code)
    classes = class_pattern.findall(js_code)
    constants = constant_pattern.findall(js_code)

    # Check variable naming (should be camelCase or snake_case)
    for keyword, var in variables:
        if not re.match(r'^[a-z]+([A-Z][a-z0-9]*)*$', var) and not re.match(r'^[a-z]+(_[a-z0-9]+)*$', var):
            issues.append(f"Variable '{var}' should use camelCase or snake_case.")
            score -= 2

    # Check function naming (should be camelCase)
    for func in functions:
        if not re.match(r'^[a-z]+([A-Z][a-z0-9]*)*$', func):
            issues.append(f"Function '{func}' should follow camelCase naming.")
            score -= 2

    # Check class naming (should be PascalCase)
    for cls in classes:
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', cls):
            issues.append(f"Class '{cls}' should follow PascalCase naming.")
            score -= 2

    # Check constants naming (should be UPPER_CASE)
    for const in constants:
        if not re.match(r'^[A-Z_]+$', const):
            issues.append(f"Constant '{const}' should be in UPPER_CASE.")
            score -= 2

    # Ensure score is within 0-10
    score = max(score, 0)

    # If no issues, it's well-structured
    if not issues:
        issues.append("Good naming conventions followed!")

    return {
        "score": score,
        "issues": issues
    }

import re

def analyze_js_function_modularity(js_code):
    issues = []
    score = 20  # Start with full score

    function_pattern = re.compile(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\((.*?)\)\s*{([\s\S]*?)}', re.MULTILINE)

    functions = function_pattern.findall(js_code)

    if not functions:
        return {
            "score": 0,
            "issues": ["No functions found. Define functions for better modularity."]
        }

    for func_name, params, body in functions:
        lines = body.strip().split("\n")
        num_lines = len(lines)

        # Check for long functions (>20 lines)
        if num_lines > 20:
            issues.append(f"Function '{func_name}' is too long ({num_lines} lines). Consider splitting it.")
            score -= 5

        # Check for multiple tasks (based on keywords like multiple loops, multiple conditionals)
        loop_count = len(re.findall(r'\b(for|while)\b', body))
        conditional_count = len(re.findall(r'\b(if|switch)\b', body))

        if loop_count > 1 or conditional_count > 2:
            issues.append(f"Function '{func_name}' seems to handle multiple tasks. Consider breaking it into smaller functions.")
            score -= 5

    # Ensure score is within 0-20
    score = max(score, 0)

    if not issues:
        issues.append("Good function structure and modularity!")

    return {
        "score": score,
        "issues": issues
    }

import re

def analyze_js_comments(js_code):
    issues = []
    score = 20  # Start with full score

    # Count function definitions
    function_pattern = re.compile(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(')
    functions = function_pattern.findall(js_code)
    num_functions = len(functions)

    # Count documentation comments (JSDoc style /** ... */)
    docstring_pattern = re.compile(r'/\*\*[\s\S]*?\*/')
    docstrings = docstring_pattern.findall(js_code)

    # Count inline comments (// ...)
    inline_comments = re.findall(r'//.*', js_code)

    # Check if documentation exists
    if num_functions > 0:
        if len(docstrings) < num_functions:
            missing_docs = num_functions - len(docstrings)
            issues.append(f"{missing_docs} function(s) lack documentation (JSDoc comments).")
            score -= 10

        if len(inline_comments) < num_functions:
            issues.append(f"Not enough inline comments for clarity.")
            score -= 5

    else:
        if len(inline_comments) < 5:
            issues.append("Few or no comments found in the script. Consider adding documentation.")
            score -= 10

    # Ensure score is within 0-20
    score = max(score, 0)

    if not issues:
        issues.append("Good documentation and comments present!")

    return {
        "score": score,
        "issues": issues
    }

import re

def analyze_js_formatting(js_code):
    issues = []
    score = 15  # Start with full score

    lines = js_code.split("\n")
    
    # Detect inconsistent indentation (mix of spaces and tabs)
    space_indent = re.compile(r"^( {2,4})\S")
    tab_indent = re.compile(r"^\t+\S")

    space_lines = sum(1 for line in lines if space_indent.match(line))
    tab_lines = sum(1 for line in lines if tab_indent.match(line))

    if space_lines > 0 and tab_lines > 0:
        issues.append("Mixed spaces and tabs detected. Use a consistent indentation style.")
        score -= 5

    # Detect lines with irregular indentation
    incorrect_indent_lines = [i+1 for i, line in enumerate(lines) if line and not line.startswith((" " * 4, "\t")) and not line.lstrip().startswith("//")]

    if incorrect_indent_lines:
        issues.append(f"Incorrect indentation found on lines: {incorrect_indent_lines[:5]}... (showing first 5)")
        score -= 5

    # Detect missing spaces around operators
    missing_spaces = re.findall(r"[^\s][=+\-*/<>!]=?[^\s]", js_code)
    if missing_spaces:
        issues.append("Missing spaces around operators (e.g., `a=1` should be `a = 1`).")
        score -= 5

    # Ensure score is within 0-15
    score = max(score, 0)

    if not issues:
        issues.append("Good formatting and indentation!")

    return {
        "score": score,
        "issues": issues
    }

import re
from collections import Counter

def analyze_js_reusability(js_code):
    issues = []
    score = 15  # Start with full score

    # Extract function bodies
    function_pattern = re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*\{([\s\S]*?)\}', re.MULTILINE)
    functions = function_pattern.findall(js_code)

    function_bodies = [func_body.strip() for _, _, func_body in functions]
    function_names = [name for name, _, _ in functions]

    # Check for duplicate function logic
    duplicate_functions = [item for item, count in Counter(function_bodies).items() if count > 1]
    if duplicate_functions:
        issues.append(f"Duplicate function logic found ({len(duplicate_functions)} occurrences). Consider reusing a single function.")
        score -= 5

    # Check for duplicate code blocks (not inside functions)
    code_lines = js_code.split("\n")
    block_counter = Counter(code_lines)
    repeated_lines = [line for line, count in block_counter.items() if count > 2 and line.strip()]

    if repeated_lines:
        issues.append(f"Repeated code detected ({len(repeated_lines)} occurrences). Consider using functions or loops for reusability.")
        score -= 5

    # Check for overly specific functions (that could be generalized)
    overly_specific_funcs = [name for name in function_names if re.search(r'getUser1|getUser2|processDataA|processDataB', name)]
    if overly_specific_funcs:
        issues.append(f"Overly specific function names found: {overly_specific_funcs}. Consider making them more general for reusability.")
        score -= 5

    # Ensure score is within 0-15
    score = max(score, 0)

    if not issues:
        issues.append("Good code reusability and adherence to DRY principles!")

    return {
        "score": score,
        "issues": issues
    }

import re

def analyze_js_best_practices(js_code):
    issues = []
    score = 20  # Start with full score

    # Check for `var` usage instead of `let` or `const`
    if re.search(r'\bvar\b', js_code):
        issues.append("Avoid using 'var'. Use 'let' or 'const' instead for better scoping.")
        score -= 5

    # Check for missing `try-catch` blocks in async functions
    if re.search(r'\basync function\b', js_code) and not re.search(r'\btry\s*\{', js_code):
        issues.append("Async functions should have proper error handling using 'try-catch'.")
        score -= 5

    # Check for direct usage of `innerHTML` (security risk)
    if re.search(r'\binnerHTML\s*=', js_code):
        issues.append("Avoid using 'innerHTML'. Use 'textContent' or 'createElement' to prevent XSS vulnerabilities.")
        score -= 5

    # Check for overly large functions (web dev best practices recommend modular functions)
    function_pattern = re.compile(r'function\s+(\w+)\s*\(.*?\)\s*\{([\s\S]*?)\}', re.MULTILINE)
    functions = function_pattern.findall(js_code)
    large_functions = [name for name, body in functions if len(body.split("\n")) > 50]

    if large_functions:
        issues.append(f"Functions {large_functions} exceed 50 lines. Consider breaking them into smaller, reusable functions.")
        score -= 5

    # Ensure score is within 0-20
    score = max(score, 0)

    if not issues:
        issues.append("Good adherence to web development best practices!")

    return {
        "score": score,
        "issues": issues
    }









