from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, models

router = APIRouter(
    prefix='/bank/employee',
    tags=["Employee"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_emp(request: schemas.EmployeeBase, db: Session = Depends(database.get_db)):
    try:
        new_emp = models.Employee(name=request.name, department_id=request.department_id, department=request.department, position=request.position, email=request.email)
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating employee: {str(e)}")
    
@router.get('/')
async def get_employee(db: Session = Depends(database.get_db)):
    try:
        emp = db.query(models.Employee).all()
        return emp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching emp: {str(e)}")
    
@router.get('/{id}')
async def get_emp_id(id: int, db: Session = Depends(database.get_db)):
    try:
        emp = db.query(models.Employee).filter(models.Employee.id == id).first()
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id = {id} not found")
        return emp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_emp(id: int, db: Session = Depends(database.get_db)):
    try:
        emp = db.query(models.Employee).filter(models.Employee.id == id).first()
        
        if not emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id = {id} not found")
        
        db.delete(emp)
        db.commit()
        
        return {"detail": "Employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
    