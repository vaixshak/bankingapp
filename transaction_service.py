from models import User, Transaction
from extensions import db

def perform_transaction(user_id, amount, txn_type):
    """
    Handles credit or debit transactions for a user and records them.
    """
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    if txn_type == "credit":
        user.balance += amount
    elif txn_type == "debit":
        if user.balance < amount:
            return {"error": "Insufficient balance"}, 400
        user.balance -= amount
    else:
        return {"error": "Invalid transaction type"}, 400

    # Record the transaction
    txn_record = Transaction(user_id=user_id, amount=amount, txn_type=txn_type, balance_after=user.balance)
    db.session.add(txn_record)
    db.session.commit()
   

    return {"message": f"Transaction successful. New balance: {user.balance}"}, 200


