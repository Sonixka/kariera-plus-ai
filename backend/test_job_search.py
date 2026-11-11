from backend.services.job_search import search_jobs
from backend.services.job_matcher import calculate_job_match


results = search_jobs("Python")

print()
print("Počet nalezených nabídek:", len(results))
print()


for job in results[:10]:
    print("Pozice:", job["title"])
    print("Lokalita:", job["location"])
    print("Plat:", job["salary"])
    print("ID:", job["source_id"])
    print("Popis:", job["description"][:300])
    print("-" * 50)

print()
print("===== TEST AI SHODY =====")

test_skills = "Python, FastAPI, SQL, JavaScript"

for job in results:
    match = calculate_job_match(job, test_skills)

    print()
    print("Pozice:", job["title"])
    print("Shoda:", match["match_score"], "%")
    print("Úroveň:", match["match_level"])
    print("Splněné dovednosti:", match["matched_skills"])
    print("Chybějící dovednosti:", match["missing_skills"])
    print("Doporučení:", match["recommendation"])
    print("-" * 50)