# FleetFlow  
### Modular Fleet & Logistics Management System

FleetFlow is a role-based fleet and logistics management system built using **Flask + SQLAlchemy + MySQL**.  
It manages vehicles, drivers, trips, maintenance, expenses, and analytics in a modular and scalable architecture.

## 🛠️ Tech Stack

**Backend**
- Python
- Flask
- Flask-Login
- Flask-Migrate
- SQLAlchemy

**Database**
- MySQL

**Frontend**
- HTML5
- Bootstrap 5
- Jinja2 Templates

**Visualization**
- Chart.js

## ✨ Features

### 🔐 Role-Based Access Control
Supports four system roles:
- **Manager**
- **Dispatcher**
- **Safety Officer**
- **Analyst**

Each role has restricted access to specific modules.

## Vehicle Registry
- Add / Edit / Retire vehicles  
- Track:
  - Type
  - Model
  - Year
  - Capacity
  - Odometer  
- Vehicle status tracking:
  - Available
  - OnTrip
  - InShop
  - Retired  


## Driver Registry
- Add / Edit drivers  
- License tracking  
- License expiry validation  
- Suspend / Reactivate drivers  
- Driver performance tracking  


## Trip Dispatcher
- Create trips (Draft)  
- Dispatch trips  
- Complete trips  
- Cancel trips  
- Odometer validation  
- Automatic vehicle & driver status updates  

### Trip Status Flow
```
FleetFlow/
│
├── app/
│ ├── models/
│ ├── routes/
│ ├── templates/
│ ├── utils/
│ ├── extensions.py
│ └── init.py
│
├── migrations/
├── run.py
├── config.py
└── README.md
```

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/FleetFlow.git
cd FleetFlow
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```


### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```


### 4️⃣ Configure Environment Variables
Create a .env file:
```bash
SECRET_KEY=YOUR_SECRET_KEY
DB_USER=MYSQL_USER
DB_PASSWORD=MYSQL_PASSWORD
DB_HOST=MYSQL_HOST
DB_NAME=DATABASE_NAME
```
### 5️⃣ Initialize Database
```bash
flask db init        # Only first time
flask db migrate -m "Initial migration"
flask db upgrade
```
### 6️⃣ Run the Application
```bash
python run.py
```
Visit:
```
http://127.0.0.1:5000
```

## Business Logic Highlights

* **Cancelled trips do not count** toward performance.
* **Driver completion % excludes cancelled trips.**
* **Vehicle & driver states auto-update** during:
  * Dispatch
  * Cancel
  * Complete
* 📈 **ROI Formula**

```text
ROI = ((Revenue - Total Cost) / Total Cost) * 100
```

## 🔒 Role Permissions Overview

| Module      | Manager | Dispatcher | Safety Officer | Analyst |
| ----------- | ------- | ---------- | -------------- | ------- |
| Vehicles    | ✅       | ❌          | ❌              | ❌       |
| Drivers     | ✅       | ✅          | ✅              | ❌       |
| Trips       | ✅       | ✅          | ❌              | ❌       |
| Maintenance | ✅       | ❌          | ✅              | ❌       |
| Performance | ✅       | ❌          | ✅              | ✅       |
| Expenses    | ✅       | ❌          | ❌              | ✅       |
| Analytics   | ✅       | ❌          | ❌              | ✅       |

## 🎨 UI Features

* Sidebar navigation
* Role display in sidebar
* Dismissible + auto-closing flash messages
* Responsive Bootstrap layout
* Chart.js data visualization

## 🚀 Future Improvements

* Export reports (PDF / CSV)
* Pagination
* Soft delete system
* Advanced filters
* Real-time dashboard refresh
* Vehicle cost-per-km analytics
* Driver scoring system
