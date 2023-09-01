from functions import document_options as doc_opt
from docx import Document
from datetime import date
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


# todo -> Make Undertaking document generator
def parent_letter_generator(defaulter_details: dict, filepath: str, mentor_name: str):
    today = date.today()
    doc = Document()
    doc_opt.make_header_for_doc(doc)
    to_para = doc.add_paragraph()
    to_para.add_run("To,").bold = True
    father_name_para = doc.add_paragraph()
    father_name_para.add_run(defaulter_details['father_name']).bold = True
    address_para = doc.add_paragraph()
    address_para.add_run(defaulter_details['address'])
    address_para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    doc_opt.make_heading_for_doc(doc, 'Subject: Attendance of your ward in theory classes and Practical sessions ',
                                 mentor_name, today.strftime("%B %d, %Y"))
    dear_parent_line = doc.add_paragraph()
    dear_parent_line.add_run('Dear Parent,')
    content_para1 = doc.add_paragraph()
    content_para1.add_run(f"This is to inform you that your ward is having less attendance "
                          f"({defaulter_details['attendance']}) in theory classes, practical sessions and tutorials.")
    content_para1.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    content_para2 = doc.add_paragraph()
    content_para2.add_run("As per the rule of Mumbai University, your ward will not be allowed to appear for the "
                          "examination if he/she fails to maintain 75% attendance in the semester.")
    content_para2.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    content_para3 = doc.add_paragraph()
    content_para3.add_run("We request you to immediately look into your ward’s attendance with the highest priority.")
    content_para3.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    hod_signature_line = doc.add_paragraph()
    hod_signature_line.add_run("_________________________________________\n")
    hod_signature_line.add_run("Head of Department").bold = True
    doc_opt.line_space_setter(doc)
    doc.save(f"{filepath}/{defaulter_details['name']} Parent Letter {today.strftime('%B %d, %Y')}.docx")
