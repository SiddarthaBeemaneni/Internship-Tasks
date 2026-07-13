# 🎫 TicketSense — Helpdesk Ticket Classifier & Router

TicketSense is a Flask-based web application that automates the classification and routing of helpdesk support tickets. It allows users to submit support requests, automatically categorizes the issue, assigns it to the appropriate department, and enables administrators to manage ticket statuses efficiently.

---

## 📌 Features

- User-friendly ticket submission form
- Automatic ticket classification
- Department-wise ticket routing
- Admin dashboard for ticket management
- Ticket status tracking
- Responsive user interface
- Flask template rendering using Jinja2
- SQLite database integration

---

## 🛠️ Technologies Used

### Backend
- Python 3
- Flask

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap (optional)

### Database
- SQLite

### Template Engine
- Jinja2

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
│   └── status.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
└── screenshots/
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/TicketSense.git
```

### 2. Navigate to the project folder

```bash
cd TicketSense
```

### 3. Create a virtual environment (Optional)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Flask application

```bash
python app.py
```

or

```bash
flask run
```

---

## 🌐 Access the Application

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📋 Modules

### User Module
- Submit support tickets
- View ticket details
- Track ticket status

### Ticket Classification Module
- Analyze ticket information
- Assign category
- Set priority

### Routing Module
- Route tickets to appropriate departments
- Technical Support
- Billing
- Customer Support
- HR

### Admin Module
- View all tickets
- Update ticket status
- Manage ticket assignments

---

## 🔄 Workflow

1. User submits a support ticket.
2. Flask receives the request.
3. Ticket is classified based on the issue.
4. Ticket is routed to the appropriate department.
5. Ticket details are stored in the database.
6. Admin reviews and updates the ticket.
7. User can track the updated ticket status.

---

## 📊 Future Enhancements

- Machine Learning-based ticket classification
- Email notifications
- SMS alerts
- REST API support
- User authentication
- Role-based access control
- Dashboard analytics
- Cloud deployment
- Chatbot integration

---

## 📸 Screenshots

Add screenshots of your application inside the `screenshots/` folder.

Example:

- Home Page
- Submit Ticket
- Dashboard
- Ticket Status

---

## 👨‍💻 Author

**Your Name**

Department of Computer Science

---

## 📄 License

This project is developed for educational purposes.

Feel free to use and modify it for learning.

---

## ⭐ Acknowledgements

- Flask Documentation
- Python Documentation
- MDN Web Docs
- Jinja2 Documentation
