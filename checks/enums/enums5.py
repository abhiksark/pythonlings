assert is_terminal(TicketState.OPEN) is False, "OPEN should not be terminal"
assert is_terminal(TicketState.CLOSED) is True, "CLOSED should be terminal"
assert is_terminal(TicketState.CANCELLED) is True, "CANCELLED should be terminal"
print("enums5 ok")
