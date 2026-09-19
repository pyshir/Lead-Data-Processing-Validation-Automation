import re
from datetime import datetime

class StandardData:

    def __init__(self, lead_no, name, email, phone, date, amount, product_id, address, status, website=None, note=None, error=None, currency='BDT'):        
        self.lead_no = lead_no
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.amount = amount
        self.currency = currency
        self.product_id = product_id
        self.address = address        
        self.website = website
        self.note = note
        self.error = error
        self.status = status

class DataGenerate:

    def __init__(self):
        self.all_data = [] # ['LEAD #001\nCustomer:....', 'LEAD #002\n...']
        self.valid_data = []
        self.cleaned_valid_data = []
        self.invalid_data = []
        self.duplicate_data = {}

    def all_data_extract(self):

        with open('data.txt', 'r') as f:
            next(f)
            data_slice = ''
            
            for i in f:
                x = re.search(r'^-{10,}$', i)
                if not x:
                    data_slice += i
                else:
                    self.all_data.append(data_slice)
                    data_slice = ''

    def valid_invalid_data_extract(self):
        
        for i in self.all_data:
            validity = True
            error = '\n'

            lead_no = re.search(r'(?<=LEAD\s#)\d{3}(?=\n)', i)
            if lead_no:
                lead_no = lead_no.group()
            else:
                error += '- Invalid lead no\n'
                validity = False
                lead_no = None

            name = re.search(r'((?<=customer:\s)|(?<=name:\s))[\w\s\.\']+(?=\n)', i, re.IGNORECASE)
            if name:
                name = name.group()
                name = name.strip().capitalize()
                name = re.sub(r'[\s]+', ' ', name)
                if name in ('Unknown', 'N/a', 'Na', 'None'):
                    error += '- Invalid name\n'
                    validity = False
                    name = None
            else:
                error += '- Invalid name\n'
                validity = False
                name = None

            email = re.search(r'((?<=Email:\s)|(?<=Email\s\=\>\s)|(?<=contact:\s))\s*[a-zA-Z]([\w\-\_]*[a-zA-Z]+\.?\w+)*@[a-zA-Z](\w*\.\w{2,})+(?=\n)', i, re.IGNORECASE)
            if email:
                email = email.group()
                email = email.strip().lower()
            else:
                error += '- Invalid email\n'
                validity = False
                email = None

            phone = re.search(r'((?<=Phone:)|(?<=Mobile:))\s*\+?\d[\d\(\)\-\s]+\d(?=\n)', i, re.IGNORECASE)
            if phone:
                phone = phone.group()
                phone = phone.strip()
                phone += '.'
                phone_counter = 2
                z = 0

                while z < len(phone):

                    if phone[z] == '(' and phone[z+1] == ')':
                        phone_counter +=1
                        break

                    elif phone[z] == '-' and phone[z+1] == '-':
                        phone_counter +=1
                        break

                    elif phone[z] == ' ' and phone[z+1] == ' ':
                        phone_counter +=1
                        break

                    elif phone[z] == '(':
                        phone_counter += 1
                        z += 1

                    elif  phone[z] == ')':
                        if phone_counter > 2:
                            phone_counter -= 1
                            z += 1
                        else:
                            phone_counter -= 1
                            break

                    else:
                        z += 1

                if phone_counter == 2:
                    phone = re.sub(r'\D', '', phone)

                    phone_val = True        
                    if 13 < len(phone) or len(phone) < 10:
                        phone_val = False

                    for p in phone:
                        if phone.count(p) > 9:
                            phone_val =  False
                            break
            
                    if not phone_val:
                        error += '- Invalid Phone\n'
                        validity = False
                        phone = None
                else:
                    error += '- Invalid Phone\n'
                    validity = False
                    phone = None

            else:
                error += '- Invalid Phone\n'
                validity = False
                phone = None
            

            date = re.search(r'(?<=Date:\s)(\d{1,2}(/|-)\d{1,2}(/|-)\d{2,4}|\w+\s\d{1,2}\,?\s\d{2,4}|\d{1,2}\s\w+,?\s\d{2,4}|\d{2,4}(/|-)\d{1,2}(/|-)\d{1,2})(?=\n)', i, re.IGNORECASE)

            if date:
                date = date.group()

                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%y', '%d-%m-%y', '%m/%d/%y', '%m-%d-%y', '%b %d, %Y', '%B %d, %Y', '%b %d, %y', '%B %d, %y', '%b %d %Y', '%B %d %Y', '%b %d %y', '%B %d %y', '%d %B, %Y', '%d %b, %Y', '%d %B, %y', '%d %b, %y', '%d %B %Y', '%d %b %Y', '%d %B %y', '%d %b %y', '%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d']

                date_match = False

                for d in date_formats:
                    try:
                        date = datetime.strptime(date, d)                        
                        date_match = True
                        break

                    except ValueError:
                        continue

                if date_match:
                    date = date.strftime('%d/%m/%Y')

                else:
                    error += '- Invalid date\n'
                    validity =  False
                    date = None

            amount = re.search(r'((?<=Budget:\s)|(?<=price:\s))[\w\d\s\$\,\.]+(?=\n)', i)
            if amount:
                amount = amount.group()
                if 'EUR' in amount:
                    amount = amount.replace('.', '').replace(',', '.')
                    amount = re.sub(r'[\s,]', '', amount)
                else:
                    amount = re.sub(r'[\s,]', '', amount)

                curr = {'EUR':143, 'GBP': 166, '$': 122, 'USD': 122, 'Tk': 1, 'BDT': 1, 'taka': 1}

                for key, value in curr.items():
                    if key in amount:
                        amt = re.sub(r'[a-zA-Z$]', '', amount)
                        amt = float(amt)
                        amount = round(amt * value, 2)
                        break
            else:
                error += '- Invalid amount\n'
                validity = False
                amount = None


            product_id = re.search(r'((?<=Product id:\s)|(?<=Product:\s))[\w\-\d]+(?=\n)', i, re.IGNORECASE)

            if product_id:
                product_id = product_id.group()
            else:
                error += '- Invalid product-id\n'
                validity = False
                product_id = None

            address = re.search(r'((?<=address:\s)|(?<=location:\s))[^\n]+(?=\n)', i, re.IGNORECASE)

            if address:
                address = address.group()
                address = address.strip().lower()
                if address in ('not provided', 'n/a', 'n\a', 'none'):
                    error += '- Invalid address\n'
                    validity = False
                    address = None
            else:
                error += '- Invalid address\n'
                validity = False
                address = None

            website = re.search(r'(?<=Website:\s)[\w:\/\.]+(?=\n)', i, re.IGNORECASE)

            if website:
                website = website.group()
            else:
                website = None
            

            note = re.search(r'(?<=Notes:\s)[\w\W]+(?=\n)', i, re.IGNORECASE)

            if note:
                note = note.group()
            else:
                note = None
            

            if validity:
                status = 'Valid'
                error = None
                standard_data = StandardData(lead_no, name, email, phone, date, amount, product_id, address, status, website, note, error)
                self.valid_data.append(standard_data)
            else:
                status = 'Invalid'
                standard_data = StandardData(lead_no, name, email, phone, date, amount, product_id, address, status, website, note, error)
                self.invalid_data.append(standard_data)

    def duplicate_data_extract(self):
        for i in range(len(self.valid_data)):
            for j in range(i+1, len(self.valid_data)):

                if self.valid_data[i].email == self.valid_data[j].email and self.valid_data[i].phone == self.valid_data[j].phone:

                    count = True
                    for p, q in self.duplicate_data.items():

                        if self.valid_data[i].lead_no in p:
                            del self.duplicate_data[p]
                            p += (self.valid_data[j].lead_no,)
                            self.duplicate_data[p] = ['EMAIL', 'PHONE']
                            count = False
                            break
                    

                    if count:
                        self.duplicate_data[self.valid_data[i].lead_no, self.valid_data[j].lead_no] = ['EMAIL', 'PHONE']
                    break

                elif self.valid_data[i].email == self.valid_data[j].email:

                    count = True
                    for p, q in self.duplicate_data.items():

                        if self.valid_data[i].lead_no in p:                            
                            del self.duplicate_data[p]
                            p += (self.valid_data[j].lead_no,)
                            self.duplicate_data[p] = ['EMAIL']
                            count = False
                            break

                    if count:
                        self.duplicate_data[self.valid_data[i].lead_no, self.valid_data[j].lead_no] = ['EMAIL']
                    break

                elif self.valid_data[i].phone == self.valid_data[j].phone:

                    count = True
                    for p, q in self.duplicate_data.items():
                        if self.valid_data[i].lead_no in p:                            
                            del self.duplicate_data[p]
                            p_new = p + (self.valid_data[j].lead_no,)
                            p = p_new
                            self.duplicate_data[p] = ['PHONE']
                            count = False
                            break

                    if count:
                        self.duplicate_data[self.valid_data[i].lead_no, self.valid_data[j].lead_no] = ['PHONE']
                    break

    def cleaned_valid_data_extract(self):
        for i in self.valid_data:
            if self.cleaned_valid_data:
                count = True
                for j in self.cleaned_valid_data:
                    if i.email == j.email and i.phone == j.phone:
                        count = False
                        break

                    elif i.email == j.email or i.phone == j.phone:
                        count = False
                        break

                if count:
                    self.cleaned_valid_data.append(i)
            else:
                self.cleaned_valid_data.append(i)

    def duplicate_data_count(self):
        count = 0
        for i, j in self.duplicate_data.items():
            if len(i) > 1:
                count += len(i) - 1
            elif len(i) == 1:
                count += 1
        return count

    def invalid_data_count(self):
        invalid_emails = 0 # Invalid email
        invalid_phones = 0 # Invalid Phone
        invalid_dates = 0 # Invalid date
        invalid_product_ids = 0 # Invalid product-id
        for i in self.invalid_data:
            if i.error is not None:
                if 'Invalid email' in i.error:
                    invalid_emails += 1

                if 'Invalid Phone' in i.error:
                    invalid_phones += 1

                if 'Invalid date' in i.error:
                    invalid_dates += 1

                if 'Invalid product-id' in i.error:
                    invalid_product_ids += 1

        return invalid_emails, invalid_phones, invalid_dates, invalid_product_ids 

    def missing_data_count(self):
        missing_name = 0
        missing_email = 0
        missing_phone = 0
        missing_address = 0
        missing_website = 0
        for i in self.invalid_data:
            if i.name == None:
                missing_name += 1
            if i.email == None:
                missing_email += 1
            if i.phone == None:
                missing_phone += 1
            if i.address == None:
                missing_address += 1
            if i.website == None:
                missing_website += 1
        for j in self.valid_data:
            if j.website == None:
                missing_website += 1

        return missing_name, missing_email, missing_phone, missing_address, missing_website
            
    def website_note_count(self):
        website_count = 0
        note_count = 0
        for i in self.valid_data:
            if i.website is not None:
                website_count += 1
            if i.note is not None:
                note_count += 1
        for j in self.invalid_data:
            if j.website is not None:
                website_count += 1
            if j.note is not None:
                note_count += 1

        return website_count, note_count

class DataClean:

    def none_clean(self, obj_data):
        clean_data = {
            key:value
            for key, value in obj_data.__dict__.items()
            if value is not None
        }
        return clean_data


if __name__ == '__main__':


    data_generate = DataGenerate()

    data_clean = DataClean()


    data_generate.all_data_extract()

    data_generate.valid_invalid_data_extract()

    data_generate.duplicate_data_extract()

    data_generate.cleaned_valid_data_extract()


# 6. Output Format
    with open('clean_leads.txt', 'w') as f:
        for i in data_generate.cleaned_valid_data:
            f.write(f"""
LEAD_ID: {i.lead_no}
NAME: {i.name}
EMAIL: {i.email}
PHONE: {i.phone}
DATE: {i.date}
AMOUNT: {i.amount}
CURRENCY: BDT
PRODUCT_ID: {i.product_id}
WEBSITE: {i.website}
ADDRESS: {i.address}
STATUS: {i.status}
NOTE: {i.note}
ERROR: {i.error}
{'-'*50}
""")

# 7. Invalid Data Report

    with open('invalid_leads.txt', 'w') as  f:   
        for i in data_generate.invalid_data:
            x = data_clean.none_clean(i)
            for p, q in x.items():
               f.write(f'{p}: {q}\n')
            f.write(f'{'-'*50}\n\n\n')

# 8. Duplicate Report

    with open('duplicate_leads.txt', 'w') as f:
        count = 1        
        for i, j in data_generate.duplicate_data.items():
            f.write(f'DUPLICATE GROUP #{count}\n\n')
            count += 1
            f.write(f'PRIMARY: \nLEAD #{i[0]}\n')
            dup_data = ''
            for p in range(1, len(i)):
                dup_data += f'LEAD #{i[p]}\n'
            f.write(f'\nDUPLICATE: \n{dup_data}')
            mat_data = ''
            for q in range(len(j)):
                mat_data += f'{j[q]}\n'        
            f.write(f'\nMATCHED BY: \n{mat_data}{'-'*50}\n\n')
        
# 9. Summary 

    dup_leads = data_generate.duplicate_data_count()
    invalid_emails, invalid_phones, invalid_dates, invalid_product_ids = data_generate.invalid_data_count()

    missing_name, missing_email, missing_phone, missing_address, missing_website = data_generate.missing_data_count()

    website_count, note_count = data_generate.website_note_count()

    with open('summary_report.txt', 'w') as f:

        f.write(f'{'='*50}\nLEAD PROCESSING SUMMARY\n{'='*50}\n\n')
        f.write(f"""
Total Leads: {len(data_generate.all_data)}\n\n
Valid Leads: {len(data_generate.cleaned_valid_data)}
Invalid Leads: {len(data_generate.invalid_data)}
Duplicate Leads: {dup_leads}\n

""")
        f.write(f'{'-'*50}\nVALIDATION ERRORS\n{'-'*50}\n\n')
        f.write(f"""
Invalid Emails: {invalid_emails}
Invalid Phones: {invalid_phones}
Invalid Dates: {invalid_dates}
Invalid Product IDs: {invalid_product_ids}\n\n
""")

        f.write(f'{'-'*50}\nMISSING DATA\n{'-'*50}\n\n')
        f.write(f"""
Missing Name: {missing_name}
Missing Email: {missing_email}
Missing Phone: {missing_phone}
Missing Address: {missing_address}
Missing Website: {missing_website}\n\n
""")

        f.write(f'{'-'*50}\nOTHER\n{'-'*50}\n\n')
        f.write(f"""
Leads With Website: {website_count}
Leads With Notes: {note_count}\n\n
""")

        f.write(f'{'='*50}')


# Edge Case 1 -  done
# Edge Case 2 -  done
# Edge Case 3 - done
# Edge Case 4 - done
# Edge Case 5 - done
# Edge Case 6 - done
# Edge Case 7 - done
# Edge Case 8 - done
# Edge Case 9 - done
# Edge Case 10 - done
# Edge Case 11 - done
# Edge Case 12 - done
# Edge Case 13 - done
# Edge Case 14 - done
# Edge Case 15 - done
# Edge Case 16 - done
# Edge Case 17 - done (Md. Rahim Uddin and Rahim Uddin can be two different people, as M. hossain, and Mohammed hossain, so name should not be a primary key, phone/email should be a primary key)
# Edge Case 18 - done
# Edge Case 19 - done
# Edge Case 20 - done





