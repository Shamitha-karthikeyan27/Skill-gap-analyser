import requests

BASE_URL = "http://127.0.0.1:5000/api"

def test_endpoints():
    try:
        # Test jobs
        print("Testing /jobs...")
        resp = requests.get(f"{BASE_URL}/jobs")
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            jobs = resp.json()
            print(f"Found {len(jobs)} jobs.")
            if jobs:
                job_id = jobs[0]['id']
                
                # Test companies
                print(f"Testing /companies?job_id={job_id}...")
                resp = requests.get(f"{BASE_URL}/companies", params={"job_id": job_id})
                print(f"Status: {resp.status_code}")
                
                # Test extract-skills
                print("Testing /extract-skills...")
                resp = requests.post(f"{BASE_URL}/extract-skills", json={"text": "I know Python and SQL."})
                print(f"Status: {resp.status_code}")
                
                # Test analyze
                print(f"Testing /analyze for job_id {job_id}...")
                resp = requests.post(f"{BASE_URL}/analyze", json={"skills": ["Python", "SQL"], "job_id": job_id})
                print(f"Status: {resp.status_code}")
                if resp.status_code == 200:
                    print("Analysis success.")
                else:
                    print(f"Analysis failed: {resp.text}")

    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    test_endpoints()
