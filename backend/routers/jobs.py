from fastapi import APIRouter, Depends, HTTPException
from backend.models.job import Job, JobStatus
from backend.database.database import get_connection
from datetime import datetime
from backend.services.job_search import search_jobs
from backend.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[Job])
def get_jobs(user_id: int = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            title,
            company,
            location,
            created_at,
            status,
            salary,
            url,
            contact,
            note
        FROM jobs
        WHERE user_id = ?
    """, (user_id,))
    
    rows = cursor.fetchall()

    conn.close()

    return [
        Job(
            id=row[0],
            title=row[1],
            company=row[2],
            location=row[3],
            created_at=row[4] if row[4] else None,
            status=row[5] if row[5] else "Aktivní",
            salary=row[6],
            url=row[7],
            contact=row[8],
            note=row[9]
        )
        for row in rows
    ]


@router.post("", response_model=Job)
def create_job(
    job: Job,
    user_id: int = Depends(get_current_user),
):
    
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now()
    # store formatted string in DB but keep datetime object for the response model
    created_at_str = created_at.strftime("%d.%m.%Y %H:%M")

    cursor.execute(
        """
        INSERT INTO jobs
        (
            title,
            company,
            location,
            created_at,
            status,
            salary,
            url,
            contact,
            note,
            user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job.title,
            job.company,
            job.location,
            created_at_str,
            job.status,
            job.salary,
            job.url,
            job.contact,
            job.note,
            user_id
        )
    )

    job_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return Job(
    id=job_id,
    title=job.title,
    company=job.company,
    location=job.location,
    created_at=created_at_str,
    status=job.status,
    salary=job.salary,
    url=job.url,
    contact=job.contact,
    note=job.note
    )


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    user_id: int = Depends(get_current_user),
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM jobs
        WHERE id = ? AND user_id = ?
        """,
        (
            job_id,
            user_id,
        )
    )

    deleted_rows = cursor.rowcount

    conn.commit()
    conn.close()

    if deleted_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Pracovní nabídka nebyla nalezena.",
        )

    return {
        "message": f"Job {job_id} deleted"
    }
    
@router.put("/{job_id}", response_model=Job)
def update_job(
    job_id: int,
    job: Job,
    user_id: int = Depends(get_current_user),
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jobs
        SET
            title = ?,
            company = ?,
            location = ?,
            salary = ?,
            url = ?,
            contact = ?,
            note = ?,
            status = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            job.title,
            job.company,
            job.location,
            job.salary,
            job.url,
            job.contact,
            job.note,
            job.status,
            job_id,
            user_id,
        )
    )

    updated_rows = cursor.rowcount

    conn.commit()
    conn.close()

    if updated_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Pracovní nabídka nebyla nalezena.",
        )

    return Job(
        id=job_id,
        title=job.title,
        company=job.company,
        location=job.location,
        salary=job.salary,
        url=job.url,
        contact=job.contact,
        note=job.note,
        status=job.status,
    )
    
    
@router.put("/{job_id}/status")
def update_job_status(
    job_id: int,
    data: JobStatus,
    user_id: int = Depends(get_current_user),
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE jobs
        SET status = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            data.status,
            job_id,
            user_id,
        )
    )

    updated_rows = cursor.rowcount

    connection.commit()
    connection.close()

    if updated_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Pracovní nabídka nebyla nalezena.",
        )

    return {
        "message": "Status aktualizován"
    }
    
@router.get("/search")
def search_job_offers(
    position: str = "",
    location: str = "",
):
    return search_jobs(position, location)    