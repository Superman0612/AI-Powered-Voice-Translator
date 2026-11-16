import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        # Dynamic access to avoid IDE/Pyright linter error for private attribute
        start_page_fn = getattr(self, "_startPage", None)
        if callable(start_page_fn):
            start_page_fn()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            # Header
            self.drawString(54, 750, "BhashaAI – AI-Powered Voice Translator for Indian Languages (Project Guide & Script)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            # Footer
            self.line(54, 45, 558, 45)
            self.drawString(54, 32, "MCA Final Year Project | AI & ML Specialization | Hinglish Complete Guide")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 32, page_text)
            self.restoreState()

def build_pdf(filename="BhashaAI_Project_Documentation_and_Script_Hinglish.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1e1b4b'),
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1e1b4b'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#312e81'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    speech_speaker_style = ParagraphStyle(
        'SpeechSpeaker',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#4338ca'),
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )

    speech_body_style = ParagraphStyle(
        'SpeechBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        leftIndent=12,
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # ================= COVER / HEADER =================
    story.append(Paragraph("BhashaAI: AI-Powered Voice Translator", title_style))
    story.append(Paragraph("MCA Final Year Project — Complete Technical Guide & Presentation Script (Hinglish)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4f46e5"), spaceAfter=12))

    # Meta box
    meta_data = [
        [
            Paragraph("<b>Project:</b> BhashaAI v2.0", table_cell_style),
            Paragraph("<b>Domain:</b> AI, Deep Learning & NLP", table_cell_style)
        ],
        [
            Paragraph("<b>Target Languages:</b> 10 Indian Scheduled Languages", table_cell_style),
            Paragraph("<b>Deployment:</b> Render (Backend) + Vercel (Frontend)", table_cell_style)
        ],
        [
            Paragraph("<b>Database:</b> Supabase PostgreSQL + Local SQLite", table_cell_style),
            Paragraph("<b>Repository:</b> GitHub (Superman0612)", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 1: OVERVIEW =================
    story.append(Paragraph("1. Project Overview (Kya hai yeh project?)", h1_style))
    story.append(Paragraph(
        "<b>BhashaAI</b> ek full-stack <b>Voice-to-Voice Neural Machine Translation system</b> hai jo specially "
        "Indian vernacular languages ke liye banaya gaya hai. Yeh system bolte waqt audio capture karta hai, "
        "usme se noise saaf karta hai, speech ko text me convert karta hai (ASR), bhasha identify karta hai (LID), "
        "target Indian language me translate karta hai (NMT), aur us translate kiye gaye text ko natural human voice me "
        "bolkar sunaata hai (TTS).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Sabse badi khoobi:</b> Is project me kisi paid 3rd-party commercial API (jaise Google Cloud Paid API ya OpenAI Paid API) "
        "ki compulsory dependency nahi hai. Saare core neural network models — <b>OpenAI Whisper</b>, <b>Meta NLLB-200</b>, "
        "aur <b>Meta MMS-TTS</b> — open-source weights ke saath CPU optimized environment me locally run hote hain.",
        body_style
    ))

    # ================= SECTION 2: PROBLEM STATEMENT =================
    story.append(Paragraph("2. Problem Statement (Yeh project kyun zaroori hai?)", h1_style))
    story.append(Paragraph(
        "Bharat me 22 constitutionally recognized bhashayein hain aur lakho log sirf apni regional language bolte hain. "
        "Market me existing voice translators me 3 major technical issues hain:",
        body_style
    ))
    story.append(Paragraph("• <b>Compulsory English Pivoting:</b> Agar Hindi se Tamil me translate karna ho, toh Google ya traditional systems pehle Hindi ko English me convert karte hain aur fir English ko Tamil me (Hindi &rarr; English &rarr; Tamil). Is double conversion ki wajah se sentence ka meaning, grammar aur cultural honorifics (aadar-satkar) kharab ho jaate hain.", bullet_style))
    story.append(Paragraph("• <b>Data Privacy & Cloud Dependency:</b> Saari voice recordings foreign commercial servers pe upload hoti hain. Rural ya secure banking/government setups me privacy maintain nahi rehti.", bullet_style))
    story.append(Paragraph("• <b>High API Cost:</b> Commercial speech APIs (Google Cloud Speech, Amazon Polly) per-second aur per-character charge karti hain, jo common public ya local businesses ke liye expensive hain.", bullet_style))
    story.append(Paragraph("<b>BhashaAI ka Solution:</b> Direct Indic-to-Indic translation pathways jo Subject-Object-Verb (SOV) sentence order ko barkaraar rakhte hain aur local/self-hosted deployment support karte hain.", body_style))

    # ================= SECTION 3: 10 LANGUAGES =================
    story.append(Paragraph("3. 10 Supported Indian Languages Catalog", h1_style))
    lang_headers = [Paragraph("<b>Language</b>", table_header_style), Paragraph("<b>ISO</b>", table_header_style), Paragraph("<b>Script</b>", table_header_style), Paragraph("<b>NLLB FLORES Code</b>", table_header_style), Paragraph("<b>Whisper Code</b>", table_header_style)]
    lang_rows = [
        [Paragraph("Hindi (हिन्दी)", table_cell_style), Paragraph("hi", table_cell_style), Paragraph("Devanagari", table_cell_style), Paragraph("hin_Deva", table_cell_style), Paragraph("hi", table_cell_style)],
        [Paragraph("English", table_cell_style), Paragraph("en", table_cell_style), Paragraph("Latin", table_cell_style), Paragraph("eng_Latn", table_cell_style), Paragraph("en", table_cell_style)],
        [Paragraph("Gujarati (ગુજરાતી)", table_cell_style), Paragraph("gu", table_cell_style), Paragraph("Gujarati", table_cell_style), Paragraph("guj_Gujr", table_cell_style), Paragraph("gu", table_cell_style)],
        [Paragraph("Marathi (मराठी)", table_cell_style), Paragraph("mr", table_cell_style), Paragraph("Devanagari", table_cell_style), Paragraph("mar_Deva", table_cell_style), Paragraph("mr", table_cell_style)],
        [Paragraph("Bengali (বাংলা)", table_cell_style), Paragraph("bn", table_cell_style), Paragraph("Bengali", table_cell_style), Paragraph("ben_Beng", table_cell_style), Paragraph("bn", table_cell_style)],
        [Paragraph("Tamil (தமிழ்)", table_cell_style), Paragraph("ta", table_cell_style), Paragraph("Tamil", table_cell_style), Paragraph("tam_Taml", table_cell_style), Paragraph("ta", table_cell_style)],
        [Paragraph("Telugu (తెలుగు)", table_cell_style), Paragraph("te", table_cell_style), Paragraph("Telugu", table_cell_style), Paragraph("tel_Telu", table_cell_style), Paragraph("te", table_cell_style)],
        [Paragraph("Kannada (ಕನ್ನಡ)", table_cell_style), Paragraph("kn", table_cell_style), Paragraph("Kannada", table_cell_style), Paragraph("kan_Knda", table_cell_style), Paragraph("kn", table_cell_style)],
        [Paragraph("Malayalam (മലയാളം)", table_cell_style), Paragraph("ml", table_cell_style), Paragraph("Malayalam", table_cell_style), Paragraph("mal_Mlym", table_cell_style), Paragraph("ml", table_cell_style)],
        [Paragraph("Punjabi (ਪੰਜਾਬੀ)", table_cell_style), Paragraph("pa", table_cell_style), Paragraph("Gurmukhi", table_cell_style), Paragraph("pan_Guru", table_cell_style), Paragraph("pa", table_cell_style)]
    ]
    lang_table = Table([lang_headers] + lang_rows, colWidths=[110, 35, 95, 140, 124])
    lang_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(lang_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 4: PIPELINE =================
    story.append(PageBreak())
    story.append(Paragraph("4. End-to-End Voice Translation Pipeline (Architecture Details)", h1_style))
    story.append(Paragraph(
        "Jab user microphone me bolta hai ya audio upload karta hai, backend me **5 sequential stages** execute hoti hain:",
        body_style
    ))

    pipeline_stages = [
        ("Stage 1: Client Web Audio DSP & Server Preprocessing",
         "Browser microphone audio natively WebM record karta hai. Humne client-side Web Audio API (AudioContext) banaya jo audio ko 16 kHz Mono 16-bit PCM WAV me convert karta hai. Server par AudioProcessor spectral noise subtraction aur silence trimming karta hai."),
        ("Stage 2: Automatic Speech Recognition (OpenAI Whisper)",
         "Audio array 80-channel log-mel spectrogram me convert hota hai. Whisper Transformer encoder audio features extract karta hai aur autoregressive decoder spoken Indian language ka text transcript generate karta hai."),
        ("Stage 3: Hierarchical Language Identification (LID)",
         "Unicode character range boundaries se pata chalta hai ki text kis script ka hai. Agar text Devanagari script me ho, toh custom morphological analyzer Marathi aur Hindi ke specific stop-words (jaise Marathi 'आहे', 'नाही', 'करतो' vs Hindi 'है', 'नहीं', 'करता') match karke 15 milliseconds me accurate bhasha detect kar leta hai."),
        ("Stage 4: Neural Machine Translation (Meta NLLB-200 600M)",
         "Source text ko target language ke FLORES code (jaise hin_Deva, tam_Taml) ke sath tokenize kiya jaata hai. Seq2Seq Transformer model direct bina English pivot ke accurate regional translation produce karta hai."),
        ("Stage 5: Text-to-Speech Synthesis (Meta MMS-TTS & Fail-Safe Fallback)",
         "Translated text ko Meta MMS-TTS (VITS: Variational Autoencoder + GAN) se synthesize kiya jaata hai. Internet available hone par high-fidelity Google gTTS aur offline hone par synthetic fallback waveform banta hai jisse system kabhi fail nahi hota.")
    ]

    for title, desc in pipeline_stages:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 10))

    # ================= SECTION 5: TECH STACK =================
    story.append(Paragraph("5. Complete Technology Stack", h1_style))
    tech_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Technologies Used</b>", table_header_style), Paragraph("<b>Key Responsibilities</b>", table_header_style)],
        [Paragraph("Frontend UI", table_cell_style), Paragraph("React 18, TypeScript, Tailwind CSS, Vite, Lucide Icons, Recharts", table_cell_style), Paragraph("Browser mic recording, audio player, realtime latency metric graphs", table_cell_style)],
        [Paragraph("Backend API", table_cell_style), Paragraph("FastAPI (ASGI), Python 3.11+, Pydantic V2, Uvicorn", table_cell_style), Paragraph("REST API gateway, JWT Bearer security, DSP orchestration", table_cell_style)],
        [Paragraph("Database", table_cell_style), Paragraph("Supabase PostgreSQL (Cloud) + SQLite (Local fallback), SQLAlchemy 2.0", table_cell_style), Paragraph("User profiles, 10 language metadata, translation history, latencies", table_cell_style)],
        [Paragraph("Deep Learning", table_cell_style), Paragraph("PyTorch (CPU Optimized), Hugging Face Transformers, Whisper", table_cell_style), Paragraph("ASR transcription, NLLB Seq2Seq translation, MMS-TTS audio", table_cell_style)],
        [Paragraph("Cloud Hosting", table_cell_style), Paragraph("Render (Backend Web Service), Vercel (Frontend SPA Edge CDN)", table_cell_style), Paragraph("Continuous deployment from GitHub (Superman0612 repository)", table_cell_style)]
    ]
    tech_table = Table(tech_data, colWidths=[90, 184, 230])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 6: PRESENTATION SCRIPT =================
    story.append(PageBreak())
    story.append(Paragraph("6. Presentation Script (Examiner ke samne bolne ki exact Script)", h1_style))
    story.append(Paragraph(
        "Is script ko aap viva presentation ya live demo ke dauran step-by-step follow kar sakte hain. "
        "Yeh Hinglish (Hindi + English technical terms) me naturally prepare ki gayi hai.",
        body_style
    ))

    script_parts = [
        ("Part 1: Opening & Introduction (Examiner ko Greeting)",
         '"Good morning / Good afternoon respected examiners and faculty members. '
         'My name is [Aapka Naam]. Today I am presenting my MCA Final Year Project titled: '
         'BhashaAI: AI-Powered Voice Translator for Indian Languages.\n\n'
         'Is project ka main objective Bharat ki diverse linguistic barriers ko solve karna hai. '
         'Humne ek aisa genuine AI/ML voice-to-voice translation system build kiya hai jo 10 scheduled Indian languages '
         'ko support karta hai, bina kisi paid third-party API par depend kiye."'),

        ("Part 2: Problem Statement & Motivation (Project kyun banaya)",
         '"Sir, aaj Google Translate ya AWS jaise systems available hain, lekin unke sath teen bade challenges hain: '
         'Pehla, unme compulsory English-Pivoting hoti hai — yaani agar Hindi se Tamil me translate karna ho toh vo pehle '
         'Hindi ko English aur fir Tamil me convert karte hain, jisse grammatical nuance aur cultural honorifics kharab ho jaate hain. '
         'Doosra, commercial cloud APIs audio recordings ko foreign servers pe bhejti hain jo data privacy rules ke against hai. '
         'Aur teesra, per-character cost aati hai.\n\n'
         'Humne BhashaAI ko open-source foundation models par CPU hardware par chalne ke liye optimize kiya hai taaki yeh direct '
         'Indic-to-Indic translation deliver kar sake."'),

        ("Part 3: Technical Architecture & Working (Pipeline Samjhana)",
         '"Sir, humare system me 5 modular deep learning stages hain:\n'
         '1. Audio DSP Stage: Browser se aane wale audio ko hum client-side Web Audio API se 16kHz mono WAV me standardize karte hain aur spectral noise reduction lagate hain.\n'
         '2. Automatic Speech Recognition: OpenAI ke Whisper Transformer model se spoken voice accurate text me transcribe hoti hai.\n'
         '3. Language Identification: Script Unicode boundaries aur morphological heuristics se language 15ms me detect hoti hai — specially Hindi aur Marathi dono Devanagari script share karte hain, isliye humne custom word-marker rules lagaye hain.\n'
         '4. Neural Machine Translation: Meta ke NLLB-200 600M parameter model se sequence-to-sequence direct translation hoti hai.\n'
         '5. Speech Synthesis: Meta MMS-TTS aur gTTS fallback se translated voice synthesize hokar browser me play hoti hai."'),

        ("Part 4: Live Demonstration (Screen dikhate waqt bolne ki script)",
         '"Ab main aapko live system ka demonstration dikhata hoon:\n'
         '- Yahan aap dekh sakte hain humara modern React + Tailwind UI chal raha hai.\n'
         '- Hum Source Language me "Auto-Detect" ya "Hindi" chunenge aur Target Language me "Tamil" ya "Gujarati" select karenge.\n'
         '- Ab main Microphone button press karke bolta hoon: "नमस्ते, भारत में आपका स्वागत है".\n'
         '- Jaise hi maine Stop kiya, system ne background me DSP -> ASR -> LID -> NMT -> TTS execute kiya.\n'
         '- Yahan aap screen par result dekh sakte hain: Source Text recognize hua, Target language me accurate translation aayi, '
         'aur audio player me natural voice generate ho gayi.\n'
         '- Niche telemetry card me aap microsecond latency breakdown dekh sakte hain — ki ASR me kitna time laga aur NMT me kitna."'),

        ("Part 5: Database & Cloud Deployment (Admin & Student Workflow)",
         '"Database layer ke liye humne Supabase PostgreSQL use kiya hai. Master Admin profile shubhamdevatwal2121@gmail.com '
         'se protected hai. System me koi static demo accounts nahi hain; koi bhi naya student ya user apna account create karta hai, '
         'aur unka personal translation history aur audio metadata unki profile me securely store hota hai.\n'
         'Backend ko Render par deploy kiya gaya hai aur Frontend ko Vercel Edge network par."')
    ]

    for heading, speech in script_parts:
        story.append(Paragraph(heading, speech_speaker_style))
        story.append(Paragraph(speech.replace('\n', '<br/>'), speech_body_style))

    story.append(Spacer(1, 10))

    # ================= SECTION 7: VIVA VOCE Q&A =================
    story.append(PageBreak())
    story.append(Paragraph("7. Top 15 Viva Voce Questions & Answers (Hinglish)", h1_style))
    story.append(Paragraph(
        "Examiner dwara pooche jane wale sabse important technical questions aur unke best answers:",
        body_style
    ))

    viva_qa = [
        ("Q1: Aapne translation ke liye NLLB-200 model kyun chuna?",
         "Answer: Meta ka NLLB-200 (No Language Left Behind) 200 se zyada languages ko support karta hai. "
         "Iska sabse bada advantage yeh hai ki yeh direct Indic-to-Indic translation support karta hai bina English pivot ke. "
         "Iska BLEU score Hindi-Tamil aur Hindi-Gujarati pairs par Google Translate se comparable aur fast hai, aur yeh open-source hai."),

        ("Q2: Whisper model ASR ke liye kaise kaam karta hai?",
         "Answer: OpenAI Whisper ek Encoder-Decoder Transformer architecture hai jo 680,000 hours ke multilingual audio par trained hai. "
         "Input audio pehle 80-channel log-mel spectrogram me convert hota hai. Encoder 1D convolution aur self-attention layers se features "
         "extract karta hai, aur Decoder autoregressively language-tagged text tokens predict karta hai."),

        ("Q3: Hindi aur Marathi dono Devanagari script me hain, toh LID dono me fark kaise karta hai?",
         "Answer: Sir, simple Unicode script matching se sirf Devanagari script detect hoti hai. "
         "Isliye humne ek custom morphological heuristic module banaya hai jo high-frequency vocabulary markers check karta hai. "
         "Agar sentence me 'आहे', 'नाही', 'करतो', 'झाला' jaise Marathi markers hain toh Marathi classify hota hai; agar 'है', 'नहीं', 'करता', 'था' "
         "hain toh Hindi classify hota hai. Yeh decision sirf 10-15 milliseconds me ho jaata hai."),

        ("Q4: Audio DSP preprocessing ka kya fayda hua?",
         "Answer: Microphone recording me background noise aur silence hota hai. "
         "Humne Sinc interpolation se 16kHz mono resampling, peak normalization (0.95 peak) aur spectral noise subtraction lagaya. "
         "Testing ke dauran noisy audio par Word Error Rate (WER) me 15.5% tak ka absolute improvement mila."),

        ("Q5: Browser se .webm format ka issue kaise solve kiya?",
         "Answer: Modern browsers (Chrome, Edge) MediaRecorder API me audio/webm Opus record karte hain jo standard Python soundfile "
         "natively decode nahi kar pata. Humne frontend me Web Audio API (OfflineAudioContext) use karke browser client-side hi "
         "audio ko 16 kHz Mono linear 16-bit PCM WAV me convert kar diya. Isse server CPU load bacha aur format compatibility 100% ho gayi."),

        ("Q6: TTS (Text-to-Speech) me kaunsa model use kiya hai?",
         "Answer: Primary model Meta MMS-TTS (Massively Multilingual Speech) hai jo VITS architecture (Variational Inference with adversarial learning for end-to-end Text-to-Speech) "
         "par based hai. Saath hi 100% uptime ke liye Google gTTS aur offline synthetic waveform fallback bhi integrate kiya hai."),

        ("Q7: Backend me FastAPI kyun chuna Django ya Flask ke badle?",
         "Answer: FastAPI ASGI-based asynchronous framework hai jo Starlette aur Pydantic par chalta hai. "
         "Yeh I/O-bound tasks (jaise audio streaming aur model inference) me Flask se 3x fast hai, automatic OpenAPI Swagger UI docs generate karta hai, "
         "aur asynchronous streaming requests smoothly handle karta hai."),

        ("Q8: Database architecture kya hai?",
         "Answer: Humne 7 normalized tables banayi hain — users, languages, audio_files, translations, model_registry, evaluation_runs, "
         "aur evaluation_results. Hosted environment me Supabase PostgreSQL use hota hai aur local development me zero-setup SQLite fallback hai."),

        ("Q9: Authentication aur Security kaise handle ki gayi hai?",
         "Answer: Passwords ko bcrypt algorithm (12 salt rounds) ke sath hash kiya jaata hai. "
         "Login hone par backend HS256 algorithm se cryptographically signed JWT (JSON Web Token) issue karta hai, jo HTTP Bearer headers me send hota hai."),

        ("Q10: User registration aur data privacy kaise manage ho rahi hai?",
         "Answer: Master Admin shubhamdevatwal2121@gmail.com ke paas complete system audit rights hain. "
         "Koi bhi naya student registration endpoint se apna account banata hai, aur foreign keys ke through unka translation data "
         "aur audio records unki profile me securely persist hote hain."),

        ("Q11: Whisper model RAM kitna leta hai aur CPU par kaise optimize kiya?",
         "Answer: Whisper Small ~500MB RAM leta hai aur Whisper Tiny sirf ~150MB RAM leta hai. "
         "Humne PyTorch float32 CPU optimization, chunking (30s windows), aur lazy model loading lagayi hai taaki bina expensive GPU ke 8GB RAM computer par smooth chale."),

        ("Q12: Latency breakdown kya rehti hai complete pipeline me?",
         "Answer: Average total cycle ~2.4 seconds hai on standard CPU: Audio DSP (~45ms), Whisper ASR (~1100ms), LID (~15ms), NLLB NMT (~750ms), TTS (~480ms)."),

        ("Q13: Machine translation quality evaluate karne ke liye kaunse metrics use kiye?",
         "Answer: BLEU (BiLingual Evaluation Understudy) n-gram precision ke liye aur chrF++ (Character n-gram F-score) morphological overlap ke liye. "
         "Indian languages agglutinative nature ki hoti hain isliye chrF++ Dravidian languages me exact score batata hai."),

        ("Q14: Production deployment architecture kya hai?",
         "Answer: Frontend React SPA Vercel Edge CDN par hosted hai jisme automatic SPA route rewrites hain. "
         "Backend FastAPI service Render cloud par Python runtime me containerized hai, aur Database Supabase managed cloud par hai."),

        ("Q15: Future Scope kya hai is project ka?",
         "Answer: Future me hum real-time WebSocket full-duplex conversational streaming add kar sakte hain, "
         "edge devices (jaise Raspberry Pi ya Android) ke liye ONNX runtime quantization kar sakte hain, aur 22 official Indian languages tak coverage extend kar sakte hain.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 2))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path

if __name__ == "__main__":
    out = build_pdf()
    print("PDF generated successfully at:", out)
