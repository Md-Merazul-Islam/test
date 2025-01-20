
# Gym Class Scheduling API Documentation

This document provides detailed API documentation for the Gym Class Scheduling system.

## **1. User Registration**

### Endpoint: `/accounts/register/`

#### Method: `POST`

### Request Body:
```json
{
    "username": "test",
    "email": "test@gamil.com",
    "password": "your_encrypted_password"
}
```

### Response:

#### Success (201):
```json
{
    "success": true,
    "statusCode": 201,
    "message": "Registration successful. You can now log in.",
    "data": {
        "username": "test",
        "email": "test@gamil.com",
        "password": "your_encrypted_password"
    }
}
```

#### Error:
```json
{
    "username": [
        "A user with that username already exists."
    ],
    "password": [
        "This field may not be blank."
    ],
    "confirm_password": [
        "This field may not be blank."
    ]
}
```

---

## **2. User Login**

### Endpoint: `/accounts/login/`

#### Method: `POST`

### Request Body:
```json
{
    "username": "test",
    "password": "your_password"
}
```

### Response:

#### Success (200):
```json
{
    "success": true,
    "statusCode": 200,
    "message": "Login successful.",
    "data": {
        "refresh": "your_refresh_token",
        "access": "your_access_token",
        "user_id": 8,
        "username": "test"
    }
}
```

#### Error (Invalid credentials):
```json
{
    "success": false,
    "message": "Invalid credentials.",
    "errorDetails": "Please check your username or password."
}
```

---

## **3. Admin Trainer Management**

### Endpoint: `/admins/trainers/`

#### Method: `GET`

### Response:
```json
{
    "username": "",
    "email": ""
}
```

---

## **4. Class Schedules (Admin)**

### Endpoint: `/admins/class-schedules/`

#### Method: `GET`

### Response:
```json
[
    {
        "id": 2,
        "date": "2025-01-21",
        "start_time": "09:01:00",
        "end_time": "11:01:00",
        "trainer": 1,
        "trainer_name": "saim",
        "current_trainees": 0
    },
    {
        "id": 3,
        "date": "2025-01-21",
        "start_time": "11:01:00",
        "end_time": "13:01:00",
        "trainer": 1,
        "trainer_name": "saim",
        "current_trainees": 0
    }
]
```

#### Error:
```json
{
    "date": null,
    "start_time": null,
    "trainer": null
}
```

---

## **5. Class Schedules (Trainer)**

### Endpoint: `/trainers/my-schedules/`

#### Method: `GET`

### Response:
```json
{
    "success": true,
    "statusCode": 200,
    "message": "Schedules fetched successfully.",
    "data": [
        {
            "id": 1,
            "date": "2025-01-21",
            "start_time": "07:00:00",
            "end_time": "09:00:00",
            "trainer": 1,
            "trainer_name": "saim",
            "current_trainees": 2
        },
        {
            "id": 2,
            "date": "2025-01-21",
            "start_time": "09:01:00",
            "end_time": "11:01:00",
            "trainer": 1,
            "trainer_name": "saim",
            "current_trainees": 0
        }
    ]
}
```

---

## **6. Class Schedule Creation (Admin)**

### Endpoint: `/admins/class-schedules/`

#### Method: `POST`

### Request Body:
```json
{
    "date": "2025-01-21",
    "start_time": "09:00:00",
    "end_time": "11:00:00",
    "trainer": 1
}
```

### Error (Maximum classes per day exceeded):
```json
{
    "success": false,
    "message": "Maximum of 5 classes can be scheduled for this day."
}
```

---

## **Authentication Flow**

1. **User Registration**:
    - The user provides a `username`, `email`, and `password`.
    - A successful response returns a confirmation message along with user data (excluding the password).

2. **User Login**:
    - The user enters their credentials (`username` and `password`).
    - On successful login, `access` and `refresh` tokens are returned.

3. **Admin Class Management**:
    - Admin can view and manage trainer schedules.
    - Admin can create or manage class schedules with a limit of 5 classes per day.
    - An error is returned if the maximum number of classes for the day is reached.

4. **Trainer Schedules**:
    - Trainers can view their own schedules with details about date, time, and current trainees.

---

### **API Endpoints Summary**

| Endpoint                            | Method  | Description                                  |
|-------------------------------------|---------|----------------------------------------------|
| `/accounts/register/`              | `POST`  | Register a new user                          |
| `/accounts/login/`                 | `POST`  | User login with credentials                  |
| `/admins/trainers/`                | `GET`   | Fetch trainer information                    |
| `/admins/class-schedules/`         | `GET`   | Fetch class schedules (Admin)                |
| `/trainers/my-schedules/`          | `GET`   | Fetch class schedules (Trainer)              |
| `/admins/class-schedules/`         | `POST`  | Create a new class schedule                  |

---

This API documentation serves as a reference for interacting with the Gym Class Scheduling system. It includes details for user registration, login, class schedule management, and trainer schedule retrieval.
