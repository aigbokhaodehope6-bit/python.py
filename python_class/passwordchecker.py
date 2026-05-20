import re
def check_password_strength(password):
  strength_score= 0

  if len(password) >= 8:
        strength_score += 1
  if re.search(r"[A-Z]", password):
        strength_score += 1
  if re.search(r"[a-z]", password):
        strength_score += 1
  if re.search(r"[0-9]", password):
        strength_score += 1
  if re.search(r"[#@$%&*!^<>:]", password):
        strength_score += 1

  if strength_score == 5:
     return "strong password"
  elif strength_score >= 3:
       return "Moderate password"
  else:
       return "weak password"
  
  
user_password = input("Enter a password to check;") 
result = check_password_strength(user_password)
print(result)
