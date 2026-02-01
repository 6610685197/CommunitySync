# =========================
# Community Sync - ADMIN CLI
# =========================

# -------- DATA (mock DB) --------

residents = [
    {"unit": "12A", "name": "Somchai Prasert", "monthly_fee": 4500},
    {"unit": "8B", "name": "Nattaporn Srisuk", "monthly_fee": 4500},
    {"unit": "15C", "name": "Wichai Thongdee", "monthly_fee": 5200},
]

bills = []
maintenance_requests = []
visitors = []
announcements = []

# -------- DASHBOARD --------


def dashboard():
    print("\n--- DASHBOARD ---")
    print(f"Total Residents: {len(residents)}")
    print(f"Total Bills: {len(bills)}")
    print(f"Pending Bills: {len([b for b in bills if b['status'] == 'Pending'])}")
    print(f"Maintenance Requests: {len(maintenance_requests)}")
    print(f"Visitors Today: {len(visitors)}")
    print(f"Announcements: {len(announcements)}")


# -------- FEES / BILLING --------


def fee_menu():
    while True:
        print("\n--- ADMIN: FEES & BILLING ---")
        print("1. View Bills")
        print("2. Create Bill")
        print("3. Edit Bill")
        print("4. Delete Bill")
        print("5. Mark Bill as Paid")
        print("6. Generate Monthly Bills")
        print("0. Back")

        c = input("Choose: ")

        if c == "1":
            for b in bills:
                print(b)
        elif c == "2":
            create_bill()
        elif c == "3":
            edit_bill()
        elif c == "4":
            delete_bill()
        elif c == "5":
            mark_bill_paid()
        elif c == "6":
            generate_monthly_bills()
        elif c == "0":
            break


def create_bill():
    bill = {
        "bill_id": input("Bill ID: "),
        "unit": input("Unit: "),
        "resident": input("Resident: "),
        "amount": int(input("Amount: ")),
        "due_date": input("Due Date (YYYY-MM-DD): "),
        "status": "Pending",
    }
    bills.append(bill)
    print("Bill created")


def edit_bill():
    bid = input("Bill ID: ")
    for b in bills:
        if b["bill_id"] == bid:
            b["unit"] = input(f"Unit [{b['unit']}]: ") or b["unit"]
            b["resident"] = input(f"Resident [{b['resident']}]: ") or b["resident"]
            amt = input(f"Amount [{b['amount']}]: ")
            b["amount"] = int(amt) if amt else b["amount"]
            b["due_date"] = input(f"Due Date [{b['due_date']}]: ") or b["due_date"]
            b["status"] = input(f"Status [{b['status']}]: ") or b["status"]
            print("Bill updated")
            return
    print("Bill not found")


def delete_bill():
    bid = input("Bill ID: ")
    for i, b in enumerate(bills):
        if b["bill_id"] == bid:
            bills.pop(i)
            print("Bill deleted 🗑")
            return
    print("Bill not found")


def mark_bill_paid():
    bid = input("Bill ID: ")
    for b in bills:
        if b["bill_id"] == bid:
            b["status"] = "Paid"
            print("Marked as Paid")
            return
    print("Bill not found")


def generate_monthly_bills():
    period = input("Billing Period (YYYY-MM): ")
    due = input("Due Date (YYYY-MM-DD): ")

    for r in residents:
        bills.append(
            {
                "bill_id": f"BILL-{period}-{r['unit']}",
                "unit": r["unit"],
                "resident": r["name"],
                "amount": r["monthly_fee"],
                "due_date": due,
                "status": "Pending",
            }
        )
    print("Monthly bills generated")


# -------- MAINTENANCE --------


def maintenance_menu():
    while True:
        print("\n--- ADMIN: MAINTENANCE ---")
        print("1. View Requests")
        print("2. Create Request")
        print("3. Edit Request")
        print("4. Delete Request")
        print("0. Back")

        c = input("Choose: ")

        if c == "1":
            for m in maintenance_requests:
                print(m)
        elif c == "2":
            maintenance_requests.append(
                {
                    "id": input("Request ID: "),
                    "unit": input("Unit: "),
                    "issue": input("Issue: "),
                    "priority": input("Priority (Low/Medium/High): "),
                    "status": "Pending",
                }
            )
            print("Request created")
        elif c == "3":
            edit_maintenance()
        elif c == "4":
            delete_item(maintenance_requests, "id")
        elif c == "0":
            break


def edit_maintenance():
    mid = input("Request ID: ")
    for m in maintenance_requests:
        if m["id"] == mid:
            m["unit"] = input(f"Unit [{m['unit']}]: ") or m["unit"]
            m["issue"] = input(f"Issue [{m['issue']}]: ") or m["issue"]
            m["priority"] = input(f"Priority [{m['priority']}]: ") or m["priority"]
            m["status"] = input(f"Status [{m['status']}]: ") or m["status"]
            print("Request updated")
            return
    print("Not found")


# -------- VISITORS --------


def visitor_menu():
    while True:
        print("\n--- ADMIN: VISITORS ---")
        print("1. View Visitors")
        print("2. Add Visitor")
        print("3. Edit Visitor")
        print("4. Delete Visitor")
        print("0. Back")

        c = input("Choose: ")

        if c == "1":
            for v in visitors:
                print(v)
        elif c == "2":
            visitors.append(
                {
                    "name": input("Name: "),
                    "unit": input("Unit: "),
                    "vehicle": input("Vehicle Plate: "),
                    "status": input("Status (Pending/Checked In/Denied): "),
                }
            )
            print("Visitor added")
        elif c == "3":
            edit_visitor()
        elif c == "4":
            delete_item(visitors, "name")
        elif c == "0":
            break


def edit_visitor():
    name = input("Visitor Name: ")
    for v in visitors:
        if v["name"] == name:
            v["unit"] = input(f"Unit [{v['unit']}]: ") or v["unit"]
            v["vehicle"] = input(f"Vehicle [{v['vehicle']}]: ") or v["vehicle"]
            v["status"] = input(f"Status [{v['status']}]: ") or v["status"]
            print("Visitor updated")
            return
    print("Not found")


# -------- ANNOUNCEMENTS --------


def announcement_menu():
    while True:
        print("\n--- ADMIN: ANNOUNCEMENTS ---")
        print("1. View Announcements")
        print("2. Create Announcement")
        print("3. Edit Announcement")
        print("4. Delete Announcement")
        print("0. Back")

        c = input("Choose: ")

        if c == "1":
            for a in announcements:
                print(a)
        elif c == "2":
            announcements.append(
                {
                    "title": input("Title: "),
                    "content": input("Content: "),
                    "status": input("Status (Draft/Published): "),
                }
            )
            print("Announcement created 📢")
        elif c == "3":
            edit_announcement()
        elif c == "4":
            delete_item(announcements, "title")
        elif c == "0":
            break


def edit_announcement():
    title = input("Title: ")
    for a in announcements:
        if a["title"] == title:
            a["content"] = input("New Content: ") or a["content"]
            a["status"] = input(f"Status [{a['status']}]: ") or a["status"]
            print("Announcement updated")
            return
    print("Not found")


# -------- UTIL --------


def delete_item(items, key):
    value = input(f"{key} to delete: ")
    for i, item in enumerate(items):
        if item[key] == value:
            items.pop(i)
            print("Deleted 🗑")
            return
    print("Not found ")


# -------- MAIN --------


def main():
    while True:
        print("\n=== COMMUNITY SYNC : ADMIN CLI ===")
        print("1. Dashboard")
        print("2. Fees & Billing")
        print("3. Maintenance")
        print("4. Visitors")
        print("5. Announcements")
        print("0. Exit")

        c = input("Select: ")

        if c == "1":
            dashboard()
        elif c == "2":
            fee_menu()
        elif c == "3":
            maintenance_menu()
        elif c == "4":
            visitor_menu()
        elif c == "5":
            announcement_menu()
        elif c == "0":
            print("Goodbye")
            break


if __name__ == "__main__":
    main()
