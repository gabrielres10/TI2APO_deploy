from experta import *
from .models import BotMessage


class BipolarExpertSystem(KnowledgeEngine):

    user = None
    
    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='yes'), Fact(stress_management='yes')))
    def advice_1(self):
        self.declare(Fact(advice='Self-compassion: Be kind to yourself. Accept your limitations and celebrate your achievements, no matter how small they are.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='yes'), Fact(stress_management='no')))
    def advice_2(self):
        self.declare(Fact(advice='Stress management: Practice relaxation techniques such as meditation, yoga, or deep breathing to manage stress.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='no'), Fact(stress_management='yes')))
    def advice_3(self):
        self.declare(Fact(advice='Keeping a journal: Recording your emotions, thoughts, and sleep patterns can help you identify triggers and patterns in your behavior.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='no'), Fact(stress_management='no')))
    def advice_4(self):
        self.declare(Fact(advice='Daily plan: Have an action plan throughout the day, including activities that allow you to have a good time to relieve stress, such as exercising, studying, reading, drawing, etc.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='yes'), Fact(stress_management='yes')))
    def advice_5(self):
        self.declare(Fact(advice='Learn to identify your triggers: Recognize which situations or factors tend to trigger episodes so you can manage them better.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='yes'), Fact(stress_management='no')))
    def advice_6(self):
        self.declare(Fact(advice='Complementary therapies: Consider alternative therapies such as acupuncture, aromatherapy, or massage to complement your treatment.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='no'), Fact(stress_management='yes')))
    def advice_7(self):
        self.declare(Fact(advice='Social support: Keep in touch with friends and family. Don’t hesitate to ask for support when you need it.'))

    @Rule(AND(Fact(difficult_daily_schedule='yes'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='no'), Fact(stress_management='no')))
    def advice_8(self):
        self.declare(Fact(advice='Medication and therapy: Follow your doctor’s instructions and attend your therapy sessions. It’s crucial not to abandon treatment without consulting first.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='yes'), Fact(stress_management='yes')))
    def advice_9(self):
        self.declare(Fact(advice='Avoid alcohol and drugs: These substances can interfere with your treatment and worsen bipolar disorder symptoms.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='yes'), Fact(stress_management='no')))
    def advice_10(self):
        self.declare(Fact(advice='Sleep well: Ensure you have a good sleep routine. Sleep quality can significantly affect your mood.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='no'), Fact(stress_management='yes')))
    def advice_11(self):
        self.declare(Fact(advice='Maintain consistency in treatment: Don’t make changes to your medication or treatment without consulting your doctor.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='yes'), Fact(regular_exercise='no'), Fact(stress_management='no')))
    def advice_12(self):
        self.declare(Fact(advice='Physical exercise: Regular physical activity can improve your mood and reduce symptoms of depression and anxiety.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='yes'), Fact(stress_management='yes')))
    def advice_13(self):
        self.declare(Fact(advice='Education: Inform yourself about bipolar disorder. The more you know, the better you can manage it.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='yes'), Fact(stress_management='no')))
    def advice_14(self):
        self.declare(Fact(advice='Healthy eating: Maintain a balanced diet to support your mental and physical health. Adequate nutrients can influence your mood.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='no'), Fact(stress_management='yes')))
    def advice_15(self):
        self.declare(Fact(advice='Set realistic goals: Set achievable and realistic objectives to stay away from stress and frustration that can trigger episodes.'))

    @Rule(AND(Fact(difficult_daily_schedule='no'), Fact(medical_treatment_adherence='no'), Fact(regular_exercise='no'), Fact(stress_management='no')))
    def advice_16(self):
        self.declare(Fact(advice='Establish a routine: Keeping regular schedules for sleeping, eating, and exercising can help stabilize your mood.'))
    
    @Rule(Fact(difficult_daily_schedule=MATCH.difficult_daily_schedule), Fact(medical_treatment_adherence=MATCH.medical_treatment_adherence),
        Fact(regular_exercise=MATCH.regular_exercise), Fact(stress_management=MATCH.stress_management), Fact(advice=MATCH.advice))
    def show_advice(self, advice):
        BotMessage.objects.create(user=self.user, content=advice)


    @classmethod
    def set_user(self, user):
        self.user = user

    @classmethod
    def ask_for_options(self):
        content = """
        Since <span>Bipolarity</span> is the disorder that you most likely have, Let's make a little
        exploratory questions in order to find a good advice for you.

        <br><br>
        Do you find it difficult to maintain a daily routine? (yes/no): <br>
        Do you regularly follow your medical and therapeutic treatment? (yes/no): <br>
        Do you exercise regularly? (yes/no): <br>
        Do you feel you have good stress management? (yes/no): <br><br>

        Remeber the separation of the answers. For example: (yes, no, no, yes)
        """
        BotMessage.objects.create(user=self.user, content=content)


    @classmethod
    def run_expert_system(self, options):
        expert_system = BipolarExpertSystem()
        expert_system.reset()

        difficult_schedule = options[0]
        medical_treatment = options[1]
        exercise = options[2]
        stress_management = options[3]
        

        expert_system.declare(Fact(difficult_daily_schedule=difficult_schedule))
        expert_system.declare(Fact(medical_treatment_adherence=medical_treatment))
        expert_system.declare(Fact(regular_exercise=exercise))
        expert_system.declare(Fact(stress_management=stress_management))

        expert_system.run()


class DepressionExpertSystem(KnowledgeEngine):

    user = None

    # Combination 1: Yes, Yes, Yes, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='yes'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='yes')))
    def advice_1(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Improve your sleep with a regular routine. Seek social support to combat the feeling of isolation. Cognitive-behavioral therapy (CBT) can help you with persistent negative thoughts.'))

    # Combination 2: Yes, Yes, Yes, No
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='yes'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='no')))
    def advice_2(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Improve your sleep with a regular routine. Seek social support to combat the feeling of isolation. It’s positive that you don’t have persistent negative thoughts.'))

    # Combination 3: Yes, Yes, No, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='yes'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='yes')))
    def advice_3(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Improve your sleep with a regular routine. Even though you don’t feel isolated, maintain your social connections. CBT can help you manage persistent negative thoughts.'))

    # Combination 4: Yes, Yes, No, No
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='yes'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='no')))
    def advice_4(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Improve your sleep with a regular routine. Even though you don’t feel isolated or have persistent negative thoughts, these changes can improve your overall well-being.'))

    # Combination 5: Yes, No, Yes, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='no'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='yes')))
    def advice_5(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Seek social support to combat the feeling of isolation. CBT can help you with persistent negative thoughts. Fortunately, you don’t have sleep problems.'))

    # Combination 6: Yes, No, Yes, No
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='no'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='no')))
    def advice_6(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Seek social support to combat the feeling of isolation. It’s positive that you don’t have sleep problems or persistent negative thoughts.'))

    # Combination 7: Yes, No, No, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='no'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='yes')))
    def advice_7(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Even though you don’t have sleep problems or feel isolated, CBT can help you manage persistent negative thoughts.'))

    # Combination 8: Yes, No, No, No
    @Rule(AND(Fact(difficulty_finding_motivation='yes'), Fact(sleep_problems='no'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='no')))
    def advice_8(self):
        self.declare(Fact(advice='Set small achievable goals: Start with simple tasks and gradually increase the difficulty. Even though you don’t have sleep problems, social isolation, or persistent negative thoughts, improving your motivation can benefit your overall well-being.'))

    # Combination 9: No, Yes, Yes, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='yes'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='yes')))
    def advice_9(self):
        self.declare(Fact(advice='Improve your sleep with a regular routine. Seek social support to combat the feeling of isolation. CBT can help you manage persistent negative thoughts. It’s positive that you don’t have motivation problems.'))

    # Combination 10: No, Yes, Yes, No
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='yes'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='no')))
    def advice_10(self):
        self.declare(Fact(advice='Improve your sleep with a regular routine. Seek social support to combat the feeling of isolation. It’s positive that you don’t have motivation problems or persistent negative thoughts.'))

    # Combination 11: No, Yes, No, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='yes'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='yes')))
    def advice_11(self):
        self.declare(Fact(advice='Improve your sleep with a regular routine. Even though you don’t have motivation problems or feel isolated, CBT can help you manage persistent negative thoughts.'))

    # Combination 12: No, Yes, No, No
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='yes'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='no')))
    def advice_12(self):
        self.declare(Fact(advice='Improve your sleep with a regular routine. Even though you don’t have motivation problems, social isolation, or persistent negative thoughts, improving your sleep can benefit your overall well-being.'))

    # Combination 13: No, No, Yes, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='no'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='yes')))
    def advice_13(self):
        self.declare(Fact(advice='Seek social support to combat the feeling of isolation. CBT can help you manage persistent negative thoughts. It’s positive that you don’t have motivation or sleep problems.'))

    # Combination 14: No, No, Yes, No
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='no'), Fact(feel_isolated='yes'), Fact(persistent_negative_thoughts='no')))
    def advice_14(self):
        self.declare(Fact(advice='Seek social support to combat the feeling of isolation. It’s positive that you don’t have motivation, sleep problems, or persistent negative thoughts.'))

    # Combination 15: No, No, No, Yes
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='no'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='yes')))
    def advice_15(self):
        self.declare(Fact(advice='CBT can help you manage persistent negative thoughts. It’s positive that you don’t have motivation, sleep, or social isolation problems.'))

    # Combination 16: No, No, No, No
    @Rule(AND(Fact(difficulty_finding_motivation='no'), Fact(sleep_problems='no'), Fact(feel_isolated='no'), Fact(persistent_negative_thoughts='no')))
    def advice_16(self):
        self.declare(Fact(advice='It’s positive that you don’t have any of these symptoms. If difficulties arise at any time, don’t hesitate to seek professional help to address them promptly.'))
    
    @Rule(Fact(difficulty_finding_motivation=MATCH.difficulty_finding_motivation), Fact(sleep_problems=MATCH.sleep_problems),
          Fact(feel_isolated=MATCH.feel_isolated), Fact(persistent_negative_thoughts=MATCH.persistent_negative_thoughts),
          Fact(advice=MATCH.advice))
    def show_advice(self, advice):
        BotMessage.objects.create(user=self.user, content=advice)


    @classmethod
    def set_user(self, user):
        self.user = user


    @classmethod
    def ask_for_options(self):
        content = """
        Since <span>Depression</span> is the disorder that you most likely have, Let's make a little
        exploratory questions in order to find a good advice for you.

        <br><br>
        Do you have trouble finding motivation for daily activities? (yes/no): <br>
        Do you have difficulty sleeping or do you oversleep? (yes/no): <br>
        Do you feel socially isolated? (yes/no): <br>
        Do you have persistent negative thoughts? (yes/no): <br><br>

        Remeber the separation of the answers. For example: (yes, no, no, yes)
        """
        BotMessage.objects.create(user=self.user, content=content)

    @classmethod
    def run_expert_system(self, options):
        expert_system = DepressionExpertSystem()
        expert_system.reset()

        difficulty_motivation = options[0]
        sleep_problems = options[1]
        feel_isolated = options[2]
        persistent_thoughts = options[3]
        

        expert_system.declare(Fact(difficulty_finding_motivation=difficulty_motivation))
        expert_system.declare(Fact(sleep_problems=sleep_problems))
        expert_system.declare(Fact(feel_isolated=feel_isolated))
        expert_system.declare(Fact(persistent_negative_thoughts=persistent_thoughts))

        expert_system.run()



class AnxietyExpertSystem(KnowledgeEngine):

    user = None

    # Combination 1: Yes, Yes, Yes, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='yes')))
    def advice_1(self):
        self.declare(Fact(advice='Try relaxation and stress management techniques. Gradual exposure and cognitive behavioral therapy (CBT) can help you.'))

    # Combination 2: Yes, Yes, Yes, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='no')))
    def advice_2(self):
        self.declare(Fact(advice='Try relaxation and stress management techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 3: Yes, Yes, No, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='yes')))
    def advice_3(self):
        self.declare(Fact(advice='Try relaxation techniques. CBT can help you with anxious thoughts.'))

    # Combination 4: Yes, Yes, No, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='no')))
    def advice_4(self):
        self.declare(Fact(advice='Try relaxation techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 5: Yes, No, Yes, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='yes')))
    def advice_5(self):
        self.declare(Fact(advice='Try relaxation techniques. Gradual exposure and CBT can help you.'))

    # Combination 6: Yes, No, Yes, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='no')))
    def advice_6(self):
        self.declare(Fact(advice='Try relaxation techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 7: Yes, No, No, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='yes')))
    def advice_7(self):
        self.declare(Fact(advice='Try relaxation techniques. CBT can help you.'))

    # Combination 8: Yes, No, No, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='yes'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='no')))
    def advice_8(self):
        self.declare(Fact(advice='Try relaxation techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 9: No, Yes, Yes, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='yes')))
    def advice_9(self):
        self.declare(Fact(advice='Try stress management techniques. Gradual exposure and CBT can help you.'))

    # Combination 10: No, Yes, Yes, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='no')))
    def advice_10(self):
        self.declare(Fact(advice='Try stress management techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 11: No, Yes, No, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='yes')))
    def advice_11(self):
        self.declare(Fact(advice='Try stress management techniques. CBT can help you.'))

    # Combination 12: No, Yes, No, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='yes'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='no')))
    def advice_12(self):
        self.declare(Fact(advice='Try stress management techniques. It is positive that you do not have persistent anxious thoughts.'))

    # Combination 13: No, No, Yes, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='yes')))
    def advice_13(self):
        self.declare(Fact(advice='Gradual exposure and CBT can help you.'))

    # Combination 14: No, No, Yes, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='yes'), Fact(persistent_anxious_thoughts='no')))
    def advice_14(self):
        self.declare(Fact(advice='Gradual exposure can help you.'))

    # Combination 15: No, No, No, Yes
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='yes')))
    def advice_15(self):
        self.declare(Fact(advice='CBT can help you.'))

    # Combination 16: No, No, No, No
    @Rule(AND(Fact(anxiety_interferes_with_relaxation='no'), Fact(difficulty_managing_daily_stress='no'), Fact(avoidance_due_to_anxiety='no'), Fact(persistent_anxious_thoughts='no')))
    def advice_16(self):
        self.declare(Fact(advice='Everything seems to be fine at this moment.'))

    @Rule(Fact(anxiety_interferes_with_relaxation=MATCH.anxiety_interferes_with_relaxation), Fact(difficulty_managing_daily_stress=MATCH.difficulty_managing_daily_stress),
          Fact(avoidance_due_to_anxiety=MATCH.avoidance_due_to_anxiety), Fact(persistent_anxious_thoughts=MATCH.persistent_anxious_thoughts),
          Fact(advice=MATCH.advice))
    def show_advice(self, advice):
        BotMessage.objects.create(user=self.user, content=advice)


    @classmethod
    def set_user(self, user):
        self.user = user


    @classmethod
    def ask_for_options(self):
        content = """
        Since <span>Anxiety</span> is the disorder that you most likely have, Let's make a little
        exploratory questions in order to find a good advice for you.

        <br><br>
        Do you feel that your anxiety interferes with your ability to relax and rest? (yes/no): <br>
        Do you have difficulties managing daily stress? (yes/no): <br>
        Do you tend to avoid situations or activities due to anxiety? (yes/no): <br>
        Do you have persistent anxious thoughts that you cannot control? (yes/no): <br><br>

        Remeber the separation of the answers. For example: (yes, no, no, yes)
        """
        BotMessage.objects.create(user=self.user, content=content)

    @classmethod
    def run_expert_system(self, options):
        expert_system = AnxietyExpertSystem()
        expert_system.reset()

        anxiety_relaxation = options[0]
        daily_stress = options[1]
        avoidance = options[2]
        persistent_thoughts = options[3]
        

        expert_system.declare(Fact(anxiety_interferes_with_relaxation=anxiety_relaxation))
        expert_system.declare(Fact(difficulty_managing_daily_stress=daily_stress))
        expert_system.declare(Fact(avoidance_due_to_anxiety=avoidance))
        expert_system.declare(Fact(persistent_anxious_thoughts=persistent_thoughts))

        expert_system.run()



class TraumaExpertSystem(KnowledgeEngine):

    user = None
    
    # Combination 1: Yes, Yes, Yes, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='yes')))
    def advice_1(self):
        self.declare(Fact(advice="Flashbacks and intrusive memories are common phenomena after a traumatic experience. Exposure therapy, under the guidance of a trained professional, can be an effective tool to process these memories and reduce their impact. Although avoiding situations that trigger these memories is understandable, gradually facing them with proper support can be beneficial for your recovery. Additionally, sleep problems and difficulties regulating emotions are typical side effects of trauma and can be addressed through specific therapeutic interventions."))

    # Combination 2: Yes, Yes, Yes, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='no')))
    def advice_2(self):
        self.declare(Fact(advice="Experiencing flashbacks and the tendency to avoid reminders of trauma are classic indicators of psychological trauma. In this context, exposure therapy, guided by a trauma expert, can offer a path to recovery. Additionally, it's important to recognize that sleep difficulties are a common response after traumatic experiences and may require specific attention within the therapeutic process."))

    # Combination 3: Yes, Yes, No, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='yes')))
    def advice_3(self):
        self.declare(Fact(advice="Experiencing flashbacks and avoiding situations related to the trauma can significantly affect your emotional well-being. In this sense, exposure therapy, accompanied by an experienced therapist, can provide you with tools to address these challenges. Additionally, it is important to highlight that sleep difficulties are a common reaction after a traumatic event and can be subject to therapeutic intervention to improve your quality of life."))

    # Combination 4: Yes, Yes, No, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='no')))
    def advice_4(self):
        self.declare(Fact(advice="Experiencing flashbacks is a common reaction after experiencing trauma. In this context, exposure therapy can be an effective therapeutic strategy to process and reduce the frequency of these intrusive memories. Additionally, sleep difficulties may arise as a result of the impact of trauma and can be addressed through specialized therapeutic interventions."))

    # Combination 5: Yes, No, Yes, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='yes')))
    def advice_5(self):
        self.declare(Fact(advice="Avoiding trauma reminders and sleep difficulties are common manifestations after traumatic experiences. Exposure therapy, supported by a trauma-trained therapist, can offer effective strategies to manage these challenges. It is also important to recognize that nightmares are a typical response after trauma and can be addressed within the therapeutic framework."))

    # Combination 6: Yes, No, Yes, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='no')))
    def advice_6(self):
        self.declare(Fact(advice="Avoiding trauma reminders and sleep difficulties are common experiences after having lived through a traumatic event. In this context, exposure therapy, guided by a trauma-specialized professional, can provide a structured approach to face these challenges. Additionally, recognizing and addressing these difficulties can be fundamental to your emotional recovery process."))

    # Combination 7: Yes, No, No, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='yes')))
    def advice_7(self):
        self.declare(Fact(advice="Avoiding trauma reminders and difficulties in regulating emotions are phenomena that can arise after having experienced a traumatic event. In this context, exposure therapy, conducted by a trauma-experienced therapist, can offer effective therapeutic strategies to address these challenges. Recognizing and working on these areas can be crucial for your recovery process."))

    # Combination 8: Yes, No, No, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='yes'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='no')))
    def advice_8(self):
        self.declare(Fact(advice="Avoiding trauma reminders is a common response after a traumatic experience. In this context, exposure therapy, provided by a trauma-specialized therapist, can offer an effective therapeutic approach to address this tendency. Recognizing and addressing these difficulties can be an important step in your emotional recovery process."))

    # Combination 9: No, Yes, Yes, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='yes')))
    def advice_9(self):
        self.declare(Fact(advice="Nightmares and difficulties in regulating emotions are common reactions after experiencing a traumatic event. In this context, exposure therapy, offered by a trauma-specialized therapist, can provide effective strategies to manage these difficulties. Recognizing and working on these areas can be fundamental to your emotional recovery process."))

    # Combination 10: No, Yes, Yes, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='no')))
    def advice_10(self):
        self.declare(Fact(advice="Nightmares are a common experience after having lived through a traumatic event. In this context, exposure therapy, provided by a trauma-experienced therapist, can offer effective therapeutic strategies to address this specific difficulty. Recognizing and working on these areas can be an important step in your emotional recovery process."))

    # Combination 11: No, Yes, No, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='yes')))
    def advice_11(self):
        self.declare(Fact(advice="Avoiding trauma reminders and difficulties in regulating emotions are common phenomena after experiencing a traumatic event. In this context, exposure therapy, under the guidance of a trauma-specialized therapist, can offer a structured approach to address these areas. Recognizing and working on these difficulties can be a significant step in your recovery process."))

    # Combination 12: No, Yes, No, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='yes'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='no')))
    def advice_12(self):
        self.declare(Fact(advice="Avoiding trauma reminders is a common response after a traumatic experience. However, it is important to recognize and address the emotional difficulties that can arise as a result of the trauma. In this context, exposure therapy, provided by a trauma-specialized therapist, can offer an effective therapeutic approach to address these difficulties."))

    # Combination 13: No, No, Yes, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='yes')))
    def advice_13(self):
        self.declare(Fact(advice="Difficulties in sleeping and regulating emotions are common reactions after having lived through a traumatic event. Exposure therapy, under the guidance of a trauma-experienced therapist, can provide effective strategies to address these challenges. Recognizing and working on these areas can be crucial to your emotional recovery process."))

    # Combination 14: No, No, Yes, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='yes'), Fact(emotional_regulation_difficulties='no')))
    def advice_14(self):
        self.declare(Fact(advice="Difficulties in sleeping are a common experience after having lived through a traumatic event. In this context, exposure therapy, provided by a trauma-specialized therapist, can offer an effective therapeutic approach to address this specific difficulty. Recognizing and working on these areas can be fundamental to your emotional recovery process."))

    # Combination 15: No, No, No, Yes
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='yes')))
    def advice_15(self):
        self.declare(Fact(advice="Recognizing and addressing the emotional difficulties that may arise after a traumatic event is an important step in your recovery process. In this sense, exposure therapy, under the guidance of a trauma-specialized therapist, can offer effective strategies to address these specific areas. Working on these difficulties can be fundamental to promoting your long-term emotional well-being."))

    # Combination 16: No, No, No, No
    @Rule(AND(Fact(flashbacks_intrusive_memories='no'), Fact(avoidance_of_reminders='no'), Fact(sleep_problems_due_to_trauma='no'), Fact(emotional_regulation_difficulties='no')))
    def advice_16(self):
        self.declare(Fact(advice="At this time, there are no signs of trauma-related issues. However, it is always important to be attentive to any changes in your emotional well-being and seek support if necessary."))


    @Rule(Fact(flashbacks_intrusive_memories=MATCH.flashbacks_intrusive_memories), Fact(avoidance_of_reminders=MATCH.avoidance_of_reminders),
          Fact(sleep_problems_due_to_trauma=MATCH.sleep_problems_due_to_trauma), Fact(emotional_regulation_difficulties=MATCH.emotional_regulation_difficulties),
          Fact(advice=MATCH.advice))
    def show_advice(self, advice):
        BotMessage.objects.create(user=self.user, content=advice)

    @classmethod
    def set_user(self, user):
        self.user = user


    @classmethod
    def ask_for_options(self):
        content = """
        Since <span>PTSD</span> is the disorder that you most likely have, Let's make a little
        exploratory questions in order to find a good advice for you.

        <br><br>
        Do you have flashbacks or intrusive memories of the traumatic event? (yes/no): <br>
        Do you avoid places, people, or activities that remind you of the trauma? (yes/no): <br>
        Do you have trouble sleeping due to nightmares or insomnia? (yes/no): <br>
        Do you feel it is difficult to control your emotions, such as fear, anger, or sadness? (yes/no): <br><br>

        Remeber the separation of the answers. For example: (yes, no, no, yes)
        """
        BotMessage.objects.create(user=self.user, content=content)

    @classmethod
    def run_expert_system(self, options):
        expert_system = TraumaExpertSystem()
        expert_system.reset()

        flashbacks = options[0]
        avoidance = options[1]
        sleep_problems = options[2]
        emotional_difficulties = options[3]
        

        expert_system.declare(Fact(flashbacks_intrusive_memories=flashbacks))
        expert_system.declare(Fact(avoidance_of_reminders=avoidance))
        expert_system.declare(Fact(sleep_problems_due_to_trauma=sleep_problems))
        expert_system.declare(Fact(emotional_regulation_difficulties=emotional_difficulties))

        expert_system.run()

