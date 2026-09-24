assert is_terminal(TicketState.OPEN) is False, (
    "is_terminal(TicketState.OPEN) should be False"
)
assert is_terminal(TicketState.CLOSED) is True, (
    "is_terminal(TicketState.CLOSED) should be True"
)
assert is_terminal(TicketState.CANCELLED) is True, (
    "is_terminal(TicketState.CANCELLED) should be True"
)
print("enums5 ok")
