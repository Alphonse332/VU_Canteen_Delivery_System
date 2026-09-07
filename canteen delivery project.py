import json
import os

ORDER_LOG_FILE = "vu_canteen_orders.json"
CAMPUS_RIDERS = ["Okello Peter", "Namubiru Joan", "Mukasa Derrick", "Atwine Brian"]

def load_records():
    if not os.path.exists(ORDER_LOG_FILE):
        return {}
    try:
        with open(ORDER_LOG_FILE, 'r') as file:
            return json.load(file)
    except:
        return {}

def save_records(data):
    try:
        with open(ORDER_LOG_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except:
        print("[WARNING] Could not update persistent storage file layer.")

def get_clean_quantity(prompt_text):
    while True:
        entry = input(prompt_text).strip()
        if entry.isdigit() and int(entry) > 0:
            return int(entry)
        print("[ERROR] Formatting syntax error: Whole numeric integers only.")

def process_new_order(orders_dict):
    print("\n================== CAMPUS DIGITAL CANTEEN MENU ==================")
    print("  [1] Luwombo (Chicken/Beef) with Matooke      UGX 15,000")
    print("  [2] Katogo (Offals & Matooke)                UGX 7,000")
    print("  [3] VU Special Fried Rice with Chicken       UGX 12,000")
    print("  [4] Stoney Ginger Beer (350ml)               UGX 2,500")
    print("  [5] African Ginger Tea (Pot)                 UGX 4,000")
    print("  [6] Fresh Passion Fruit Juice                UGX 3,500")
    print("  [7] Rolex (2 Eggs, 2 Chapatis)               UGX 4,000")
    print("  [8] Samosa (Beef/Vegetable - Pair)           UGX 3,000")
    print("  [9] Gonja (Roasted Plantain)                 UGX 3,000")
    print("=================================================================")
    
    basket = []
    prices_map = {"1": 15000, "2": 7000, "3": 12000, "4": 2500, "5": 4000, "6": 3500, "7": 4000, "8": 3000, "9": 3000}
    names_map = {"1": "Luwombo with Matooke", "2": "Katogo", "3": "VU Special Fried Rice", "4": "Stoney Ginger Beer", "5": "African Ginger Tea", "6": "Fresh Passion Fruit Juice", "7": "Rolex", "8": "Samosa", "9": "Gonja"}

    while True:
        selection = input("\nEnter Target Item ID key (or type 'D' when complete): ").strip()
        if selection.upper() == 'D':
            break
        if selection not in prices_map:
            print("[ERROR] Selection mapping mismatch: Input key does not match menu profiles.")
            continue
        
        item_price = prices_map[selection]
        item_name = names_map[selection]
        qty = get_clean_quantity(f"Identify desired quantity portions for '{item_name}': ")
        
        basket.append({"title": item_name, "rate": item_price, "volume": qty})
        print(f"[ADDED] Portioned item collection verified: {qty}x {item_name}")

    if len(basket) == 0:
        print("[INFO] Transaction cycle abandoned: Empty baskets cannot register tracking logs.")
        return orders_dict

    cart_subtotal = sum(row["rate"] * row["volume"] for row in basket)

    print("\n📍 Identify Target Destination Campus Sector Area:")
    print("  [1] Main Campus / Main Hall       (Base Fee: UGX 1,500)")
    print("  [2] Science & IT Labs Block       (Base Fee: UGX 2,500)")
    print("  [3] Hostels & External Annexes    (Base Fee: UGX 4,000)")
    
    zone_choice = input("Enter sector option mapping coordinate code (1-3): ").strip()
    
    dropzone = "General Campus Sector Ground"
    shipping_tariff = 2000
    if zone_choice == "1":
        dropzone = "Main Campus / Main Hall"
        shipping_tariff = 1500
    elif zone_choice == "2":
        dropzone = "Science & IT Labs Block"
        shipping_tariff = 2500
    elif zone_choice == "3":
        dropzone = "Hostels & External Annexes"
        shipping_tariff = 4000

    if cart_subtotal >= 40000:
        print("[PROMO] High-Value balance rule verified: Subtotal breaks UGX 40,000! Shipping fee waived.")
        shipping_tariff = 0

    invoice_sum = cart_subtotal + shipping_tariff
    assigned_uid = f"VU-{1000 + len(orders_dict) + 1}"
    assigned_courier = CAMPUS_RIDERS[len(orders_dict) % len(CAMPUS_RIDERS)]

    orders_dict[assigned_uid] = {
        "basket": basket,
        "subtotal": cart_subtotal,
        "shipping": shipping_tariff,
        "total": invoice_sum,
        "destination": dropzone,
        "rider": assigned_courier,
        "status": "Pending"
    }

    save_records(orders_dict)
    print(f"\n[SUCCESS] Document transaction recorded: Reference Index Code [{assigned_uid}]")
    print(f"   Invoice Sum: UGX {invoice_sum:,} | Dispatched Courier: {assigned_courier}")
    return orders_dict

def modify_order_lifecycle(orders_dict):
    target_uid = input("\nEnter Order UID reference code to alter (e.g., VU-1001): ").strip().upper()
    if target_uid not in orders_dict:
        print("[ERROR] Search trace failure: UID missing from active transaction paths.")
        return orders_dict

    active_file = orders_dict[target_uid]
    current_milestone = active_file["status"]
    print(f"Order File {target_uid} Tracked State: [{current_milestone}] | Agent: {active_file['rider']}")

    if current_milestone == "Delivered":
        print("[INFO] Lifecycle loop complete: Terminal order documents cannot be mutated further.")
        return orders_dict

    print("\nIdentify workflow advancement path target execution:")
    if current_milestone == "Pending":
        print("  Transition courier assignment deployment ('Out for Delivery')")
    elif current_milestone == "Out for Delivery":
        print("  Validate destination customer confirmation ('Delivered')")
    print("  [Any Other Key] Keep existing workspace tracking configuration position")
    
    command_action = input("Enter operation code: ").strip()

    if command_action == "1" and current_milestone == "Pending":
        active_file["status"] = "Out for Delivery"
        print(f"[SUCCESS] State change validated: Order {target_uid} moved to [Out for Delivery].")
    elif command_action == "1" and current_milestone == "Out for Delivery":
        active_file["status"] = "Delivered"
        print(f"[SUCCESS] State change validated: Order {target_uid} closed cleanly as [Delivered].")
    else:
        print("[INFO] Request execution canceled: State values preserved unchanged.")
        return orders_dict

    save_records(orders_dict)
    return orders_dict

def extract_sales_analytics(orders_dict):
    print("\n==============================================================")
    print("    VICTORIA UNIVERSITY CANTEEN ANALYTICS & REVENUE SUMMARY   ")
    print("==============================================================")
    
    cumulative_revenue = 0
    queues = {"Pending": 0, "Out for Delivery": 0, "Delivered": 0}
    sku_counts = {}

    for profile in orders_dict.values():
        flag = profile["status"]
        queues[flag] = queues.get(flag, 0) + 1
        if flag == "Delivered":
            cumulative_revenue += profile["total"]
        for line in profile["basket"]:
            title = line["title"]
            volume = line["volume"]
            sku_counts[title] = sku_counts.get(title, 0) + volume

    highest_velocity_sku = "No closed dataset entries tracked"
    if len(sku_counts) > 0:
        champion_title = max(sku_counts, key=sku_counts.get)
        highest_velocity_sku = f"{champion_title} ({sku_counts[champion_title]} units itemized)"

    print(f"Total Confirmed Earnings: UGX {cumulative_revenue:,}")
    print(f"Top Velocity Canteen SKU: {highest_velocity_sku}")
    print("\nLogistics Queue Tracking Metrics:")
    for stage, volume in queues.items():
        print(f"  - Active Status '{stage:<18}' Ledger Size: {volume} units")
    print("==============================================================")

def compile_live_grid(orders_dict):
    if len(orders_dict) == 0:
        print("\n[INFO] Diagnostic Monitor: System operational memory queues currently empty.")
        return
    print("\n============================================ LOGISTICS SYSTEM TRACE LEDGER MONITOR ============================================")
    print(f"{'Order UID':<11} {'Campus Landmark Sector Location':<35} {'Grand Invoice':<18} {'Assigned Dispatcher':<22} {'Current Status'}")
    print("-" * 120)
    for uid, layer in orders_dict.items():
        print(f"{uid:<11} {layer['destination']:<35} UGX {layer['total']:<14,} {layer['rider']:<22} [{layer['status']}]")
    print("===============================================================================================================================")

def main():
    orders_master = load_records()
    while True:
        print("\n==================================================")
        print("     VICTORIA UNIVERSITY CANTEEN DELIVERY HUB     ")
        print("==================================================")
        print("  1. Compile New Digital Delivery Order")
        print("  2. Advance Order Pipeline Delivery Stage")
        print("  3. Display Financial Ledger Sales Reports")
        print("  4. View All Logged System Active Orders")
        print("  5. Shutdown Application Workspace Securely")
        print("==================================================")
        
        user_selection = input("Select operation interface execution code (1-5): ").strip()
        if user_selection == "1":
            orders_master = process_new_order(orders_master)
        elif user_selection == "2":
            orders_master = modify_order_lifecycle(orders_master)
        elif user_selection == "3":
            extract_sales_analytics(orders_master)
        elif user_selection == "4":
            compile_live_grid(orders_master)
        elif user_selection == "5":
            print("\n[INFO] Runtime instances cached safely. Group project workspace closed cleanly.")
            break
        else:
            print("\n[ERROR] Selection coordinate error: Input index out of bounds (1-5).")

if __name__ == "__main__":
    main()
