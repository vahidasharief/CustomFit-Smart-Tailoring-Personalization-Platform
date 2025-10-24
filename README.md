# 🧵 CustomFit – Smart Tailoring & Personalization Platform

> **“Fashion meets technology.”**  
> CustomFit is a smart web platform that connects customers with local tailors to design, customize, and book fittings for their perfect outfit.  
> The application combines modern UI design, intelligent data handling, and seamless backend logic to create a professional-grade tailoring experience.

---

## 🌟 Overview

CustomFit empowers users to explore curated outfit designs, choose from skilled tailors, input custom measurements, and schedule appointments — all from a single, elegant interface.

This project was designed as a **complete full-stack application** showcasing:
- Responsive front-end development with **Tailwind CSS**
- Back-end API integration via **Flask**
- Database modeling with **MySQL**
- Real-time appointment management and admin oversight

---

## 🧠 Core Features

### 👗 Design Collection
Explore a range of curated fashion designs — from classic suits to casual wear.  
Each design card includes style details, pricing, and a booking link for quick scheduling.

### 👔 Tailor Profiles
Browse through professional tailors with verified experience.  
Each tailor card includes their specialty, years of experience, and a direct “Book Appointment” option.

### 📅 Smart Appointment Booking
Users can:
- Select designs and tailors
- Enter measurements
- Pick appointment date & time  
Everything is validated both client- and server-side for a smooth experience.

### 🧑‍💼 Admin Dashboard
Admins can:
- View all bookings in a clean tabular interface
- Export booking details as CSV
- Manage customer interactions efficiently

### 🧭 Modern, Minimal UI
Built with **Tailwind CSS**, featuring:
- Soft shadows, rounded corners, and balanced typography
- Consistent color palette for a professional aesthetic
- Fully responsive design for mobile, tablet, and desktop

---

## 🧱 System Architecture

Frontend (HTML, CSS, JS, Tailwind)
↓
Flask App (Python)
↓
MySQL Database


- **Frontend:** Lightweight static pages enhanced with Tailwind utilities.
- **Backend:** Flask serves routes, handles form submissions, and manages session state.
- **Database:** MySQL stores users, designs, tailors, and bookings.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript, TailwindCSS |
| **Backend** | Python 3.11, Flask |
| **Database** | MySQL|
| **Environment** | Virtualenv, dotenv |
| **Data Serialization** | JSON |
| **Version Control** | Git, GitHub |
| **Deployment Ready** | Dockerized setup with Compose |
| **Testing Tools** | Postman, Curl, Flask Debug Server |

---

## 💾 Database Design

**Entities:**
- `User`: Stores user credentials, names, and session info.
- `Tailor`: Contains professional details (name, specialty, experience).
- `Design`: Defines available outfit categories and metadata.
- `Booking`: Stores customer measurements, design, tailor, date, and notes.

**Relationships:**
- A `User` can make multiple `Bookings`.
- A `Booking` links one `User`, one `Design`, and one `Tailor`.

**Schema Snapshot:**
```sql
users(id, name, email, password_hash, created_at)
tailors(id, name, email, phone, specialty, experience_years)
designs(id, name, category, description, price_range, image)
bookings(id, user_id, design_id, tailor_id, appointment_date, appointment_time, measurements, notes)


#### Homepage — Design Collection
<img width="3195" height="1757" alt="image" src="https://github.com/user-attachments/assets/b0663506-1a56-4b66-bf67-f38a5d827b20" />



#### Tailors Page
<img width="3199" height="1821" alt="image" src="https://github.com/user-attachments/assets/660a58e4-edbd-4f0c-8729-dcff9e8a9c68" />

#### Booking Form

<img width="3199" height="1846" alt="image" src="https://github.com/user-attachments/assets/55f0df78-2ac9-49df-acfe-294e80a230f4" />







