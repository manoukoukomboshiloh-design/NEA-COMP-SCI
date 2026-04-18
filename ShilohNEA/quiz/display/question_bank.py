import json
import os

USER_QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "user_questions.json")

question_data = {
    "topics": {
        "Measurements and their errors": {
            "notes": [
"SI prefixes represent powers of 10 used to express very large or very small quantities. Examples include: tera (10^12), giga (10^9), mega (10^6), kilo (10^3), centi (10^-2), milli (10^-3), micro (10^-6), nano (10^-9), pico (10^-12), femto (10^-15).",

"Random errors cause measurements to vary unpredictably. They affect precision and cannot be completely eliminated.",

"Random errors can be reduced by repeating measurements and calculating a mean, using digital equipment such as dataloggers or cameras, and using appropriate measuring instruments.",

"Systematic errors affect accuracy and cause measurements to be consistently too high or too low.",

"Systematic errors can be reduced by calibrating equipment, reading scales at eye level to avoid parallax error, and using control experiments.",

"Precision describes how close repeated measurements are to each other.",

"Accuracy describes how close a measurement is to the true or accepted value.",

"Repeatability means obtaining the same results when the experiment is repeated using the same method, equipment, and experimenter.",

"Reproducibility means obtaining the same results using different equipment, methods, or experimenters.",

"Absolute uncertainty is the uncertainty given as a fixed amount (e.g. ±0.1 cm).",

"Fractional uncertainty is the absolute uncertainty divided by the measured value.",

"Percentage uncertainty is the fractional uncertainty multiplied by 100.",

"Uncertainty in the gradient of a graph can be estimated by drawing the steepest and shallowest reasonable lines of best fit.",

"Physicists must be able to estimate orders of magnitude and approximate values of physical quantities."
            ],
            "questions": [
                {
                    "id": 1,
                    "question": "What do each of these prefixes mean and to what power of 10 are they?: T, G, M, k, c, m, μ, n, p, f?",
                    "answer": "Tera:12, Giga:9, Mega:6, kilo:3, centi:-2, milli:-3, micro:-6, nano:-9, pico:-12, femto:-15."
                },
                {
                    "id": 2,
                    "question": "What do random errors affect and what can't we do to them?",
                    "answer": "They affect precision, and we cannot get rid of them completely."
                },
                {
                    "id": 3,
                    "question": "Describe absolute, fractional and percentage uncertainty.",
                    "answer": "Absolute: uncertainty as a fixed quantity. Fractional: uncertainty as a fraction. Percentage: uncertainty as a percentage."
                },
                {
                    "id": 4,
                    "question": "How do you reduce random errors? Give 3 answers.",
                    "answer": "Take a minimum of 3 repeats and calculate a mean. Use computers, dataloggers or cameras. Use appropriate equipment."
                },
                {
                    "id": 5,
                    "question": "Describe the difference between precision and accuracy.",
                    "answer": "Precision describes the closeness of repeated measurements, whereas accuracy is how close a measurement is to the true value."
                },
                {
                    "id": 6,
                    "question": "What is the difference between repeatability and reproducibility?",
                    "answer": "Repeatability is getting the same results when the experiment is redone with the same method, equipment and experimenter. Reproducibility is getting the same results with different techniques, equipment or experimenters."
                },
                {
                    "id": 7,
                    "question": "What skill must physicists have in order to approximate the values of physical quantities?",
                    "answer": "Estimation."
                },
                {
                    "id": 8,
                    "question": "How can we find uncertainty in a gradient?",
                    "answer": "By drawing lines of best fit and worst fit."
                },
                {
                    "id": 9,
                    "question": "What is systematic error?",
                    "answer": "An error affecting accuracy, causing values to be too high or too low each time."
                },
                {
                    "id": 10,
                    "question": "How can systematic errors be reduced?",
                    "answer": "By calibrating apparatus, reading the meniscus at eye level to reduce parallax error, and using controls in experiments."
                }
            ]
        },

        "Particles": {
            "notes": [
"Specific charge is the charge-to-mass ratio of a particle (charge ÷ mass).",

"There are four fundamental interactions: gravitational, electromagnetic, strong nuclear, and weak nuclear.",

"Alpha decay emits two protons and two neutrons (a helium nucleus).",

"Beta-minus decay emits an electron and an antineutrino.",

"Annihilation occurs when a particle and its antiparticle meet and convert their mass into energy, producing two gamma photons moving in opposite directions.",

"Pair production occurs when a high-energy photon converts into a particle-antiparticle pair, usually an electron and a positron.",

"In electron capture the exchanged W boson is positive, whereas in electron-proton collisions the exchanged W boson is negative.",

"Leptons do not experience the strong nuclear interaction, whereas hadrons do.",

"Baryons eventually decay into a proton.",

"Strange particles are produced through the strong interaction but decay through the weak interaction."
            ],
            "questions": [
                {
                    "id": 11,
                    "question": "What is the specific charge of a particle?",
                    "answer": "The specific charge of a particle is the ratio of its charge to its mass."
                },
                {
                    "id": 12,
                    "question": "What are the 4 fundamental interactions?",
                    "answer": "Gravitational, electromagnetic, strong nuclear, weak nuclear."
                },
                {
                    "id": 13,
                    "question": "What is emitted during alpha decay?",
                    "answer": "2 protons and 2 neutrons, which is a helium nucleus."
                },
                {
                    "id": 14,
                    "question": "What is emitted during beta-minus decay?",
                    "answer": "An electron and an antineutrino."
                },
                {
                    "id": 15,
                    "question": "What is annihilation?",
                    "answer": "When a particle and its antiparticle meet, they annihilate and produce two gamma photons moving in opposite directions to conserve momentum."
                },
                {
                    "id": 16,
                    "question": "What is pair production?",
                    "answer": "Photon energy is converted into a particle-antiparticle pair, usually an electron and a positron."
                },
                {
                    "id": 17,
                    "question": "What is the difference between electron capture and electron-proton collisions?",
                    "answer": "The exchanged W boson in electron capture is positive, whereas in electron-proton collisions it is negative."
                },
                {
                    "id": 18,
                    "question": "What can leptons not do that hadrons can?",
                    "answer": "Leptons cannot interact via the strong nuclear force, whereas hadrons can."
                },
                {
                    "id": 19,
                    "question": "What do all baryons eventually decay into?",
                    "answer": "A proton."
                },
                {
                    "id": 20,
                    "question": "When are strange particles produced and how do they decay?",
                    "answer": "Strange particles are produced through the strong interaction and decay through the weak interaction."
                }
            ]
        },

        "EM Radiation": {
            "notes": [
"The photoelectric effect is the emission of electrons from a metal surface when electromagnetic radiation with a frequency above a certain threshold strikes the surface.",

"The work function is the minimum energy required to remove an electron from the surface of a metal.",

"The threshold frequency is the minimum frequency of electromagnetic radiation required to emit electrons from a metal surface.",

"Increasing the intensity of radiation increases the number of emitted electrons but does not increase their maximum kinetic energy.",

"Photon energy is given by E = hf, where h is Planck's constant and f is frequency.",

"Electrons can move to higher energy levels when they absorb energy through collisions; this process is called excitation.",

"When an excited electron returns to a lower energy level it emits a photon with energy equal to the energy difference between the levels.",

"A line spectrum consists of discrete wavelengths of light emitted by atoms as electrons transition between energy levels.",

"Light demonstrates wave-particle duality: it behaves as a wave in phenomena such as interference and diffraction, and as particles called photons in interactions such as the photoelectric effect.",

"The de Broglie wavelength states that particles have wave properties with wavelength λ = h / mv.",

"Discovering new particles in accelerators can take time because production rates are extremely low and large datasets are needed to identify them."
            ],
            "questions": [
                {
                    "id": 21,
                    "question": "What is the photoelectric effect?",
                    "answer": "The emission of electrons from a metal surface when electromagnetic radiation of a high enough frequency is incident on it."
                },
                {
                    "id": 22,
                    "question": "What is the difference between work function and threshold frequency?",
                    "answer": "The work function is the minimum energy needed to liberate an electron from the surface of a metal. Threshold frequency is the minimum frequency of incident radiation needed to liberate an electron from the surface of a metal."
                },
                {
                    "id": 23,
                    "question": "Explain why increasing the intensity of incident radiation does not increase the maximum kinetic energy of emitted electrons in the photoelectric effect.",
                    "answer": "Increasing the intensity increases the number of photons incident per second, but each photon still has the same energy, E = hf. Therefore the maximum kinetic energy remains unchanged."
                },
                {
                    "id": 24,
                    "question": "Electrons gain energy from collisions to move up energy levels in a process called what?",
                    "answer": "Excitation."
                },
                {
                    "id": 25,
                    "question": "What happens to the electron after excitation?",
                    "answer": "The electron returns to a lower energy level, emitting a photon with energy equal to the difference between the energy levels."
                },
                {
                    "id": 26,
                    "question": "What is meant by the term 'line spectrum'?",
                    "answer": "A line spectrum is a spectrum consisting of discrete lines at specific wavelengths, characteristic of the element emitting the radiation."
                },
                {
                    "id": 27,
                    "question": "What are the 4 fundamental interactions?",
                    "answer": "Gravitational, electromagnetic, strong nuclear, weak nuclear."
                },
                {
                    "id": 28,
                    "question": "How can light be both a wave and a particle?",
                    "answer": "Light shows wave-like properties such as interference and diffraction, but also particle-like properties because it can be quantised into photons that carry energy and momentum."
                },
                {
                    "id": 29,
                    "question": "What is the de Broglie wavelength?",
                    "answer": "The de Broglie wavelength is the wavelength associated with a particle of mass m moving at velocity v, given by λ = h / mv."
                },
                {
                    "id": 30,
                    "question": "Why does it take a while to discover new particles in particle accelerators?",
                    "answer": "The production rates of new particles can be very low, so large amounts of data and sophisticated analysis are needed to identify them amongst background noise."
                }
            ]
        },

        "Waves": {
            "notes": [
"The principle of superposition states that when waves overlap, the resultant displacement equals the vector sum of the individual displacements.",

"Coherent sources produce waves with a constant phase difference and the same frequency.",

"Constructive interference occurs when waves meet in phase and amplitudes add together.",

"Destructive interference occurs when waves meet out of phase and cancel each other out.",

"Diffraction is the spreading of waves when they pass through a gap or around an obstacle.",

"In longitudinal waves the oscillations are parallel to the direction of wave travel.",

"In transverse waves the oscillations are perpendicular to the direction of wave travel.",

"Polarisation is evidence that waves are transverse because the oscillations occur in one plane.",

"Phase difference describes the difference in phase between two points in a wave cycle.",

"The speed of a wave depends on the properties of the medium through which it travels.",

"Standing waves are formed when two waves of equal frequency travel in opposite directions and interfere, producing nodes and antinodes.",

"Wave frequency can be calculated using f = v / λ where v is wave speed and λ is wavelength."
            ],
            "questions": [
                {
                    "id": 31,
                    "question": "What is the principle of superposition?",
                    "answer": "When two or more waves overlap, the resultant displacement at any point is the vector sum of the displacements due to each individual wave."
                },
                {
                    "id": 32,
                    "question": "What is meant by coherent sources?",
                    "answer": "Waves that maintain a constant phase relationship with each other over time."
                },
                {
                    "id": 33,
                    "question": "What is the difference between constructive and destructive interference?",
                    "answer": "Constructive interference occurs when waves meet in phase, resulting in a larger amplitude. Destructive interference occurs when waves meet out of phase, resulting in a smaller amplitude or cancellation."
                },
                {
                    "id": 34,
                    "question": "What is meant by diffraction?",
                    "answer": "Diffraction is the bending of waves around obstacles or through openings, causing spreading and interference patterns."
                },
                {
                    "id": 35,
                    "question": "What is the difference between longitudinal waves and transverse waves?",
                    "answer": "In longitudinal waves, oscillations are parallel to the direction of travel. In transverse waves, oscillations are perpendicular to the direction of travel."
                },
                {
                    "id": 36,
                    "question": "How does polarisation demonstrate the transverse nature of waves?",
                    "answer": "Polarisation can only happen with transverse waves because their oscillations are perpendicular to the direction of propagation."
                },
                {
                    "id": 37,
                    "question": "What is meant by phase difference?",
                    "answer": "Phase difference is the difference in phase angle between two points on a wave, or between two waves at a given point."
                },
                {
                    "id": 38,
                    "question": "What factors affect the speed of a wave?",
                    "answer": "The medium it travels through and the properties of that medium."
                },
                {
                    "id": 39,
                    "question": "What is meant by standing waves?",
                    "answer": "Two waves of the same frequency and amplitude travelling in opposite directions interfere to produce nodes and antinodes."
                },
                {
                    "id": 40,
                    "question": "How can we calculate the frequency of a wave using its speed and wavelength?",
                    "answer": "Frequency = speed / wavelength."
                }
            ]
        },

        "Mechanics": {
            "notes": [
"Newton's First Law states that an object remains at rest or continues in uniform motion in a straight line unless acted upon by a resultant external force.",

"Newton's Second Law states that force equals mass multiplied by acceleration (F = ma).",

"Newton's Third Law states that for every action there is an equal and opposite reaction.",

"Scalar quantities have magnitude only, whereas vector quantities have both magnitude and direction.",

"Momentum is the product of mass and velocity (p = mv).",

"The principle of conservation of momentum states that the total momentum in a closed system remains constant.",

"Work done is the product of force and displacement in the direction of the force (W = Fd).",

"Kinetic energy is the energy an object has due to its motion and is given by KE = 1/2 mv².",

"Gravitational potential energy is energy stored due to height in a gravitational field and is given by PE = mgh.",

"Power is the rate of energy transfer or work done and is given by P = W / t."
            ],
            "questions": [
                {
                    "id": 41,
                    "question": "What is Newton's First Law of Motion?",
                    "answer": "An object remains at rest or continues in uniform motion in a straight line unless acted on by a resultant external force."
                },
                {
                    "id": 42,
                    "question": "What is Newton's Second Law of Motion?",
                    "answer": "The acceleration of an object is directly proportional to the resultant force acting on it and inversely proportional to its mass, F = ma."
                },
                {
                    "id": 43,
                    "question": "What is Newton's Third Law of Motion?",
                    "answer": "For every action there is an equal and opposite reaction."
                },
                {
                    "id": 44,
                    "question": "What is the difference between scalar and vector quantities?",
                    "answer": "Scalar quantities have magnitude only, whereas vector quantities have both magnitude and direction."
                },
                {
                    "id": 45,
                    "question": "What is meant by momentum?",
                    "answer": "Momentum is the product of an object's mass and velocity, p = mv."
                },
                {
                    "id": 46,
                    "question": "What is the principle of conservation of momentum?",
                    "answer": "In a closed system, the total momentum before an interaction is equal to the total momentum after the interaction."
                },
                {
                    "id": 47,
                    "question": "What is meant by work done?",
                    "answer": "Work done is the product of the force applied and the displacement in the direction of the force, W = Fd."
                },
                {
                    "id": 48,
                    "question": "What is kinetic energy?",
                    "answer": "Kinetic energy is the energy an object has because of its motion, KE = 1/2 mv^2."
                },
                {
                    "id": 49,
                    "question": "What is potential energy?",
                    "answer": "Potential energy is energy stored due to position or configuration, for example gravitational potential energy mgh."
                },
                {
                    "id": 50,
                    "question": "What is meant by power in physics?",
                    "answer": "Power is the rate at which work is done or energy is transferred, P = W / t."
                }
            ]
        }
    }
}


def _next_question_id(data):
    max_id = 0
    for topic_info in data.get("topics", {}).values():
        for question in topic_info.get("questions", []):
            max_id = max(max_id, int(question.get("id", 0)))
    return max_id + 1


def load_user_questions(data=None, json_path=USER_QUESTIONS_FILE):
    if data is None:
        data = question_data

    if not os.path.exists(json_path):
        return data

    try:
        with open(json_path, "r", encoding="utf-8") as handle:
            stored_data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return data

    next_id = _next_question_id(data)
    for topic, questions in stored_data.get("topics", {}).items():
        if topic not in data["topics"]:
            data["topics"][topic] = {"notes": [], "questions": []}

        existing_pairs = {
            (item.get("question", ""), item.get("answer", ""))
            for item in data["topics"][topic].get("questions", [])
        }

        for question in questions:
            pair = (question.get("question", "").strip(), question.get("answer", "").strip())
            if not pair[0] or not pair[1] or pair in existing_pairs:
                continue

            entry = {
                "id": int(question.get("id", next_id)),
                "question": pair[0],
                "answer": pair[1],
            }
            data["topics"][topic].setdefault("questions", []).append(entry)
            existing_pairs.add(pair)
            next_id = max(next_id, entry["id"] + 1)

    return data


def save_user_question(topic, question, answer, json_path=USER_QUESTIONS_FILE):
    topic = topic.strip()
    question = question.strip()
    answer = answer.strip()

    if not topic or not question or not answer:
        raise ValueError("Topic, question and answer cannot be blank.")

    stored_data = {"topics": {}}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as handle:
                stored_data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            stored_data = {"topics": {}}

    stored_data.setdefault("topics", {}).setdefault(topic, [])
    next_id = max(
        _next_question_id(question_data),
        1 + max(
            (int(item.get("id", 0)) for items in stored_data["topics"].values() for item in items),
            default=0,
        ),
    )

    new_entry = {
        "id": next_id,
        "question": question,
        "answer": answer,
    }
    stored_data["topics"][topic].append(new_entry)

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(stored_data, handle, indent=4)

    return new_entry


load_user_questions(question_data)