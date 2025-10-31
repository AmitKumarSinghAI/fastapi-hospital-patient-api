from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Dict, List, Annotated, Literal, Optional
import json

# ---------------------------------------------------------
# Initialize FastAPI App
# ---------------------------------------------------------
app = FastAPI(title="Patient Management API", description="API to manage patient health records")

# ---------------------------------------------------------
# Helper Functions: Load & Save JSON Data
# ---------------------------------------------------------
def helper():
    """Read and return data from patients.json"""
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def save(data):
    """Write updated data back to patients.json"""
    with open('patients.json', 'w') as file:
        json.dump(data, file, indent=4)


# ---------------------------------------------------------
# GET → View All Patients
# ---------------------------------------------------------
@app.get('/views')
def views():
    """Return all patient data"""
    data = helper()
    return data


# ---------------------------------------------------------
# GET → View Patient by ID
# ---------------------------------------------------------
@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description='Show the details by ID', examples=['P003', 'P002'])
):
    """Return a single patient's data using their ID"""
    data = helper()
    patient_ids = ", ".join(list(data.keys()))

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=400,
        detail=f'Patient not found. Try valid ID like: {patient_ids}'
    )


# ---------------------------------------------------------
# GET → Sort Patients by Height, Weight, or BMI
# ---------------------------------------------------------
@app.get('/sort')
def sort(
    sort_by: str = Query(..., description='Sort by height, weight, or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):
    """Sort all patient records by height, weight, or BMI"""
    data = helper()
    valid = ['height', 'weight', 'bmi']

    if sort_by not in valid:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid field! Use one of: {valid}'
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail='Please enter a valid order: asc or desc'
        )

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=(order == 'desc')
    )

    return sorted_data


# ---------------------------------------------------------
# Pydantic Model → Patient Schema
# ---------------------------------------------------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient', example='Binay')]
    city: Annotated[str, Field(..., description='City where patient lives', example='Mumbai')]
    age: Annotated[int, Field(gt=0, lt=100, description='Age of the patient')]
    gender: Annotated[str, Literal['male', 'female', 'other']]
    height: Annotated[float, Field(gt=0, description='Height in meters')]
    weight: Annotated[float, Field(gt=3, description='Weight in kilograms')]

    # Auto-calculated BMI
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Auto-calculated Verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 40:
            return 'Overweight'
        else:
            return 'Obese'


# ---------------------------------------------------------
# POST → Create New Patient
# ---------------------------------------------------------
@app.post('/create')
def create(patient: Patient):
    """Add a new patient record"""
    data = helper()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump(exclude={'id'})
    save(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'Patient created successfully'}
    )


# ---------------------------------------------------------
# PUT → Update Existing Patient
# ---------------------------------------------------------
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
    height: Optional[float] = None
    weight: Optional[float] = None


@app.put('/update/{patient_id}')
def update(patient_id: str, patient_update: PatientUpdate):
    """Update existing patient record by ID"""
    data = helper()

    if patient_id not in data:
        raise HTTPException(status_code=400, detail='Patient ID not found')

    patient_info = data[patient_id]
    update_info = patient_update.model_dump(exclude_unset=True)

    # Apply updates
    for key, value in update_info.items():
        patient_info[key] = value

    # Validate updated info
    pydantic_obj = Patient(id=patient_id, **patient_info)
    patient_info = pydantic_obj.model_dump(exclude={'id'})

    data[patient_id] = patient_info
    save(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})


# ---------------------------------------------------------
# DELETE → Delete Patient
# ---------------------------------------------------------
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    """Delete patient record by ID"""
    data = helper()

    if patient_id not in data:
        raise HTTPException(status_code=400, detail='Patient not found')

    del data[patient_id]
    save(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})
