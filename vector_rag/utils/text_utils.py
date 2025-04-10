def validate_context(context):
    """
    Validates the context to ensure it's not empty.
    """
    if not context.strip():
        raise ValueError("The context provided is empty. Please provide valid input.")
    return context
