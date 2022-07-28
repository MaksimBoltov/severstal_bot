from database import session
from models import Counterparties


def get_counterparty(counterparty_id: int) -> Counterparties:
    """"""
    counterparty = session.query(Counterparties).filter(Counterparties.id == counterparty_id).first()
    return counterparty
