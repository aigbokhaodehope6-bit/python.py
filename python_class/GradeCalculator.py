score = int(input("Enter your grade score: "))
if score >= 90:
    print("Grade: A (Excellent)")
elif score >= 80:
    print("Grade: B (Good)")
elif score >= 70:
    print("Grade: C (Average)")
elif score >= 60:
    print("Grade: D (Below Average)")
else:
    print("Grade: F (Fail)")