# Static Analysis Findings

## Purpose

Static code analysis checks source code for likely defects, unsafe patterns, and style problems without requiring a test to exercise every affected path. It helps find issues early, but its results still need human review.

## Original execution

Before editing the program, it completed successfully (exit code 0). It reported that seat B1 was available, calculated a promotional price of 16.0, generated an MD5 ticket hash and a four-digit PIN (6625 on this run), and counted one sold seat. It also wrote `seating_chart.txt` and printed the token-like value noted below. The run was performed in a temporary directory so the generated chart did not alter the project.

## Tool differences

- **Pylint** checks a broad set of code-quality and correctness conventions, including naming, unused variables, risky defaults, and documentation. It also reports a score.
- **Bandit** searches Python source for security-sensitive patterns such as dynamic evaluation, weak hashes, predictable random values, and shell execution.
- **Flake8** combines style checks with checks for common Python mistakes such as unused imports and variables.

## Findings and fixes

| Issue | Type | Tool | Original line number | Description | Fix applied | Verification result |
|---|---|---|---:|---|---|---|
| Shared mutable default | Potential bug | Pylint | 15 | The default list could be reused across calls, unexpectedly carrying order history between reservations. | Changed the default to `None` and create a fresh list when one is not supplied. | Caller-provided history was recorded; default is `None`; reservation checks passed. |
| Bare exception and ignored errors | Error handling / security | Pylint, Bandit (B110), Flake8 | 26 | A bare `except` hid every exception and did nothing, making failures hard to detect. | Check whether the seat exists before changing its state. | Cancelling an unknown seat safely leaves the seat data unchanged. |
| Dynamic expression evaluation | Security | Pylint, Bandit (B307) | 42 | `eval` could execute arbitrary Python instead of only calculating a discount. | Accept a numeric discount rate, validate it is between 0 and 1, and calculate the price directly. | A 20% discount on the premium seat returns 16.0; an out-of-range rate raises `ValueError`; Bandit reports no issues. |
| Weak ticket hash | Security | Bandit (B324) | 47 | MD5 is no longer appropriate for a security-sensitive hash. | Use SHA-256. | The resulting hash is 64 hexadecimal characters; Bandit reports no issues. |
| Predictable booking PIN | Security | Bandit (B311) | 51 | `random.randint` is not intended for security-sensitive values such as booking PINs. | Generate the four-digit PIN using `secrets.randbelow`. | 500 generated PINs were all in the inclusive range 1000-9999; Bandit reports no issues. |
| Shell command with a filename | Security | Bandit (B605) | 58 | Passing a filename to `os.system` could allow shell interpretation of special characters. | Removed the shell command and print the confirmation directly from Python. | Export with `&` in the filename created only the requested file and printed the literal filename; Bandit reports no issues. |
| Unused `math` import | Code quality | Pylint, Flake8 (F401) | 6 | The module was imported but never used. | Removed the import. | Final Pylint and Flake8 reports are clean. |
| Unused fee and `None` comparison | Code quality | Pylint, Flake8 (F841, E711) | 31-32 | The fee value was unused, and the seat lookup compared against `None` with `==`. | Removed the unused variable and use `is None`. | Final Pylint and Flake8 reports are clean. |
| Long string formatting | Style | Pylint, Flake8 (E501) | 19 | Percent-formatting made the reservation log line longer than the configured Flake8 limit. | Use an f-string. | Final Flake8 report is empty. |

### Manual security review

The original program also contained a token-like hard-coded value at line 70 and printed it at line 79. Bandit did not report it, and the value was not verified as a real credential. Since the sample program did not need it, the constant and its output were removed rather than treating it as a valid secret.

## Scores and remaining warnings

- Initial Pylint score: **5.37/10**
- Final Pylint score: **10.00/10**
- Final Bandit run: **No issues identified** (zero findings)
- Final Flake8 run: **No output** (zero findings)
- Remaining actionable warnings: **None**

The original Bandit report included five findings: B110, B307, B324, B311, and B605. Each was resolved without suppressing a check. Static analysis cannot prove the program is free of every defect; its checks are pattern-based and should be combined with tests and manual review.

## Reports

- Baseline: `reports/before/pylint_report.txt`, `reports/before/bandit_report.txt`, and `reports/before/flake8_report.txt`
- Final: `reports/after/pylint_report.txt`, `reports/after/bandit_report.txt`, and `reports/after/flake8_report.txt`
