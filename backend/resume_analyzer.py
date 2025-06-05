import google.generativeai as genai
 
genai.configure(api_key='AIzaSyAhaM-kcC5q3ke8ej3oPMjM5PRPVgyXP3s')
def analyze_resume(resume_text,job):
    if not resume_text:
        return {"error": "Resume text is required for analysis."}
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    base_prompt = f"""
    You are a professional resume evaluator for {job} job.Here's my resume:{resume_text}\nSo according to {job} job Please score it out of 100, point out key improvements, and suggest how to tailor it for a software engineer role. Also give a presise score more like a real world score and if the format of resume dosen't match to a regular format the give score as 0, Give the score in 1st 3spaces :
    """
    try:
        response = model.generate_content(base_prompt)
        analysis = response.text.strip()
    except Exception as e:
        analysis='Thenga'
        print(e)
    
    return analysis

