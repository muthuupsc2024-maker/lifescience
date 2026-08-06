import psycopg2
import subprocess
import json

def run_mulesoft_pipeline():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="Admin1234"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT lab_id, patient_external_id, patient_full_name, test_code, numeric_value, unit_of_measure, result_status FROM hospital_patient_labs WHERE sync_status = 'NEW';")
    rows = cur.fetchall()
    
    print(f"[MuleSoft LSC Engine] Found {len(rows)} new patient lab records in PostgreSQL database.")
    
    for row in rows:
        lab_id, pat_id, pat_name, test_code, val, unit, status = row
        print(f" -> Processing Lab Record: {lab_id} | Patient: {pat_name} ({pat_id}) | Value: {val} {unit}")
        
        # DataWeave 2.0 Mapping into CareObservation SObject
        cmd = [
            "sf", "data", "create", "record",
            "--target-org", "muthulifescience",
            "--sobject", "CareObservation",
            "--values", f"Name='FHIR R4 Observation: {test_code}' ObservedSubjectId='{pat_id}' NumericValue={val} ObservedValueText='{val} {unit}' ObservationStatus='Final' Category='Laboratory' SourceSystem='Epic EHR - MuleSoft Direct PostgreSQL Pipeline' SourceSystemIdentifier='{lab_id}'"
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(f" -> Salesforce Record Creation Result: {res.stdout.strip()}")
        
        # Update PostgreSQL database sync_status = 'PROCESSED'
        cur.execute("UPDATE hospital_patient_labs SET sync_status = 'PROCESSED' WHERE lab_id = %s;", (lab_id,))
        print(f" -> Updated PostgreSQL sync_status = 'PROCESSED' for lab_id: {lab_id}")
        
    conn.commit()
    cur.close()
    conn.close()
    print("[MuleSoft LSC Engine] Pipeline execution finished cleanly!")

if __name__ == "__main__":
    run_mulesoft_pipeline()
