import pandas as pd

print("🔄 Generating Natural Language Semantic Counseling Dataset...")

# We map multiple natural phrases to the same professional counseling remedies
counseling_matrix = {
    "Questions": [
        # --- Academic / Grade Concerns (Simple/Natural Language) ---
        "I am failing my classes and my marks are terrible.",
        "my gpa is so low i'm going to fail this semester.",
        "I don't understand anything the professor is teaching, it's too hard.",
        "I'm falling behind in my programming and algorithm courses help.",
        "I missed my assignment deadlines what should I do now?",
        "I am so stressed about my upcoming engineering exams.",
        
        # --- Attendance Concerns (Simple/Natural Language) ---
        "I missed too many classes because I was sick, will I get detained?",
        "my attendance percentage is dropping fast how do I fix it?",
        "I haven't been going to college lately and I'm scared about attendance.",
        
        # --- Financial / Fee Concerns (Simple/Natural Language) ---
        "I don't have money to pay my college fees this semester.",
        "I'm completely broke and my family is under huge financial strain.",
        "I have a big outstanding balance on my student portal and I'm scared.",
        "Can I get a scholarship or a fee waiver because I can't afford college?",
        "Is there an installment plan for clearing my university registration dues?",
        
        # --- Burnout / Emotional Concerns (Simple/Natural Language) ---
        "I feel completely exhausted and just want to quit college.",
        "Academic pressure is causing me massive burnout and panic attacks.",
        "I feel lonely at university and don't have any friends or support groups.",
        "I am feeling so anxious about campus placement drives and getting a job."
    ],
    "Answers": [
        # --- Academic Responses ---
        "### 📋 Academic Recovery Action Plan\n\nI hear you, and it's completely normal to hit a rough patch with dense engineering subjects. Let's fix this step-by-step:\n\n1. **Use the 25-Minute Rule (Pomodoro):** Break your syllabus down into tiny chunks. Study hard with zero distractions for 25 minutes, then walk away for 5.\n2. **Free Peer-Tutoring Registry:** Check your student portal. You can sign up to get paired with a senior student who aced this exact class last semester. They can explain the logic in simple, casual terms.\n3. **Office Hours:** Don't hesitate to message your professor directly for a 10-minute review session. They appreciate students who show a proactive attitude.",
        "### 📋 Academic Recovery Action Plan\n\nI hear you, and it's completely normal to hit a rough patch with dense engineering subjects. Let's fix this step-by-step:\n\n1. **Use the 25-Minute Rule (Pomodoro):** Break your syllabus down into tiny chunks. Study hard with zero distractions for 25 minutes, then walk away for 5.\n2. **Free Peer-Tutoring Registry:** Check your student portal. You can sign up to get paired with a senior student who aced this exact class last semester. They can explain the logic in simple, casual terms.\n3. **Office Hours:** Don't hesitate to message your professor directly for a 10-minute review session. They appreciate students who show a proactive attitude.",
        "### 📋 Academic Recovery Action Plan\n\nI hear you, and it's completely normal to hit a rough patch with dense engineering subjects. Let's fix this step-by-step:\n\n1. **Use the 25-Minute Rule (Pomodoro):** Break your syllabus down into tiny chunks. Study hard with zero distractions for 25 minutes, then walk away for 5.\n2. **Free Peer-Tutoring Registry:** Check your student portal. You can sign up to get paired with a senior student who aced this exact class last semester. They can explain the logic in simple, casual terms.\n3. **Office Hours:** Don't hesitate to message your professor directly for a 10-minute review session. They appreciate students who show a proactive attitude.",
        "### 💻 Practical Programming Solutions\n\nCoding logic takes time to build. Focus on writing small, working blocks of code rather than massive programs. Practice basic array/string structures daily on free sandboxes, and utilize visual debugging tools to see exactly how your variables change at each line step.",
        "### 📝 Assignment Deadline Protocol\n\nWrite a polite, honest email to your course instructor *before* the evaluations close. Explain the genuine reason for the delay and submit whatever percentage of work you have finished. Most faculty members grant partial credit for honesty rather than unexcused absences.",
        "### 📋 Academic Recovery Action Plan\n\nI hear you, and it's completely normal to hit a rough patch with dense engineering subjects. Let's fix this step-by-step:\n\n1. **Use the 25-Minute Rule (Pomodoro):** Break your syllabus down into tiny chunks. Study hard with zero distractions for 25 minutes, then walk away for 5.\n2. **Free Peer-Tutoring Registry:** Check your student portal. You can sign up to get paired with a senior student who aced this exact class last semester. They can explain the logic in simple, casual terms.\n3. **Office Hours:** Don't hesitate to message your professor directly for a 10-minute review session. They appreciate students who show a proactive attitude.",
        
        # --- Attendance Responses ---
        "### 📊 Attendance Recovery Strategy\n\nFirst, breathe—this is a solvable problem. Go see your course coordinator immediately. Bring official documentation (like a medical certificate) to formally explain your absences. Moving forward, prioritize attending remaining lectures and request extra credit assignments to make up for missed class marks.",
        "### 📊 Attendance Recovery Strategy\n\nFirst, breathe—this is a solvable problem. Go see your course coordinator immediately. Bring official documentation (like a medical certificate) to formally explain your absences. Moving forward, prioritize attending remaining lectures and request extra credit assignments to make up for missed class marks.",
        "### 📊 Attendance Recovery Strategy\n\nFirst, breathe—this is a solvable problem. Go see your course coordinator immediately. Bring official documentation (like a medical certificate) to formally explain your absences. Moving forward, prioritize attending remaining lectures and request extra credit assignments to make up for missed class marks.",
        
        # --- Financial Responses ---
        "### 🛡️ Financial Support Action Plan\n\nFinancial constraints are systemic challenges—they do not define your potential or worth as a student. Let's review your options:\n\n1. **Fee Deferral:** Visit the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This can freeze late penalties and buy your family more time.\n2. **Library Book Banks:** Avoid out-of-pocket textbook expenses by registering for your campus library's book-bank system, which lets you borrow core curriculum books for free all semester.\n3. **Emergency Grants:** Ask an administrator about mid-semester student aid funds or NGO-backed stipends available on the portal.",
        "### 🛡️ Financial Support Action Plan\n\nFinancial constraints are systemic challenges—they do not define your potential or worth as a student. Let's review your options:\n\n1. **Fee Deferral:** Visit the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This can freeze late penalties and buy your family more time.\n2. **Library Book Banks:** Avoid out-of-pocket textbook expenses by registering for your campus library's book-bank system, which lets you borrow core curriculum books for free all semester.\n3. **Emergency Grants:** Ask an administrator about mid-semester student aid funds or NGO-backed stipends available on the portal.",
        "### 🛡️ Financial Support Action Plan\n\nFinancial constraints are systemic challenges—they do not define your potential or worth as a student. Let's review your options:\n\n1. **Fee Deferral:** Visit the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This can freeze late penalties and buy your family more time.\n2. **Library Book Banks:** Avoid out-of-pocket textbook expenses by registering for your campus library's book-bank system, which lets you borrow core curriculum books for free all semester.\n3. **Emergency Grants:** Ask an administrator about mid-semester student aid funds or NGO-backed stipends available on the portal.",
        "### 🛡️ Financial Support Action Plan\n\nFinancial constraints are systemic challenges—they do not define your potential or worth as a student. Let's review your options:\n\n1. **Fee Deferral:** Visit the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This can freeze late penalties and buy your family more time.\n2. **Library Book Banks:** Avoid out-of-pocket textbook expenses by registering for your campus library's book-bank system, which lets you borrow core curriculum books for free all semester.\n3. **Emergency Grants:** Ask an administrator about mid-semester student aid funds or NGO-backed stipends available on the portal.",
        "### 🛡️ Financial Support Action Plan\n\nFinancial constraints are systemic challenges—they do not define your potential or worth as a student. Let's review your options:\n\n1. **Fee Deferral:** Visit the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This can freeze late penalties and buy your family more time.\n2. **Library Book Banks:** Avoid out-of-pocket textbook expenses by registering for your campus library's book-bank system, which lets you borrow core curriculum books for free all semester.\n3. **Emergency Grants:** Ask an administrator about mid-semester student aid funds or NGO-backed stipends available on the portal.",
        
        # --- Burnout Responses ---
        "### 🧠 Burnout & Neural Recovery Framework\n\nExhaustion is a physical signal that your nervous system is overloaded, not a sign of weakness. Take a complete 24-hour break from books and screens. Prioritize 8 hours of sleep tonight, and let us help you set up an informal, private talk with a supportive campus advisor to safely scale back your workload pressure.",
        "### 🧠 Burnout & Neural Recovery Framework\n\nExhaustion is a physical signal that your nervous system is overloaded, not a sign of weakness. Take a complete 24-hour break from books and screens. Prioritize 8 hours of sleep tonight, and let us help you set up an informal, private talk with a supportive campus advisor to safely scale back your workload pressure.",
        "### 🤝 Community & Connection Support\n\nUniversity is a massive social adjustment. The quickest way to build genuine friendships is through shared goals. Try joining a student-run coding club, campus sports society, or signing up as a volunteer for upcoming hackathons. Working together on small projects breaks the ice naturally.",
        "### 🚀 Placement Anxiety Guidance\n\nAnxiety about your career is incredibly common. Turn that nervous energy into action by setting up mock interviews with your teammates. Focus your energy on building 2 clean, functional full-stack projects on GitHub to anchor your resume, rather than trying to memorize everything at once."
    ]
}

df_clean = pd.DataFrame(counseling_matrix)
df_clean.to_csv("counseling_data.csv", index=False)
print(f"💾 Dataset compiled! Created {len(df_clean)} natural semantic rows successfully.")