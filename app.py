import streamlit as st
from bank import Bank
from ai_talker import ask_ai
import json
from datetime import datetime
import io

st.set_page_config(page_title="Dhrumil's Bank", layout="wide")

bg_color = "#0e1117"
text_color = "white"
button_bg = "#1f2937"
button_text = "white"

st.markdown(f"""
    <style>
    body, .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    .stButton>button {{
        background-color: {button_bg};
        color: {button_text};
    }}
    .transaction-receipt {{
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        border: 2px solid #4CAF50;
    }}
    .success-message {{
        color: #4CAF50;
        font-weight: bold;
    }}
    .error-message {{
        color: #ff6b6b;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ---------------- #
def generate_receipt(transaction_type, amount, account_no, balance_before, balance_after, to_account=None, recipient_name=None):
    """Generate a receipt for transactions"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_id = f"{timestamp.replace(' ', '').replace('-', '').replace(':', '')}{account_no}"
    
    receipt = f"""
═══════════════════════════════════════
        DHRUMIL'S BANK - RECEIPT
═══════════════════════════════════════

Transaction Type: {transaction_type.upper()}
Date & Time: {timestamp}
Account Number: {account_no}
Amount: ₹{amount:,.2f}

Balance Before: ₹{balance_before:,.2f}
Balance After: ₹{balance_after:,.2f}
"""
    
    if to_account and recipient_name:
        receipt += f"\nTransferred To: {to_account} ({recipient_name})"
    elif to_account:
        receipt += f"\nTransferred To: {to_account}"
    
    receipt += f"""

Transaction ID: {transaction_id}
Status: COMPLETED ✓

═══════════════════════════════════════
Thank you for banking with Dhrumil's Bank
═══════════════════════════════════════
"""
    return receipt

def find_user_by_account(account_no):
    """Find user by account number"""
    return Bank.find_user_by_account(account_no)

def update_user_in_database(user):
    """Update user data in the database"""
    for i, existing_user in enumerate(Bank.data):
        if existing_user["account_no"] == user["account_no"]:
            Bank.data[i] = user
            break
    with open(Bank.database, "w") as f:
        json.dump(Bank.data, f, indent=4)

def validate_account_number(account_no_str):
    """Validate account number format"""
    if not account_no_str:
        return False, "Account number cannot be empty"
    
    if len(account_no_str) != 7:
        return False, "Account number must be 7 characters long"
    
    return True, "Valid"

# ---------------- LOGIN STATE ---------------- #
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "last_transaction" not in st.session_state:
    st.session_state.last_transaction = None

def login_form():
    st.subheader("🔑 Login to Your Account")
    
    with st.form("login_form"):
        acc = st.text_input("Account Number", placeholder="Enter your 7-character account number")
        pin = st.text_input("PIN", type="password", placeholder="Enter your 4-digit PIN")
        submitted = st.form_submit_button("🚀 Login")
        
        if submitted:
            if not acc:
                st.error("❌ Please enter your account number")
            elif not pin:
                st.error("❌ Please enter your PIN")
            elif not pin.isdigit():
                st.error("❌ PIN must be numeric")
            else:
                user = Bank.login(acc, int(pin))
                if user:
                    st.session_state.logged_in_user = user
                    st.success(f"✅ Welcome back, {user['name']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid account number or PIN. Please try again.")

# ---------------- SIDEBAR MENU ---------------- #
if st.session_state.logged_in_user:
    with st.sidebar:
        st.image("https://img.icons8.com/external-flaticons-flat-flat-icons/64/external-bank-100-most-used-icons-flaticons-flat-flat-icons.png", width=60)
        st.markdown(f"**Welcome, {st.session_state.logged_in_user['name']}!**")
        st.markdown(f"**Balance: ₹{st.session_state.logged_in_user['balance']:,.2f}**")
        st.markdown("---")
        
    menu = st.sidebar.selectbox(
        "🏦 Banking Services",
        ["🏠 Dashboard", "📊 Account Details", "💰 Deposit Money", "💸 Withdraw Money", "🔄 Transfer Money", "✏️ Update Profile", "🗑️ Delete Account", "🚪 Logout"]
    )
else:
    menu = st.sidebar.selectbox(
        "🏦 Banking Services",
        ["🆕 Create Account", "🔑 Login"]
    )

# ---------------- CHATBOT ---------------- #
if "chatbot_open" not in st.session_state:
    st.session_state.chatbot_open = False

# Chatbot toggle in top-right corner
col1, col2 = st.columns([0.85, 0.15])
with col2:
    if st.button("💬 Ask Nishu", key="chat_toggle", help="Click to toggle AI Assistant"):
        st.session_state.chatbot_open = not st.session_state.chatbot_open

if st.session_state.chatbot_open:
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader("🤖 Nishu - Your AI Banking Assistant")
        question = st.text_area("💭 Ask me anything about banking or your account:", 
                                placeholder="e.g., How can I transfer money? What are the withdrawal limits?")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📤 Send", key="send_chat"):
                if question.strip():
                    with st.spinner("🤔 Nishu is thinking..."):
                        answer = ask_ai(question)
                        st.markdown("**🤖 Nishu's Response:**")
                        st.info(answer)
                else:
                    st.warning("Please enter a question first!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- BANK FUNCTIONS ---------------- #
bank = Bank()

# Main title
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #4CAF50; font-size: 3rem; margin-bottom: 0;'>🏦 Dhrumil's Bank</h1>
    <p style='color: #888; font-size: 1.2rem;'>Your Trusted Digital Banking Partner</p>
</div>
""", unsafe_allow_html=True)

if menu == "🆕 Create Account" and not st.session_state.logged_in_user:
    st.subheader("🆕 Create Your New Account")
    st.markdown("Join thousands of satisfied customers!")
    
    with st.form("create_account_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            age = st.number_input("🎂 Age", min_value=18, max_value=100, step=1, value=18)
            phone = st.text_input("📱 Phone Number", placeholder="10-digit mobile number")
        
        with col2:
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            pin = st.text_input("🔐 PIN (4 digits)", type="password", placeholder="Create a 4-digit PIN")
            confirm_pin = st.text_input("🔐 Confirm PIN", type="password", placeholder="Re-enter your PIN")
        
        terms = st.checkbox("I agree to the Terms and Conditions")
        submitted = st.form_submit_button("🎉 Create My Account")
        
        if submitted:
            if not all([name, phone, email, pin]):
                st.error("❌ Please fill all required fields")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("❌ PIN must be exactly 4 digits")
            elif pin != confirm_pin:
                st.error("❌ PINs do not match")
            elif len(phone) != 10 or not phone.isdigit():
                st.error("❌ Phone number must be 10 digits")
            elif not terms:
                st.error("❌ Please accept the Terms and Conditions")
            else:
                try:
                    new_account = {
                        "name": name,
                        "age": int(age),
                        "phone_number": int(phone),
                        "email": email,
                        "pin": int(pin),
                        "account_no": bank._Bank__accnumgen(),
                        "balance": 0
                    }
                    Bank.data.append(new_account)
                    with open(Bank.database, "w") as f:
                        json.dump(Bank.data, f, indent=4)
                    
                    st.success("🎉 Account created successfully!")
                    st.balloons()
                    
                    # Display account details in a nice format
                    st.markdown("### 📋 Your Account Details")
                    st.info(f"""
                    **🎯 Account Number:** `{new_account['account_no']}`  
                    **👤 Name:** {new_account['name']}  
                    **📧 Email:** {new_account['email']}  
                    **💰 Initial Balance:** ₹0.00
                    
                    ⚠️ **Important:** Please save your account number safely!
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Error creating account: {e}")

elif menu == "🔑 Login" and not st.session_state.logged_in_user:
    login_form()

elif menu == "🏠 Dashboard" and st.session_state.logged_in_user:
    user = st.session_state.logged_in_user
    
    # Account overview cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; color: white;'>
            <h3>💰 Current Balance</h3>
            <h2>₹{user['balance']:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; color: white;'>
            <h3>🏦 Account Number</h3>
            <h2>{user['account_no']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; color: white;'>
            <h3>👤 Account Holder</h3>
            <h2>{user['name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Deposit Money", key="quick_deposit"):
            st.session_state.quick_action = "deposit"
    
    with col2:
        if st.button("💸 Withdraw Money", key="quick_withdraw"):
            st.session_state.quick_action = "withdraw"
    
    with col3:
        if st.button("🔄 Transfer Money", key="quick_transfer"):
            st.session_state.quick_action = "transfer"

elif menu == "📊 Account Details" and st.session_state.logged_in_user:
    st.subheader("📊 Your Account Information")
    
    user = st.session_state.logged_in_user
    
    # Display account details in a formatted way
    st.markdown(f"""
    <div style='background: #1e1e1e; padding: 25px; border-radius: 15px; border-left: 5px solid #4CAF50;'>
    <h3 style='color: #4CAF50; margin-bottom: 20px;'>Account Information</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
        <div>
            <strong>👤 Account Holder:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>{user['name']}</span>
        </div>
        <div>
            <strong>🏦 Account Number:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>{user['account_no']}</span>
        </div>
        <div>
            <strong>🎂 Age:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>{user['age']} years</span>
        </div>
        <div>
            <strong>💰 Current Balance:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>₹{user['balance']:,.2f}</span>
        </div>
        <div>
            <strong>📱 Phone Number:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>{user['phone_number']}</span>
        </div>
        <div>
            <strong>📧 Email Address:</strong><br>
            <span style='color: #4CAF50; font-size: 1.1em;'>{user['email']}</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

elif menu == "💰 Deposit Money" and st.session_state.logged_in_user:
    st.subheader("💰 Deposit Money to Your Account")
    
    # Initialize deposit success flag
    if "deposit_success" not in st.session_state:
        st.session_state.deposit_success = False
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Current Balance:** ₹{st.session_state.logged_in_user['balance']:,.2f}")
        
        with st.form("deposit_form"):
            amount = st.number_input("💵 Deposit Amount (₹)", min_value=1, max_value=10000, step=1)
            st.markdown("*Minimum: ₹1 | Maximum: ₹10,000*")
            submitted = st.form_submit_button("💰 Deposit Now")
            
            if submitted:
                balance_before = st.session_state.logged_in_user["balance"]
                st.session_state.logged_in_user["balance"] += amount
                balance_after = st.session_state.logged_in_user["balance"]
                
                update_user_in_database(st.session_state.logged_in_user)
                
                # Generate receipt
                receipt = generate_receipt("Deposit", amount, 
                                         st.session_state.logged_in_user["account_no"],
                                         balance_before, balance_after)
                st.session_state.last_transaction = receipt
                st.session_state.deposit_success = True
                
                st.success(f"🎉 Successfully deposited ₹{amount:,.2f}!")
                st.balloons()
                
                # Show updated balance
                st.info(f"**New Balance:** ₹{balance_after:,.2f}")
        
        # Download button outside the form
        if st.session_state.deposit_success and st.session_state.last_transaction:
            st.download_button(
                label="📥 Download Receipt",
                data=st.session_state.last_transaction,
                file_name=f"deposit_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="deposit_receipt"
            )
            if st.button("✅ Transaction Complete", key="complete_deposit"):
                st.session_state.deposit_success = False
    
    with col2:
        st.markdown("### 💡 Tips")
        st.info("""
        **Deposit Guidelines:**
        - Minimum deposit: ₹1
        - Maximum deposit: ₹10,000
        - Instant processing
        - Receipt available immediately
        """)

elif menu == "💸 Withdraw Money" and st.session_state.logged_in_user:
    st.subheader("💸 Withdraw Money from Your Account")
    
    # Initialize withdraw success flag
    if "withdraw_success" not in st.session_state:
        st.session_state.withdraw_success = False
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_balance = st.session_state.logged_in_user["balance"]
        st.markdown(f"**Current Balance:** ₹{current_balance:,.2f}")
        
        with st.form("withdraw_form"):
            max_withdraw = min(current_balance, 10000)
            amount = st.number_input(f"💸 Withdrawal Amount (₹)", 
                                   min_value=1, 
                                   max_value=max_withdraw if max_withdraw > 0 else 1, 
                                   step=1)
            st.markdown(f"*Available for withdrawal: ₹{max_withdraw:,.2f}*")
            submitted = st.form_submit_button("💸 Withdraw Now")
            
            if submitted:
                if current_balance < amount:
                    st.error("⚠️ Insufficient balance for this withdrawal!")
                else:
                    balance_before = st.session_state.logged_in_user["balance"]
                    st.session_state.logged_in_user["balance"] -= amount
                    balance_after = st.session_state.logged_in_user["balance"]
                    
                    update_user_in_database(st.session_state.logged_in_user)
                    
                    # Generate receipt
                    receipt = generate_receipt("Withdrawal", amount,
                                             st.session_state.logged_in_user["account_no"],
                                             balance_before, balance_after)
                    st.session_state.last_transaction = receipt
                    st.session_state.withdraw_success = True
                    
                    st.success(f"✅ Successfully withdrawn ₹{amount:,.2f}!")
                    st.info(f"**Remaining Balance:** ₹{balance_after:,.2f}")
        
        # Download button outside the form
        if st.session_state.withdraw_success and st.session_state.last_transaction:
            st.download_button(
                label="📥 Download Receipt",
                data=st.session_state.last_transaction,
                file_name=f"withdrawal_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="withdraw_receipt"
            )
            if st.button("✅ Transaction Complete", key="complete_withdraw"):
                st.session_state.withdraw_success = False
    
    with col2:
        st.markdown("### 💡 Tips")
        st.info("""
        **Withdrawal Guidelines:**
        - Check available balance
        - Maximum per transaction: ₹10,000
        - Instant processing
        - Receipt generated automatically
        """)

elif menu == "🔄 Transfer Money" and st.session_state.logged_in_user:
    st.subheader("🔄 Transfer Money to Another Account")
    
    current_balance = st.session_state.logged_in_user["balance"]
    st.markdown(f"**Your Balance:** ₹{current_balance:,.2f}")
    
    # Initialize transfer success flag
    if "transfer_success" not in st.session_state:
        st.session_state.transfer_success = False
    
    with st.form("transfer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            to_account = st.text_input("🏦 Recipient Account Number", 
                                     placeholder="Enter 7-character account number")
            amount = st.number_input("💰 Transfer Amount (₹)", 
                                   min_value=1, 
                                   max_value=min(current_balance, 10000), 
                                   step=1)
        
        with col2:
            # Real-time recipient validation
            if to_account:
                if len(to_account) == 7:
                    recipient = find_user_by_account(to_account)
                    if recipient:
                        st.success(f"✅ Recipient: **{recipient['name']}**")
                        st.info(f"📧 Email: {recipient['email']}")
                    else:
                        st.error("❌ Account not found")
                elif len(to_account) > 0:
                    st.warning("⚠️ Account number should be 7 characters")
        
        st.markdown(f"*Maximum transfer: ₹{min(current_balance, 10000):,.2f}*")
        submitted = st.form_submit_button("🚀 Transfer Money")
        
        if submitted:
            # Validation
            if not to_account:
                st.error("❌ Please enter recipient account number")
            elif len(to_account) != 7:
                st.error("❌ Account number must be 7 characters")
            elif to_account == st.session_state.logged_in_user["account_no"]:
                st.error("❌ Cannot transfer to your own account")
            elif amount <= 0:
                st.error("❌ Transfer amount must be greater than 0")
            elif current_balance < amount:
                st.error("❌ Insufficient balance for this transfer")
            else:
                recipient = find_user_by_account(to_account)
                if not recipient:
                    st.error("❌ Recipient account not found")
                else:
                    # Perform transfer
                    sender_balance_before = st.session_state.logged_in_user["balance"]
                    
                    st.session_state.logged_in_user["balance"] -= amount
                    recipient["balance"] += amount
                    
                    sender_balance_after = st.session_state.logged_in_user["balance"]
                    
                    # Update both accounts in database
                    update_user_in_database(st.session_state.logged_in_user)
                    update_user_in_database(recipient)
                    
                    # Generate transfer receipt
                    receipt = generate_receipt("Transfer", amount,
                                             st.session_state.logged_in_user["account_no"],
                                             sender_balance_before, sender_balance_after,
                                             to_account, recipient['name'])
                    st.session_state.last_transaction = receipt
                    st.session_state.transfer_success = True
                    
                    st.success(f"🎉 Successfully transferred ₹{amount:,.2f} to **{recipient['name']}**!")
                    st.balloons()
                    st.info(f"**Your New Balance:** ₹{sender_balance_after:,.2f}")
    
    # Download button outside the form
    if st.session_state.transfer_success and st.session_state.last_transaction:
        st.download_button(
            label="📄 Download Transfer Receipt",
            data=st.session_state.last_transaction,
            file_name=f"transfer_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="transfer_receipt"
        )
        # Reset the flag after showing download button
        if st.button("✅ Transaction Complete", key="complete_transfer"):
            st.session_state.transfer_success = False

elif menu == "✏️ Update Profile" and st.session_state.logged_in_user:
    st.subheader("✏️ Update Your Profile Information")
    
    user = st.session_state.logged_in_user
    
    with st.form("update_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("👤 Full Name", value=user["name"])
            new_phone = st.text_input("📱 Phone Number", value=str(user["phone_number"]))
        
        with col2:
            new_email = st.text_input("📧 Email Address", value=user["email"])
            new_pin = st.text_input("🔐 New PIN (4 digits)", type="password", 
                                  placeholder="Enter new PIN or leave empty to keep current")
        
        submitted = st.form_submit_button("💾 Save Changes")
        
        if submitted:
            # Validation
            errors = []
            if not new_name.strip():
                errors.append("Name cannot be empty")
            elif not new_name.replace(" ", "").isalpha():
                errors.append("Name should contain only letters")
            
            if len(new_phone) != 10 or not new_phone.isdigit():
                errors.append("Phone number must be 10 digits")
            
            if "@" not in new_email or "." not in new_email:
                errors.append("Please enter a valid email address")
            
            if new_pin and (len(new_pin) != 4 or not new_pin.isdigit()):
                errors.append("PIN must be exactly 4 digits")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Update user information
                st.session_state.logged_in_user.update({
                    "name": new_name.strip(),
                    "phone_number": int(new_phone),
                    "email": new_email.strip(),
                })
                
                if new_pin:
                    st.session_state.logged_in_user["pin"] = int(new_pin)
                
                update_user_in_database(st.session_state.logged_in_user)
                st.success("✅ Profile updated successfully!")
                st.balloons()

elif menu == "🗑️ Delete Account" and st.session_state.logged_in_user:
    st.subheader("🗑️ Delete Your Account")
    
    st.warning("⚠️ **DANGER ZONE** - This action cannot be undone!")
    
    user = st.session_state.logged_in_user
    balance = user["balance"]
    
    if balance > 0:
        st.error(f"❌ Cannot delete account with remaining balance of ₹{balance:,.2f}")
        st.info("💡 Please withdraw all funds before deleting your account.")
    else:
        st.markdown("""
        ### Account Deletion Confirmation
        
        You are about to permanently delete your account. This will:
        - Remove all your account information
        - Cancel any pending transactions
        - Permanently delete your account number
        
        **This action cannot be reversed.**
        """)
        
        with st.form("delete_account_form"):
            confirm_name = st.text_input(f"Type your name '{user['name']}' to confirm:")
            confirm_text = st.text_input("Type 'DELETE' to confirm account deletion:")
            submitted = st.form_submit_button("🗑️ DELETE MY ACCOUNT", type="primary")
            
            if submitted:
                if confirm_name != user['name']:
                    st.error("❌ Name confirmation doesn't match")
                elif confirm_text != "DELETE":
                    st.error("❌ Please type 'DELETE' to confirm")
                else:
                    # Delete account
                    Bank.data.remove(st.session_state.logged_in_user)
                    with open(Bank.database, "w") as f:
                        json.dump(Bank.data, f, indent=4)
                    
                    st.success("✅ Account deleted successfully!")
                    st.info("Thank you for banking with us. We're sorry to see you go!")
                    
                    # Clear session state
                    st.session_state.logged_in_user = None
                    st.session_state.last_transaction = None
                    
                    st.rerun()

elif menu == "🚪 Logout" and st.session_state.logged_in_user:
    st.subheader("👋 Logout")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: #1e1e1e; border-radius: 15px;'>
            <h3>Are you sure you want to logout?</h3>
            <p>You'll need to login again to access your account.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Yes, Logout", key="confirm_logout"):
                st.session_state.logged_in_user = None
                st.session_state.last_transaction = None
                st.success("👋 Successfully logged out!")
                st.info("Thank you for banking with us!")
                st.rerun()
        
        with col_no:
            if st.button("❌ Cancel", key="cancel_logout"):
                st.info("Logout cancelled. Welcome back!")

# ---------------- RECENT TRANSACTION RECEIPT ---------------- #
if st.session_state.last_transaction and st.session_state.logged_in_user:
    with st.expander("📄 Latest Transaction Receipt", expanded=False):
        st.markdown("### Transaction Details")
        st.text(st.session_state.last_transaction)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="💾 Download Receipt",
                data=st.session_state.last_transaction,
                file_name=f"transaction_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="latest_receipt"
            )
        with col2:
            if st.button("🗑️ Clear Receipt", key="clear_receipt"):
                st.session_state.last_transaction = None
                st.rerun()

# ---------------- FOOTER ---------------- #
st.markdown("---")

# Banking Statistics (for demonstration)
if st.session_state.logged_in_user:
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Your Balance", f"₹{st.session_state.logged_in_user['balance']:,.2f}")
    
    with col2:
        total_accounts = len(Bank.data)
        st.metric("👥 Total Customers", f"{total_accounts:,}")
    
    with col3:
        st.metric("🏦 Account Type", "Savings")
    
    with col4:
        st.metric("⭐ Your Status", "Active")

# ---------------- ABOUT SECTION ---------------- #
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 25px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;'>
    <h2>👨‍💻 About the Developer</h2>
    <p style='font-size: 1.1em; margin: 15px 0;'>
        Hi! I'm <strong>Dhrumil Shah</strong> — a passionate AI/ML student and tech explorer.<br>
        I love building innovative AI tools, automation scripts, and interactive web applications.
    </p>
    
<div style='margin: 20px 0;'>
    <a href='https://www.linkedin.com/in/dhrumil-shah-646815350' target='_blank' 
        style='color: white; text-decoration: none; margin: 0 10px;'>
        💼 LinkedIn
    </a>
    <a href='https://github.com/dhrumilshah-216' target='_blank' 
        style='color: white; text-decoration: none; margin: 0 10px;'>
        💻 GitHub
    </a>
    <a href='https://dhrumilshahportfolio.netlify.app/' target='_blank' 
        style='color: white; text-decoration: none; margin: 0 10px;'>
        🌐 Portfolio
    </a>
</div>
    
<p style='font-size: 0.9em; opacity: 0.8;'>
    This banking application demonstrates modern web development with Python, Streamlit, and AI integration.
</p>
</div>
""", unsafe_allow_html=True)

# Security notice
st.markdown("""
<div style='background: #2d2d2d; padding: 15px; border-radius: 10px; 
            border-left: 4px solid #ff9800; margin: 20px 0;'>
    <h4 style='color: #ff9800; margin: 0 0 10px 0;'>🔒 Security Notice</h4>
    <p style='margin: 0; font-size: 0.9em;'>
        This is a demonstration banking application. In a real banking system, additional security measures 
        such as encryption, multi-factor authentication, and regulatory compliance would be implemented.
    </p>
</div>
""", unsafe_allow_html=True)