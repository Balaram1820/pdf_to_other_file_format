import csv
import json
import xml.etree.ElementTree as ET
from io import StringIO

import PyPDF2


def pdf_to_text(pdf_path, password=None):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        # Decrypt the PDF if it is encrypted
        if reader.is_encrypted:
            reader.decrypt(password)

        text_buffer = StringIO()
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text_buffer.write(page.extract_text())

        text = text_buffer.getvalue()
        text_buffer.close()

        return text


def text_to_csv(text, csv_path):
    lines = text.strip().split('\n')

    # Write the text to a CSV file
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([line.split('\t') for line in lines])


def text_to_json(text, json_path):
    lines = text.strip().split('\n')
    data = [line.split('\t') for line in lines]
    json_data = json.dumps(data)

    # Write the text to a JSON file
    with open(json_path, 'w') as json_file:
        json_file.write(json_data)


def text_to_xml(text, xml_path):
    lines = text.strip().split('\n')
    root = ET.Element('root')
    for line in lines:
        row = ET.SubElement(root, 'row')
        columns = line.split('\t')
        for i, column in enumerate(columns):
            col = ET.SubElement(row, f'col{i+1}')
            col.text = column

    tree = ET.ElementTree(root)

    # Write the text to an XML file
    tree.write(xml_path)


# Example usage
pdf_file_path = 'path/to/pdf/file.pdf'
pdf_password = 'password'  # Set the password if applicable
text_output_path = 'output.txt'
csv_output_path = 'output.csv'
json_output_path = 'output.json'
xml_output_path = 'output.xml'

# Convert the PDF to text
text_output = pdf_to_text(pdf_file_path, pdf_password)

# Save the text to a file
with open(text_output_path, 'w') as text_file:
    text_file.write(text_output)

# Convert the text to CSV
text_to_csv(text_output, csv_output_path)

# Convert the text to JSON
text_to_json(text_output, json_output_path)

# Convert the text to XML
text_to_xml(text_output, xml_output_path)

# Display a message
print("PDF conversion complete. The text has been saved in 'output.txt', 'output.csv', 'output.json', and 'output.xml'.")
