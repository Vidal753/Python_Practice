import pypdf
import re
import sys
import xlsxwriter
import io
from alive_progress import alive_bar


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
    content = cliente.split('\n')[0]
    content = re.findall(r'[0-9]{6,6}', content)
    if len(content) > 0:
        return [content[0], 1]
    return [None, 0]


def extract_box_description(cliente, line):
    content = cliente.split('\n')[line]
    if 'AREA' not in content and '*' not in content and content[0] != '-':
        return [content, line + 1]
    return [None, line]


def extract_department(cliente, line):
    content = cliente.split('\n')[line]
    if 'AREA' in content:
        return [content.replace('AREA ', ''), line + 1]
    return ['', line]


def extract_template(cliente, line):
    content = cliente.split('\n')[line]
    if '*' in content:
        return [content.replace('*', ''), line + 1]
    return ['', line]


def extract_folders(cliente):
    content = cliente.replace('CLIENTE MOVISTAR', '').replace('CLIENTE TIGO', '')
    content = re.split(r'\n[0-9]{0,5}-', content)[1:]
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


def extract_customer_name(folder):
    return [folder[0], 1]


def extract_customer_number(folder, line):
    if len(folder) > line:
        content = re.findall(r'CLIENTE [0-9]{0,7}', folder[line])
        if len(content) > 0:
            return [folder[line], line + 1]
    return [None, line]


def extract_customer_account(folder, line):
    if len(folder) > line:
        content = re.findall(r'CUENTA [0-9]{0,7}', folder[line])
        if len(content) > 0:
            return [folder[line], line + 1]
    return [None, line]


def extract_customer_cel(folder, line):
    if len(folder) > line:
        content = re.findall(r'CELULAR [0-9]{0,8}', folder[line])
        if len(content) > 0:
            return [folder[line], line + 1]
    return [None, line]


def extract_customer_order(folder, line):
    if len(folder) > line:
        content = re.findall(r'OS [0-9]{0,6}', folder[line])
        if len(content) > 0:
            return [folder[line], line + 1]
    return [None, line]


def extract_customer_date(folder, line):
    if len(folder) > line:
        content = re.findall(r'[0-9]{2,2}/', folder[line])
        if len(content) > 0:
            return folder[line]
    return None


def customer_folders(cliente):
    content = cliente.replace('CLIENTE MOVISTAR', '').replace('CLIENTE TIGO', '')
    content = re.split(r'\n[0-9]{0,5}-', content)[1:]
    customers = []
    for folder in content:
        folder = re.split('\n', folder)
        if len(folder) > 2:
            is_customer = re.findall(r'CLIENTE [0-9]{7,7}', folder[1])
            if is_customer:
                customer_name, position_num = extract_customer_name(folder)
                customer_number, position_acc = extract_customer_number(folder, position_num)
                customer_account, position_cel = extract_customer_account(folder, position_acc)
                customer_cel, position_or = extract_customer_cel(folder, position_cel)
                customer_order, position_date = extract_customer_order(folder, position_or)
                customer_date = extract_customer_date(folder, position_date)
                customers.append(
                    dict(nombre_cliente=customer_name, numero_cliente=customer_number, numero_cuenta=customer_account,
                         numero_celular=customer_cel, orden=customer_order, fecha=customer_date))
    if len(customers) > 0:
        return [customers, True]
    return [customers, False]


def generate_customer_sheet(workbook, customers):
    customers_worksheet = workbook.add_worksheet(name='clientes')
    customers_columns = ['nombre_cliente', 'numero_cliente', 'numero_cuenta', 'numero_celular', 'orden', 'fecha']
    row = 0
    for column, name in enumerate(customers_columns):
        customers_worksheet.write(row, column, name)
    row += 1
    for customer in customers:
        for info in customer:
            for column, name in enumerate(customers_columns):
                customers_worksheet.write(row, column, info[name])
            row += 1


def generate_box_sheet(workbook, boxes):
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


def indexar_archivo(path):
    boxes = []
    customers = []
    pdf = pypdf.PdfReader(path)
    content = ''
    with alive_bar(len(pdf.pages)) as bar:
        print("Cargando datos...")
        for page in pdf.pages:
            content += page.extract_text()
            bar()
        content = split_cliente(content)
    with alive_bar(len(content) - 1) as bar:
        print("Recolectando datos...")
        for cliente in content[1:]:
            customer, is_customer = customer_folders(cliente)
            if is_customer:
                customers.append(customer)
            else:
                code, position_des = extract_code(cliente)
                description, position_dep = extract_box_description(cliente, position_des)
                department, position_tem = extract_department(cliente, position_dep)
                template, position_folder = extract_template(cliente, position_tem)
                folders = extract_folders(cliente)

                boxes.append(
                    dict(code=code, description=description, department=department, template=template, folders=folders))
            bar()
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
    generate_box_sheet(workbook, boxes)
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

    generate_customer_sheet(workbook, customers)
    workbook.filename = 'tigo.xlsx'
    workbook.close()
    print('Archivo generado!')


if __name__ == '__main__':
    indexar_archivo(sys.argv[1])
