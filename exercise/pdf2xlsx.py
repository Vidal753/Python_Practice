import pypdf
import re
import sys
import xlsxwriter
import io


def split_cliente(content):
    content = re.split(r'INV[ ]{1,2}CLIENTE|INV[ ]{1,2}DATABANK', content)
    clientes = []
    for cliente in content:
        cliente = re.sub(r'[ ]{2,}', " ", cliente)
        cliente = re.sub(r'\n ', "\n", cliente)
        cliente = re.sub(r'\n{2,}', '\n', cliente).strip()
        clientes.append(cliente)
    return clientes


def extract_code(cliente):
    return cliente.split('\n')[0]


def extract_box_description(cliente, line=1):
    content = cliente.split('\n')[line]
    if 'AREA' not in content and '*' not in content and content[0] != '-':
        return content
    return None


def extract_department(cliente, line=2):
    content = cliente.split('\n')[line]
    if 'AREA' in content:
        return content
    return ''


def extract_template(cliente, line=3):
    content = cliente.split('\n')[line]
    if '*' in content:
        return content.replace('*', '')
    return None


def extract_folders(cliente, template):
    content = cliente.split(template)[1]
    content = content.replace('CLIENTE MOVISTAR', '')
    content = content.replace('CLIENTE TIGO', '')
    content = re.split(r'\n[0-9]{0,4}-', content)
    folders = []
    for folder in content:
        folder = folder.replace('\n', '')
        if folder:
            folders.append(folder.strip())
    return folders


def extract_years(folders):
    years = []
    for folder in folders:
        years += re.findall(r'[0-9]{4,4}', folder)
    return set(years)


def indexar_archivo(path):
    boxes = []
    pdf = pypdf.PdfReader(path)
    content = ''
    for page in pdf.pages:
        content += page.extract_text()
    content = split_cliente(content)
    for cliente in content[1:-1]:
        print('_'*100)
        print(cliente)
        code = extract_code(cliente)
        description = extract_box_description(cliente)
        department = extract_department(cliente, 2 if description else 1)
        if description and department:
            template = extract_template(cliente, 3)
        elif not description and not department:
            template = extract_template(cliente, 1)
        else:
            template = extract_template(cliente, 2)

        if template:
            folders = extract_folders(cliente, template)
        elif department:
            folders = extract_folders(cliente, department)
        else:
            folders = extract_folders(cliente, description if description else code)
        department = str(department).replace("AREA ", "")
        boxes.append(
            dict(code=code, description=description, department=department, template=template, folders=folders))
    for box in boxes:
        years = extract_years(box['folders'])
        if years:
            box['desde'] = min(years)
            box['hasta'] = max(years)
        else:
            box['desde'] = None
            box['hasta'] = None
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    boxes_worksheet = workbook.add_worksheet(name='cajas')
    boxes_columns = ['code', 'description', 'department', 'template', 'desde', 'hasta']
    row = 0
    for column, name in enumerate(boxes_columns):
        boxes_worksheet.write(row, column, name)
    row += 1
    for box in boxes:
        for column, name in enumerate(boxes_columns):
            boxes_worksheet.write(row, column, box[name])
        row += 1

    folder_worksheet = workbook.add_worksheet(name='folders')
    file_columns = ['code', 'description', 'department', 'template']
    row = 0
    for column, name in enumerate(file_columns):
        folder_worksheet.write(row, column, name)
    row += 1

    for box in boxes:
        for folder in box['folders']:
            folder_worksheet.write(row, 0, str(box['code']))
            folder_worksheet.write(row, 1, folder)
            folder_worksheet.write(row, 2, str(box['department']))
            folder_worksheet.write(row, 3, str(box['template']))
            row += 1

    workbook.filename = 'tigo.xlsx'
    workbook.close()


if __name__ == '__main__':
    indexar_archivo(sys.argv[1])
