from medquery.guardrails.topic import check_topic


def main() -> None:
    queries = [
    # Clearly medical
    "What are the symptoms of diabetes?",
    "What is insulin?",
    "Can high blood pressure be dangerous?",

    # Medical but without obvious medical terminology
    "Why am I feeling dizzy?",
    "I have been coughing for three weeks.",
    "What should I do about constant tiredness?",

    # Clearly non-medical
    "Who won the cricket match yesterday?",
    "What is the capital of France?",
    "How do I reverse a linked list in Java?",

    # Potentially tricky
    "What is a healthy diet?",
    "How can I sleep better?",
]

    for query in queries:
        result = check_topic(query)

        print(f"\nQuery: {query}")
        print(f"Allowed: {result.allowed}")
        print(f"Reason: {result.reason}")


if __name__ == "__main__":
    main()