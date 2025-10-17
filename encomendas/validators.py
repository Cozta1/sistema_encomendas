import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    """
    Validador que exige pelo menos 6 caracteres, 1 letra minúscula, 1 maiúscula e 1 número.
    """
    def validate(self, password, user=None):
        if len(password) < 6:
            raise ValidationError(
                "A senha deve conter pelo menos 6 caracteres.",
                code='password_too_short',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "A senha deve conter pelo menos uma letra minúscula.",
                code='password_no_lower',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "A senha deve conter pelo menos uma letra maiúscula.",
                code='password_no_upper',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                "A senha deve conter pelo menos um número.",
                code='password_no_digit',
            )

    def get_help_text(self):
        return (
            "Sua senha deve conter pelo menos 6 caracteres, "
            "incluindo pelo menos uma letra minúscula, uma maiúscula e um número."
        )