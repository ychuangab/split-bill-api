from .models import Participant, Balance, Settlement


def calculate_balances(participants: list[Participant]) -> tuple[float, float, list[Balance]]:
    """計算 total、per_person_share 與每人 balance（正=應收，負=欠款）。"""
    total = sum(p.paid for p in participants)
    share = total / len(participants)
    balances = [
        Balance(name=p.name, balance=round(p.paid - share, 10))
        for p in participants
    ]
    return round(total, 2), round(share, 2), balances


def calculate_settlements(balances: list[Balance]) -> list[Settlement]:
    """Greedy two-pointer：最少筆數清算轉帳清單。"""
    debtors = sorted(
        [(b.name, -b.balance) for b in balances if b.balance < -1e-9],
        key=lambda x: x[1],
        reverse=True,
    )
    creditors = sorted(
        [(b.name, b.balance) for b in balances if b.balance > 1e-9],
        key=lambda x: x[1],
        reverse=True,
    )

    settlements: list[Settlement] = []
    i, j = 0, 0
    debtors = list(debtors)
    creditors = list(creditors)

    while i < len(debtors) and j < len(creditors):
        debtor_name, debt = debtors[i]
        creditor_name, credit = creditors[j]

        amount = min(debt, credit)
        settlements.append(
            Settlement(from_=debtor_name, to=creditor_name, amount=round(amount, 2))
        )

        debt -= amount
        credit -= amount

        if debt < 1e-9:
            i += 1
        else:
            debtors[i] = (debtor_name, debt)

        if credit < 1e-9:
            j += 1
        else:
            creditors[j] = (creditor_name, credit)

    return settlements
