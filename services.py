from crud import get_counterparty


def valid_counterparty(counterparty_number: int) -> bool:
    """Проверяет наличие контрагента в базе данных."""
    if get_counterparty(counterparty_number):
        return True
    return False
