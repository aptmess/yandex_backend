from fastapi import HTTPException, status

EXCEPTION_404_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail='Item not found'
)

EXCEPTION_400_BAD_REQUEST_VALIDATION_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='Validation Failed'
)
