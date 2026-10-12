import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ============================================================
# COURSE DATA
# ============================================================

COURSES = {

    "cs": {
        "name": "Computer Science (CS)",

        "first": [
            "Myanmar",
            "English",
            "Physics",
            "Introduction to Computer Systems + Digital Logic Fundamentals (I)",
            "Mathematics of Computing I",
            "Computer Application Techniques (I) + Data Structure",
            "Programming Logic & Design + Computer Programming Techniques"
        ],

        "second": [
            "English",
            "Java Programming Language",
            "Mathematics of Computing II",
            "Digital Logic Fundamentals II + Advanced Data Structure",
            "Database Management System + Object Oriented Analysis and Design",
            "Computer Application Techniques II",
            "Software Engineering + System Analysis and Design"
        ],

        "third": [
            "English",
            "Computer Organization + Assembly Language + Operating Systems",
            "Mathematics of Computing III",
            "Data and Computer Communications I + Computer Networking",
            "Software Engineering + Database Management System",
            "Computer Application Techniques III",
            "Advanced Java Programming (J2EE) + Advanced Programming Techniques"
        ],

        "fourth": [
            "English",
            "Operations Research + Digital Business and E-Commerce Management",
            "Mathematics of Computing IV",
            "Analysis of Algorithms + Operating Systems",
            "Database Management System + Management Information System + Information Assurance and Security",
            "Software Engineering + Unified Modeling Language",
            "Artificial Intelligence + Computer Graphics"
        ],

        "fifth": [
            "English",
            "Mathematics of Computing V",
            "Distributed Systems + Advanced Networking",
            "Information Assurance and Security",
            "Advanced Artificial Intelligence + Natural Language Processing",
            "Computing Applied Algorithm",
            "Computer Vision and Interactive Computer Graphics",
            "Web Engineering",
            "Data Mining",
            "Business Application Techniques (ERP)",
            "Internship / Project"
        ]
    },


    "ct": {
        "name": "Computer Technology (CT)",

        "first": [
            "Myanmar",
            "English",
            "Physics",
            "Introduction to Computer Systems + Digital Logic Fundamentals (I)",
            "Mathematics of Computing I",
            "Computer Application Techniques (I) + Data Structure",
            "Programming Logic & Design + Computer Programming Techniques"
        ],

        "second": [
            "English",
            "Java Programming Language",
            "Mathematics of Computing II",
            "Digital Logic Fundamentals II + Advanced Data Structure",
            "Database Management System + System Analysis and Design",
            "Computer Application Techniques II (Web Programming) + Digital System Design",
            "Electrical Circuits I"
        ],

        "third": [
            "English",
            "Computer Organization + Assembly Language + Operating Systems",
            "Mathematics of Computing III",
            "Data and Computer Communications I + Computer Networking",
            "Electronics I",
            "Linear Control Systems + Computer Architecture I",
            "Electrical Circuits II + Microprocessor Architecture and Interfacing"
        ],

        "fourth": [
            "English",
            "Artificial Intelligence + Database Management System",
            "Mathematics of Computing IV",
            "Introduction to Microcontrollers + Introduction to Embedded Systems",
            "Computer Architecture II",
            "Control Systems + Cryptography",
            "Data and Computer Communications II + Computer Security"
        ],

        "fifth": [
            "English",
            "Mathematics of Computing V",
            "Distributed Systems + Advanced Networking",
            "Computer System Fundamentals",
            "Embedded Systems",
            "Network Security",
            "Image Processing and Computer Vision",
            "Digital Signal Processing"
        ]
    }
}


# ============================================================
# DEGREE INFORMATION
# ============================================================

DEGREE_INFORMATION = {

    "bcsc": {
        "name": "Bachelor of Computer Science (B.C.Sc.)",
        "icon": "💻",
        "text": """💻 Bachelor of Computer Science (B.C.Sc.)

UCS Monywa တွင် Computer Science ဆိုင်ရာ
ဘွဲ့ကြိုသင်တန်းကို ဖွင့်လှစ်သင်ကြားပေးပါသည်။

📚 Degree: B.C.Sc.
🎓 Bachelor of Computer Science

⏰ Duration: 5 Years"""
    },

    "bctech": {
        "name": "Bachelor of Computer Technology (B.C.Tech.)",
        "icon": "🖥️",
        "text": """🖥️ Bachelor of Computer Technology (B.C.Tech.)

UCS Monywa တွင် Computer Technology ဆိုင်ရာ
ဘွဲ့ကြိုသင်တန်းကို ဖွင့်လှစ်သင်ကြားပေးပါသည်။

📚 Degree: B.C.Tech.
🎓 Bachelor of Computer Technology

⏰ Duration: 5 Years"""
    },

    "dcsc": {
        "name": "Diploma in Computer Science (D.C.Sc.)",
        "icon": "📜",
        "text": """📜 Diploma in Computer Science (D.C.Sc.)

UCS Monywa တွင် Computer Science ဆိုင်ရာ
Diploma Program ဖြစ်ပါသည်။

📚 Degree: D.C.Sc.
📜 Diploma in Computer Science"""
    },

    "mcsc": {
        "name": "Master of Computer Science (M.C.Sc.)",
        "icon": "🎓",
        "text": """🎓 Master of Computer Science (M.C.Sc.)

UCS Monywa တွင် Computer Science ဆိုင်ရာ
မဟာဘွဲ့သင်တန်းကို ဖွင့်လှစ်သင်ကြားပေးပါသည်။

📚 Degree: M.C.Sc.
🎓 Master of Computer Science"""
    },

    "mctech": {
        "name": "Master of Computer Technology (M.C.Tech.)",
        "icon": "🎓",
        "text": """🎓 Master of Computer Technology (M.C.Tech.)

UCS Monywa တွင် Computer Technology ဆိုင်ရာ
မဟာဘွဲ့သင်တန်းကို ဖွင့်လှစ်သင်ကြားပေးပါသည်။

📚 Degree: M.C.Tech.
🎓 Master of Computer Technology"""
    },

    "misc": {
        "name": "Master of Information Science (M.I.Sc.)",
        "icon": "🎓",
        "text": """🎓 Master of Information Science (M.I.Sc.)

UCS Monywa တွင် Information Science ဆိုင်ရာ
မဟာဘွဲ့သင်တန်းကို ဖွင့်လှစ်သင်ကြားပေးပါသည်။

📚 Degree: M.I.Sc.
🎓 Master of Information Science"""
    }
}


# ============================================================
# TIMETABLE DATA
# ============================================================

TIMETABLES = {

    "first": {
        "name": "First Year",
        "majors": [
            {
                "name": "Computer Science (CS)",
                "image": "timetable/firstA.jpg"
            },
            {
                "name": "Computer Technology (CT)",
                "image": "timetable/firstB.jpg"
            }
        ]
    },

    "second": {
        "name": "Second Year",
        "majors": [
            {
                "name": "Computer Science (CS)",
                "image": "timetable/secondCS.jpg"
            },
            {
                "name": "Computer Technology (CT)",
                "image": "timetable/secondCT.jpg"
            }
        ]
    },

    "third": {
        "name": "Third Year",
        "majors": [
            {
                "name": "Computer Science (CS)",
                "image": "timetable/thirdCS.jpg"
            },
            {
                "name": "Computer Technology (CT)",
                "image": "timetable/thirdCT.jpg"
            }
        ]
    },

    "fourth": {
        "name": "Fourth Year",
        "majors": [
            {
                "name": "Computer Science (CS)",
                "image": "timetable/fourthCS.jpg"
            },
            {
                "name": "Computer Technology (CT)",
                "image": "timetable/fourthCT.jpg"
            }
        ]
    },

    "fifth": {
        "name": "Fifth Year",
        "majors": [
            {
                "name": "Computer Science (CS)",
                "image": "timetable/fifthCS.jpg"
            },
            {
                "name": "Computer Technology (CT)",
                "image": "timetable/fifthCT.jpg"
            }
        ]
    },

    "master": {
        "name": "Master",
        "majors": [
            {
                "name": "Master of Computer Science (M.C.Sc.)",
                "image": "timetable/MCSc.jpg"
            },
            {
                "name": "Master of Information Science (M.I.Sc.)",
                "image": "timetable/MISc.jpg"
            }
        ]
    }
}


# ============================================================
# GENERAL CHATBOT PATTERNS
# ============================================================

PATTERNS = [

    (
        r".*(မင်္ဂလာပါ|ဟယ်လို|hello|hi).*",
        """မင်္ဂလာပါ 👋

UCS Monywa Assistant Chatbot မှ
ကြိုဆိုပါတယ်။

တက္ကသိုလ်၊ သင်တန်း၊ ဘွဲ့၊ အချိန်ဇယား
နှင့် ကျောင်းသားရေးရာများကို မေးမြန်းနိုင်ပါတယ်။"""
    ),

    (
        r".*(နာမည်|name).*",
        """🤖 UCS Monywa University အတွက်
အထောက်အကူပြု University Assistant Chatbot ဖြစ်ပါတယ်။"""
    ),

    (
        r".*(career|အလုပ်အကိုင်|အလုပ်ရနိုင်|အလုပ်အကိုင်အခွင့်အလမ်း).*",
        """💼 Computer-related courses များ
ပြီးဆုံးပါက

• Software Developer
• Web Developer
• Mobile App Developer
• Database Administrator
• Network Engineer
• System Administrator
• IT Support
• Data / AI-related Jobs

စသည့် Career Path များကို
လေ့လာနိုင်ပါသည်။"""
    ),

    (
        r".*(programming|ပရိုဂရမ်|programming language|coding).*",
        """💻 Programming သင်ခန်းစာများတွင်

Python
Java
C/C++
Web Programming

စသည့် Programming Technologies
များကို လေ့လာနိုင်ပါသည်။"""
    ),

    (
        r".*(ဝင်ခွင့်|admission|apply|လျှောက်).*",
        """🎓 တက္ကသိုလ်ဝင်ခွင့်

ဝင်ခွင့်အတွက် သတ်မှတ်ထားသော
အချက်အလက်များနှင့် လိုအပ်ချက်များကို
တက္ကသိုလ်၏ official announcement တွင်
စစ်ဆေးပါ။

📌 လိုအပ်နိုင်သော စာရွက်စာတမ်းများ

• မှတ်ပုံတင်မိတ္တူ
• ဓာတ်ပုံ
• တက္ကသိုလ်ဝင်စာမေးပွဲ အောင်စာရင်း
• ဝင်ခွင့်လျှောက်လွှာ"""
    ),

    (
        r".*(ကျောင်းလခ|အခကြေးငွေ|fee|fees).*",
        """💰 ကျောင်းလခနှင့် အခကြေးငွေ

တက္ကသိုလ်ကျောင်းလခ၊ သင်တန်းကြေးနှင့်
အခြားအခကြေးငွေများကို Finance Office
တွင် မေးမြန်းနိုင်ပါသည်။"""
    ),

    (
        r".*(စာရင်းသွင်း|ကျောင်းအပ်|registration|register|enrollment|enrol).*",
        """📋 ကျောင်းသားစာရင်းသွင်းခြင်း

ဝင်ခွင့်ရရှိပြီးသော ကျောင်းသား/ကျောင်းသူများသည်
သတ်မှတ်ထားသောကာလအတွင်း
ကျောင်းသားစာရင်းသွင်းခြင်းကို
ဆောင်ရွက်ရပါမည်။"""
    ),

    (
        r".*(စာမေးပွဲ|exam|examination).*",
        """📝 စာမေးပွဲအချိန်ဇယားကို
သက်ဆိုင်ရာ Department မှ
ကြေညာပေးပါမည်။"""
    ),

    (
        r".*(အမှတ်|result|results|grade|ရလဒ်).*",
        """📊 ရလဒ်များကို Student Portal
မှတစ်ဆင့် ကြည့်ရှုနိုင်ပါသည်။"""
    ),

    (
        r".*(စာကြည့်တိုက်|library).*",
        """📚 စာကြည့်တိုက်

UCS Monywa စာကြည့်တိုက်တွင်

• သင်ရိုးစာအုပ်များ
• Research Papers
• Academic Journals
• Computer Science စာအုပ်များ
• Computer Technology စာအုပ်များ

ကို ရှာဖွေဖတ်ရှုနိုင်ပါသည်။"""
    ),

    (
        r".*(အဆောင်|hostel).*",
        """🏠 Hostel အတွက်
Student Affairs Office သို့
ဆက်သွယ်မေးမြန်းနိုင်ပါသည်။"""
    ),

    (
        r".*(wifi|wi-fi|internet).*",
        """📶 Campus WiFi နှင့် Internet
အသုံးပြုမှုဆိုင်ရာ အချက်အလက်များကို
တက္ကသိုလ်ဘက်မှ သတ်မှတ်ပေးထားသော
စည်းမျဉ်းများအတိုင်း အသုံးပြုနိုင်ပါသည်။"""
    ),

    (
        r".*(အချိန်|ဖွင့်ချိန်|ပိတ်ချိန်|ရုံးချိန်|open|close|hour).*",
        """⏰ ရုံးချိန်

တနင်္လာ - သောကြာ
9:00 AM - 4:00 PM"""
    ),

    (
        r".*(နေရာ|လိပ်စာ|ကျောင်းဘယ်မှာရှိ|location|address).*",
        """📍 University of Computer Studies, Monywa

စစ်ကိုင်းတိုင်းဒေသကြီး၊
ယင်းမာပင်မြို့နယ်၊
အောင်ဇေယျမြို့သစ်၊
မုံရွာ-ယာကြီး-ကလေးဝလမ်းပေါ်တွင်
တည်ရှိပါသည်။"""
    ),

    (
        r".*(ဆက်သွယ်|ဖုန်း|အီးမေးလ်|contact|phone|email).*",
        """📞 ဆက်သွယ်ရန်

Phone: 09-XXXXXXXXX
Email: info@university.edu.mm"""
    ),

    (
        r".*(ပညာသင်ဆု|ထောက်ပံ့ကြေး|scholarship|financial aid).*",
        """🎓 Scholarship ဆိုင်ရာ
အချက်အလက်များကို
Student Affairs Office တွင်
စုံစမ်းနိုင်ပါသည်။"""
    ),

    (
        r".*(ပိတ်ရက်|ပြက္ခဒိန်|holiday|vacation|calendar).*",
        """📅 Academic Calendar နှင့်
ကျောင်းပိတ်ရက်များကို
တက္ကသိုလ်၏ official announcement
တွင် ကြည့်ရှုနိုင်ပါသည်။"""
    ),

    (
        r".*(ကလပ်|အသင်း|လှုပ်ရှားမှု|club|activity|event).*",
        """🎉 တက္ကသိုလ်တွင်

• Project Exhibition
• Sports Competition
• Esports Competition
• Chess Competition
• International Girls in ICT Day

စသည့် လှုပ်ရှားမှုများ
ကျင်းပပြုလုပ်နိုင်ပါသည်။"""
    ),

    (
        r".*(ကဒ်|ကတ်|id card|student id).*",
        """🪪 Student ID Card ပြုလုပ်ရန်
သို့မဟုတ် ပျောက်ဆုံးပါက
Student Affairs Office သို့
သတင်းပို့ပါ။"""
    ),

    (
        r".*(ထောက်ခံစာ|အမှတ်စာရင်း|certificate|transcript|recommendation).*",
        """📄 Transcript နှင့် ထောက်ခံစာများ
လျှောက်ထားရန် Student Affairs Office
သို့ ဆက်သွယ်ပါ။"""
    ),

    (
        r".*(စည်းကမ်း|ဝတ်စုံ|ယူနီဖောင်း|rule|dress code|uniform).*",
        """👔 ကျောင်းသားများသည်
တက္ကသိုလ်သတ်မှတ် ဝတ်စုံနှင့်
စည်းကမ်းများကို လိုက်နာရပါမည်။"""
    ),

    (
        r".*(ကျေးဇူး|thank|thanks).*",
        """ရပါတယ် 😊

ကူညီပေးနိုင်တာ ဝမ်းသာပါတယ်။"""
    )
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_timetable(year=None, major=None):

    if not year:
        return TIMETABLES

    data = TIMETABLES.get(year)

    if not data:
        return None

    if major:

        for item in data["majors"]:

            if major == "cs" and "Computer Science" in item["name"]:
                return item

            if major == "ct" and "Computer Technology" in item["name"]:
                return item

    return data


def get_course(course=None, year=None):

    if not course:
        return COURSES

    course = course.lower()

    if course not in COURSES:
        return None

    if not year:
        return COURSES[course]

    return COURSES[course].get(year)


# ============================================================
# FIND YEAR
# ============================================================

def find_year(text):

    text = text.lower()

    if re.search(
        r"(first\s*year|1st\s*year|year\s*1|\bfirst\b|ပထမနှစ်|ပထမ)",
        text
    ):
        return "first"

    if re.search(
        r"(second\s*year|2nd\s*year|year\s*2|\bsecond\b|ဒုတိယနှစ်|ဒုတိယ)",
        text
    ):
        return "second"

    if re.search(
        r"(third\s*year|3rd\s*year|year\s*3|\bthird\b|တတိယနှစ်|တတိယ)",
        text
    ):
        return "third"

    if re.search(
        r"(fourth\s*year|4th\s*year|year\s*4|\bfourth\b|စတုတ္ထနှစ်|စတုတ္ထ)",
        text
    ):
        return "fourth"

    if re.search(
        r"(fifth\s*year|5th\s*year|year\s*5|\bfifth\b|ပဉ္စမနှစ်|ပဉ္စမ)",
        text
    ):
        return "fifth"

    if re.search(
        r"(master|postgraduate|မဟာဘွဲ့)",
        text
    ):
        return "master"

    return None


# ============================================================
# FIND MAJOR
# ============================================================

def find_major(text):

    text = text.lower()

    if re.search(
        r"(computer\s+science|\bcs\b|ကွန်ပျူတာသိပ္ပံ)",
        text
    ):
        return "cs"

    if re.search(
        r"(computer\s+technology|\bct\b|ကွန်ပျူတာနည်းပညာ)",
        text
    ):
        return "ct"

    return None


# ============================================================
# CHATBOT RESPONSE
# ============================================================

def chatbot_response(text):

    text_lower = text.lower().strip()

    # --------------------------------------------------------
    # TIMETABLE
    # --------------------------------------------------------

    if re.search(
        r"(timetable|time\s*table|schedule|အချိန်ဇယား|ဇယား)",
        text_lower
    ):

        year = find_year(text_lower)
        major = find_major(text_lower)

        return {
            "type": "timetable",
            "year": year,
            "major": major
        }


    # --------------------------------------------------------
    # COURSE
    # --------------------------------------------------------

    if re.search(
        r"(course|courses|သင်တန်း|ဘာသာရပ်|သင်ရိုး|subjects|subject)",
        text_lower
    ):

        course = find_major(text_lower)
        year = find_year(text_lower)

        return {
            "type": "course",
            "course": course,
            "year": year
        }


    # --------------------------------------------------------
    # DEGREE
    # --------------------------------------------------------

    degree_patterns = {

        "bcsc": [
            r"b\.?\s*c\.?\s*sc",
            r"\bbcsc\b",
            r"bachelor\s+of\s+computer\s+science"
        ],

        "bctech": [
            r"b\.?\s*c\.?\s*tech",
            r"\bbctech\b",
            r"bachelor\s+of\s+computer\s+technology"
        ],

        "dcsc": [
            r"d\.?\s*c\.?\s*sc",
            r"\bdcsc\b",
            r"diploma\s+in\s+computer\s+science"
        ],

        "mcsc": [
            r"m\.?\s*c\.?\s*sc",
            r"\bmcsc\b",
            r"master\s+of\s+computer\s+science"
        ],

        "mctech": [
            r"m\.?\s*c\.?\s*tech",
            r"\bmctech\b",
            r"master\s+of\s+computer\s+technology"
        ],

        "misc": [
            r"m\.?\s*i\.?\s*sc",
            r"\bmisc\b",
            r"master\s+of\s+information\s+science"
        ]
    }


    for degree, patterns in degree_patterns.items():

        for pattern in patterns:

            if re.search(pattern, text_lower):

                return {
                    "type": "degree",
                    "degree": degree
                }


    # --------------------------------------------------------
    # DEGREE GENERAL QUESTION
    # --------------------------------------------------------

    if re.search(
        r"(degree|ဘွဲ့|ဘွဲ့များ|ဘွဲ့အမျိုးအစား)",
        text_lower
    ):

        return {
            "type": "degree_select"
        }


    # --------------------------------------------------------
    # GENERAL PATTERNS
    # --------------------------------------------------------

    for pattern, response in PATTERNS:

        if re.search(pattern, text_lower):

            return {
                "type": "text",
                "text": response
            }


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return {
        "type": "text",
        "text": """တောင်းပန်ပါတယ် 🙏

မေးခွန်းကို နားမလည်သေးပါ။

အောက်ပါအကြောင်းအရာများကို မေးနိုင်ပါတယ်။

🎓 ဘွဲ့
📚 သင်ရိုး / Courses
🕐 အချိန်ဇယား
📝 ဝင်ခွင့်
📋 ကျောင်းအပ်ခြင်း
💰 ကျောင်းလခ
📊 ရလဒ်
📖 စာကြည့်တိုက်
🏠 အဆောင်
📞 ဆက်သွယ်ရန်
📍 တည်နေရာ"""
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        greeting="မင်္ဂလာပါ"
    )


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "type": "text",
                "text": "Invalid request."
            })


        message = str(
            data.get("message", "")
        ).strip()


        if not message:

            return jsonify({
                "type": "text",
                "text": "ကျေးဇူးပြု၍ မေးခွန်းတစ်ခု ရိုက်ထည့်ပါ။"
            })


        response = chatbot_response(message)


        # ----------------------------------------------------
        # TIMETABLE
        # ----------------------------------------------------

        if response["type"] == "timetable":

            year = response.get("year")
            major = response.get("major")


            if not year:

                return jsonify({
                    "type": "timetable_select",
                    "text": "🕐 ဘယ်နှစ်နှစ်ရဲ့ အချိန်ဇယားကို ကြည့်ချင်ပါသလဲ?"
                })


            timetable_data = get_timetable(
                year,
                major
            )


            if not timetable_data:

                return jsonify({
                    "type": "text",
                    "text": "❌ Timetable မတွေ့ပါ။"
                })


            if major:

                return jsonify({
                    "type": "timetable",
                    "year": year,
                    "year_name": TIMETABLES[year]["name"],
                    "images": [timetable_data]
                })


            return jsonify({
                "type": "timetable",
                "year": year,
                "year_name": TIMETABLES[year]["name"],
                "images": TIMETABLES[year]["majors"]
            })


        # ----------------------------------------------------
        # COURSE
        # ----------------------------------------------------

        if response["type"] == "course":

            course = response.get("course")
            year = response.get("year")


            if not course:

                return jsonify({
                    "type": "course_select",
                    "text": "📚 Computer Science သို့မဟုတ် Computer Technology ကို ရွေးချယ်ပါ။"
                })


            if not year:

                return jsonify({
                    "type": "course_year_select",
                    "course": course,
                    "text": "📚 ဘယ်နှစ်နှစ်ကို သိချင်ပါသလဲ?"
                })


            subjects = COURSES[course].get(year)


            if not subjects:

                return jsonify({
                    "type": "text",
                    "text": "❌ Course မတွေ့ပါ။"
                })


            return jsonify({
                "type": "course",
                "course": course,
                "course_name": COURSES[course]["name"],
                "year": year,
                "subjects": subjects
            })


        # ----------------------------------------------------
        # DEGREE
        # ----------------------------------------------------

        if response["type"] == "degree":

            degree = response.get("degree")

            information = DEGREE_INFORMATION.get(degree)


            if information:

                return jsonify({
                    "type": "degree",
                    "degree": degree,
                    "name": information["name"],
                    "icon": information["icon"],
                    "text": information["text"]
                })


            return jsonify({
                "type": "text",
                "text": "❌ Degree information မတွေ့ပါ။"
            })


        # ----------------------------------------------------
        # DEGREE SELECT
        # ----------------------------------------------------

        if response["type"] == "degree_select":

            return jsonify({
                "type": "degree_select",
                "text": "🎓 ဘွဲ့အမျိုးအစားကို ရွေးချယ်ပါ။"
            })


        # ----------------------------------------------------
        # NORMAL TEXT
        # ----------------------------------------------------

        return jsonify(response)


    except Exception as error:

        print("CHAT ERROR:", error)

        return jsonify({
            "type": "text",
            "text": "❌ Server error ဖြစ်နေပါသည်။ Terminal ကို စစ်ဆေးပါ။"
        }), 500


# ============================================================
# TIMETABLE API
# ============================================================

@app.route("/timetable/<year>")
def timetable(year):

    year = year.lower()

    if year not in TIMETABLES:

        return jsonify({
            "success": False,
            "text": "Timetable not found."
        }), 404


    return jsonify({
        "success": True,
        "year": year,
        "year_name": TIMETABLES[year]["name"],
        "images": TIMETABLES[year]["majors"]
    })


# ============================================================
# COURSE API
# ============================================================

@app.route("/course/<course>/<year>")
def course(course, year):

    course = course.lower()
    year = year.lower()


    if course not in COURSES:

        return jsonify({
            "success": False,
            "text": "Course not found."
        }), 404


    if year not in COURSES[course]:

        return jsonify({
            "success": False,
            "text": "Year not found."
        }), 404


    return jsonify({
        "success": True,
        "course": course,
        "course_name": COURSES[course]["name"],
        "year": year,
        "subjects": COURSES[course][year]
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("UCS MONYWA UNIVERSITY ASSISTANT CHATBOT")
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
