# 🏦 Dhrumil's Bank Management System

A comprehensive digital banking application built with Python, featuring both command-line and web interfaces, along with AI-powered customer support.

[Live demo](https://dhrumil-bank-management-system.streamlit.app/)

## 📋 Table of Contents
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Integration](#-api-integration)
- [Security Features](#-security-features)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

### Core Banking Operations
- **Account Creation**: Secure account registration with validation
- **Money Management**: 
  - Deposit funds (₹1 - ₹10,000 per transaction)
  - Withdraw money with balance verification
  - Transfer money between accounts
- **Account Services**:
  - View account details and balance
  - Update profile information
  - Delete account (with safety confirmations)

### Advanced Features
- **🤖 AI Assistant**: Integrated AI chatbot "Nishu" for banking queries
- **📄 Transaction Receipts**: Downloadable transaction receipts with unique IDs
- **🎨 Modern Web Interface**: Beautiful Streamlit-based GUI with gradient designs
- **💾 Data Persistence**: JSON-based data storage with automatic updates
- **🔒 Security**: PIN-based authentication and input validation

### User Interface Options
1. **Command Line Interface** (`main.py`): Traditional CLI for terminal users
2. **Web Application** (`app.py`): Modern web interface with rich UI/UX

## 🏗 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Core Logic    │    │   Data Layer    │
│                 │    │                 │    │                 │
│ • Streamlit UI  │◄──►│  Bank Class     │◄──►│   data.json     │
│ • CLI Interface │    │  • Validation   │    │   • User Data   │
│                 │    │  • Operations   │    │   • Persistence │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   AI Service    │
│                 │
│ • OpenRouter    │
│ • AI Assistant │
└─────────────────┘
```

## 🛠 Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/dhrumilshah-216/Bank-Management-System
cd bank-management-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit requests python-dotenv
```

### Step 3: Environment Setup
Create a `.env` file in the project root:

```env
# OpenRouter API Configuration
API_KEY=your_openrouter_api_key_here
MODEL=meta-llama/llama-3.1-8b-instruct:free
url=https://openrouter.ai/api/v1/chat/completions
prompt=You are Nishu, a helpful banking assistant. Answer questions about banking, account management, and financial services. Be friendly and professional.
```

### Step 4: Run the Application

#### Web Interface (Recommended)
```bash
streamlit run app.py
```

#### Command Line Interface
```bash
python main.py
```

## 🚀 Usage

### Web Application Features

#### 1. Account Creation
- Navigate to "🆕 Create Account"
- Fill in personal details (name, age, phone, email, PIN)
- System validates all inputs and generates unique account number
- Minimum age requirement: 18 years

#### 2. Banking Operations
- **Login**: Use your 7-character account number and 4-digit PIN
- **Dashboard**: View balance, account info, and quick actions
- **Deposits**: Add money to your account (₹1 - ₹10,000)
- **Withdrawals**: Remove money with balance verification
- **Transfers**: Send money to other accounts with real-time recipient verification

#### 3. AI Assistant "Nishu"
- Click "💬 Ask Nishu" button
- Ask questions about banking, account management, or general financial queries
- Get instant AI-powered responses

#### 4. Account Management
- Update profile information (name, phone, email, PIN)
- View detailed account information
- Delete account (requires zero balance and confirmation)

### Command Line Interface
Run `python main.py` and follow the menu:
```
0 - Exit
1 - Create an account
2 - Deposit money
3 - Withdraw money
4 - See account details
5 - Update details
6 - Delete account
```

## 📁 Project Structure

```
bank-management-system/
│
├── main.py              # CLI version of the banking application
├── app.py               # Streamlit web application
├── bank.py              # Core Bank class with all banking operations
├── ai_talker.py         # AI integration module (OpenRouter API)
├── data.json            # JSON database for user accounts
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys, config)
└── README.md            # Project documentation
```

### File Descriptions

- **`bank.py`**: Core banking logic with account operations, validation, and data management
- **`main.py`**: Command-line interface with menu-driven interaction
- **`app.py`**: Streamlit web application with modern UI and enhanced features
- **`ai_talker.py`**: AI chatbot integration using OpenRouter API
- **`data.json`**: Persistent storage for all user account data
- **`requirements.txt`**: Python package dependencies for easy installation

## 🤖 API Integration

### OpenRouter AI Integration
The system integrates with OpenRouter API to provide intelligent customer support:

- **Model**: Configurable (default: Meta Llama 3.1 8B)
- **Purpose**: Banking assistance and customer queries
- **Features**: Natural language interaction, banking guidance
- **Security**: API key stored in environment variables

## 🔒 Security Features

### Data Validation
- **Email**: Regex pattern validation
- **Phone**: 10-digit number validation
- **PIN**: 4-digit numeric validation
- **Age**: Minimum 18 years requirement
- **Name**: Alphabetic characters only

### Account Security
- **Unique Account Numbers**: 7-character randomly generated IDs
- **PIN Authentication**: Required for all sensitive operations
- **Transaction Limits**: ₹10,000 maximum per transaction
- **Balance Verification**: Prevents overdrafts

### Safety Features
- Account deletion requires zero balance
- Transfer validation prevents self-transfers
- Confirmation prompts for destructive operations
- Error handling for invalid inputs

## 💡 Key Highlights

- **Dual Interface**: Both CLI and web interfaces available
- **Real-time Validation**: Instant feedback on user inputs
- **Professional Receipts**: Detailed transaction receipts with unique IDs
- **AI Integration**: Smart customer support with OpenRouter
- **Modern Design**: Gradient UI with responsive layout
- **Data Persistence**: Automatic JSON database updates

## 🔧 Configuration

### Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `API_KEY` | OpenRouter API key | `sk-or-v1-xxx...` |
| `MODEL` | AI model to use | `meta-llama/llama-3.1-8b-instruct:free` |
| `url` | OpenRouter API endpoint | `https://openrouter.ai/api/v1/chat/completions` |
| `prompt` | System prompt for AI | `You are Nishu, a helpful banking assistant...` |

## 🚨 Known Limitations

- **Demo Purpose**: This is an educational/demonstration project
- **Security**: In production, additional security measures would be required:
  - Encryption for sensitive data
  - Multi-factor authentication
  - Regulatory compliance (PCI DSS, etc.)
  - Secure password hashing
- **Scalability**: JSON storage suitable for small-scale demonstration only
- **Concurrent Access**: No multi-user concurrency handling

## 🔮 Future Enhancements

- [ ] Database migration (SQLite/PostgreSQL)
- [ ] Transaction history and statements
- [ ] Account types (Checking, Savings, Fixed Deposit)
- [ ] Interest calculation
- [ ] Loan management system
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Mobile app development
- [ ] Blockchain integration
- [ ] Advanced security features

## 🛡️ Requirements

### Python Dependencies
```txt
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### System Requirements
- Python 3.7 or higher
- Internet connection (for AI features)
- Modern web browser (for Streamlit app)
- 50MB free disk space

## 📖 Usage Examples

### Creating an Account (CLI)
```bash
python main.py
# Select option 1
# Follow prompts to enter details
```

### Web Application Login
1. Open `http://localhost:8501` after running `streamlit run app.py`
2. Choose "🔑 Login"
3. Enter your account number and PIN
4. Access full banking dashboard

### Using AI Assistant
1. Click "💬 Ask Nishu" in the web app
2. Type your banking question
3. Get instant AI-powered responses

## 🏆 Developer Information

**Created by**: Dhrumil Shah  
**Role**: AI/ML Student & Tech Explorer  
**Focus**: AI Tools, Automation, Web Applications  

### Connect with the Developer
- 💼 [LinkedIn](https://www.linkedin.com/in/dhrumil-shah-646815350)
- 💻 [GitHub](https://github.com/dhrumilshah-216)
- 🌐 [Portfolio](https://dhrumilshahportfolio.netlify.app/)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This is a demonstration banking application created for educational purposes. It should not be used for actual financial transactions or storing real financial data. Always implement proper security measures, encryption, and regulatory compliance for production banking applications.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **OpenRouter**: For AI API integration
- **Python Community**: For excellent libraries and documentation

---

*Built with ❤️ by Dhrumil Shah - Transforming ideas into digital reality*