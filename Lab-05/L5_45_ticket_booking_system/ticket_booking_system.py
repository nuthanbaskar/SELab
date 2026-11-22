"""Movie theater ticket booking and seating management module."""

import hashlib
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat and optionally record the order."""
    if order_history is None:
        order_history = []
    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False
    theater_seats[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a reservation if the requested seat exists."""
    if seat_id in theater_seats:
        theater_seats[seat_id]["is_sold"] = False


def check_seat_status(seat_id):
    """Return whether a seat exists and is not sold."""
    if theater_seats.get(seat_id) is None:
        return False
    return not theater_seats[seat_id]["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Calculate a promotional price using a discount rate from zero to one."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_price = theater_seats[seat_id]["price"]
    return base_price * (1 - discount_rate)


def generate_ticket_hash(ticket_code):
    """Return a hash for a ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Generate a four-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the theater seating chart to a file."""
    with open(filename, "w", encoding="utf-8") as seating_chart:
        seating_chart.write(str(theater_seats))
    print(f"Seating chart exported to: {filename}")


def get_theater_summary(seats):
    """Return the number of sold seats in the supplied theater."""
    return sum(seat["is_sold"] for seat in seats.values())


def main():
    """Run a sample ticket booking workflow."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))


if __name__ == "__main__":
    main()
