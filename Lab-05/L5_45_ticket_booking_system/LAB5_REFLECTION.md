# Lab 5 Reflection

1. **What is static code analysis?** It examines source code without running every possible input, looking for likely bugs, security risks, and code-quality issues.

2. **How do Pylint, Bandit, and Flake8 differ?** Pylint checks broad code quality and reports a score. Bandit focuses on risky security patterns. Flake8 checks style and common issues such as unused imports.

3. **What issues did the tools detect in this program?** They found a shared mutable default, a bare exception, dynamic `eval`, MD5 hashing, a predictable PIN generator, shell execution with a filename, an unused import and variable, a `None` comparison, and a long formatting line. Manual review also noticed a token-like string was hard-coded and printed.

4. **How did fixing the issues improve code quality and security?** Reservations no longer share a default list, cancellation handles unknown seats explicitly, and discount calculation no longer evaluates Python code. The program now uses SHA-256 and a cryptographically secure PIN generator, avoids shell execution, and no longer prints the token-like value. The final Pylint score is 10.00/10, and Bandit and Flake8 report no findings.

5. **What are the limitations of static analysis?** Tools can miss problems they do not recognize, and some warnings require context to judge. A clean report does not prove that every input works or that the program is secure, so tests and manual review are still important.
