"""Builds resume.pdf: single column, standard headings, embedded Times New Roman,
real selectable text and no tables, images or icons, so applicant tracking systems read it cleanly.

Usage:  python build_resume.py [output.pdf]     (needs: pip install reportlab)
Edit the CONTENT section below, then run it again.
"""
import sys
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, HRFlowable, Paragraph, SimpleDocTemplate, Spacer

# ---------------------------------------------------------------- CONTENT
NAME = "Jayati Rai"
CONTACT = [
    "Varanasi, India",
    "jayatirai3@gmail.com",
    '<link href="https://github.com/Jayati-Rai">github.com/Jayati-Rai</link>',
    '<link href="https://www.linkedin.com/in/jayati-rai/">linkedin.com/in/jayati-rai</link>',
]

SUMMARY = (
    "Android developer who builds user-focused apps in Kotlin and Jetpack Compose, with Firebase, Room and Firestore "
    "for data, and automates manual spreadsheet work with Python. Completed the 12-course Meta Android Developer "
    "Professional Certificate and is pursuing an M.Sc. in Computational Science &amp; Applications at Banaras Hindu "
    "University, building on a B.Sc. in Physics and a BCA. Brings an analytical, problem-solving approach to "
    "mobile development. Seeking an Android developer role or internship."
)

EDUCATION = [
    ("Banaras Hindu University, Varanasi", "Aug 2025 \u2013 Present",
     "M.Sc. Computational Science &amp; Applications"),
    ("Ewing Christian College", "Nov 2021 \u2013 Jun 2024", "B.Sc. Physics"),
    ("Manipal University Jaipur (Online)", "Nov 2021 \u2013 Jun 2024", "Bachelor of Computer Applications (BCA)"),
]

PROJECTS = [
    ("Eccian2.0", "Kotlin, Jetpack Compose, Firebase",
     '<link href="https://github.com/Jayati-Rai/Eccian2.0">github.com/Jayati-Rai/Eccian2.0</link>',
     [
         "Developed an Android campus app in Kotlin and Jetpack Compose that consolidates academic resources, news, "
         "notifications and student tools into a single platform.",
         "Organized content into study notes, previous-year questions, news and notifications, and subject-wise resources.",
         "Integrated Firebase for backend services.",
     ]),
    ("Shelf Organizer", "Kotlin, Jetpack Compose, Room, SQL, Firestore",
     '<link href="https://github.com/Jayati-Rai/Shelf_Organizer">github.com/Jayati-Rai/Shelf_Organizer</link>',
     [
         "Engineered an Android inventory app in Kotlin and Jetpack Compose for managing items across multiple stores, "
         "with structured item records, search and filtering, and inventory tracking.",
         "Combined Room (SQL) for persistent local storage with Firestore for cloud sync.",
     ]),
    ("Automated Vetan Bill Generator", "Python, OpenPyXL, Excel VBA, Flask",
     '<link href="https://github.com/Jayati-Rai/pdf-to-jsl">github.com/Jayati-Rai/pdf-to-jsl</link>',
     [
         "Automated the preparation of salary grant sheets for aided schools in Uttar Pradesh using Python and OpenPyXL "
         "on Excel templates.",
         "Preserved formulas, merged cells, formatting and macro-enabled workbooks (Excel VBA) so generated sheets keep "
         "the original template intact.",
         "Reduced preparation time from 15\u201340 minutes to under 30 seconds per sheet (estimate documented in the repository).",
     ]),
]

SKILLS = [
    ("Languages", "Kotlin, Java, Python, C, C++"),
    ("Android", "Jetpack Compose, Navigation, Android Studio, App architecture"),
    ("Data and Backend", "Firebase Firestore, Cloud Storage, Room, SQL, REST APIs, Ktor"),
    ("Tools", "Git, GitHub, Flask, OpenPyXL, Excel VBA"),
    ("Concepts", "Object-oriented programming, data structures and algorithms (in progress), UX/UI design principles"),
    ("Domain", "Physics, scientific computing, machine learning basics"),
]

CERTIFICATIONS = [
    ("Meta Android Developer Professional Certificate, Meta (Coursera)", "Oct 2026",
     "12-course program covering Android development, Kotlin, UX/UI design, data, React, React Native, an Android "
     "capstone project and coding interview preparation."),
]
CERT_COURSES = (
    "Principles of UX/UI Design (Aug 2024); Create the User Interface in Android Studio (Oct 2024); Advanced "
    "Programming in Kotlin (Dec 2024); Working with Data in Android (Dec 2024); Coding Interview Preparation "
    "(Oct 2026); Android App Capstone (Oct 2026)."
)
CERT_LINK = '<link href="https://coursera.org/verify/professional-cert/CVJ8XI1Q37QZ">coursera.org/verify/professional-cert/CVJ8XI1Q37QZ</link>'

# ---------------------------------------------------------------- LAYOUT
FONT_DIR = "C:/Windows/Fonts/"
for face, file in (("TNR", "times.ttf"), ("TNR-B", "timesbd.ttf"), ("TNR-I", "timesi.ttf"), ("TNR-BI", "timesbi.ttf")):
    pdfmetrics.registerFont(TTFont(face, FONT_DIR + file))
pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-B", italic="TNR-I", boldItalic="TNR-BI")

SIZE, LEAD = 10.5, 12.6
base = ParagraphStyle("base", fontName="TNR", fontSize=SIZE, leading=LEAD, textColor="black")
name_style = ParagraphStyle("name", parent=base, fontName="TNR-B", fontSize=22, leading=26, alignment=TA_CENTER)
contact_style = ParagraphStyle("contact", parent=base, alignment=TA_CENTER)
summary_style = ParagraphStyle("summary", parent=base)
heading_style = ParagraphStyle("heading", parent=base, fontName="TNR-B", fontSize=11.5, leading=14, spaceBefore=7)
bullet_style = ParagraphStyle("bullet", parent=base, leftIndent=16, bulletIndent=5, bulletFontName="TNR", spaceBefore=1)
right_style = ParagraphStyle("right", parent=base, alignment=TA_RIGHT)

MARGIN = 0.6 * inch
WIDTH = letter[0] - 2 * MARGIN


class Row(Flowable):
    """Left text and right-aligned text on one baseline (for dates)."""

    def __init__(self, left, right, left_style=base, right_width=1.7 * inch):
        super().__init__()
        self.left = Paragraph(left, left_style)
        self.right = Paragraph(right, right_style)
        self.right_width = right_width

    def wrap(self, avail_w, avail_h):
        self.avail_w = avail_w
        _, lh = self.left.wrap(avail_w - self.right_width, avail_h)
        _, rh = self.right.wrap(self.right_width, avail_h)
        self.height = max(lh, rh)
        return avail_w, self.height

    def draw(self):
        self.left.drawOn(self.canv, 0, self.height - self.left.height)
        self.right.drawOn(self.canv, self.avail_w - self.right_width, self.height - self.right.height)


def heading(title):
    return [Paragraph(title.upper(), heading_style), HRFlowable(width="100%", thickness=0.8, color="black", spaceBefore=1, spaceAfter=3)]


def bullets(items):
    return [Paragraph(text, bullet_style, bulletText="\u2022") for text in items]


def build(path):
    doc = SimpleDocTemplate(
        path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=0.5 * inch, bottomMargin=0.45 * inch,
        title=f"{NAME} - Resume", author=NAME, subject="Resume",
    )
    s = [Paragraph(NAME, name_style), Paragraph(" | ".join(CONTACT), contact_style), Spacer(1, 4)]

    s += heading("Summary") + [Paragraph(SUMMARY, summary_style)]

    s += heading("Technical Skills")
    for label, items in SKILLS:
        s.append(Paragraph(f"<b>{label}:</b> {items}", base))

    s += heading("Projects")
    for title, stack, link, points in PROJECTS:
        s += [Row(f"<b>{title}</b> | <i>{stack}</i>", link, right_width=2.55 * inch)] + bullets(points) + [Spacer(1, 3)]

    s += heading("Education")
    for school, dates, degree in EDUCATION:
        s += [Row(f"<b>{school}</b>", dates), Paragraph(f"<i>{degree}</i>", base), Spacer(1, 2)]

    s += heading("Certifications")
    for title, date, detail in CERTIFICATIONS:
        s += [Row(f"<b>{title}</b>", date), Paragraph(detail, base)]
    s += [Paragraph(f"<b>Courses completed:</b> {CERT_COURSES}", base), Paragraph(f"<b>Credential:</b> {CERT_LINK}", base)]

    doc.build(s)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "resume.pdf")
