# =====================================================================@000000=
# This is a template for a new problem part. To create a new part, delete
# the template and fill in your content.
#
# Define a function `multiply(x, y)` that returns the product of `x` and `y`.
# For example:
#
#     >>> multiply(3, 7)
#     21
#     >>> multiply(6, 7)
#     42
# =============================================================================

def multiply(x, y):
    return x * y

Check.part()
Check.equal('multiply(3, 7)', 21) and Check.equal('multiply(6, 7)', 42)
Check.equal('multiply(10, 10)', 100) and Check.equal('multiply(11, 10)', 110)
Check.secret(multiply(100, 100))
Check.secret(multiply(500, 123))
