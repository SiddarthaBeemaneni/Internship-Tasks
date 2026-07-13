# 🎫 TicketSense — Helpdesk Ticket Classifier & Router

TicketSense is a Flask-based web application that automates the classification and routing of helpdesk support tickets. The system enables users to submit support requests, automatically categorizes them based on their content, routes them to the appropriate department, and allows administrators to manage and track ticket statuses efficiently.

---

## 🚀 Features

- 📝 Submit support tickets through a user-friendly interface
- 🤖 Automatic ticket classification
- 📂 Department-wise ticket routing
- 📊 Admin dashboard to manage tickets
- 🔍 Track ticket status
- 📱 Responsive web interface
- 🎨 Flask template rendering with Jinja2
- 💾 SQLite database integration
- ✅ Form validation using JavaScript

---

## 🛠️ Tech Stack

### Backend
- Python 3.x
- Flask

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Template Engine

### Database
- SQLite

### Tools
- Git & GitHub
- VS Code

---

## 📂 Project Structure

```
TicketSense/
│
├── app.py
├── requirements.txt
├── database.db
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── submit.html
│   ├── dashboard.html
│   ├── status.html
│   └── login.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── models.py
├── routes.py
├── utils.py
└── screenshots/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/TicketSense.git
```

### 2. Navigate to the project directory

```bash
cd TicketSense
```

### 3. Create a virtual environment (Optional)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

or

```bash
flask run
```

---

## 🌐 Usage

Open your browser and visit:

```
http://127.0.0.1:5000
```

1. Submit a helpdesk ticket.
2. The system classifies the ticket automatically.
3. The ticket is routed to the appropriate department.
4. The administrator reviews and updates the ticket status.
5. Users can track the progress of their tickets.

---

## 📌 Modules

### User Module
- Submit tickets
- View ticket details
- Track ticket status

### Ticket Classification Module
- Analyze ticket content
- Predict category
- Assign priority

### Routing Module
- Route tickets to:
  - Technical Support
  - Billing
  - Customer Service
  - HR
  - Network Team

### Admin Module
- View all tickets
- Update ticket status
- Manage ticket assignments

### Database Module
- Store user information
- Store ticket details
- Maintain ticket history

---

## 🔄 Workflow

```
User
   │
   ▼
Submit Ticket
   │
   ▼
Flask Backend
   │
   ▼
Ticket Classification
   │
   ▼
Department Routing
   │
   ▼
SQLite Database
   │
   ▼
Admin Dashboard
   │
   ▼
Status Updated
   │
   ▼
User Views Ticket Status
```

---

## 📊 Future Enhancements

- Machine Learning-based ticket classification
- Email notifications
- SMS alerts
- User authentication
- Role-based access control
- REST API support
- Cloud deployment
- Analytics dashboard
- Chatbot integration
- Mobile application

---

## 📸 Screenshots

Add screenshots of your application inside the `screenshots/` folder.

Example:

- Home Page
- Submit Ticket Page
- Dashboard
- Ticket Status Page

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

## 📄 License

This project is developed for educational purposes under the MIT License.

---

## 👨‍💻 Author

**Your Name**

B.Tech / MCA Student

Innolift Ventures Internship – 2026

---

## 🙏 Acknowledgements

- Flask Documentation
- Python Documentation
- SQLite Documentation
- MDN Web Docs
- Jinja2 Documentation
- Scikit-learn Documentation