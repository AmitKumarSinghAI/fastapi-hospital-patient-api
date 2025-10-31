# 🏥 FastAPI Hospital Patient Management API

A simple **FastAPI** project to manage hospital patient records — create, read, update, and delete patient details.  
Data is stored in a local JSON file (no database required). Ideal for learning **FastAPI CRUD operations**.

---

## 🚀 Features
- Add new patient records  
- View all or specific patient data  
- Update existing patient details  
- Delete patient records  
- JSON-based data storage  
- FastAPI + Pydantic validation  

---

## 🧩 Tech Stack
- **FastAPI** – web framework  
- **Uvicorn** – ASGI server  
- **Pydantic** – data validation  
- **Python 3.10+**

---

## 📁 Project Structure

```
fastapi-hospital-patient-api/
│
├── main.py               # Main FastAPI application
├── patients.json         # JSON file for storing patient data
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create and activate a virtual environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install fastapi uvicorn
```

### 3️⃣ Run the API
```bash
uvicorn main:app --reload
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| **POST** | `/create` | Add a new patient |
| **GET** | `/views` | Get all patient records |
| **GET** | `/patient/{patient_id}` | Get patient by ID |
| **GET** | `/sort` | Sort patient data by height, weight, or BMI |
| **PUT** | `/update/{patient_id}` | Update patient info |
| **DELETE** | `/delete/{patient_id}` | Delete patient |

---

## 🧪 Example JSON Data

```json
{
  "P001": {
    "name": "Ravi Sharma",
    "city": "Delhi",
    "age": 32,
    "gender": "male",
    "height": 1.70,
    "weight": 82,
    "bmi": 28.37,
    "verdict": "Overweight"
  }
}
```

---

## 🧠 Notes
- Data is stored locally in `patients.json`.
- Each patient has a unique `id`.
- Perfect for FastAPI beginners learning CRUD operations.

---

## ✨ Author
**Amit Kumar Singh Kurmi**  
🎯 Aspiring AI Engineer | Python & FastAPI Learner
