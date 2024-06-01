from django.shortcuts import render, redirect
from .models import Message, BotMessage
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import difflib
from .program_section import ProgramState as pg
from .expert_system import BipolarExpertSystem as bes
from .expert_system import DepressionExpertSystem as des
from .expert_system import TraumaExpertSystem as tes
from .expert_system import AnxietyExpertSystem as aes
from .bayesian_model import BayesianModel

def register(request):
    if request.method == "POST":
        # Obtener los datos del formulario del request.POST
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validar los datos del formulario
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "register.html")

        # Comprobar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, "register.html")

        # Crear el usuario
        user = User.objects.create_user(
            username=username, email=email, password=password1
        )

        # Guardar el usuario
        user.save()

        # Redirigir al usuario a la página de inicio de sesión
        return redirect("login")

    # Si la petición no es POST, mostrar el formulario
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Usar auth_login en lugar de login
            messages.success(request, f"Bienvenido, {username}!")
            bot_content = f"""Hello and welcome, <span> {user.username} </span>!<br><br>
            I'm a Bot Message here to offer you support and guidance on your journey to mental wellbeing. Whether you're looking for answers, advice, or just someone to talk to, I'm here for you.<br><br>
            Remember that you are not alone in this. We all face challenges in life, and it's completely normal to seek help when things feel overwhelming. Together, we can explore options and find solutions that help you feel better.<br><br>
            Whenever you need it, don't hesitate to share your concerns or questions with me. I am here to listen to you and provide you with the support you need.<br><br>
            
            Would you like to take the first step towards understanding your thoughts and emotions better? If you're ready to explore your feelings and receive guidance, I can help you start a psychological analysis. 

            <br><br> Just say <span>'yes'</span> to begin, or <span>'no'</span>. I'm here for you.

            """


            BotMessage.objects.create(user=user, content=bot_content)

            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "login.html")


def logout_view(request):
    pg.reset_variables()
    logout(request)
    return redirect("login")


@login_required
def home(request):

    if request.method == "POST":
        content = request.POST.get("message")
        print(f"Mensaje by {request.user}: {content}")
        if content:
            Message.objects.create(user=request.user, content=content)
            program_section = pg.get_program_section()
            if program_section == "init":
                process_input(content, request.user, program_section) # yes or no
            elif program_section == "ask_to_confirm_dissorder":
                process_input(content, request.user, program_section) # yes or no
            elif program_section == "select_dissorder": #yes
                select_dissorder(content, request.user)
            elif program_section == "ask_for_symptoms":
                select_symtomps(content, request.user)
            elif program_section == "select_expert_system_options":
                select_expert_system_options(content, request.user)
            elif program_section == "reset":
                select_reset_option(content, request.user)

        
        return redirect("home")

    user_messages = Message.objects.filter(user=request.user)
    bot_messages = BotMessage.objects.filter(user=request.user)
    # Añadir un atributo "tipo" a cada mensaje para indicar su tipo
    for message in user_messages:
        message.tipo = "user"
    for message in bot_messages:
        message.tipo = "bot"

    # Combinar los mensajes y ordenarlos por timestamp
    all_messages = sorted(
        list(user_messages) + list(bot_messages),
        key=lambda msg: msg.timestamp
    )

    return render(request, "chat.html", {"all_messages": all_messages})


#This method starts the flow of the program
def process_input(user_input, user, program_section):
    # Convertir la entrada del usuario a minúsculas para hacerla case-insensitive
    input_lower = user_input.lower()
    
    # Definir las opciones disponibles
    available_options = ["yes", "no"]
    
    # Inicializar una lista para almacenar las opciones seleccionadas por el usuario
    selected_options = []
    
    # Iterar sobre las palabras en la entrada del usuario
    for word in input_lower.split(','):
        # Encontrar la opción más similar a la palabra ingresada por el usuario
        closest_match = difflib.get_close_matches(word.strip(), available_options, n=1)
        # Si se encuentra una coincidencia cercana, agregarla a las opciones seleccionadas
        if closest_match:
            selected_options.append(closest_match[0])
    
    # Imprimir las opciones seleccionadas por el usuario
    if (len(selected_options)==0):
        print( "init")
        create_bot_message(user, "I'm sorry, I didn't quite catch that. Could you please choose one of the options provided?")
    elif (selected_options[0] == 'yes'):
        print("Entra: ", program_section)
        if program_section == "init":
            ask_to_confirm_disorder(user)
            pg.set_program_section("ask_to_confirm_dissorder")
        elif program_section == "ask_to_confirm_dissorder":
            ask_select_dissorder(user)
    else:
        if(program_section == "init"):
            create_bot_message(user, """No problem at all! If you ever change your mind or feel like you need support in the future, don't hesitate to reach out. I'm here to help whenever you need.
                <br><br> Feel free to type <span>yes</span> whenever you change your opinion""")
        
        if(program_section == "ask_to_confirm_dissorder"):
            bayesian_questionary(user)


# This method is called when the program_section is ask_to_confirm_dissorder
def ask_to_confirm_disorder(user):
    content = """Have you suffered from some of these disorders?: <br><br>

                    - Bipolar Disorder<br>
                    - Major Depression<br>
                    - Anxiety<br>
                    - PTSD<br><br>

                    (Yes or No)"""
    create_bot_message(user, content)

def ask_select_dissorder(user):
    content = """Please select one or more from any of the following disorders:<br><br>
            
            - Bipolar Disorder<br>
            - Major Depression<br>
            - Anxiety Disorder<br>
            - PTSD<br><br>
            
            Please type the disorder you suffer from and press Enter: (For example: Bipolar, Anxiety)"""
    create_bot_message(user, content)
    pg.set_program_section("select_dissorder")

def select_dissorder(content, user):
     # Convertir la entrada del usuario a minúsculas para hacerla case-insensitive
    input_lower = content.lower()
    
    # Definir las opciones disponibles
    available_options = ["ptsd", "Bipolar Disorder", "Major Depression", "Anxiety Disorder"]
    
    # Inicializar una lista para almacenar las opciones seleccionadas por el usuario
    selected_options = []
    
    # Iterar sobre las palabras en la entrada del usuario
    for word in input_lower.split(','):
        # Encontrar la opción más similar a la palabra ingresada por el usuario
        closest_match = difflib.get_close_matches(word.strip(), available_options, n=1)
        # Si se encuentra una coincidencia cercana, agregarla a las opciones seleccionadas
        if closest_match:
            selected_options.append(closest_match[0])

    if (len(selected_options)==0):
        print("Select disorder")
        create_bot_message(user, "I'm sorry, I didn't quite catch that. Could you please choose one of the options provided?")
    else:
        new_json = {}
        for elem in selected_options:
            clean_elem = elem.replace(" ", "")
            if clean_elem == "ptsd":
                clean_elem = clean_elem.upper()

            new_json[clean_elem] = 1

        pg.set_json(new_json)
        bayesian_questionary(user)


def bayesian_questionary(user):
    content = """Please select one or more from any of the following symptoms:<br><br>
            
            - Mood Changes<br>
            - Anxiety<br>
            - Sleep Problems<br>
            - Appetite Changes<br>
            - Cognitive Difficulties<br>
            - Behavioral Changes<br>
            - None <br><br>
            
            Please type the disorder you suffer from and press Enter: (For example: Bipolar, Anxiety)<br>
            If you chose "None" and any other, this field will stay empty.<br><br>
            """
    create_bot_message(user, content)
    pg.set_program_section("ask_for_symptoms")


def select_symtomps(content, user):
     # Convertir la entrada del usuario a minúsculas para hacerla case-insensitive
    input_lower = content.lower()
    
    # Definir las opciones disponibles
    available_options = ["Mood Changes", "Anxiety", "Sleep Problems", "Appetite Changes", "Cognitive Difficulties","Behavioral Changes", "None" ]
    
    # Inicializar una lista para almacenar las opciones seleccionadas por el usuario
    selected_options = []
    
    # Iterar sobre las palabras en la entrada del usuario
    for word in input_lower.split(','):
        # Encontrar la opción más similar a la palabra ingresada por el usuario
        closest_match = difflib.get_close_matches(word.strip(), available_options, n=1)
        # Si se encuentra una coincidencia cercana, agregarla a las opciones seleccionadas
        if closest_match:
            selected_options.append(closest_match[0])

    if (len(selected_options)==0):
        create_bot_message(user, "I'm sorry, I didn't quite catch that. Could you please choose one of the options provided?")
    else:
        if ("None" not in selected_options):
            current_json = pg.get_json()
            for elem in selected_options:
                clean_elem = elem.replace(" ", "")
                current_json[clean_elem] = 1

            pg.set_json(current_json)
        
        print(pg.get_json())

        bayesian_model = BayesianModel()
        prob, disorder = bayesian_model.use(pg.get_json())

        pg.set_expert_system_id(disorder)
        pg.set_prob(prob)

        dissorder_message = f"""
        Based on your responses, it seems like you may be experiencing symptoms consistent with <span>{disorder}</span> with a <span>{round(prob*100,1)}%</span> of probability. While this is not a diagnosis, it's essential to seek professional help and discuss your concerns with a qualified mental health provider for a comprehensive evaluation and appropriate treatment. Remember, you're not alone, and there are effective treatments available to help you manage your symptoms and improve your well-being.

        """

        create_bot_message(user, dissorder_message)
        ask_for_expert_system_options(user)


def select_expert_system_options(content, user):
     # Convertir la entrada del usuario a minúsculas para hacerla case-insensitive
    input_lower = content.lower()
    
    # Definir las opciones disponibles
    available_options = ["yes", "no"]
    
    # Inicializar una lista para almacenar las opciones seleccionadas por el usuario
    selected_options = []
    
    # Iterar sobre las palabras en la entrada del usuario
    for word in input_lower.split(','):
        # Encontrar la opción más similar a la palabra ingresada por el usuario
        closest_match = difflib.get_close_matches(word.strip(), available_options, n=1)
        # Si se encuentra una coincidencia cercana, agregarla a las opciones seleccionadas
        if closest_match:
            selected_options.append(closest_match[0])

    if (len(selected_options)==0):
        create_bot_message(user, "I'm sorry, I didn't quite catch that. Could you please choose one of the options provided?")
    elif (len(selected_options)!=4):
        create_bot_message(user, "All the options must be filled. There must be 4 and only 4 answers")
    else:
        exec_expert_system(user, selected_options)


def ask_for_expert_system_options(user):

    if pg.get_expert_system_id() == "BipolarDisorder":
        bes.set_user(user)
        bes.ask_for_options()
        
    if pg.get_expert_system_id() == 'MajorDepression':
        des.set_user(user)
        des.ask_for_options()

    if pg.get_expert_system_id() == "PTSD":
        tes.set_user(user)
        tes.ask_for_options()

    if pg.get_expert_system_id() == 'AnxietyDisorder':
        aes.set_user(user)
        aes.ask_for_options()

    pg.set_program_section("select_expert_system_options")


#This method creates a message from the bot
def create_bot_message(user, bot_content):
    BotMessage.objects.create(user=user, content=bot_content)


def exec_expert_system(user, options):

    if pg.get_expert_system_id() == "BipolarDisorder":
        bes.run_expert_system(options)

    if pg.get_expert_system_id() == 'MajorDepression':
        des.run_expert_system(options)

    if pg.get_expert_system_id() == "PTSD":
        tes.run_expert_system(options)

    if pg.get_expert_system_id() == 'AnxietyDisorder':
        aes.run_expert_system(options)

    goodbye_message = f"""
    Thank you for taking the time to complete the assessment. Remember, your mental health is important, and seeking support is a crucial step towards well-being. If you need further assistance or have any questions, please don't hesitate to reach out to a mental health professional. Take care, and we wish you the best on your journey to better mental health.
    <br><br>

    Type <span>yes</span> if you want to continue another psychologic assistance. Type <span>no</span> otherwise.

    """
    create_bot_message(user, goodbye_message)

    pg.set_program_section("reset")


def select_reset_option(content, user):
    # Convertir la entrada del usuario a minúsculas para hacerla case-insensitive
    input_lower = content.lower()
    
    # Definir las opciones disponibles
    available_options = ["yes", "no"]
    
    # Inicializar una lista para almacenar las opciones seleccionadas por el usuario
    selected_options = []
    
    # Iterar sobre las palabras en la entrada del usuario
    for word in input_lower.split(','):
        # Encontrar la opción más similar a la palabra ingresada por el usuario
        closest_match = difflib.get_close_matches(word.strip(), available_options, n=1)
        # Si se encuentra una coincidencia cercana, agregarla a las opciones seleccionadas
        if closest_match:
            selected_options.append(closest_match[0])

    if (len(selected_options)==0):
        create_bot_message(user, "I'm sorry, I didn't quite catch that. Could you please choose one of the options provided?")
    elif (selected_options[0] == 'yes'):
        welcome_back_message = f"""
        Thank you for using our system again!
        """
        create_bot_message(user, welcome_back_message)
        pg.reset_variables()

        bot_content = f"""Hello and welcome, <span> {user.username} </span>!<br><br>
        I'm a Bot Message here to offer you support and guidance on your journey to mental wellbeing. Whether you're looking for answers, advice, or just someone to talk to, I'm here for you.<br><br>
        Remember that you are not alone in this. We all face challenges in life, and it's completely normal to seek help when things feel overwhelming. Together, we can explore options and find solutions that help you feel better.<br><br>
        Whenever you need it, don't hesitate to share your concerns or questions with me. I am here to listen to you and provide you with the support you need.<br><br>
        
        Would you like to take the first step towards understanding your thoughts and emotions better? If you're ready to explore your feelings and receive guidance, I can help you start a psychological analysis. 

        <br><br> Just say <span>'yes'</span> to begin, or <span>'no'</span>. I'm here for you.

        """


        BotMessage.objects.create(user=user, content=bot_content)

    elif (selected_options[0] == 'no'):
        create_bot_message(user, """No problem at all! If you ever change your mind or feel like you need support in the future, don't hesitate to reach out. I'm here to help whenever you need.
                <br><br> Feel free to type <span>yes</span> whenever you change your opinion""")