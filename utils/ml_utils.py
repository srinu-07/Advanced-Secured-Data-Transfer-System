def is_key_strong(key):
    return (
        len(key) >= 32 and
        any(c.isupper() for c in key) and
        any(c.islower() for c in key) and
        any(c.isdigit() for c in key)
    )

def get_strength_label(key):
    if is_key_strong(key):
        return "Strong"
    return "Weak"