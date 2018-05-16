import re
import pandas as pd

# Definicion de las funciones para extraccion de los datos del archivo, a partir de expresiones regulares
def extract_permit_date(data):
    permit_date_re = '(\d{2})/(\d{2})/(\d{4})'
    if re.search(permit_date_re, data):
        return re.search(permit_date_re, data).group(3) + '-' + re.search(permit_date_re, data).group(1) + '-'\
               + re.search(permit_date_re, data).group(2)
    else:
        return ''


def extract_house_street_address(data):
    house_street_address_re = '(\d{4,}\s[a-zA-Z]([a-zA-Z0-9]+ ?)+)(\s+)(\d{12,14})'
    if re.search(house_street_address_re, data):
        return re.search(house_street_address_re, data).group(1)
    else:
        return ''


def extract_house_parcel_number(data):
    house_parcel_number_re = '\d{12,14}'
    if re.search(house_parcel_number_re, data):
        return re.search(house_parcel_number_re, data).group()
    else:
        return ''


def extract_lot(data):
    lot_re = '(\d{12,14})\s+(([\w]+ ?)+)'
    if re.search(lot_re, data):
        return re.search(lot_re, data).group(2)
    else:
        return ''


def extract_more_lot(data):
    more_lot_re = '^\s{,100}(([\w/]+ {1,3})+)'
    if re.search(more_lot_re, data):
        return re.search(more_lot_re, data).group(1)
    else:
        return ''


def extract_permit_type(data):
    permit_type_re = '(\d{12,14})\s+(([\w,/-]+ )+)?\s+(\w{2,4})\s+([\w/]+ ?)'
    if re.search(permit_type_re, data):
        return re.search(permit_type_re, data).group(5)
    else:
        return ''


def extract_more_permit_type(data):
    more_permit_type_re = '^.{103,126}?(([\w/]+ ?)+)'
    if re.search(more_permit_type_re, data):
        return re.search(more_permit_type_re, data).group(1)
    else:
        return ''


def extract_permit_description(data):
    permit_description_re = '(( [\w,/]+)+)\s+(\$\d+(,\d+)+)'
    if re.search(permit_description_re, data):
        return re.search(permit_description_re, data).group(1)
    else:
        return ''


def extract_more_permit_description(data):
    more_permit_description_re = '^.{125,149}?(([\w\.&,]+ ?)+)'
    if re.search(more_permit_description_re, data):
        return re.search(more_permit_description_re, data).group(1)
    else:
        return ''


def extract_cost(data):
    cost_re = '\$(\d+)(,(\d+))?'
    if re.search(cost_re, data):
        cost = re.search(cost_re, data).group(1)
        if re.search(cost_re, data).group(3):
            cost += re.search(cost_re, data).group(3)
        return cost
    else:
        return ''


def extract_square_footage(data):
    square_footage_re = '(\$(\d+)(,(\d+))?)\s+(\d+(,\d+)?)'
    if re.search(square_footage_re, data):
        return re.search(square_footage_re, data).group(5)
    else:
        return ''


def extract_company_name(data):
    company_name_re = '(\$(\d+)(,(\d+))?)\s{4,9}(\d+(,\d+)?)?\s{4,21}((\w+ )+)'
    if re.search(company_name_re, data):
        return re.search(company_name_re, data).group(7)
    else:
        company_name_re = '\d{12,14}.{85,110}?((\w+ ?)+)'
        if re.search(company_name_re, data):
            return re.search(company_name_re, data).group(1)
        else:
            return ''


def extract_more_company_name(data):
    more_company_name_re = '^.{168,190}?(([\w\.\*&]+ ?)+)'
    if re.search(more_company_name_re, data):
        return re.search(more_company_name_re, data).group(1)
    else:
        return ''


def extract_house_owner_name(data):
    house_owner_name_re = '(( [\w\.\*&,]+)+)$'
    if re.search(house_owner_name_re, data):
        return re.search(house_owner_name_re, data).group(1)
    else:
        return ''


def extract_more_house_owner_name(data):
    more_house_owner_name_re = '.{220,}(( [\w\.\*&,]+)+)$'
    if re.search(more_house_owner_name_re, data):
        return re.search(more_house_owner_name_re, data).group(1)
    else:
        return ''


# Defino el archivo del cual extraere los datos y lo abro
datos = "./city.txt"
with open(datos) as f:
    reader = f.readlines()
# Creo el diccionario con los campos que contendra la salida
salida = {
    'permit_date': [],
    'house_street_address': [],
    'house_parcel_number': [],
    'lot': [],
    'permit_type': [],
    'permit_description': [],
    'cost': [],
    'square_footage': [],
    'company_name': [],
    'house_owner_name': []
}
# Creo las variables que usare para evitarme el problema con las concatenaciondes de string y None types
current_permit_date = ''
current_house_street_address = ''
current_house_parcel_number = ''
current_lot = ''
current_permit_type = ''
current_permit_description = ''
current_cost = ''
current_square_footage = ''
current_company_name = ''
current_house_owner_name = ''
# Itero sobre todas las lineas del archivo
for contador, line in enumerate(reader):
    # Si la linea contiene alguna de esas palabras (APN, Issue Date, Code al finalizar la linea o Permits Issued) ignoro
    # la linea, ya que forma parte de las cabeceras de las tablas y de la pagina, y no contienen informacion que me
    # interese
    if re.search('APN', line) or re.search('Issue Date', line) or re.search('Code$', line) \
            or re.search('Permits Issued', line):
        continue
    # Si la linea a la que llego contiene solo un salto de linea, es el cambio de entrada, por lo que guardo los datos
    # que ya tengo en el diccionario y luego continuo con la siguiente linea
    if re.search('^\\n$', line) and contador > 4:
        salida['permit_date'].append(current_permit_date)
        salida['house_street_address'].append(current_house_street_address)
        salida['house_parcel_number'].append(current_house_parcel_number)
        salida['lot'].append(current_lot)
        salida['permit_type'].append(current_permit_type)
        salida['permit_description'].append(current_permit_description)
        salida['cost'].append(current_cost)
        salida['square_footage'].append(current_square_footage)
        salida['company_name'].append(current_company_name)
        salida['house_owner_name'].append(current_house_owner_name)
        continue
    # Si la linea que estoy leyendo contiene la una fecha de permiso, quiere decir que esta comenzando dicha entrada,
    # por lo que busco los campos necesarios
    new_line = extract_permit_date(line) is not ''
    if new_line:
        current_permit_date = extract_permit_date(line)
        current_house_street_address = extract_house_street_address(line)
        current_house_parcel_number = extract_house_parcel_number(line)
        current_lot = extract_lot(line)
        current_permit_type = extract_permit_type(line)
        current_permit_description = extract_permit_description(line)
        current_cost = extract_cost(line)
        current_square_footage = extract_square_footage(line)
        current_company_name = extract_company_name(line)
        current_house_owner_name = extract_house_owner_name(line)
    # De lo contrario busco las continuaciones de los campos pertinentes y lo concateno con lo que habia extraido
    # previamente
    elif contador > 5:
        current_lot += ' ' + str(extract_more_lot(line))
        current_permit_type += ' ' + str(extract_more_permit_type(line))
        current_permit_description += ' ' + str(extract_more_permit_description(line))
        current_company_name += ' ' + str(extract_more_company_name(line))
        current_house_owner_name += ' ' + str(extract_more_house_owner_name(line))
# Por ultimo creo el dataframe y lo transformo a un archivo CSV
df = pd.DataFrame(salida)
df.to_csv('./salida.csv', index=0)