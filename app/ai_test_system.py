import json
import random
from datetime import datetime

# --------------------------
# TEST QUESTION BANK
# --------------------------
question_bank = {
    "coding_proficiency": [
        {
            "id": 1,
            "question": "Write a Python function to check if a string is a palindrome.",
            "difficulty": "medium",
            "expected_keywords": ["def", "return", "==", "string[::-1]"]
        },
        {
            "id": 2,
            "question": "Implement a function to find the factorial of a number using recursion.",
            "difficulty": "easy",
            "expected_keywords": ["def", "return", "recursion"]
        },
        {
            "id": 3,
            "question": "Write a Python function to count the number of vowels in a string.",
            "difficulty": "easy",
            "expected_keywords": ["def", "for", "in", "return"]
        },
        {
            "id": 4,
            "question": "Implement a function to check if a number is prime.",
            "difficulty": "medium",
            "expected_keywords": ["def", "for", "if", "return"]
        },
        {
            "id": 5,
            "question": "Write a Python program to reverse the words in a sentence (not characters).",
            "difficulty": "medium",
            "expected_keywords": ["split", "join", "return"]
        },
        {
            "id": 6,
            "question": "Implement a function to compute the nth Fibonacci number iteratively.",
            "difficulty": "medium",
            "expected_keywords": ["for", "range", "return"]
        }
    ],
    "logic": [
        {
            "id": 1,
            "question": "A farmer has 17 sheep, all but 9 run away. How many are left?",
            "options": [8, 9, 17, 0],
            "answer": 9
        },
        {
            "id": 2,
            "question": "If 5 machines take 5 minutes to make 5 widgets, how long would 100 machines take to make 100 widgets?",
            "options": [5, 10, 50, 100],
            "answer": 5
        },
        {
            "id": 3,
            "question": "A bat and a ball cost ₹1.10. The bat costs ₹1 more than the ball. How much is the ball?",
            "options": [0.10, 0.05, 1.00, 0.15],
            "answer": 0.05
        },
        {
            "id": 4,
            "question": "If you have three apples and take away two, how many do you have?",
            "options": [1, 2, 3, 0],
            "answer": 2
        },
        {
            "id": 5,
            "question": "Two fathers and two sons go fishing. Each catches one fish, but only three fish are caught. How?",
            "options": [
                "One fish was shared",
                "One person lied",
                "They are grandfather, father, and son",
                "There was a counting mistake"
            ],
            "answer": "They are grandfather, father, and son"
        },
        {
            "id": 6,
            "question": "You have a 3L jug and a 5L jug. How do you measure exactly 4L?",
            "options": [
                "Fill 5L jug, pour into 3L jug twice",
                "Fill 5L jug, pour into 3L jug, empty 3L jug, pour remaining 2L into 3L jug, fill 5L jug again and pour into 3L jug till full",
                "Just fill 3L jug and measure",
                "Impossible"
            ],
            "answer": "Fill 5L jug, pour into 3L jug, empty 3L jug, pour remaining 2L into 3L jug, fill 5L jug again and pour into 3L jug till full"
        }
    ],
    "analytical": [
        {
            "id": 1,
            "question": "If the probability of rain tomorrow is 0.7, what is the probability it will not rain?",
            "options": [0.3, 0.7, 0.5, 1.0],
            "answer": 0.3
        },
        {
            "id": 2,
            "question": "A train travels 60 km in 1.5 hours. What is its average speed?",
            "options": [30, 40, 50, 60],
            "answer": 40
        },
        {
            "id": 3,
            "question": "The average of five numbers is 20. If one number is 10, what is the average of the remaining four?",
            "options": [22.5, 20, 25, 21.25],
            "answer": 22.5
        },
        {
            "id": 4,
            "question": "A bag contains 6 red and 4 blue balls. What is the probability of drawing a red ball?",
            "options": [0.4, 0.5, 0.6, 0.7],
            "answer": 0.6
        },
        {
            "id": 5,
            "question": "If A = 60% of B, and B = 120% of C, what percent of C is A?",
            "options": [50, 60, 72, 80],
            "answer": 72
        },
        {
            "id": 6,
            "question": "A number is increased by 20% and then decreased by 20%. What is the net change?",
            "options": ["No change", "Increase of 4%", "Decrease of 4%", "Decrease of 20%"],
            "answer": "Decrease of 4%"
        }
    ],
    "mathematics": [
        # ---- 12th Grade Level ----
        {
            "id": 1,
            "question": "Differentiate: f(x) = x^3 + 5x^2 - 4x + 7",
            "options": ["3x^2 + 10x - 4", "3x^2 + 5x - 4", "x^3 + 10x - 4", "3x^2 + 10x + 4"],
            "answer": "3x^2 + 10x - 4"
        },
        {
            "id": 2,
            "question": "If sin²θ + cos²θ = 1 and sinθ = 3/5, find cosθ.",
            "options": ["4/5", "3/5", "√3/5", "1/5"],
            "answer": "4/5"
        },
        # ---- College Level ----
        {
            "id": 3,
            "question": "Find the determinant of the matrix [[1, 2], [3, 4]]",
            "options": [-2, -1, 2, 1],
            "answer": -2
        },
        {
            "id": 4,
            "question": "Evaluate the integral ∫ x² dx",
            "options": ["x³/3 + C", "x²/2 + C", "2x + C", "3x² + C"],
            "answer": "x³/3 + C"
        },
        # ---- Tricky Algebra ----
        {
            "id": 5,
            "question": "If x + 1/x = 4, find x² + 1/x².",
            "options": [14, 15, 16, 8],
            "answer": 14
        },
        {
            "id": 6,
            "question": "Solve for x: 2x + 3 = 7",
            "options": [2, 3, 4, 5],
            "answer": 2
        }
    ]
}

# --------------------------
# TEST GENERATION FUNCTION
# --------------------------
def generate_test(user_id, category=None, num_questions=2):
    test = {}
    selected_categories = [category] if category else question_bank.keys()

    for cat in selected_categories:
        test[cat] = random.sample(question_bank[cat], min(num_questions, len(question_bank[cat])))

    test_metadata = {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "test": test
    }

    return test_metadata


# --------------------------
# EVALUATION FUNCTION
# --------------------------
def evaluate_test(user_answers, test_data):
    score = {cat: 0 for cat in test_data['test'].keys()}
    max_score = {cat: len(qs) for cat, qs in test_data['test'].items()}

    for cat, questions in test_data['test'].items():
        for q in questions:
            q_id = q['id']
            if cat == "coding_proficiency":
                # Just keyword-based scoring (you can integrate AI code evaluator later)
                if any(keyword in user_answers.get(cat, {}).get(str(q_id), "") for keyword in q['expected_keywords']):
                    score[cat] += 1
            else:
                if user_answers.get(cat, {}).get(str(q_id)) == q['answer']:
                    score[cat] += 1

    return {"score": score, "max_score": max_score}


# ------------------------------
# BACKEND CONNECTION SIMULATION
# ------------------------------
if __name__ == "__main__":
    # Step 1: Generate a test
    user_id = "user_123"
    test_data = generate_test(user_id)
    print("Generated Test:\n", json.dumps(test_data, indent=2))

    # Step 2: Simulated User Answers
    user_answers = {
        "logic": {"1": 9},
        "analytical": {"2": 40},
        "coding_proficiency": {"1": "def is_palindrome(s): return s == s[::-1]"},
        "mathematics": {"1": "3x^2 + 10x - 4"}
    }

    # Step 3: Evaluate Test
    result = evaluate_test(user_answers, test_data)
    print("\nEvaluation Result:\n", json.dumps(result, indent=2))
