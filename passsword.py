import pyttsx3 

def speak(text):
    print(text)
    engine = pyttsx3.init()          # fresh engine each time avoids "goes quiet" bug
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Human-friendly time formatter (your function)

def human_time(seconds):
    # Works with int or float
    if seconds < 1:
        return f"{seconds*1000:.1f} ms"
    intervals = [
        ("years", 60*60*24*365),
        ("days", 60*60*24),
        ("hours", 60*60),
        ("minutes", 60),
        ("seconds", 1),
    ]   
    parts = []
    rem = int(seconds)
    for name, sec_per in intervals:
        if rem >= sec_per:
            qty = rem // sec_per
            parts.append(f"{qty} {name}")
            rem = rem % sec_per
    return ", ".join(parts) if parts else "0 seconds"

SPECIALS = "!@#$%^&*()_+-=[]{}|;:,.<>?" 

def analyze_password(password):
    score = 0
    feedback = []
 
    if len(password) >= 12:
        score += 25
        feedback.append("Good length.")
    elif len(password) >= 8:
        score += 15
        feedback.append("Use at least 12 characters for better security.")
    else:
        score += 5
        feedback.append("Password is too short. Use at least 8 characters.")

    # Character classes
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIALS for c in password)

    char_types = sum([has_lower, has_upper, has_digit, has_special])
    score += char_types * 15

    if not has_lower:  feedback.append("Add lowercase letters.")
    if not has_upper:  feedback.append("Add uppercase letters.")
    if not has_digit:  feedback.append("Add numbers.")
    if not has_special: feedback.append("Add special characters.")

    # Common passwords
    common = ["password", "123456", "qwerty", "admin", "welcome"]
    if password.lower() in common:
        score -= 20
        feedback.append("This is a common password. Easy to guess.")

    # Repeats
    if any(password[i] == password[i+1] == password[i+2] for i in range(len(password)-2)):
        score -= 10
        feedback.append("Avoid repeating characters.")

    # Strength label
    if score >= 70:
        strength = "Strong"
    elif score >= 50:
        strength = "Moderate"
    elif score >= 30:
        strength = "Weak"
    else:
        strength = "Very Weak"

    # Estimate the brute-force search space from used character sets

    charset = 0
    if has_lower:  charset += 26
    if has_upper:  charset += 26
    if has_digit:  charset += 10
    if has_special: charset += len(SPECIALS)
    if charset == 0:
        charset = 1  # fallback

    # Expected guesses is half the space (average case)
    expected_guesses = pow(charset, len(password)) // 2

    # Threat models (guesses per second)
    rates = {
        "Online (rate-limited ~1/s)": 1,                 # conservative online
        "Offline (fast GPU ~1e10/s)": 10_000_000_000,    # rough modern GPU rig
    }

    crack_times = {
        label: human_time(expected_guesses // gps if gps > 0 else 0)
        for label, gps in rates.items()
    }

    return {
        "score": max(0, score),
        "strength": strength,
        "feedback": feedback,
        "crack_times": crack_times,
        "charset_size": charset
    }

# Main Code (every line speaks)

print("_"*55)
speak("Sir, Your Password Analyzer is activated.")

while True:
    speak("Please enter the password (Or 'quit' to exit:) :")
    password = input(": ")
 
    if password.lower() == 'quit':
        speak("Shutting Down. Stay Safe.")
        print("_"*55)
        break

    if not password:
        speak("Please enter a password:\t\n")
        continue

    result = analyze_password(password)

    speak(f"Password Strength: {result['strength']} with a score of {result['score']} out of 100.")
    speak(f"Character set size detected: {result['charset_size']}.")

    if result['feedback']:
        speak("Suggestions to improve your password:")
        for s in result['feedback']:
            speak(s)   
    else:
        speak("Great password. No improvements required.")

    speak("Estimated time to crack by brute force:")
    for label, t in result['crack_times'].items():
        speak(f"{label}: {t}")

    # speak("----------------------------------------")
