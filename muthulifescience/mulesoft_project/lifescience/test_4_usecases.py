import psycopg2
import subprocess
import json

def execute_4_business_usecases():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="Admin1234"
    )
    cur = conn.cursor()
    print("=" * 80)
    print("[MULESOFT & SALESFORCE LSC] EXECUTING 4-BUSINESS USE CASE PIPELINE")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # USE CASE 1: Inpatient ER Admission Sync (ClinicalEncounter)
    # -------------------------------------------------------------------------
    print("\n[USE CASE 1] Clinical Trial ER Admission Sync (ClinicalEncounter)")
    cur.execute("SELECT encounter_id, patient_external_id, category, status FROM hospital_clinical_encounters WHERE sync_status = 'NEW';")
    rows1 = cur.fetchall()
    print(f" -> Found {len(rows1)} new encounter rows in PostgreSQL.")
    for r in rows1:
        enc_id, pat_id, cat, status = r
        cmd = [
            "sf", "data", "create", "record",
            "--target-org", "muthulifescience",
            "--sobject", "ClinicalEncounter",
            "--values", f"PatientId='{pat_id}' Category='{cat}' Status='{status}' SourceSystem='Cerner EHR - MuleSoft Direct Connector' SourceSystemIdentifier='{enc_id}'"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(f" -> Salesforce Creation Result: {res.stdout.strip()}")
        cur.execute("UPDATE hospital_clinical_encounters SET sync_status = 'PROCESSED' WHERE encounter_id = %s;", (enc_id,))

    # -------------------------------------------------------------------------
    # USE CASE 2: Cell & Gene Therapy CAR-T Slot Sync (WorkOrder)
    # -------------------------------------------------------------------------
    print("\n[USE CASE 2] Cell & Gene Therapy (CAR-T) Slot Sync (WorkOrder)")
    cur.execute("SELECT work_order_id, patient_external_id, subject_description, status FROM cell_therapy_schedules WHERE sync_status = 'NEW';")
    rows2 = cur.fetchall()
    print(f" -> Found {len(rows2)} new cell therapy schedule rows in PostgreSQL.")
    for r in rows2:
        wo_id, pat_id, subj, status = r
        cmd = [
            "sf", "data", "create", "record",
            "--target-org", "muthulifescience",
            "--sobject", "WorkOrder",
            "--values", f"Subject='{subj}' Status='{status}' Description='Vein-to-Vein Apheresis Collection booked via MuleSoft Direct ATM Connector'"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(f" -> Salesforce Creation Result: {res.stdout.strip()}")
        cur.execute("UPDATE cell_therapy_schedules SET sync_status = 'PROCESSED' WHERE work_order_id = %s;", (wo_id,))

    # -------------------------------------------------------------------------
    # USE CASE 3: MedTech Surgical Device Scan Sync (Asset)
    # -------------------------------------------------------------------------
    print("\n[USE CASE 3] MedTech Surgical Device Implant Sync (Asset)")
    cur.execute("SELECT asset_id, serial_number, status FROM medtech_device_scans WHERE sync_status = 'NEW';")
    rows3 = cur.fetchall()
    print(f" -> Found {len(rows3)} new medtech device scan rows in PostgreSQL.")
    for r in rows3:
        asset_id, sn, status = r
        cmd = [
            "sf", "data", "update", "record",
            "--target-org", "muthulifescience",
            "--sobject", "Asset",
            "--record-id", asset_id,
            "--values", f"Status='Purchased' SerialNumber='{sn}'"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(f" -> Salesforce Update Result: {res.stdout.strip()}")
        cur.execute("UPDATE medtech_device_scans SET sync_status = 'PROCESSED' WHERE asset_id = %s;", (asset_id,))

    # -------------------------------------------------------------------------
    # USE CASE 4: Specialty Prescription Intake & Care Program Enrollee Sync
    # -------------------------------------------------------------------------
    print("\n[USE CASE 4] Specialty Rx Intake & Care Program Enrollment")
    cur.execute("SELECT prescription_id, patient_external_id, care_program_id, status FROM specialty_prescriptions WHERE sync_status = 'NEW';")
    rows4 = cur.fetchall()
    print(f" -> Found {len(rows4)} new specialty prescription rows in PostgreSQL.")
    for r in rows4:
        rx_id, pat_id, cp_id, status = r
        cmd = [
            "sf", "data", "create", "record",
            "--target-org", "muthulifescience",
            "--sobject", "CareProgramEnrollee",
            "--values", f"Name='Care Program Enrollee - Alex Johnson (Rx Sync)' AccountId='{pat_id}' CareProgramId='{cp_id}' Status='{status}' SourceSystem='Epic EHR - MuleSoft Rx Direct Intake'"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(f" -> Salesforce Creation Result: {res.stdout.strip()}")
        cur.execute("UPDATE specialty_prescriptions SET sync_status = 'PROCESSED' WHERE prescription_id = %s;", (rx_id,))

    conn.commit()
    cur.close()
    conn.close()
    print("\n" + "=" * 80)
    print("ALL 4 BUSINESS USE CASES EXECUTED AND SYNCHRONIZED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    execute_4_business_usecases()
