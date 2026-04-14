graph = { "Measurements and their errors": ["Waves"],
          "Particles": ["EM Radiation"],
            "EM Radiation": ["Waves"],
              "Waves": ["Mechanics"],
                "Mechanics": ["Waves"] }

def next_step(score, selected_topic, data):
    print("What next?")

    if score >= 4:
        next_topics = graph.get(selected_topic, [])

        if next_topics:
            print(f"Since you're so good, why don't you try: {next_topics[0]}")

            answer = input("Enter yes to continue or no to return to menu: ")

            if answer.lower() == "yes":
                next_topic = get_next_topic(selected_topic, graph)
                if next_topic:
                    get_questions(next_topic, data)

    else:
        print("Ah that didn't go to plan but it's ok!")
        print("1. Stay on this topic")
        print("2. Switch topics")
        print("q. Quit")

        choice = input("The choice is yours...: ")

        if choice == "1":
            show_topic_notes(selected_topic, data)

        elif choice == "2":
            new_topic = display_menu(data)
            if new_topic:
                get_questions(new_topic, data)

        elif choice == "q":
            print("We're in the learning phase, take a break and hit back stronger!")

        else:
            print("Not a valid response")